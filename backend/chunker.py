# import tiktoken

def chunk_file(file_path, max_tokens=400):
    """Split file into chunks of ~400 tokens"""
    try:
        with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
            content = f.read()
    except Exception as e:
        print(f"Error reading {file_path}: {e}")
        return []
    
    # Get relative path for metadata
    try:
        import os
        rel_path = os.path.relpath(file_path, os.path.dirname(os.path.dirname(file_path)))
    except:
        rel_path = os.path.basename(file_path)
    
    # Simple chunking by lines (each line roughly 10-20 tokens)
    lines = content.split('\n')
    chunks = []
    current_chunk = []
    current_tokens = 0
    
    # Rough estimate: 1 token ≈ 4 characters
    for line in lines:
        line_tokens = len(line) // 4
        
        if current_tokens + line_tokens > max_tokens and current_chunk:
            # Save current chunk
            chunk_text = '\n'.join(current_chunk)
            chunks.append({
                'file': rel_path,
                'chunk_id': len(chunks),
                'text': chunk_text,
                'tokens': current_tokens
            })
            current_chunk = []
            current_tokens = 0
        
        current_chunk.append(line)
        current_tokens += line_tokens
    
    # Add last chunk
    if current_chunk:
        chunk_text = '\n'.join(current_chunk)
        chunks.append({
            'file': rel_path,
            'chunk_id': len(chunks),
            'text': chunk_text,
            'tokens': current_tokens
        })
    
    return chunks