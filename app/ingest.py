import os
import fitz  # PyMuPDF
from dotenv import load_dotenv
from supabase import create_client
from qdrant_client import QdrantClient
from qdrant_client.http.models import Distance, VectorParams
from llama_index.embeddings.google_genai import GoogleGenAIEmbedding

load_dotenv()


supabase = create_client(os.getenv("SUPABASE_URL"), os.getenv("SUPABASE_KEY"))
qdrant = QdrantClient(url=os.getenv("QDRANT_URL"), api_key=os.getenv("QDRANT_API_KEY"))

# 2. Setup Embedding Model (Free Inference API)
embed_model = GoogleGenAIEmbedding(
    model_name="models/gemini-embedding-2-preview", # Upgrade to multimodal
    api_key=os.getenv("GEMINI_API_KEY")
)

# COLLECTION_NAME = "multimodal_rag_collection"
COLLECTION_NAME = "multimodal_rag_v3"

# try:
#     qdrant.delete_collection(COLLECTION_NAME)
#     print("🗑️ Old collection deleted")
# except Exception:
#     print("No collection to delete")

def init_qdrant():
    """Ensures the collection exists with the correct 3072 dimensions"""
    collections = qdrant.get_collections().collections
    exists = any(c.name == COLLECTION_NAME for c in collections)
    
    # If you want to force-reset during testing, uncomment the next two lines:
    # if exists: qdrant.delete_collection(COLLECTION_NAME); exists = False
    
    if not exists:
        print(f"Creating collection: {COLLECTION_NAME} (3072 dims)")
        qdrant.create_collection(
            collection_name=COLLECTION_NAME,
            # CHANGED: 3072 is the default for Gemini Embedding 2
            vectors_config=VectorParams(size=3072, distance=Distance.COSINE),
        )

def ingest_pdf(pdf_path):
    if not os.path.exists(pdf_path):
        print(f"❌ Error: File {pdf_path} not found.")
        return

    init_qdrant()
    doc = fitz.open(pdf_path)
    file_name = os.path.basename(pdf_path)
    
    print(f"🚀 Starting ingestion for: {file_name}")

    for i, page in enumerate(doc):
        # A. Convert Page to Image
        pix = page.get_pixmap(matrix=fitz.Matrix(2, 2)) # Higher res for better VLM reading
        img_name = f"page_{i}_{file_name}.png"
        img_local_path = f"assets/{img_name}"
        pix.save(img_local_path)
        
        # B. Upload to Supabase
        with open(img_local_path, "rb") as f:
            # We use 'upsert=True' so you can re-run tests without errors
            supabase.storage.from_("multimodal-rag").upload(
                path=img_name, 
                file=f, 
                file_options={"upsert": "true"}
            )
            img_url = supabase.storage.from_("multimodal-rag").get_public_url(img_name)
        
        # C. Generate Embedding for the page text
        page_text = page.get_text()
        # If page is empty (just an image), we use a placeholder or caption
        text_to_embed = page_text if page_text.strip() else f"Image content from {file_name} page {i}"
        vector = embed_model.get_text_embedding(text_to_embed)
        
        # D. Store in Qdrant
        qdrant.upsert(
            collection_name=COLLECTION_NAME,
            points=[{
                "id": i + hash(file_name) % 10**8, # Basic unique ID
                "vector": vector,
                "payload": {
                    "text": page_text,
                    "image_url": img_url,
                    "source": file_name,
                    "page_number": i
                }
            }]
        )
        print(f"✅ Indexed Page {i} | URL: {img_url}")

if __name__ == "__main__":
    # Change 'test.pdf' to whatever file you have in your /data folder!
    # Ensure the file exists before running.
    sample_file = "data/test1.pdf" 
    ingest_pdf(sample_file)