import requests
import json

class EmbeddingGenerator:
    def __init__(self, model="nomic-embed-text"):  # Keep nomic-embed-text for embeddings
        self.model = model  # nomic-embed-text is best for embeddings
        self.ollama_url = "http://localhost:11434/api/embeddings"
    
    def generate_embedding(self, text):
        """Generate embedding for a text chunk using Ollama"""
        try:
            payload = {
                "model": self.model,  # This stays as nomic-embed-text
                "prompt": text[:2000]  # Limit text length for embeddings
            }
            
            response = requests.post(self.ollama_url, json=payload)
            if response.status_code == 200:
                result = response.json()
                return result.get('embedding', [])
            else:
                print(f"Error generating embedding: {response.status_code}")
                return None
        except Exception as e:
            print(f"Exception in embedding generation: {e}")
            return None

    def generate_batch_embeddings(self, chunks):
        """Generate embeddings for a list of chunks"""
        print(f"Generating embeddings for {len(chunks)} chunks...")
        embedded_chunks = []
        for i, chunk in enumerate(chunks):
            if i % 10 == 0:
                print(f"Progress: {i}/{len(chunks)} chunks processed")
            
            embedding = self.generate_embedding(chunk['text'])
            if embedding:
                chunk['embedding'] = embedding
                embedded_chunks.append(chunk)
            
        return embedded_chunks