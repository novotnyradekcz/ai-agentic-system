"""
Vector Database Module
Handles embedding generation and storage in ChromaDB.
"""

import chromadb
from chromadb.config import Settings
from sentence_transformers import SentenceTransformer
from typing import List, Dict, Optional
import os
import sys
from pathlib import Path
from tqdm import tqdm
import warnings
import contextlib

# Disable ChromaDB telemetry to avoid error messages
os.environ['ANONYMIZED_TELEMETRY'] = 'False'
os.environ['CHROMA_TELEMETRY_IMPL'] = 'none'

# Suppress telemetry errors from ChromaDB (known issue with ChromaDB's telemetry)
import logging
logging.getLogger('chromadb.telemetry.posthog').setLevel(logging.CRITICAL)
logging.getLogger('chromadb.telemetry').setLevel(logging.CRITICAL)


class VectorDatabase:
    """Manages embeddings and vector database operations using ChromaDB."""
    
    def __init__(
        self,
        collection_name: str = "rag_documents",
        embedding_model: str = "all-MiniLM-L6-v2",
        persist_directory: str = "./chroma_db"
    ):
        """
        Initialize the vector database.
        
        Args:
            collection_name: Name of the ChromaDB collection
            embedding_model: Name of the sentence-transformers model
            persist_directory: Directory to persist the database
        """
        self.collection_name = collection_name
        self.persist_directory = persist_directory
        
        # Create persist directory if it doesn't exist
        Path(persist_directory).mkdir(parents=True, exist_ok=True)
        
        # Initialize ChromaDB client
        print(f"Initializing ChromaDB at: {persist_directory}")
        self.client = chromadb.PersistentClient(
            path=persist_directory,
            settings=Settings(
                anonymized_telemetry=False  # Disable telemetry to avoid error messages
            )
        )
        
        # Load embedding model
        print(f"Loading embedding model: {embedding_model}")
        self.embedding_model = SentenceTransformer(embedding_model)
        print("Model loaded successfully!")
        
        # Get or create collection
        try:
            self.collection = self.client.get_collection(name=collection_name)
            print(f"Loaded existing collection: {collection_name}")
        except:
            self.collection = self.client.create_collection(
                name=collection_name,
                metadata={"hnsw:space": "cosine"}
            )
            print(f"Created new collection: {collection_name}")
    
    def generate_embeddings(self, texts: List[str]) -> List[List[float]]:
        """
        Generate embeddings for a list of texts.
        
        Args:
            texts: List of text strings
        
        Returns:
            List of embedding vectors
        """
        print(f"Generating embeddings for {len(texts)} texts...")
        embeddings = self.embedding_model.encode(
            texts,
            show_progress_bar=True,
            convert_to_numpy=True
        )
        return embeddings.tolist()
    
    def add_documents(self, chunks: List[Dict], batch_size: int = 100):
        """
        Add document chunks to the vector database.
        
        Args:
            chunks: List of chunk dictionaries with 'text' and metadata
            batch_size: Number of documents to process at once
        """
        if not chunks:
            print("No chunks to add!")
            return
        
        print(f"\nAdding {len(chunks)} chunks to the database...")
        
        # Process in batches
        for i in tqdm(range(0, len(chunks), batch_size), desc="Processing batches"):
            batch = chunks[i:i + batch_size]
            
            # Extract texts
            texts = [chunk['text'] for chunk in batch]
            
            # Generate unique IDs
            ids = [f"doc_{i+j}" for j in range(len(batch))]
            
            # Generate embeddings
            embeddings = self.generate_embeddings(texts)
            
            # Prepare metadata
            metadatas = []
            for chunk in batch:
                metadata = {k: str(v) for k, v in chunk.items() if k != 'text'}
                metadatas.append(metadata)
            
            # Add to collection
            self.collection.add(
                ids=ids,
                embeddings=embeddings,
                documents=texts,
                metadatas=metadatas
            )
        
        print(f"Successfully added {len(chunks)} chunks to the database!")
    
    def query(
        self,
        query_text: str,
        n_results: int = 5
    ) -> Dict:
        """
        Query the vector database for similar documents.
        
        Args:
            query_text: The search query
            n_results: Number of results to return
        
        Returns:
            Dictionary containing results with documents, distances, and metadata
        """
        # Generate query embedding
        query_embedding = self.embedding_model.encode([query_text])[0].tolist()
        
        # Query the collection
        results = self.collection.query(
            query_embeddings=[query_embedding],
            n_results=n_results
        )
        
        return {
            'documents': results['documents'][0],
            'distances': results['distances'][0],
            'metadatas': results['metadatas'][0],
            'ids': results['ids'][0]
        }
    
    def get_collection_stats(self) -> Dict:
        """
        Get statistics about the collection.
        
        Returns:
            Dictionary with collection statistics
        """
        count = self.collection.count()
        return {
            'name': self.collection_name,
            'total_documents': count,
            'persist_directory': self.persist_directory
        }
    
    def delete_collection(self):
        """Delete the entire collection."""
        self.client.delete_collection(name=self.collection_name)
        print(f"Deleted collection: {self.collection_name}")
    
    def reset_collection(self):
        """Reset the collection by deleting and recreating it."""
        try:
            self.delete_collection()
        except:
            pass
        
        self.collection = self.client.create_collection(
            name=self.collection_name,
            metadata={"hnsw:space": "cosine"}
        )
        print(f"Reset collection: {self.collection_name}")


if __name__ == "__main__":
    # Example usage
    db = VectorDatabase(collection_name="test_collection")
    
    # Sample documents
    sample_chunks = [
        {
            'text': 'This is the first document about machine learning.',
            'source': 'sample',
            'chunk_id': 0
        },
        {
            'text': 'This is the second document about deep learning.',
            'source': 'sample',
            'chunk_id': 1
        }
    ]
    
    # Add documents
    db.add_documents(sample_chunks)
    
    # Query
    results = db.query("machine learning", n_results=2)
    print(f"\nQuery Results:")
    for i, (doc, score) in enumerate(zip(results['documents'], results['distances'])):
        print(f"\n{i+1}. Score: {score:.4f}")
        print(f"   Text: {doc[:100]}...")
    
    # Stats
    stats = db.get_collection_stats()
    print(f"\nCollection Stats: {stats}")
