
# 🧠 Multimodal RAG Engine v2 (2026 Edition)

A high-performance, **Vision-Native Retrieval-Augmented Generation (RAG)** engine.

Unlike traditional RAG systems that only *read* text, this engine **sees your documents**—extracting insights from complex charts, diagrams, and formulas using the **Gemini 3 Flash architecture**.

---

## 🚀 Key Features

### 🔍 Multimodal Intelligence

* Uses `gemini-3-flash-preview`
* Reasons across **text + high-resolution page images**

### 🧩 Unified Vector Space

* Powered by `gemini-embedding-2-preview`
* Maps text and images into a shared **3072-dimensional space**

### ☁️ Persistent Cloud Memory

* **Qdrant Cloud** → Fast, scalable vector search
* **Supabase Storage** → Secure public hosting for document images

### 🌍 Global Retrieval

* Query across your **entire PDF library**
* No need to specify individual files

### ⚡ Production-Ready API

* Built with **FastAPI**
* Async endpoints
* Auto-generated Swagger docs

---

## 🛠️ Tech Stack

| Component     | Technology                    |
| ------------- | ----------------------------- |
| LLM           | Google Gemini 3 Flash         |
| Embeddings    | Gemini Embedding 2 (3072-dim) |
| Orchestration | LlamaIndex (2026 Unified SDK) |
| Vector Store  | Qdrant Cloud                  |
| Image Hosting | Supabase Storage              |
| Backend       | FastAPI / Uvicorn             |
| Deployment    | Render.com                    |

---

## 📁 Project Structure

```
mre/
├── app/
│   ├── main.py          # FastAPI Application & Endpoints
│   ├── ingest.py        # PDF processing & Indexing logic
│   └── query.py         # Multimodal retrieval & Reasoning
├── data/                # Local PDF storage (ignored by git)
├── assets/              # Temporary image cache (ignored by git)
├── requirements.txt     # Production dependencies
├── render.yaml          # Infrastructure-as-Code for Render
└── .env                 # API Keys (Keep this private!)
```

---

## ⚙️ Setup & Installation

### 1️⃣ Clone & Setup Environment

```bash
git clone https://github.com/yourusername/mre.git
cd mre

python -m venv venv
source venv/bin/activate   # Windows: venv\Scripts\activate

pip install -r requirements.txt
```

---

### 2️⃣ Configure Environment Variables

Create a `.env` file in the root directory:

```env
GEMINI_API_KEY=your_key
QDRANT_URL=your_qdrant_cloud_url
QDRANT_API_KEY=your_key
SUPABASE_URL=your_supabase_project_url
SUPABASE_KEY=your_service_role_key
```

---

### 3️⃣ Run Locally

```bash
uvicorn app.main:app --reload
```

👉 Open: [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)

---

## 📡 API Endpoints

### 📤 `POST /upload`

Upload a PDF file. The engine will:

* Convert each page → high-resolution PNG
* Upload images → Supabase
* Embed text + visuals → Qdrant

---

### 💬 `POST /chat`

Ask questions using:

* Text
* Image
* Or both (multimodal)

#### Example Queries

```
Explain the architecture in the diagram on page 4.
```

```
Find this component in my textbooks.  (with image input)
```

---

## 📐 Mathematical Foundation

The engine uses **Cosine Similarity** to retrieve relevant context:

```
similarity = (A · B) / (||A|| ||B||)
```

Where:

* **A** = Query vector
* **B** = Document/page vector

---

### 🧠 Why It Works

* Uses **Matryoshka Representation Learning (MRL)**
* Enables **high-precision retrieval at scale**
* Maintains performance even with large datasets

---

## ✨ Summary

This system is not just RAG—it's a **Vision-Aware Knowledge Engine** capable of:

* Understanding diagrams 🧾
* Interpreting charts 📊
* Reasoning across modalities 🧠

---

