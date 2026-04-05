🧠 Multimodal RAG Engine v2 (2026 Edition)A high-performance, Vision-Native Retrieval-Augmented Generation (RAG) engine. Unlike traditional RAG systems that only "read" text, this engine "sees" your documents—extracting insights from complex charts, diagrams, and formulas using the Gemini 3 Flash architecture.🚀 Key FeaturesMultimodal Intelligence: Uses gemini-3-flash-preview to reason across both text and high-resolution page images.Unified Vector Space: Powered by gemini-embedding-2-preview, mapping text and images into a shared 3072-dimensional space.Persistent Cloud Memory:Qdrant Cloud: Scalable vector database for lightning-fast similarity search.Supabase Storage: Secure, public-access bucket for document image hosting.Global Retrieval: Search across your entire library of PDFs simultaneously without needing to specify a file.Production-Ready API: Built with FastAPI, featuring asynchronous endpoints and auto-generated Swagger documentation.🛠️ Tech StackComponentTechnologyLLMGoogle Gemini 3 FlashEmbeddingsGemini Embedding 2 (3072-dim)OrchestrationLlamaIndex (2026 Unified SDK)Vector StoreQdrant CloudImage HostingSupabase StorageBackendFastAPI / UvicornDeploymentRender.com📁 Project StructurePlaintextmre/
├── app/
│   ├── main.py          # FastAPI Application & Endpoints
│   ├── ingest.py        # PDF processing & Indexing logic
│   └── query.py         # Multimodal retrieval & Reasoning
├── data/                # Local PDF storage (ignored by git)
├── assets/              # Temporary image cache (ignored by git)
├── requirements.txt     # Production dependencies
├── render.yaml          # Infrastructure-as-Code for Render
└── .env                 # API Keys (Keep this private!)
⚙️ Setup & Installation1. Clone & EnvironmentBashgit clone https://github.com/yourusername/mre.git
cd mre
python -m venv venv
source venv/bin/activate  # venv\Scripts\activate on Windows
pip install -r requirements.txt
2. Configure Environment VariablesCreate a .env file in the root directory:PlaintextGEMINI_API_KEY=your_key
QDRANT_URL=your_qdrant_cloud_url
QDRANT_API_KEY=your_key
SUPABASE_URL=your_supabase_project_url
SUPABASE_KEY=your_service_role_key
3. Run LocallyBashuvicorn app.main:app --reload
Visit http://127.0.0.1:8000/docs to start testing!📡 API EndpointsPOST /uploadUpload a PDF file. The engine will:Render each page as a high-res PNG.Upload images to Supabase.Embed text and visual features into Qdrant.POST /chatAsk a question. You can send a text prompt or a combination of text and an image.Example Query: "Explain the architecture in the diagram on page 4."Visual Query: Upload a photo of a circuit and ask, "Find this component in my textbooks."📐 Mathematical FoundationThe engine uses Cosine Similarity to find the most relevant context:$$\text{similarity} = \frac{\mathbf{A} \cdot \mathbf{B}}{\|\mathbf{A}\| \|\mathbf{B}\|}$$Where $\mathbf{A}$ is your query vector and $\mathbf{B}$ is the document page vector. By using Matryoshka Representation Learning (MRL) within the Gemini 2 embeddings, we achieve high-precision retrieval even at large scales.