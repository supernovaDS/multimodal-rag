import os
import shutil
from fastapi import FastAPI, UploadFile, File, HTTPException
from pydantic import BaseModel
from dotenv import load_dotenv
from app.ingest import ingest_pdf
from app.query import ask_engine
from fastapi.concurrency import run_in_threadpool
from fastapi import Form

load_dotenv()

app = FastAPI(title="Multimodal RAG Engine API")

# Data model for queries
class QueryRequest(BaseModel):
    prompt: str

@app.get("/")
async def root():
    return {"status": "online", "message": "Multimodal RAG Engine is running."}

@app.post("/upload")
async def upload_document(file: UploadFile = File(...)):
    if not file.filename.endswith(".pdf"):
        raise HTTPException(status_code=400, detail="Only PDF files are supported.")
    
    temp_path = f"data/{file.filename}"
    with open(temp_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
    
    try:
        # 🔥 FIX HERE
        await run_in_threadpool(ingest_pdf, temp_path)
        return {"message": f"Successfully indexed {file.filename}"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        if os.path.exists(temp_path):
            os.remove(temp_path)

@app.post("/chat")
async def chat(
    prompt: str = Form(...),
    file: UploadFile = File(None)
):
    user_image_path = None

    if file:
        user_image_path = f"assets/query_{file.filename}"
        with open(user_image_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

    try:
        # 🔥 FIX HERE
        answer = await run_in_threadpool(ask_engine, prompt, user_image_path)
        return {"answer": str(answer)}

    except Exception as e:
        return {"error": str(e)}

    finally:
        # Cleanup
        if user_image_path and os.path.exists(user_image_path):
            os.remove(user_image_path)
            
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)