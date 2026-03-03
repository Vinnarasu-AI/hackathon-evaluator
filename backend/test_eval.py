from evaluator import evaluate_project
import os

# Create dummy repo path if needed, but better to test with a real small one
test_url = "https://github.com/octocat/Spoon-Knife"
from github_cloner import clone_repository
try:
    path = clone_repository(test_url)
    print(f"Cloned to {path}")
    results = evaluate_project(path)
    print("Evaluation successful!")
except Exception as e:
    import traceback
    print(f"Error: {e}")
    traceback.print_exc()
