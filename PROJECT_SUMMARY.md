# 🎓 AI Academy HW4 - RAG Pipeline Project
## Complete Implementation ✅

### 📦 What Has Been Created

A fully functional RAG (Retrieval-Augmented Generation) pipeline with all required components:

#### ✅ Assignment Requirements Fulfilled:

**1. Load and Process Data**
- ✅ PDF text extraction ([modules/pdf_loader.py](modules/pdf_loader.py))
- ✅ Audio transcription using Whisper ([modules/audio_transcriber.py](modules/audio_transcriber.py))

**2. Chunk the Text**
- ✅ Semantic text chunking with overlap ([modules/text_chunker.py](modules/text_chunker.py))

**3. Embed and Store in Vector Database**
- ✅ Sentence Transformers for embeddings
- ✅ ChromaDB vector database ([modules/vector_database.py](modules/vector_database.py))

**4. Retrieve and Generate**
- ✅ Complete RAG system with retrieval and LLM generation ([modules/rag_system.py](modules/rag_system.py))
- ✅ Support for OpenAI, Anthropic, and Google Gemini models

---

## 📁 Project Structure

```
rag_pipeline/
├── 📄 README.md              # Comprehensive documentation
├── 📄 QUICKSTART.md          # Quick reference guide
├── 📄 requirements.txt       # All dependencies
├── 🔧 setup.sh               # Automated setup script
├── 🧪 test_setup.py          # Verification tests
├── 💡 examples.py            # Usage examples
├── 🚀 main.py                # Main pipeline orchestrator
├── 🔐 .env.example           # API key template
├── 📂 data/                  # Place your files here
│   └── README.md
└── 📂 modules/               # Core components
    ├── __init__.py
    ├── pdf_loader.py         # PDF processing
    ├── audio_transcriber.py  # Audio to text
    ├── text_chunker.py       # Text chunking
    ├── vector_database.py    # Embeddings & ChromaDB
    └── rag_system.py         # RAG Q&A system
```

---

## 🚀 Getting Started (4 Steps)

### Step 0: Install ffmpeg (Required)
```bash
# macOS
brew install ffmpeg

# Ubuntu/Debian
sudo apt-get install ffmpeg
```

### Step 1: Setup Environment
```bash
cd "/Users/rano/Documents/AI Academy/HW4/rag_pipeline"
./setup.sh
```

### Step 2: Configure API Keys
```bash
cp .env.example .env
# Edit .env and add your OpenAI or Anthropic API key
```

### Step 3: Add Your Data & Run
```bash
# Add your files
cp your_document.pdf data/
cp your_audio.mp3 data/

# Process and start Q&A
python main.py --interactive
```

---

## 📖 Documentation

- **[README.md](README.md)** - Complete documentation with all features
- **[QUICKSTART.md](QUICKSTART.md)** - Quick reference for common commands
- **[examples.py](examples.py)** - Code examples for each component
- **[test_setup.py](test_setup.py)** - Verify your installation

---

## 🎯 Key Features

### 1. **Multiple Data Sources**
   - PDF documents
   - Audio files (MP3, WAV, M4A, FLAC, OGG, WMA)
   - Video files (MP4 - audio extraction)

### 2. **Smart Processing**
   - Reliable text extraction
   - Whisper-based transcription
   - Semantic chunking with overlap

### 3. **Powerful Retrieval**
   - Sentence Transformers embeddings
   - ChromaDB vector database
   - Cosine similarity search

### 4. **Flexible Generation**
   - OpenAI GPT models
   - Anthropic Claude models
   - Google Gemini models
   - Customizable parameters

### 5. **Easy to Use**
   - Command-line interface
   - Interactive Q&A mode
   - Python API for custom scripts

---

## 💻 Usage Examples

### Process All Files
```bash
python main.py
```

### Ask a Question
```bash
python main.py --query "What is the main topic?"
```

### Interactive Mode
```bash
python main.py --interactive
```

### Process Specific File
```bash
python main.py --pdf data/paper.pdf --query "Summarize this"
```

### Use Claude Instead of GPT
```bash
python main.py --llm anthropic --interactive
```

---

## 🧪 Test Your Setup

Run the test script to verify everything is working:

```bash
python test_setup.py
```

This will check:
- ✅ Python version
- ✅ All dependencies installed
- ✅ API keys configured
- ✅ Core components working
- ✅ Data directory ready

---

## 🔧 Technical Details

### Technologies Used:
- **PDF Processing**: PyPDF2
- **Audio Transcription**: OpenAI Whisper
- **Text Chunking**: LangChain RecursiveCharacterTextSplitter
- **Embeddings**: Sentence Transformers (all-MiniLM-L6-v2)
- **Vector Database**: ChromaDB
- **LLMs**: OpenAI GPT-3.5/4, Anthropic Claude, Google Gemini

### Default Configuration:
- Chunk size: 1000 characters
- Chunk overlap: 200 characters
- Top-k retrieval: 5 chunks
- Embedding dimensions: 384
- Similarity metric: Cosine

---

## 📚 Module Documentation

### PDF Loader
```python
from modules import PDFLoader
loader = PDFLoader("document.pdf")
text = loader.extract_text()
```

### Audio Transcriber
```python
from modules import AudioTranscriber
transcriber = AudioTranscriber(model_size="base")
result = transcriber.transcribe_audio("audio.mp3")
```

### Text Chunker
```python
from modules import TextChunker
chunker = TextChunker(chunk_size=1000, chunk_overlap=200)
chunks = chunker.chunk_text(text)
```

### Vector Database
```python
from modules import VectorDatabase
db = VectorDatabase(collection_name="my_docs")
db.add_documents(chunks)
results = db.query("search query", n_results=5)
```

### RAG System
```python
from modules import RAGSystem
rag = RAGSystem(vector_db=db)
result = rag.answer_question("Your question?")
print(result['answer'])
```

---

## 🎓 Learning Outcomes

This project demonstrates:
1. **Document Processing**: Extract text from various formats
2. **Embeddings**: Convert text to vector representations
3. **Vector Databases**: Efficient similarity search
4. **Retrieval-Augmented Generation**: Combine retrieval with LLMs
5. **End-to-End ML Pipeline**: From data to production

---

## 🐛 Troubleshooting

### Dependencies Not Installing?
```bash
pip install --upgrade pip
pip install -r requirements.txt
```

### Whisper Model Download Fails?
- Check internet connection
- Model downloads on first use (~150MB)

### API Errors?
- Verify API keys in `.env`
- Check API key has credits/is active

### ChromaDB Errors?
```bash
rm -rf chroma_db/
python main.py --reset
```

---

## 🎉 You're Ready!

Your complete RAG pipeline is set up and ready to use. 

**Next Steps:**
1. ✅ Run `python test_setup.py` to verify
2. ✅ Add your PDF/audio files to `data/`
3. ✅ Configure API keys in `.env`
4. ✅ Run `python main.py --interactive`
5. ✅ Start asking questions!

---

## 📧 Support

For questions about this implementation:
- Check [README.md](README.md) for detailed docs
- Run `python test_setup.py` for diagnostics
- Review [examples.py](examples.py) for code samples

---

**Created for AI Academy HW4**
*Complete RAG Pipeline Implementation*

Happy coding! 🚀
