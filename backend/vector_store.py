import faiss
import numpy as np
import pickle
import os

class VectorStore:
    def __init__(self, dimension=768):  # nomic-embed-text dimension
        self.dimension = dimension
        self.index = faiss.IndexFlatL2(dimension)
        self.metadata = []
        self.id_to_chunk = {}
    
    def add_embeddings(self, embedded_chunks):
        """Add embeddings to FAISS index"""
        embeddings = []
        
        for chunk in embedded_chunks:
            embedding = np.array(chunk['embedding']).astype('float32')
            
            # Normalize embedding
            faiss.normalize_L2(embedding.reshape(1, -1))
            
            embeddings.append(embedding)
            
            # Store metadata
            metadata_id = len(self.metadata)
            self.metadata.append({
                'file': chunk['file'],
                'chunk_id': chunk['chunk_id'],
                'text': chunk['text']
            })
            self.id_to_chunk[metadata_id] = chunk
        
        if embeddings:
            embeddings_array = np.array(embeddings)
            self.index.add(embeddings_array)
        
        print(f"Added {len(embeddings)} chunks to vector store")
    
    def search(self, query_embedding, k=5):
        """Search for similar chunks"""
        query_array = np.array([query_embedding]).astype('float32')
        faiss.normalize_L2(query_array)
        
        distances, indices = self.index.search(query_array, k)
        
        results = []
        for i, idx in enumerate(indices[0]):
            if idx != -1 and idx < len(self.metadata):
                results.append({
                    **self.metadata[idx],
                    'distance': float(distances[0][i])
                })
        
        return results
    
    def save(self, path='../data/vector_db'):
        """Save vector store to disk"""
        os.makedirs(path, exist_ok=True)
        
        # Save FAISS index
        faiss.write_index(self.index, f'{path}/index.faiss')
        
        # Save metadata
        with open(f'{path}/metadata.pkl', 'wb') as f:
            pickle.dump({
                'metadata': self.metadata,
                'id_to_chunk': self.id_to_chunk
            }, f)
        
        print(f"Vector store saved to {path}")
    
    def load(self, path='../data/vector_db'):
        """Load vector store from disk"""
        if os.path.exists(f'{path}/index.faiss'):
            self.index = faiss.read_index(f'{path}/index.faiss')
            
            with open(f'{path}/metadata.pkl', 'rb') as f:
                data = pickle.load(f)
                self.metadata = data['metadata']
                self.id_to_chunk = data['id_to_chunk']
            
            print(f"Vector store loaded from {path}")
            return True
        return False