import google.generativeai as genai
from pydantic import BaseModel
import os
import json
from dotenv import load_dotenv
import docx
import pypdf

load_dotenv()

# 1. Configure Gemini
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
model = genai.GenerativeModel("gemini-2.5-flash")

# 2. Define Schema
class MatchResult(BaseModel):
    skills_match: float
    experience_match: float
    project_relevance: float
    overall_match: float
    matching_skills: list[str]
    missing_skills: list[str]
    explanation: str

resume_directory="C:/Internship_prep/Job-Matcher-AI/resumes"

# with open("Resume.txt","r",encoding="utf-8") as C_V: 
#   candidate=C_V.read()

with open("Job_discription.txt") as JD:
   
  Job = JD.read()


def Analyze_resume(candidate,Job,file_name):
  print(file_name)
  prompt = f"""
  You are an AI that evaluates {candidate} profile against job requirements.
  Return results STRICTLY in this JSON format ":

  {{
    "skills_match": number,
    "experience_match": number,
    "project_relevance": number,
    "overall_match": number,
    "matching_skills": [list of matched skills],
    "missing_skills": [list of missing skills],
    "explanation": "one-line explanation"
  }}
  Job desicription is{Job}:
  (missing_skills,matching skills should strictly taken from the job discription)

  make sure the be precise about the data in the json"""

  response = model.generate_content(
      prompt,
      generation_config={"response_mime_type": "application/json",
                        "temperature":0})

  # 4. Parse JSON into Python object
  result_pre = MatchResult.model_validate_json( response.text)
  result=result_pre.model_dump_json(indent=8)
  print(result)

#reads from word documents
def read_docx(doc):
  document=docx.Document(doc)
  full_text=[]
  for paragraph in document.paragraphs:
    full_text.append(paragraph.text)
  return '\n'.join(full_text)

#reads from pdf file
def read_pdf(pdf):
  pdf_doc=pypdf.PdfReader(pdf)
  text=" "
  for words in pdf_doc.pages:
    text+= words.extract_text()
  return text

for resume in os.scandir(resume_directory):
  if resume.name.endswith('.txt'):
    with open(resume.path,encoding="utf-8") as res:
         
      res_txt=res.read()
    Analyze_resume(res_txt,Job,resume.name)
  elif resume.name.endswith('.docx'):
    res_txt=read_docx(resume)
    Analyze_resume(res_txt,Job,resume.name)
  elif resume.name.endswith('.pdf'):
    res_txt=read_pdf(resume.path)
    Analyze_resume(res_txt,Job,resume.name)

  

