import json
import faiss
import numpy as np
from sentence_transformers import SentenceTransformer
import os

# Define file paths
CHUNKS_FILE = "chunks/all_chunks.json"
VECTOR_STORE_DIR = "vector_store"
os.makedirs(VECTOR_STORE_DIR, exist_ok=True)
FAISS_INDEX_FILE = os.path.join(VECTOR_STORE_DIR, "docs.index")
METADATA_FILE = os.path.join(VECTOR_STORE_DIR, "metadata.json")

def create_vector_store():
    """
    Reads text chunks, converts them to vectors, and stores them in a FAISS index.
    """
    # Load the pre-trained Sentence Transformer model
    print("Loading Sentence Transformer model...")
    model = SentenceTransformer('all-MiniLM-L6-v2')
    
    # Load the text chunks from the JSON file
    print("Loading text chunks from JSON file...")
    with open(CHUNKS_FILE, "r", encoding="utf-8") as f:
        chunks_data = json.load(f)

    texts = [chunk['text'] for chunk in chunks_data]
    
    # Generate embeddings for all text chunks
    print("Generating embeddings for all chunks...")
    embeddings = model.encode(texts, convert_to_tensor=False)
    
    # Get the dimension of the embeddings
    dimension = embeddings.shape[1]
    
    # Create a FAISS index
    print("Creating FAISS index...")
    index = faiss.IndexFlatL2(dimension)
    
    # Add the embeddings to the index
    index.add(embeddings.astype('float32'))

    # Save the FAISS index and metadata
    print("Saving FAISS index and metadata...")
    faiss.write_index(index, FAISS_INDEX_FILE)
    
    metadata = [
        {"text": chunk['text'], "source": chunk['source']}
        for chunk in chunks_data
    ]
    with open(METADATA_FILE, "w", encoding="utf-8") as f:
        json.dump(metadata, f, indent=2)

    print("\nVector store successfully created!")
    print(f"FAISS index saved to {FAISS_INDEX_FILE}")
    print(f"Metadata saved to {METADATA_FILE}")
    print(f"Total documents indexed: {len(chunks_data)}")
    
if __name__ == "__main__":
    create_vector_store()