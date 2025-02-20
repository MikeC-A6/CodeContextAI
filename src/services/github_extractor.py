import os
import re
import shutil
import tempfile
from urllib.parse import urlparse
from typing import List, Dict, Optional
import json
from dataclasses import dataclass

import git
import pathspec

from ..config.ignore_patterns import DEFAULT_IGNORE_PATTERNS
from .pattern_matcher import PatternMatcher
from .file_system import FileSystem, FileInfo
from .repo_cloner import RepoCloner, RepoInfo

@dataclass
class ExtractedFile:
    """Represents an extracted file with its content."""
    path: str
    content: str
    language: str
    type: str = "code"
    size: int = 0
    is_truncated: bool = False

class GitHubExtractor:
    """Extracts code from GitHub repositories with intelligent filtering."""
    
    def __init__(self, max_file_size_bytes: int = 5 * 1024 * 1024):
        self.pattern_matcher = PatternMatcher(DEFAULT_IGNORE_PATTERNS)
        self.file_system = FileSystem(max_file_size_bytes)
        self.repo_cloner = RepoCloner()
    
    def analyze_repo(self, github_url: str) -> Dict:
        """Analyze repository without downloading content."""
        repo_info = None
        try:
            repo_info = self.repo_cloner.clone(github_url)
            target_dir = self._get_target_dir(repo_info)
            
            # Get filtered files
            files = self._get_filtered_files(target_dir)
            
            # Analyze files
            total_size = sum(f.size for f in files)
            by_extension = {}
            for f in files:
                by_extension[f.extension] = by_extension.get(f.extension, 0) + 1
            
            large_files = [f.relative_path for f in files if f.is_large]
            
            return {
                "total_files": len(files),
                "total_size_bytes": total_size,
                "by_extension": by_extension,
                "large_files": large_files,
                "processed_patterns": self.pattern_matcher.processed_patterns
            }
            
        finally:
            if repo_info:
                self.repo_cloner.cleanup(repo_info)
    
    def extract_to_jsonl(self, github_url: str) -> List[Dict]:
        """Extract code from GitHub URL to JSONL format."""
        # First analyze the repo
        analysis = self.analyze_repo(github_url)
        
        # Check total size
        total_size_mb = analysis["total_size_bytes"] / (1024 * 1024)
        if total_size_mb > 50:  # 50MB limit
            raise ValueError(
                f"Repository is too large ({total_size_mb:.1f}MB). "
                f"Contains {len(analysis['large_files'])} large files. "
                "Please use a smaller repository or specify a subdirectory."
            )
        
        # Now do the actual extraction
        repo_info = None
        try:
            repo_info = self.repo_cloner.clone(github_url)
            target_dir = self._get_target_dir(repo_info)
            files = self._get_filtered_files(target_dir)
            return self._convert_to_jsonl(files)
        finally:
            if repo_info:
                self.repo_cloner.cleanup(repo_info)
    
    def _get_target_dir(self, repo_info: RepoInfo) -> str:
        """Get the target directory to process."""
        if repo_info.subdir:
            full_path = os.path.join(repo_info.clone_path, repo_info.subdir)
            if not os.path.isdir(full_path):
                raise ValueError(f"Subdirectory does not exist: {repo_info.subdir}")
            return full_path
        return repo_info.clone_path
    
    def _get_filtered_files(self, directory: str) -> List[FileInfo]:
        """Get list of files after applying ignore patterns."""
        all_files = self.file_system.list_files(directory)
        return [f for f in all_files if not self.pattern_matcher.should_ignore(f.relative_path)]
    
    def _convert_to_jsonl(self, files: List[FileInfo]) -> List[Dict]:
        """Convert files to JSONL format."""
        result = []
        for file_info in files:
            content = self.file_system.read_file(file_info)
            if content is None:
                continue
                
            language = self._map_extension_to_language(file_info.extension)
            extracted = ExtractedFile(
                path=file_info.relative_path,
                content=content,
                language=language or "unknown",
                size=file_info.size,
                is_truncated=file_info.is_large
            )
            
            result.append(extracted.__dict__)
        
        return result
    
    def _map_extension_to_language(self, ext: str) -> Optional[str]:
        """Map file extension to language name."""
        ext_map = {
            # Python
            ".py": "python",
            ".pyi": "python",
            ".pyx": "python",
            # JavaScript/TypeScript
            ".js": "javascript",
            ".jsx": "javascript",
            ".ts": "typescript",
            ".tsx": "typescript",
            # Web
            ".html": "html",
            ".htm": "html",
            ".css": "css",
            ".scss": "scss",
            ".sass": "scss",
            ".less": "less",
            # Java
            ".java": "java",
            ".kt": "kotlin",
            ".scala": "scala",
            ".groovy": "groovy",
            # C-family
            ".c": "c",
            ".h": "c",
            ".cpp": "cpp",
            ".hpp": "cpp",
            ".cc": "cpp",
            ".cxx": "cpp",
            ".cs": "csharp",
            # Other languages
            ".go": "go",
            ".rb": "ruby",
            ".php": "php",
            ".rs": "rust",
            ".swift": "swift",
            ".m": "objective-c",
            ".lua": "lua",
            ".pl": "perl",
            ".sh": "shell",
            ".bash": "shell",
            ".zsh": "shell",
            ".fish": "shell",
            # Template files
            ".jinja": "jinja",
            ".jinja2": "jinja",
            ".j2": "jinja",
            ".template": "template"
        }
        return ext_map.get(ext) 