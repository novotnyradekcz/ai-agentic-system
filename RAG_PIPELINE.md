# 📚 RAG Pipeline - Foundation for the Agentic System

## Overview

This RAG (Retrieval-Augmented Generation) pipeline serves as the **foundation and core knowledge retrieval system** for the AI Agentic System. While the agentic system adds autonomous reasoning, tool-calling, reflection, and evaluation capabilities, this original pipeline provides the essential data processing and retrieval mechanisms that power the agent's knowledge base.

**Relationship to Agentic System:**
- **RAG Pipeline** (this document): Core data preparation, embedding, and retrieval
- **Agentic System** ([README.md](README.md)): Enhanced with reasoning, tools, reflection, and evaluation

If you're looking for the full agentic system with autonomous capabilities, see [README.md](README.md). This document covers the underlying RAG infrastructure.

---

## Features

A complete RAG pipeline in Python that processes PDFs and audio files, creates embeddings, stores them in a vector database, and enables intelligent question-answering using LLMs.

### Core Components

✅ **Data Processing:**
- 📄 PDF text extraction
- 🎵 Audio transcription using OpenAI Whisper
- 🎬 MP4 video audio extraction and transcription

✅ **Text Processing:**
- ✂️ Smart text chunking with overlap
- 🔢 Vector embeddings using Sentence Transformers

✅ **Storage & Retrieval:**
- 💾 ChromaDB vector database for efficient similarity search
- 🔍 Semantic search and retrieval

✅ **Generation:**
- 🤖 LLM integration (Google Gemini / OpenAI GPT / Anthropic Claude)
- 💬 Context-aware answer generation

---

## Project Structure

```
ai_agentic_system/
├── run_pipeline.py              # RAG pipeline orchestrator
├── examples_pipeline.py         # Pipeline usage examples
├── test_pipeline.py             # Pipeline verification tests
├── setup_pipeline.sh            # Automated setup script
├── requirements.txt             # Dependencies
├── .env.example                 # Environment configuration template
│
├── data/                        # Input documents
│   ├── *.pdf
│   └── *.mp3, *.mp4, etc.
│
└── modules/                     # Pipeline modules
    ├── pdf_loader.py            # PDF text extraction
    ├── audio_transcriber.py     # Audio to text transcription
    ├── text_chunker.py          # Text chunking logic
    ├── vector_database.py       # Vector DB and embeddings
    └── rag_system.py            # RAG query and generation
```

---

## Installation

### Prerequisites

- Python 3.8 or higher
- pip package manager
- **ffmpeg** (required for audio/video processing)
- (Optional) GPU with CUDA for faster audio transcription

**Install ffmpeg:**
```bash
# macOS
brew install ffmpeg

# Ubuntu/Debian
sudo apt-get install ffmpeg

# Windows
# Download from https://ffmpeg.org/download.html
```

### Setup Steps

#### 1. Navigate to Project
```bash
cd "/Users/rano/Documents/AI Academy/Capstone Project/ai_agentic_system"
```

#### 2. Create Virtual Environment (Optional but Recommended)
```bash
python -m venv venv

# Activate on macOS/Linux:
source venv/bin/activate

# Activate on Windows:
# venv\Scripts\activate
```

#### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

**Note:** Installing Whisper and PyTorch may take some time. For GPU support:
```bash
# For CUDA 11.8 (check your CUDA version):
pip install torch==2.5.0+cu118 torchaudio==2.5.0+cu118 -f https://download.pytorch.org/whl/torch_stable.html
```

#### 4. Configure API Keys

Create a `.env` file:
```bash
cp .env.example .env
```

Edit `.env` and add at least one API key:
```bash
# Google Gemini (Default, Recommended)
GOOGLE_API_KEY=your_google_api_key_here

# OpenAI (Optional)
OPENAI_API_KEY=your_openai_api_key_here

# Anthropic (Optional)
ANTHROPIC_API_KEY=your_anthropic_api_key_here
```

**Get API Keys:**
- **Google Gemini**: https://makersuite.google.com/app/apikey
- **OpenAI**: https://platform.openai.com/api-keys
- **Anthropic**: https://console.anthropic.com/settings/keys

#### 5. Add Your Data
```bash
# Place PDFs and audio files in the data/ directory
cp your_document.pdf data/
cp your_audio.mp3 data/
cp your_video.mp4 data/
```

---

## Quick Start

### Automated Setup (macOS/Linux)
```bash
./setup_pipeline.sh
```

### Manual Process All Files
```bash
python run_pipeline.py
```

### Ask a Single Question
```bash
python run_pipeline.py --query "What is the main topic discussed?"
```

### Interactive Q&A Mode
```bash
python run_pipeline.py --interactive
```

---

## Usage Examples

### Process Specific Files

**Process a specific PDF:**
```bash
python run_pipeline.py --pdf data/research_paper.pdf --query "What are the key findings?"
```

**Process audio file:**
```bash
python run_pipeline.py --audio data/lecture.mp3 --query "What topics were covered?"
```

**Process directory:**
```bash
python run_pipeline.py --data-dir /path/to/documents --interactive
```

### Use Different LLM Providers

**Google Gemini (Default):**
```bash
python run_pipeline.py --interactive
```

**OpenAI GPT:**
```bash
python run_pipeline.py --llm openai --interactive
```

**Anthropic Claude:**
```bash
python run_pipeline.py --llm anthropic --interactive
```

### Advanced Options

**Reset database and start fresh:**
```bash
python run_pipeline.py --reset
```

**Custom model selection:**
```bash
python run_pipeline.py --llm openai --model gpt-4 --interactive
python run_pipeline.py --llm gemini --model gemini-2.5-pro --interactive
```

**Adjust retrieval parameters:**
```bash
python run_pipeline.py --n-results 10 --interactive
```

---

## Configuration

### LLM Providers

**Google Gemini (Default)**
- Fast and cost-effective
- Models: `gemini-2.5-flash` (default), `gemini-2.5-pro`
- Requires: `GOOGLE_API_KEY`

**OpenAI**
- Models: `gpt-3.5-turbo` (default), `gpt-4`, `gpt-4-turbo`
- Requires: `OPENAI_API_KEY`

**Anthropic Claude**
- Models: `claude-3-sonnet-20240229` (default), `claude-3-opus-20240229`
- Requires: `ANTHROPIC_API_KEY`

### Model Selection

**Whisper Models (Audio Transcription):**
- `tiny` - Fastest, least accurate
- `base` - Default, good balance ⭐
- `small` - Better accuracy
- `medium` - High accuracy
- `large` - Best accuracy, slowest

**Embedding Models:**
- `all-MiniLM-L6-v2` - Default, fast ⭐
- `all-mpnet-base-v2` - Better quality
- `multi-qa-MiniLM-L6-cos-v1` - Optimized for Q&A

**Chunking Parameters:**
- `chunk_size` - Default: 1000 characters
- `chunk_overlap` - Default: 200 characters

---

## Pipeline Components

### 1. PDF Loader (`modules/pdf_loader.py`)
- Extracts text from PDF documents
- Handles various PDF formats
- Preserves document structure

### 2. Audio Transcriber (`modules/audio_transcriber.py`)
- Uses OpenAI Whisper for transcription
- Supports multiple audio formats (MP3, WAV, M4A, FLAC, OGG)
- Extracts audio from video files (MP4)
- Configurable model size for speed/accuracy tradeoff

### 3. Text Chunker (`modules/text_chunker.py`)
- Semantic chunking with configurable size and overlap
- Preserves context across chunks
- Generates statistics for analysis

### 4. Vector Database (`modules/vector_database.py`)
- ChromaDB for persistent storage
- Sentence Transformers for embeddings
- Cosine similarity search
- Collection management

### 5. RAG System (`modules/rag_system.py`)
- Retrieves relevant context from vector database
- Formats context for LLM
- Generates answers using selected LLM
- Multi-provider support

---

## Python API Usage

### Basic Pipeline

```python
from modules.rag_system import RAGSystem
from modules.vector_database import VectorDatabase

# Initialize
vector_db = VectorDatabase(collection_name="my_kb")
rag = RAGSystem(vector_db=vector_db, llm_provider="gemini")

# Query
result = rag.answer_question(
    "What is machine learning?",
    n_results=5,
    return_context=True
)

print(result['answer'])
```

### Custom Pipeline

```python
from pathlib import Path
from modules.pdf_loader import PDFLoader
from modules.text_chunker import TextChunker
from modules.vector_database import VectorDatabase
from modules.rag_system import RAGSystem

# Load document
loader = PDFLoader("data/document.pdf")
text = loader.extract_text()

# Chunk text
chunker = TextChunker(chunk_size=1000, chunk_overlap=200)
chunks = chunker.chunk_text(text, metadata={'source': 'document.pdf'})

# Store in database
vector_db = VectorDatabase(collection_name="custom_kb")
vector_db.add_documents(chunks)

# Query
rag = RAGSystem(vector_db=vector_db, llm_provider="openai")
result = rag.answer_question("Summarize the key points")
print(result['answer'])
```

### Audio Processing

```python
from modules.audio_transcriber import AudioTranscriber

# Transcribe audio
transcriber = AudioTranscriber(model_size="base")
result = transcriber.transcribe_audio("data/lecture.mp3")

print(result['text'])
print(f"Language: {result['language']}")
```

---

## Supported File Formats

### Documents
- PDF (`.pdf`)

### Audio
- MP3 (`.mp3`)
- WAV (`.wav`)
- M4A (`.m4a`)
- FLAC (`.flac`)
- OGG (`.ogg`)
- WMA (`.wma`)

### Video (Audio Extraction)
- MP4 (`.mp4`)

---

## Output and Logs

### Session Logs
Interactive sessions are saved to `logs/`:
- `session_YYYYMMDD_HHMMSS.txt` - Full Q&A transcript

### Query Logs
Individual queries are logged:
- `query_YYYYMMDD_HHMMSS.txt` - Single query with answer and sources

### Database
Vector database persists in:
- `chroma_db/` (ChromaDB storage)

---

## Troubleshooting

### Common Issues

**1. ffmpeg not found**
```bash
# Install ffmpeg first
brew install ffmpeg  # macOS
sudo apt-get install ffmpeg  # Linux
```

**2. API Key Errors**
- Verify `.env` file exists and contains valid keys
- Check key format (should start with correct prefix)
- Ensure environment variables are loaded

**3. CUDA/GPU Issues**
- Install CPU version if no GPU available
- Verify CUDA version matches PyTorch version
- For CPU-only: `pip install torch torchaudio`

**4. Memory Issues**
- Reduce chunk size for large documents
- Use smaller Whisper model (`tiny` or `base`)
- Process files individually instead of batch

**5. Slow Transcription**
- Use smaller Whisper model
- Enable GPU support if available
- Process shorter audio segments

### Database Management

**Reset/Clear Database:**
```bash
python run_pipeline.py --reset
```

**Manually delete database:**
```bash
rm -rf chroma_db/
```

---

## Performance Tips

### Speed Optimization
1. **Use GPU** for audio transcription (50-100x faster)
2. **Smaller Whisper model** (`base` vs `large`)
3. **Faster embedding model** (`all-MiniLM-L6-v2`)
4. **Batch processing** for multiple files
5. **Adjust chunk size** (larger = fewer chunks)

### Quality Optimization
1. **Better Whisper model** (`medium` or `large`)
2. **Quality embedding model** (`all-mpnet-base-v2`)
3. **More retrieval results** (increase `n_results`)
4. **Smaller chunk size** for precise retrieval
5. **Use advanced LLM** (GPT-4, Claude Opus)

---

## Testing

Run verification tests:
```bash
python test_pipeline.py
```

Run example scripts:
```bash
python examples_pipeline.py
```

---

## Technical Details

### Architecture

```
Input Documents → Load & Extract → Chunk Text → Generate Embeddings → Store in Vector DB
                                                                              ↓
User Query ← Generate Answer ← Format Context ← Retrieve Similar Chunks ← Query Vector DB
```

### Dependencies

- **PyPDF2 / pypdf** - PDF processing
- **openai-whisper** - Audio transcription
- **moviepy** - Video audio extraction
- **LangChain** - Text processing utilities
- **sentence-transformers** - Embeddings
- **chromadb** - Vector database
- **openai** - OpenAI API client
- **anthropic** - Anthropic API client
- **google-generativeai** - Google Gemini API client

### Storage

- **Vector Database**: ChromaDB (persistent)
- **Embeddings**: 384-dimensional vectors (all-MiniLM-L6-v2)
- **Distance Metric**: Cosine similarity

---

## Upgrade to Agentic System

This RAG pipeline is the foundation for the **AI Agentic System** which adds:

✨ **Autonomous Reasoning** - Plans and thinks through tasks
✨ **Tool-Based Actions** - Generates content, sends emails, etc.
✨ **Self-Reflection** - Evaluates its own performance
✨ **Quality Evaluation** - Tracks metrics and success rates

To use the full agentic system:
```bash
python run_agent.py
```

See [README.md](README.md) for details.

---

## Related Documentation

- **[README.md](README.md)** - Full AI Agentic System documentation
- **[QUICKSTART.md](QUICKSTART.md)** - Quick start for agentic system
- **[DEFAULT_LLM.md](DEFAULT_LLM.md)** - LLM configuration details
- **[architecture.mmd](architecture.mmd)** - System architecture diagram

---

## License

Educational project for AI Academy Capstone.

---

## Support

For issues with the agentic system, see [README.md](README.md).
For RAG pipeline issues, review this document's troubleshooting section.
