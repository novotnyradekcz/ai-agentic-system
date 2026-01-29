"""
Test Script - Verify RAG Pipeline Components
"""

import sys
from pathlib import Path

def test_imports():
    """Test 1: Verify all imports work."""
    print("\n" + "="*80)
    print("Test 1: Testing Imports")
    print("="*80)
    
    try:
        from modules import (
            PDFLoader,
            AudioTranscriber,
            TextChunker,
            VectorDatabase,
            RAGSystem
        )
        print("✓ All imports successful")
        return True
    except ImportError as e:
        print(f"❌ Import failed: {e}")
        print("\nRun: pip install -r requirements.txt")
        return False


def test_text_chunker():
    """Test 2: Test text chunking."""
    print("\n" + "="*80)
    print("Test 2: Testing Text Chunker")
    print("="*80)
    
    try:
        from modules.text_chunker import TextChunker
        
        sample_text = """
        This is a test document. It has multiple sentences.
        
        This is another paragraph. It will be chunked.
        
        And here is a third paragraph for good measure.
        """
        
        chunker = TextChunker(chunk_size=50, chunk_overlap=10)
        chunks = chunker.chunk_text(sample_text)
        
        print(f"✓ Created {len(chunks)} chunks")
        print(f"✓ First chunk: {chunks[0]['text'][:50]}...")
        return True
        
    except Exception as e:
        print(f"❌ Text chunking failed: {e}")
        return False


def test_vector_database():
    """Test 3: Test vector database operations."""
    print("\n" + "="*80)
    print("Test 3: Testing Vector Database")
    print("="*80)
    
    try:
        from modules.vector_database import VectorDatabase
        
        # Create test database
        db = VectorDatabase(
            collection_name="test_collection",
            persist_directory="./test_chroma_db"
        )
        
        # Add test documents
        test_chunks = [
            {'text': 'Python is a programming language', 'source': 'test'},
            {'text': 'Machine learning uses algorithms', 'source': 'test'}
        ]
        
        db.add_documents(test_chunks)
        print(f"✓ Added {len(test_chunks)} documents")
        
        # Query
        results = db.query("programming", n_results=1)
        print(f"✓ Query successful: found {len(results['documents'])} results")
        
        # Cleanup
        db.delete_collection()
        print("✓ Collection deleted")
        
        # Clean up directory
        import shutil
        shutil.rmtree("./test_chroma_db", ignore_errors=True)
        
        return True
        
    except Exception as e:
        print(f"❌ Vector database test failed: {e}")
        return False


def test_environment_variables():
    """Test 4: Check environment variables."""
    print("\n" + "="*80)
    print("Test 4: Testing Environment Variables")
    print("="*80)
    
    import os
    from dotenv import load_dotenv
    
    load_dotenv()
    
    openai_key = os.getenv("OPENAI_API_KEY")
    anthropic_key = os.getenv("ANTHROPIC_API_KEY")
    google_key = os.getenv("GOOGLE_API_KEY")
    
    if openai_key and openai_key != "your_openai_api_key_here":
        print("✓ OpenAI API key found")
    else:
        print("⚠️  OpenAI API key not configured")
    
    if anthropic_key and anthropic_key != "your_anthropic_api_key_here":
        print("✓ Anthropic API key found")
    else:
        print("⚠️  Anthropic API key not configured")
    
    if google_key and google_key != "your_google_api_key_here":
        print("✓ Google Gemini API key found")
    else:
        print("⚠️  Google Gemini API key not configured")
    
    if (openai_key and openai_key != "your_openai_api_key_here") or \
       (anthropic_key and anthropic_key != "your_anthropic_api_key_here") or \
       (google_key and google_key != "your_google_api_key_here"):
        print("\n✓ At least one LLM API key configured")
        return True
    else:
        print("\n⚠️  No LLM API keys configured")
        print("Add your keys to .env file to use the RAG system")
        print("Note: Gemini is the default LLM provider")
        return False


def test_data_directory():
    """Test 5: Check data directory."""
    print("\n" + "="*80)
    print("Test 5: Testing Data Directory")
    print("="*80)
    
    data_dir = Path("data")
    
    if not data_dir.exists():
        print("❌ Data directory not found")
        return False
    
    pdf_files = list(data_dir.glob("*.pdf"))
    audio_files = []
    for ext in ['.mp3', '.wav', '.m4a', '.flac', '.ogg']:
        audio_files.extend(data_dir.glob(f"*{ext}"))
    
    print(f"✓ Data directory exists")
    print(f"  Found {len(pdf_files)} PDF files")
    print(f"  Found {len(audio_files)} audio files")
    
    if pdf_files:
        for pdf in pdf_files[:3]:
            print(f"    - {pdf.name}")
    
    if audio_files:
        for audio in audio_files[:3]:
            print(f"    - {audio.name}")
    
    if not pdf_files and not audio_files:
        print("\n⚠️  No data files found in data/ directory")
        print("Add PDF or audio files to test the full pipeline")
    
    return True


def test_pdf_loader():
    """Test 6: Test PDF loading (if PDFs exist)."""
    print("\n" + "="*80)
    print("Test 6: Testing PDF Loader")
    print("="*80)
    
    data_dir = Path("data")
    pdf_files = list(data_dir.glob("*.pdf"))
    
    if not pdf_files:
        print("⚠️  No PDF files to test")
        print("Add a PDF to data/ directory to test this feature")
        return True
    
    try:
        from modules.pdf_loader import PDFLoader
        
        pdf_path = pdf_files[0]
        print(f"Testing with: {pdf_path.name}")
        
        loader = PDFLoader(str(pdf_path))
        text = loader.extract_text()
        
        print(f"✓ Extracted {len(text)} characters")
        print(f"✓ Preview: {text[:100]}...")
        return True
        
    except Exception as e:
        print(f"❌ PDF loading failed: {e}")
        return False


def test_system_requirements():
    """Test 7: Check system requirements."""
    print("\n" + "="*80)
    print("Test 7: Testing System Requirements")
    print("="*80)
    
    import sys
    print(f"✓ Python version: {sys.version.split()[0]}")
    
    # Check Python version
    if sys.version_info >= (3, 8):
        print("✓ Python 3.8+ requirement met")
    else:
        print("❌ Python 3.8+ required")
        return False
    
    # Check key packages
    packages = [
        'torch',
        'whisper',
        'chromadb',
        'sentence_transformers',
        'langchain',
        'openai',
        'anthropic'
    ]
    
    missing = []
    for package in packages:
        try:
            __import__(package)
            print(f"✓ {package} installed")
        except ImportError:
            print(f"❌ {package} not installed")
            missing.append(package)
    
    if missing:
        print(f"\n❌ Missing packages: {', '.join(missing)}")
        print("Run: pip install -r requirements.txt")
        return False
    
    return True


def run_all_tests():
    """Run all tests."""
    print("\n" + "="*80)
    print("RAG Pipeline - Component Tests")
    print("="*80)
    
    tests = [
        ("System Requirements", test_system_requirements),
        ("Imports", test_imports),
        ("Text Chunker", test_text_chunker),
        ("Vector Database", test_vector_database),
        ("Environment Variables", test_environment_variables),
        ("Data Directory", test_data_directory),
        ("PDF Loader", test_pdf_loader),
    ]
    
    results = []
    for name, test_func in tests:
        try:
            result = test_func()
            results.append((name, result))
        except Exception as e:
            print(f"\n❌ Unexpected error in {name}: {e}")
            results.append((name, False))
    
    # Summary
    print("\n" + "="*80)
    print("Test Summary")
    print("="*80)
    
    passed = sum(1 for _, result in results if result)
    total = len(results)
    
    for name, result in results:
        status = "✓ PASS" if result else "❌ FAIL"
        print(f"{status}: {name}")
    
    print(f"\nPassed: {passed}/{total}")
    
    if passed == total:
        print("\n🎉 All tests passed! Your RAG pipeline is ready to use.")
        print("\nNext steps:")
        print("1. Add your data files to data/ directory")
        print("2. Run: python main.py --interactive")
    else:
        print("\n⚠️  Some tests failed. Please resolve the issues above.")
        print("\nCommon fixes:")
        print("1. Install dependencies: pip install -r requirements.txt")
        print("2. Configure API keys: cp .env.example .env")
        print("3. Add data files: cp your_file.pdf data/")
    
    return passed == total


if __name__ == "__main__":
    success = run_all_tests()
    sys.exit(0 if success else 1)
