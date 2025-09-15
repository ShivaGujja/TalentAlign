import google.generativeai as genai
from pydantic import BaseModel
import os
import json
from dotenv import load_dotenv
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


def Analyze_resume(candidate,Job):
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

  Job desicription is{Job}:

  make sure the be precise about the data in the json"""

  response = model.generate_content(
      prompt,
      generation_config={"response_mime_type": "application/json",
                        "temperature":0})

  # 4. Parse JSON into Python object
  result_pre = MatchResult.model_validate_json( response.text)
  result=result_pre.model_dump_json(indent=8)
  print(result)


for resume in os.scandir(resume_directory):
   if resume.name.endswith('.txt'):
      with open(resume.path,encoding="utf-8") as res:
         
        res_txt=res.read()
      Analyze_resume(res_txt,Job)
  

