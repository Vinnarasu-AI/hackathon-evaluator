import requests
import json
import time

class OllamaClient:
    def __init__(self, model="llama3:latest"):
        self.model = model
        self.ollama_url = "http://localhost:11434/api/generate"
        self.embeddings_url = "http://localhost:11434/api/embeddings"
    
    def test_connection(self):
        """Test if Ollama is reachable"""
        try:
            response = requests.get('http://localhost:11434/api/tags', timeout=5)
            return response.status_code == 200
        except:
            return False
    
    def evaluate_criterion(self, criterion, chunks):
        """Send chunks to Ollama for evaluation"""
        
        # Test connection first
        if not self.test_connection():
            return self.fallback_response(criterion['name'], "Ollama not reachable")
        
        # Prepare context from chunks
        context_chunks = []
        for chunk in chunks[:3]:  # Limit to 3 chunks
            context_chunks.append(f"File: {chunk['file']}\n```\n{chunk['text'][:800]}...\n```")
        
        context = "\n\n".join(context_chunks)
        
        prompt = f"""You are a professional hackathon evaluator. Evaluate this criterion:

CRITERION: {criterion['name']}
DESCRIPTION: {criterion['description']}

CODE TO ANALYZE:
{context}

Return a JSON object with:
1. score: number from 0-10
2. issues: array of specific problems found
3. suggestions: array of actionable improvements

JSON RESPONSE:
{{
  "criterion": "{criterion['name']}",
  "score": 7,
  "issues": ["issue1", "issue2"],
  "suggestions": ["suggestion1", "suggestion2"]
}}

ONLY RETURN THE JSON. NO OTHER TEXT."""
        
        try:
            payload = {
                "model": self.model,
                "prompt": prompt,
                "stream": False,
                "options": {
                    "temperature": 0.1,
                    "top_p": 0.9,
                    "num_predict": 512
                }
            }
            
            response = requests.post(self.ollama_url, json=payload, timeout=60)
            
            if response.status_code == 200:
                result = response.json()
                response_text = result.get('response', '{}')
                
                # Clean response
                response_text = self.clean_json_response(response_text)
                
                try:
                    json_result = json.loads(response_text)
                    return self.validate_result(json_result, criterion['name'])
                except:
                    return self.fallback_response(criterion['name'], "Invalid JSON response")
            else:
                return self.fallback_response(criterion['name'], f"HTTP {response.status_code}")
                
        except requests.exceptions.Timeout:
            return self.fallback_response(criterion['name'], "Timeout")
        except Exception as e:
            print(f"Exception: {e}")
            return self.fallback_response(criterion['name'], str(e))
    
    def clean_json_response(self, text):
        """Extract JSON from response"""
        # Remove markdown
        text = text.replace('```json', '').replace('```', '')
        
        # Find first { and last }
        start = text.find('{')
        end = text.rfind('}') + 1
        
        if start != -1 and end > start:
            return text[start:end]
        return text
    
    def validate_result(self, result, criterion_name):
        """Ensure result has correct structure"""
        validated = {
            "criterion": result.get('criterion', criterion_name),
            "score": min(10, max(0, int(result.get('score', 5)))),
            "issues": result.get('issues', ['No issues identified']),
            "suggestions": result.get('suggestions', ['No suggestions available'])
        }
        
        # Ensure arrays
        if not isinstance(validated['issues'], list):
            validated['issues'] = [str(validated['issues'])]
        if not isinstance(validated['suggestions'], list):
            validated['suggestions'] = [str(validated['suggestions'])]
        
        return validated
    
    def fallback_response(self, criterion_name, reason="Unknown error"):
        """Return fallback response"""
        return {
            "criterion": criterion_name,
            "score": 5,
            "issues": [f"Evaluation failed: {reason}"],
            "suggestions": ["Check Ollama connection and try again"]
        }