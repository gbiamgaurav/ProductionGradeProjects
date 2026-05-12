# 🤖 Enterprise Agentic RAG

A production-grade Retrieval-Augmented Generation (RAG) system built with **LangChain**, **LangGraph**, and **Vertex AI**, designed for enterprise-scale document processing, semantic search, and intelligent question-answering.

## 📋 Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Architecture](#architecture)
- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Environment Setup](#environment-setup)
- [Project Structure](#project-structure)
- [Usage](#usage)
- [Configuration](#configuration)
- [Development](#development)

---

## 🎯 Overview

Enterprise Agentic RAG is a sophisticated system that combines:
- **Agentic Orchestration**: LangGraph for state-machine-driven agent workflows
- **Semantic Search**: Qdrant vector database with GPU-accelerated embeddings
- **Enterprise Integration**: Google Cloud Platform (GCP) for storage, OCR, and LLM services
- **Real-time Processing**: FastAPI backend with Streamlit frontend
- **Observability**: Comprehensive tracing with LangSmith and Logfire

---

## ✨ Features

### Core Capabilities
- ✅ Multi-format document ingestion (PDF, Word, PowerPoint, HTML)
- ✅ Intelligent document parsing with Google Document AI
- ✅ Semantic chunking and embedding generation
- ✅ Vector similarity search with semantic reranking
- ✅ Agentic RAG with cyclic reasoning (LangGraph)
- ✅ Conversation memory with PostgreSQL persistence
- ✅ Semantic caching with Redis
- ✅ Real-time observability and distributed tracing

### Infrastructure
- ☁️ Google Cloud Storage for scalable document storage
- ☁️ Vertex AI for embeddings, ranking, and LLM inference
- 🗄️ Cloud SQL (PostgreSQL) for persistent memory
- 📦 Qdrant for vector search at scale
- 🔴 Redis for semantic caching and session management

---

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────────┐
│         Streamlit Frontend (Chat UI)                │
└─────────────┬───────────────────────────────────────┘
              │
┌─────────────▼───────────────────────────────────────┐
│    FastAPI Backend (Uvicorn ASGI Server)            │
├─────────────────────────────────────────────────────┤
│  LangGraph Agents  │  RAG Pipeline  │  APIs          │
└─────────┬───────────┬───────────────┬────────────────┘
          │           │               │
    ┌─────▼─────┐┌────▼────┐┌────────▼────────┐
    │  Qdrant   ││ Postgres ││   GCS Buckets   │
    │  (Vector) ││ (Memory) ││   (Documents)   │
    └───────────┘└──────────┘└─────────────────┘
          │           │               │
    ┌─────▼───────────▼───────────────▼─────────┐
    │   Google Cloud Platform (Vertex AI)       │
    │  • Document AI (OCR)                      │
    │  • Embeddings & Models                    │
    │  • Ranking Models                         │
    └───────────────────────────────────────────┘
```

---

## 📦 Prerequisites

- **Python**: 3.10 or higher
- **Git**: For version control
- **Google Cloud Account**: With enabled services (Storage, Vertex AI, Document AI, Cloud SQL)
- **Qdrant Cloud**: Vector database account
- **API Keys**: Groq, LangSmith, Logfire

### Services to Enable in GCP

```bash
gcloud services enable \
  storage.googleapis.com \
  aiplatform.googleapis.com \
  documentai.googleapis.com \
  cloudsql.googleapis.com \
  servicenetworking.googleapis.com
```

---

## 🚀 Installation

### 1. Clone the Repository

```bash
cd /path/to/ScalableEnterpriseRAG
```

### 2. Create Virtual Environment

```bash
# Create virtual environment
python3 -m venv .venv

# Activate virtual environment
source .venv/bin/activate  # On macOS/Linux
# or
.venv\Scripts\activate  # On Windows
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Setup Environment Variables

```bash
# Copy the example environment file
cp .env.example .env

# Edit .env with your credentials
nano .env  # or use your preferred editor
```

---

## 🔧 Environment Setup

### Required Environment Variables

Create a `.env` file in the project root with the following variables:

#### **Groq API** (Fast LLM Inference)
```
GROQ_API_KEY=your_groq_api_key_here
```
Get your key from: https://console.groq.com

#### **Qdrant Vector Database**
```
QDRANT_API_KEY=your_qdrant_api_key_here
QDRANT_CLUSTER_ENDPOINT=https://your-cluster.gcp.cloud.qdrant.io
```
Setup at: https://cloud.qdrant.io

#### **Google Cloud Platform**
```
PROJECT_ID=your-gcp-project-id
LOCATION=us-central1
GCP_DOC_AI_LOCATION=us
GCP_DOC_AI_PROCESSOR_ID=your_processor_id_here
GCP_RAW_BUCKET=your-raw-bucket-name
GCP_PROCESSED_BUCKET=your-processed-bucket-name
VPC_CONNECTOR=default
```

#### **Observability & Tracing**
```
LOGFIRE_TOKEN=pylf_v1_us_your_token_here
LANGSMITH_TRACING=true
LANGSMITH_ENDPOINT=https://api.smith.langchain.com
LANGSMITH_API_KEY=lsv2_pt_your_api_key_here
LANGSMITH_PROJECT=EnterpriseRAG
```

> **⚠️ Security Note**: Never commit `.env` to version control. Use `.env.example` as a template.

---

## 📁 Project Structure

```
ScalableEnterpriseRAG/
├── README.md                      # This file
├── .env.example                   # Environment template (commit to git)
├── .env                           # Local environment (DO NOT commit)
├── .gitignore                     # Git ignore rules
├── requirements.txt               # Python dependencies
├── commands.md                    # CLI commands reference
├── iam_commands.md                # IAM/GCP commands reference
├── .logfire/                      # Logfire observability config
├── .venv/                         # Virtual environment
└── data/
    ├── raw/                       # Raw input documents
    ├── processed/                 # Processed documents
    ├── noisy_data/                # Sample noisy data for testing
    └── true_data/                 # Sample clean reference data
```

---

## 💻 Usage

### Running the Application

#### **Start FastAPI Backend**
```bash
# Activate virtual environment
source .venv/bin/activate

# Run the backend API
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

The API will be available at: `http://localhost:8000`
API Documentation: `http://localhost:8000/docs`

#### **Start Streamlit Frontend**
```bash
# In a new terminal, activate virtual environment
source .venv/bin/activate

# Run the Streamlit app
streamlit run app/frontend.py
```

The UI will be available at: `http://localhost:8501`

### API Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/health` | GET | Health check |
| `/chat` | POST | Submit query to RAG system |
| `/documents/upload` | POST | Upload documents for processing |
| `/documents/list` | GET | List processed documents |
| `/search` | POST | Semantic search |
| `/history` | GET | Retrieve conversation history |

---

## ⚙️ Configuration

### Key Configuration Files

#### **requirements.txt**
All Python dependencies with explanatory comments:
- Core frameworks (FastAPI, Streamlit)
- LLM orchestration (LangChain, LangGraph)
- Vector databases (Qdrant, Redis)
- GCP integrations
- Observability tools

#### **commands.md**
Reference for common CLI commands:
- Environment setup
- Database operations
- Deployment commands

#### **iam_commands.md**
GCP IAM and access control commands:
- Service account creation
- Permission management
- Key generation

---

## 🛠️ Development

### Setting Up for Development

```bash
# Install development dependencies (if any)
pip install -r requirements.txt

# Verify installation
python -c "import langchain; import langraph; print('✅ All imports successful')"
```

### Testing Environment Setup

```bash
# Source activation script
source .venv/bin/activate

# Set development environment
export ENVIRONMENT=development
export LOGFIRE_TOKEN=your_token
export GROQ_API_KEY=your_key
```

### Code Structure Pattern

```python
# Example: Query to RAG system
from langchain_core.messages import HumanMessage
from langgraph.graph import StateGraph

# Create agent
agent = create_rag_agent()

# Query
response = agent.invoke({"messages": [HumanMessage(content="Your question")]})
```

### Common Development Tasks

| Task | Command |
|------|---------|
| Format code | `black . && isort .` |
| Lint | `pylint app/` |
| Type check | `mypy app/` |
| Run tests | `pytest tests/` |
| Check dependencies | `pip list` |

---

## 🔐 Security Best Practices

1. **Never commit `.env`**: Only commit `.env.example`
2. **Rotate API Keys**: Periodically rotate all API keys
3. **Use Service Accounts**: For GCP, use service accounts instead of user credentials
4. **Enable Logging**: Keep comprehensive audit logs in Logfire/LangSmith
5. **Network Security**: Use VPC connectors and private networks where possible
6. **Secrets Management**: Consider using Google Secret Manager for production

---

## 📊 Monitoring & Observability

### LangSmith Dashboard
Monitor agent runs and LLM calls:
https://smith.langchain.com

### Logfire Observability
View distributed traces and performance metrics:
https://logfire.pydantic.dev

### Application Logs
Logs are generated with `loguru` and can be configured in your app startup.

---

## 🤝 Contributing

1. Create a feature branch: `git checkout -b feature/your-feature`
2. Make your changes
3. Update `.env.example` if adding new configuration
4. Update documentation
5. Submit a pull request

---

## 📝 License

[Add your license information here]

---

## 📞 Support

For issues, questions, or contributions:
- Check `commands.md` for common commands
- Review GCP setup in `iam_commands.md`
- Enable verbose logging with Logfire for debugging

---

## 🎓 Key Resources

- **LangChain**: https://docs.langchain.com
- **LangGraph**: https://github.com/langchain-ai/langgraph
- **Qdrant**: https://qdrant.tech/documentation
- **Google Vertex AI**: https://cloud.google.com/vertex-ai/docs
- **FastAPI**: https://fastapi.tiangolo.com

---

**Last Updated**: May 12, 2026
**Version**: 1.0.0
