"""
Text Chunking Module
Splits text into smaller, semantically meaningful chunks for embedding.
"""

from typing import List, Dict, Optional
import re
from langchain.text_splitter import RecursiveCharacterTextSplitter, CharacterTextSplitter


class TextChunker:
    """Splits text into semantically meaningful chunks."""
    
    def __init__(
        self, 
        chunk_size: int = 1000,
        chunk_overlap: int = 200,
        separators: Optional[List[str]] = None
    ):
        """
        Initialize text chunker.
        
        Args:
            chunk_size: Maximum size of each chunk in characters
            chunk_overlap: Number of overlapping characters between chunks
            separators: List of separators to split on (default: paragraphs, sentences, etc.)
        """
        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap
        
        # Default separators: try to split on paragraphs, then sentences, then words
        if separators is None:
            separators = ["\n\n", "\n", ". ", "! ", "? ", "; ", ", ", " ", ""]
        
        self.splitter = RecursiveCharacterTextSplitter(
            chunk_size=chunk_size,
            chunk_overlap=chunk_overlap,
            separators=separators,
            length_function=len
        )
    
    def chunk_text(self, text: str, metadata: Optional[Dict] = None) -> List[Dict]:
        """
        Split text into chunks with metadata.
        
        Args:
            text: Input text to chunk
            metadata: Optional metadata to attach to each chunk
        
        Returns:
            List of dictionaries containing chunk text and metadata
        """
        if not text or not text.strip():
            return []
        
        # Clean the text
        text = self._clean_text(text)
        
        # Split into chunks
        chunks = self.splitter.split_text(text)
        
        # Add metadata to each chunk
        chunk_data = []
        for i, chunk in enumerate(chunks):
            chunk_dict = {
                'text': chunk,
                'chunk_id': i,
                'chunk_size': len(chunk)
            }
            
            # Add custom metadata if provided
            if metadata:
                chunk_dict.update(metadata)
            
            chunk_data.append(chunk_dict)
        
        return chunk_data
    
    def chunk_documents(
        self, 
        documents: List[Dict[str, str]]
    ) -> List[Dict]:
        """
        Chunk multiple documents with their metadata.
        
        Args:
            documents: List of dictionaries with 'text' and optional metadata
        
        Returns:
            List of all chunks from all documents
        """
        all_chunks = []
        
        for doc_idx, doc in enumerate(documents):
            text = doc.get('text', '')
            
            # Prepare metadata
            metadata = {
                'doc_id': doc_idx,
                'source': doc.get('source', 'unknown')
            }
            
            # Add any additional metadata from the document
            for key, value in doc.items():
                if key not in ['text']:
                    metadata[key] = value
            
            # Chunk this document
            doc_chunks = self.chunk_text(text, metadata)
            all_chunks.extend(doc_chunks)
        
        return all_chunks
    
    @staticmethod
    def _clean_text(text: str) -> str:
        """
        Clean text by removing excessive whitespace and special characters.
        
        Args:
            text: Input text
        
        Returns:
            Cleaned text
        """
        # Replace multiple spaces with single space
        text = re.sub(r' +', ' ', text)
        
        # Replace multiple newlines with double newline
        text = re.sub(r'\n\s*\n', '\n\n', text)
        
        # Remove leading/trailing whitespace
        text = text.strip()
        
        return text
    
    def get_chunk_stats(self, chunks: List[Dict]) -> Dict:
        """
        Get statistics about the chunks.
        
        Args:
            chunks: List of chunk dictionaries
        
        Returns:
            Dictionary with chunk statistics
        """
        if not chunks:
            return {
                'total_chunks': 0,
                'avg_chunk_size': 0,
                'min_chunk_size': 0,
                'max_chunk_size': 0
            }
        
        chunk_sizes = [chunk['chunk_size'] for chunk in chunks]
        
        return {
            'total_chunks': len(chunks),
            'avg_chunk_size': sum(chunk_sizes) / len(chunk_sizes),
            'min_chunk_size': min(chunk_sizes),
            'max_chunk_size': max(chunk_sizes),
            'total_characters': sum(chunk_sizes)
        }


if __name__ == "__main__":
    # Example usage
    sample_text = """
    This is a sample document. It contains multiple sentences and paragraphs.
    
    This is the second paragraph. It demonstrates how the text chunker works.
    The chunker will split this text into smaller, manageable pieces.
    
    This is the third paragraph. Each chunk will have some overlap with the previous one.
    This helps maintain context across chunks.
    """
    
    chunker = TextChunker(chunk_size=100, chunk_overlap=20)
    chunks = chunker.chunk_text(sample_text, metadata={'source': 'example'})
    
    print(f"Created {len(chunks)} chunks:")
    for i, chunk in enumerate(chunks):
        print(f"\nChunk {i + 1}:")
        print(f"Size: {chunk['chunk_size']} characters")
        print(f"Text: {chunk['text'][:100]}...")
    
    stats = chunker.get_chunk_stats(chunks)
    print(f"\nChunk Statistics:")
    for key, value in stats.items():
        print(f"{key}: {value}")
