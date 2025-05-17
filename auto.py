import subprocess

input_code = """from fastapi import FastAPI, File, Form, UploadFile
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
import os, tempfile
from git import Repo
from docx import Document
import fitz  # PyMuPDF

app = FastAPI()

# Enable CORS for frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

def extract_text(file: UploadFile):
    if file.filename.endswith(".txt"):
        return file.file.read().decode()
    elif file.filename.endswith(".docx"):
        doc = Document(file.file)
        return "\n".join(p.text for p in doc.paragraphs)
    elif file.filename.endswith(".pdf"):
        pdf = fitz.open(stream=file.file.read(), filetype="pdf")
        return "\n".join(page.get_text() for page in pdf)
    else:
        raise ValueError("Unsupported file type")

@app.post("/auto-commit/")
async def auto_commit(
    file: UploadFile = File(...),
    repo_url: str = Form(...),
    branch: str = Form(default="main"),
    commit_interval: int = Form(default=5)
):
    with tempfile.TemporaryDirectory() as tmpdir:
        # Clone repo
        repo = Repo.clone_from(repo_url, tmpdir)
        filepath = os.path.join(tmpdir, "autocommit.txt")

        content = extract_text(file)
        with open(filepath, "w") as f:
            f.write("")

        buffer = ""
        for i, c in enumerate(content):
            with open(filepath, "a") as f:
                f.write(c)
            buffer += c

            if len(buffer) >= commit_interval or i == len(content) - 1:
                repo.git.add("autocommit.txt")
                repo.git.commit(m=f"Add: {buffer!r}")
                buffer = ""

        origin = repo.remote(name='origin')
        try:
            origin.push()
        except Exception:
            repo.git.push("--set-upstream", "origin", branch)

    return JSONResponse({"status": "Completed and pushed successfully."})

"""


output_file = "main.py"
with open(output_file, "w") as f:
    pass

buffer = ""

for i, char in enumerate(input_code):
    with open(output_file, "a") as f:
        f.write(char)
    buffer += char

    if len(buffer) == 5 or i == len(input_code) - 1:
        try:
            subprocess.run(["git", "add", "."], check=True)
            subprocess.run(["git", "commit", "-m", f"Add: {repr(buffer)}"], check=True)
            # Try normal push first
            try:
                subprocess.run(["git", "push"], check=True)
            except subprocess.CalledProcessError:
                # Set upstream only once if needed
                subprocess.run(["git", "push", "--set-upstream", "origin", "master"], check=True)
            print(f"Committed: {repr(buffer)}")
        except subprocess.CalledProcessError as e:
            print(f"Git error: {e}")
        buffer = ""
