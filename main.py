from fastapi import FastAPI, File, Form, UploadFile
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
import os, tempfile
from git import Repo
from docx import Document
import fitz  # PyMuPDF

app = FastAPI