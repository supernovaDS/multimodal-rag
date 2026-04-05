import os
from dotenv import load_dotenv
from qdrant_client import QdrantClient
from google import genai
from google.genai import types
from llama_index.embeddings.google_genai import GoogleGenAIEmbedding
from llama_index.llms.google_genai import GoogleGenAI 
from llama_index.core.schema import ImageDocument
# Helper to fetch images from URLs
from llama_index.core.multi_modal_llms.generic_utils import load_image_urls

load_dotenv()

qdrant = QdrantClient(url=os.getenv("QDRANT_URL"), api_key=os.getenv("QDRANT_API_KEY"))
google_client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

llm = GoogleGenAI(
    model="models/gemini-3-flash-preview", 
    api_key=os.getenv("GEMINI_API_KEY")
)

embed_model = GoogleGenAIEmbedding(
    model_name="models/gemini-embedding-2-preview",
    api_key=os.getenv("GEMINI_API_KEY")
)

COLLECTION_NAME = "multimodal_rag_v3"

def get_raw_image_embedding(image_path):
    with open(image_path, "rb") as f:
        image_data = f.read()
    result = google_client.models.embed_content(
        model="gemini-embedding-2-preview",
        contents=[types.Part.from_bytes(data=image_data, mime_type="image/png")],
        config=types.EmbedContentConfig(output_dimensionality=3072)
    )
    return result.embeddings[0].values

def ask_engine(query_text, user_image_path=None):
    # 1. Retrieval
    if user_image_path:
        query_vector = get_raw_image_embedding(user_image_path)
    else:
        query_vector = embed_model.get_text_embedding(query_text)
    
    response = qdrant.query_points(
        collection_name=COLLECTION_NAME,
        query=query_vector,
        limit=2
    )

    image_urls = []
    context_text = ""
    
    for res in response.points:
        # RESTORED: Add the actual text content back to context
        page_text = res.payload.get('text', '')
        source_info = f"--- Source: {res.payload['source']} (Page {res.payload['page_number']}) ---\n"
        context_text += f"{source_info}{page_text}\n\n"
        
        # Collect URLs for fetching
        image_urls.append(res.payload['image_url'])

    # 2. Fetch images so Gemini gets the actual visual data
    image_documents = load_image_urls(image_urls)
    
    # Add user's query image if provided
    if user_image_path:
        image_documents.append(ImageDocument(image_path=user_image_path))

    # 3. Explicit Prompting
    prompt = f"""
    You are analyzing a retrieved technical document. 
    Use the provided text context and the attached images to answer the question.
    If you see a diagram that explains the text, describe it in your answer.

    Question: {query_text}

    RETRIVED TEXT CONTEXT:
    {context_text}
    """
    
    answer = llm.complete(prompt=prompt, image_documents=image_documents)
    return answer

if __name__ == "__main__":
    query = input("Ask your PDF a question: ")
    # Optional: logic to handle local image testing via CLI
    ANS = ask_engine(query)
    
    print(f"\n Answer: \n{ANS}")