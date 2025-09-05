import os
from langchain_text_splitters import RecursiveCharacterTextSplitter
import json

# Define the directory where the cleaned documentation is stored
CLEAN_DOCS_DIR = "clean_docs"
CHUNKS_DIR = "chunks"
os.makedirs(CHUNKS_DIR, exist_ok=True)

def chunk_documents():
    """Reads documents and splits them into smaller, manageable chunks."""
    all_chunks = []
    
    # Text Splitter settings
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=200,
        length_function=len
    )

    print("Starting document chunking...")
    
    for filename in os.listdir(CLEAN_DOCS_DIR):
        if filename.endswith(".txt"):
            file_path = os.path.join(CLEAN_DOCS_DIR, filename)
            with open(file_path, "r", encoding="utf-8") as f:
                content = f.read()

            # Split the document into chunks
            chunks = text_splitter.split_text(content)
            
            # Add metadata to each chunk
            for chunk_content in chunks:
                chunk = {
                    "text": chunk_content,
                    "source": filename
                }
                all_chunks.append(chunk)

            print(f"Split {filename} into {len(chunks)} chunks.")

    # Save all chunks to a single JSON file
    with open(os.path.join(CHUNKS_DIR, "all_chunks.json"), "w", encoding="utf-8") as f:
        json.dump(all_chunks, f, indent=2)

    print(f"\nSuccessfully created {len(all_chunks)} total chunks.")
    print("Chunks saved to chunks/all_chunks.json")

if __name__ == "__main__":
    chunk_documents()