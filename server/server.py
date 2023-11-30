import json
import os
from typing import Optional
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import subprocess

app = FastAPI()

class TopicRequest(BaseModel):
    subject: str
    out_file: str
    iterations: int

# In textbook_quality/server/server.py
@app.post("/generate_topics")
async def generate_topics(request: TopicRequest):
    try:
        subprocess.check_call([
            "python", "topic_generator.py", 
            request.subject, request.out_file, 
            "--iterations", str(request.iterations)
        ])
        # Assuming the generated file is saved as 'request.out_file.json'
        file_path = os.path.join("app", "data", f"{request.out_file}")

        with open(file_path, "r") as file:
            data = json.load(file)
    except subprocess.CalledProcessError as e:
        raise HTTPException(status_code=500, detail="Generation failed.") from e

    return {"status": "success", "data": data}

class TopicAugmentorRequest(BaseModel):
    in_file: str
    out_file: str
    domain: Optional[str] = None

@app.post("/augment_topics")
async def augment_topics(request: TopicAugmentorRequest):
    try:
        subprocess.check_call([
            "python", "topic_augmentor.py", 
            request.in_file, request.out_file, 
            "--domain", request.domain if request.domain else ""
        ])
        file_path = os.path.join("app", "data", f"{request.out_file}")

        with open(file_path, "r") as file:
            data = json.load(file)
    except subprocess.CalledProcessError as e:
        raise HTTPException(status_code=500, detail="Augmentation failed.") from e

    return {"status": "success", "data": data}

class BookGeneratorRequest(BaseModel):
    topics_file: str
    books_file: str
    workers: int

@app.post("/generate_books")
async def generate_books(request: BookGeneratorRequest):
    try:
        subprocess.check_call([
            "python", "book_generator.py", 
            request.topics_file, request.books_file, 
            "--workers", str(request.workers)
        ])
        file_path = os.path.join("app", "data", f"{request.books_file}")

        with open(file_path, "r") as file:
            data = json.load(file)
    except subprocess.CalledProcessError as e:
        raise HTTPException(status_code=500, detail="Book generation failed.") from e

    return {"status": "success", "data": data}