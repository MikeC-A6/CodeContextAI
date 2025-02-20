import os
import re
import shutil
import tempfile
from urllib.parse import urlparse
from typing import List, Dict
import json

import git
import pathspec

# Default patterns to ignore when extracting code
DEFAULT_PATTERNS = [
    ".git/**",
    "node_modules/**",
    "*.pyc",
    "__pycache__/**",
    "*.jpg", "*.jpeg", "*.png", "*.gif", "*.ico",
    "*.pdf", "*.mov", "*.mp4", "*.mp3", "*.wav",
    "*.o", "*.so", "*.dll", "*.dylib",
    "*.class", "*.jar",
    "dist/**", "build/**",
    ".env",
]

class GitHubExtractor:
    def __init__(self, max_file_size_bytes: int = 5 * 1024 * 1024):
        self.max_file_size = max_file_size_bytes
        
    def extract_to_jsonl(self, github_url: str) -> List[Dict]:
        """
        Extract code from a GitHub URL (repo or subdirectory) and return as JSONL-compatible list.
        Each item in the list will have the format expected by the existing file handler:
        {
            "path": "relative/path/to/file",
            "content": "file contents",
            "language": "python",
            "type": "code"
        }
        """
        repo_url, branch, subdir = self._parse_github_url(github_url)
        temp_dir = None
        
        try:
            # Clone the repo
            temp_dir = self._clone_repo(repo_url, branch)
            
            # Build ignore spec
            ignore_spec = pathspec.PathSpec.from_lines("gitwildmatch", DEFAULT_PATTERNS)
            
            # Gather files
            files = self._gather_files(temp_dir, subdir, ignore_spec)
            
            # Convert to JSONL format
            return self._convert_to_jsonl(files, temp_dir)
            
        finally:
            if temp_dir:
                shutil.rmtree(temp_dir, ignore_errors=True)
    
    def _parse_github_url(self, url: str) -> tuple[str, str, str]:
        """Parse GitHub URL into (repo_url, branch, subdirectory)"""
        parsed = urlparse(url)
        segments = [s for s in parsed.path.split('/') if s]
        
        if len(segments) < 2:
            raise ValueError("Invalid GitHub URL: not enough path segments")
            
        org = segments[0]
        repo = segments[1]
        base_repo_url = f"https://github.com/{org}/{repo}.git"
        
        branch = "main"
        subdir_idx = 2
        if len(segments) >= 4 and segments[2] == "tree":
            branch = segments[3]
            subdir_idx = 4
            
        subdir = "/".join(segments[subdir_idx:])
        return base_repo_url, branch, subdir
    
    def _clone_repo(self, repo_url: str, branch: str) -> str:
        """Shallow clone the repo and return temp directory path"""
        tmp_dir = tempfile.mkdtemp(prefix="repo-clone-")
        try:
            git.Repo.clone_from(repo_url, tmp_dir, branch=branch, depth=1)
            return tmp_dir
        except Exception as exc:
            shutil.rmtree(tmp_dir, ignore_errors=True)
            raise RuntimeError(f"Failed to clone repository: {exc}")
    
    def _gather_files(self, base_path: str, subdirectory: str, ignore_spec) -> List[str]:
        """Gather all relevant files from the directory"""
        gathered = []
        target_dir = os.path.join(base_path, subdirectory) if subdirectory else base_path
        
        if not os.path.isdir(target_dir):
            raise ValueError(f"Subdirectory does not exist: {subdirectory}")
            
        for root, _, files in os.walk(target_dir):
            for filename in files:
                rel_path = os.path.relpath(os.path.join(root, filename), base_path)
                if ignore_spec.match_file(rel_path):
                    continue
                    
                full_path = os.path.join(root, filename)
                try:
                    if os.path.getsize(full_path) > self.max_file_size:
                        continue
                except OSError:
                    continue
                    
                gathered.append(full_path)
        return gathered
    
    def _convert_to_jsonl(self, file_paths: List[str], base_path: str) -> List[Dict]:
        """Convert files to JSONL format compatible with existing file handler"""
        result = []
        for fp in file_paths:
            rel_path = os.path.relpath(fp, base_path)
            try:
                with open(fp, "r", encoding="utf-8", errors="ignore") as f:
                    content = f.read()
            except Exception as exc:
                content = f"[Error reading file: {exc}]"
                
            # Determine language from extension
            _, ext = os.path.splitext(fp)
            language = self._map_extension_to_language(ext)
            
            result.append({
                "path": rel_path.replace("\\", "/"),
                "content": content,
                "language": language,
                "type": "code"
            })
        return result
    
    def _map_extension_to_language(self, ext: str) -> str:
        """Map file extension to language name"""
        ext = ext.lower()
        ext_map = {
            ".py": "python",
            ".js": "javascript",
            ".jsx": "javascript",
            ".ts": "typescript",
            ".tsx": "typescript",
            ".html": "html",
            ".css": "css",
            ".json": "json",
            ".md": "markdown",
            ".yml": "yaml",
            ".yaml": "yaml",
            ".java": "java",
            ".c": "c",
            ".cpp": "cpp",
            ".cs": "csharp",
        }
        return ext_map.get(ext, "unknown") 