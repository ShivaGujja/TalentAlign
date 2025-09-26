import os
import uuid
import shutil
import json
from pathlib import Path
from typing import List,Optional,Dict,Tuple
import hashlib

from fastapi import Form,FastAPI,UploadFile,HTTPException,File
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from dotenv import load_dotenv

import google.generativeai as genai
import docx
import pypdf

load_dotenv()

genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
model = genai.GenerativeModel("gemini-2.5-flash")



app = FastAPI(title="Job Matcher API",version="1.0")
app.add_middleware(
    CORSMiddleware,
        allow_origins=["http://localhost:5173", "http://127.0.0.1:5173"],
        allow_methods=["*"],
        allow_headers=["*"],
    )
    
BASE_DIR =Path(__file__).parent
DATA_DIR =BASE_DIR/ "data"
RESUME_DIR = DATA_DIR /"resumes"
JOB_DIR = DATA_DIR /"jobs"
RESULTS_FILE =DATA_DIR /"result.json"

for d in (DATA_DIR,RESUME_DIR,JOB_DIR):
    d.mkdir(parents=True,exist_ok=True)

jobs: Dict[str,dict]={}
candidates: Dict[str,dict]={}
results_store:Dict[Tuple[str,str],dict]={}

class UploadJobResponse(BaseModel):
    job_id:str
    message:str

class UploadResumeResponse(BaseModel):
    candidate_id: str
    message: str


class AnalyzeRequest(BaseModel):
    job_id: str
    candidate_ids: Optional[List[str]] = None

class MatchResult(BaseModel):
    skills_match: float
    experience_match: float
    project_relevance: float
    overall_match: float
    matching_skills: List[str]
    missing_skills: List[str]
    explanation: str

class AnalyzeResponseItem(BaseModel):
    job_id: str
    candidate_id: str
    filename: str
    result: MatchResult

class AnalyzeResponse(BaseModel):
    results: List[AnalyzeResponseItem]

def read_docx(path: Path) -> str:
    doc = docx.Document(str(path))
    return "\n".join([p.text for p in doc.paragraphs])

def read_pdf(path: Path) -> str:
    reader = pypdf.PdfReader(str(path))
    text = []
    for page in reader.pages:
        page_text = page.extract_text() or ""
        text.append(page_text)
    return "\n".join(text)

def read_txt(path: Path) -> str:
    with open(path, "r", encoding="utf-8", errors="replace") as f:
        return f.read()

def extract_text_from_file(path: Path) -> str:
    ext = path.suffix.lower()
    if ext == ".pdf":
        return read_pdf(path)
    if ext == ".docx":
        return read_docx(path)
    
    return read_txt(path)

def parse_json_from_model_text(text: str) -> dict:
    try:
        return json.loads(text)
    except Exception:
        first = text.find("{")
        last = text.rfind("}")
        if first != -1 and last != -1 and last > first:
            try:
                return json.loads(text[first:last+1])
            except Exception:
                pass
    raise ValueError(" Could not parse JSON from Gemini output")



def prompt_for_job_candidate(job_text: str, candidate_text: str) -> str:
    
    return f"""
You are an AI that evaluates a candidate profile against job requirements.
Return results STRICTLY in JSON exactly in this format (no extra text):

{{
  "skills_match": number,
  "experience_match": number,
  "project_relevance": number,
  "overall_match": number,
  "matching_skills": ["..."],
  "missing_skills": ["..."],
  "explanation": "one-line explanation"
}}

Job description:
{job_text}

Candidate resume:
{candidate_text}

Important:
- Use only the job text to pull matching_skills and missing_skills.
- Numbers should be 0-100 (percent style).
- If you cannot find a fact in the context, don't invent it.
"""

def call_gemini_json(job_text: str, candidate_text: str) -> MatchResult:
    prompt = prompt_for_job_candidate(job_text, candidate_text)
    response = model.generate_content(
        prompt,
        generation_config={"response_mime_type": "application/json", "temperature": 0}
    )

    text = getattr(response, "text", None) or str(response)
    parsed = parse_json_from_model_text(text)

    
    parsed["matching_skills"] = parsed.get("matching_skills", [])
    parsed["missing_skills"] = parsed.get("missing_skills", [])
    return MatchResult(**parsed)


def make_cache_key(job_text: str, candidate_text: str) -> str:
    h = hashlib.sha256()
    h.update(job_text.encode("utf-8"))
    h.update(b"||")
    h.update(candidate_text.encode("utf-8"))
    return h.hexdigest()
@app.post("/upload_job", response_model=UploadJobResponse)
async def upload_job(job_text: Optional[str] = Form(None), job_file: Optional[UploadFile] = File(None)):
    if not job_text and not job_file:
        raise HTTPException(status_code=400, detail="Provide job_text or job_file")

    job_id = str(uuid.uuid4())
    if job_file:
        dest = JOB_DIR / f"{job_id}_{job_file.filename}"
        with open(dest, "wb") as f: shutil.copyfileobj(job_file.file, f)
        job_text = extract_text_from_file(dest)
    else:
        dest = JOB_DIR / f"{job_id}.txt"
        with open(dest, "w", encoding="utf-8") as f: f.write(job_text)

    jobs[job_id] = {"text": job_text, "filename": str(dest)}
    return {"job_id": job_id, "message": "Job uploaded"}

@app.post("/upload_resume", response_model=UploadResumeResponse)
async def upload_resume(file: UploadFile = File(...)):
    candidate_id = str(uuid.uuid4())
    dest = RESUME_DIR / f"{candidate_id}_{file.filename}"
    with open(dest, "wb") as f: shutil.copyfileobj(file.file, f)
    candidates[candidate_id] = {"text": extract_text_from_file(dest), "filename": str(dest)}
    return {"candidate_id": candidate_id, "message": "Resume uploaded"}


@app.post("/analyze", response_model=AnalyzeResponse)
def analyze(req: AnalyzeRequest):
    """
    Analyze candidate(s) against a job.
    Provide job_id and (optional) candidate_ids list. If candidate_ids is omitted, analyze all uploaded resumes.
    """
    job_id = req.job_id
    if job_id not in jobs:
        raise HTTPException(status_code=404, detail="job_id not found")

    job_text = jobs[job_id]["text"]
    target_candidates = req.candidate_ids or list(candidates.keys())
    result_items = []

    for cid in target_candidates:
        if cid not in candidates:
            
            continue
        candidate_text = candidates[cid]["text"]
        cache_key = make_cache_key(job_text, candidate_text)

        
        if (job_id, cid) in results_store:
            result = results_store[(job_id, cid)]
        else:
            
            try:
                match: MatchResult = call_gemini_json(job_text, candidate_text)
                result = match.model_dump()
            except Exception as e:
                
                result = {
                    "skills_match": 0.0,
                    "experience_match": 0.0,
                    "project_relevance": 0.0,
                    "overall_match": 0.0,
                    "matching_skills": [],
                    "missing_skills": [],
                    "explanation": f"LLM error: {str(e)}"
                }
            results_store[(job_id, cid)] = result

        result_items.append({
            "job_id": job_id,
            "candidate_id": cid,
            "filename": candidates[cid]["filename"],
            "result": result
        })

    
    try:
        with open(RESULTS_FILE, "w", encoding="utf-8") as f:
            json.dump({f"{k[0]}__{k[1]}": v for k, v in results_store.items()}, f, indent=2)
    except Exception:
        pass

    
    response_items = []
    for it in result_items:
        response_items.append(
            AnalyzeResponseItem(
                job_id=it["job_id"],
                candidate_id=it["candidate_id"],
                filename=it["filename"],
                result=MatchResult(**it["result"])
            )
        )

    return AnalyzeResponse(results=response_items)


@app.get("/results")
def get_results(job_id: Optional[str] = None):
    """
    Return cached results. If job_id supplied, filter to that job.
    """
    out = []
    for (j,c), res in results_store.items():
        if job_id and j != job_id:
            continue
        out.append({"job_id": j, "candidate_id": c, "result": res})
    return {"count": len(out), "items": out}

