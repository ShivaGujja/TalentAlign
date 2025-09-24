import os
import dotenv
import pypdf
import docx
import shutil

from fastapi import Form,FastAPI,UploadFile,HTTPException,File