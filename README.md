🚀 Advanced Retrieval-Augmented Generation (RAG) Lab
Production-ready RAG implementations: From semantic search to autonomous agents.
This repository serves as a deep-dive laboratory for the evolution of RAG. It moves beyond "Hello World" implementations to explore sophisticated, evaluated systems capable of handling real-world data complexities.
📖 Overview
Standard RAG often fails in production due to "noise" in retrieval or the inability to reason through complex queries. This lab provides hands-on solutions for:
 * Retrieval Noise: Filtering out irrelevant context.
 * Temporal Sensitivity: Handling data with time-specific relevance (e.g., financial filings).
 * Entity Disambiguation: Distinguishing between similar terms in different contexts.
 * Rigid Pipelines: Moving from linear flows to dynamic, self-correcting agents.
🛠️ The Notebooks
| Project | Focus | Stack | Dataset |
|---|---|---|---|
| Node Postprocessor | Reranking, filtering & context compression | LlamaIndex, Gemini, PydanticAI | Historical Geology (1878/1905) |
| Production RAG | Agentic planning, rewriting & RAGAS evaluation | LangGraph, OpenAI, FAISS, Ragas | NVIDIA 2023 10-K |
| Index-Aware & HyDE | Query expansion & Hypothetical Embeddings | LlamaIndex, Gemini, HuggingFace | "Anabasis of Alexander" |
🔍 Key Concepts Explored
1. Hypothetical Document Embeddings (HyDE)
HyDE instructs an LLM to generate a "fake" answer to a query first. By embedding this hypothetical answer instead of the raw query, we often find a closer vector match in the actual documentation, effectively solving the vocabulary mismatch problem.
2. Node Post-processing & Re-ranking
 * Intelligent Processing: Moving beyond top-k by using metadata extraction and relevance score thresholds.
 * Temporal Filtering: Automatically prioritizing the most recent information based on document metadata.
 * Context Compression: Reducing the token load by extracting only the most relevant sentences from retrieved chunks.
3. Agentic RAG with LangGraph
Traditional RAG is a one-way street (Retrieve \rightarrow Augment \rightarrow Generate). With LangGraph, we implement cyclic workflows where the system can "think" before it speaks.
Agentic Capabilities included:
 * Query Decomposition: Breaking a complex question into smaller, solvable sub-tasks.
 * Tool Usage: Dynamically choosing between local vector stores and web search (e.g., Tavily).
 * Self-Reflection: An "Evaluator" step that checks if the retrieved context actually supports the generated answer.
🚀 Getting Started
Prerequisites
 * Python 3.9+
 * A .env file in the root directory with the following keys:
<!-- end list -->
GEMINI_API_KEY="..."      # For notebooks 1 & 3
HF_TOKEN="..."            # For HuggingFace embeddings
OPENAI_API_KEY="..."      # For notebook 2
GROQ_API_KEY="..."        # Optional: For high-speed inference
TAVILY_API_KEY="..."      # For web search tools

Installation
# Clone the repository
git clone https://github.com/yourusername/advanced-rag-lab.git
cd advanced-rag-lab

# Setup environment
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
jupyter notebook

> Note: Each notebook is designed to be self-contained; datasets are fetched automatically during execution.
