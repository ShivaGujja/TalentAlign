import google.generativeai as genai
from pydantic import BaseModel
import os
import json
from dotenv import load_dotenv
import docx
import pypdf


load_dotenv()


genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
model = genai.GenerativeModel("gemini-2.5-flash")


class MatchResult(BaseModel):
    skills_match: float
    experience_match: float
    project_relevance: float
    overall_match: float
    matching_skills: list[str]
    missing_skills: list[str]
    explanation: str

resume_directory = "C:/Internship_prep/Job-Matcher-AI/backend/resumes"



def Analyze_resume(candidate, Job, file_name):
    print(f"Analyzing: {file_name}")

    prompt = f"""
    You are an AI that evaluates {candidate} profile against job requirements.
    Return results STRICTLY in this JSON format:

    {{
      "skills_match": number,
      "experience_match": number,
      "project_relevance": number,
      "overall_match": number,
      "matching_skills": [list of matched skills],
      "missing_skills": [list of missing skills],
      "explanation": "one-line explanation"
    }}

    Job description is {Job}:
    (missing_skills, matching_skills should strictly be present in {Job})
    """

    response = model.generate_content(
        prompt,
        generation_config={"response_mime_type": "application/json", "temperature": 0}
    )

    
    result_pre = MatchResult.model_validate_json(response.text)
    return result_pre



def read_docx(doc):
    document = docx.Document(doc)
    full_text = []
    for paragraph in document.paragraphs:
        full_text.append(paragraph.text)
    return '\n'.join(full_text)



def read_pdf(pdf):
    pdf_doc = pypdf.PdfReader(pdf)
    text = ""
    for words in pdf_doc.pages:
        text += words.extract_text()
    return text



def main():
    all_results = []

    
    with open("Job_discription.txt", encoding="utf-8") as JD:
        Job = JD.read()

    
    for resume in os.scandir(resume_directory):
        if resume.name.endswith('.txt'):
            with open(resume.path, encoding="utf-8") as res:
                res_txt = res.read()
            result = Analyze_resume(res_txt, Job, resume.name)

        elif resume.name.endswith('.docx'):
            res_txt = read_docx(resume)
            result = Analyze_resume(res_txt, Job, resume.name)

        elif resume.name.endswith('.pdf'):
            res_txt = read_pdf(resume.path)
            result = Analyze_resume(res_txt, Job, resume.name)

        else:
            print(f"Skipping unsupported file: {resume.name}")
            continue

        
        all_results.append({
            "candidate_file": resume.name,
            "Overall_score": result.overall_match,
            "details": result.model_dump()
        })

    
    all_results.sort(key=lambda x: x["Overall_score"], reverse=True)

    
    output_file_name = "final_output.json"
    with open(output_file_name, 'w', encoding='utf-8') as f:
        json.dump(all_results, f, indent=4)

    print("-- Analysis completed. Results saved to final_output.json --")


if __name__ == "__main__":
    main()
