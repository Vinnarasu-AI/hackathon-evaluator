from github_cloner import get_files_to_scan
from chunker import chunk_file
from embeddings import EmbeddingGenerator
from vector_store import VectorStore
from ollama_client import OllamaClient
from criteria import EVALUATION_CRITERIA
import os
import time

def evaluate_project(repo_path):
    """Main evaluation function"""
    print(f"Starting evaluation of {repo_path}")
    
    # Step 2: Get files to scan
    files = get_files_to_scan(repo_path)
    print(f"Found {len(files)} files to scan")
    
    # Step 3: Chunk files
    all_chunks = []
    for file in files:
        chunks = chunk_file(file)
        all_chunks.extend(chunks)
    print(f"Created {len(all_chunks)} chunks")
    
    # Step 4: Generate embeddings
    embedder = EmbeddingGenerator()
    embedded_chunks = embedder.generate_batch_embeddings(all_chunks)
    print(f"Generated {len(embedded_chunks)} embeddings")
    
    # Step 5: Store in vector DB
    vector_store = VectorStore()
    if embedded_chunks:
        vector_store.add_embeddings(embedded_chunks)
        vector_store.save()
    else:
        print("Warning: No embeddings generated")
        return {"error": "Failed to generate embeddings"}
    
    # Step 6-9: Evaluate each criterion
    ollama = OllamaClient(model="llama3:latest")  # Explicitly set to llama3
    results = {
        "project_name": os.path.basename(repo_path),
        "total_files": len(files),
        "total_chunks": len(all_chunks),
        "criteria_results": [],
        "timestamp": time.strftime("%Y-%m-%d %H:%M:%S")
    }
    
    total_score = 0
    
    for i, criterion in enumerate(EVALUATION_CRITERIA):
        print(f"\n[{i+1}/{len(EVALUATION_CRITERIA)}] Evaluating: {criterion['name']}")
        
        # Generate query embedding
        query_embedding = embedder.generate_embedding(criterion['query'])
        
        if query_embedding:
            # Search for relevant chunks
            relevant_chunks = vector_store.search(query_embedding, k=5)
            print(f"Found {len(relevant_chunks)} relevant chunks")
            
            # Get evaluation from Ollama (now using Llama3)
            result = ollama.evaluate_criterion(criterion, relevant_chunks)
            
            if result:
                results['criteria_results'].append(result)
                total_score += result.get('score', 0)
                print(f"Score: {result.get('score', 0)}/10")
            else:
                # Fallback result
                results['criteria_results'].append({
                    "criterion": criterion['name'],
                    "score": 5,
                    "issues": ["Evaluation failed - check Ollama connection"],
                    "suggestions": ["Ensure Ollama is running with llama3:latest"]
                })
                total_score += 5
        else:
            results['criteria_results'].append({
                "criterion": criterion['name'],
                "score": 5,
                "issues": ["Failed to generate query embedding"],
                "suggestions": ["Check embedding model (nomic-embed-text)"]
            })
            total_score += 5
    
    # Step 10: Calculate final score
    results['total_score'] = total_score
    results['max_score'] = len(EVALUATION_CRITERIA) * 10
    results['percentage'] = round((total_score / results['max_score']) * 100, 2)
    
    print(f"\n{'='*50}")
    print(f"Evaluation complete!")
    print(f"Total Score: {total_score}/{results['max_score']} ({results['percentage']}%)")
    print(f"{'='*50}")
    
    return results