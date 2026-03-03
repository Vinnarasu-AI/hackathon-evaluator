import os
import git
import shutil
from pathlib import Path

import stat

def remove_readonly(func, path, _: any):
    """Clear the readonly bit and reattempt the removal"""
    os.chmod(path, stat.S_IWRITE)
    func(path)

def clone_repository(github_url):
    """Clone GitHub repository and return local path"""
    try:
        # Get absolute path for uploads
        current_dir = os.path.dirname(os.path.abspath(__file__))
        uploads_dir = os.path.join(current_dir, 'uploads')
        os.makedirs(uploads_dir, exist_ok=True)
        
        # Extract repo name
        if github_url.endswith('.git'):
            repo_name = github_url.split('/')[-1].replace('.git', '')
        else:
            repo_name = github_url.split('/')[-1]
        
        repo_path = os.path.join(uploads_dir, repo_name)
        
        # Remove if already exists (with Windows read-only fix)
        if os.path.exists(repo_path):
            print(f"Removing existing directory: {repo_path}")
            shutil.rmtree(repo_path, onerror=remove_readonly)
        
        # Clone repository
        print(f"Cloning {github_url} to {repo_path}...")
        git.Repo.clone_from(github_url, repo_path, depth=1)  # depth=1 for faster clone
        print(f"Clone complete!")
        
        return repo_path
    
    except git.GitCommandError as e:
        raise Exception(f"Git error: {str(e)}")
    except Exception as e:
        raise Exception(f"Failed to clone repository: {str(e)}")

def get_files_to_scan(repo_path):
    """Get all relevant files for scanning"""
    relevant_extensions = {
        '.py', '.js', '.java', '.html', '.css', 
        '.md', '.txt', '.json', '.yml', '.yaml',
        '.rb', '.go', '.rs', '.php', '.ts'
    }
    
    # Always include these files even if extension not matched
    always_include = ['README.md', 'package.json', 'requirements.txt', 
                      'Dockerfile', 'Makefile', '.env.example']
    
    files_to_scan = []
    skipped_dirs = {'node_modules', '__pycache__', '.git', 'venv', 'env',
                    'dist', 'build', 'images', 'videos', 'binaries'}
    
    for root, dirs, files in os.walk(repo_path):
        # Skip unwanted directories
        dirs[:] = [d for d in dirs if d not in skipped_dirs]
        
        for file in files:
            file_path = os.path.join(root, file)
            
            # Skip binary/large files
            try:
                if os.path.getsize(file_path) > 1024 * 1024:  # 1MB
                    continue
            except:
                continue
            
            file_ext = os.path.splitext(file)[1].lower()
            
            # Check if file should be scanned
            if file_ext in relevant_extensions or file in always_include:
                files_to_scan.append(file_path)
    
    print(f"Found {len(files_to_scan)} files to scan")
    return files_to_scan