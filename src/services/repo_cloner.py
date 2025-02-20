"""Git repository cloning service."""
import tempfile
import shutil
from dataclasses import dataclass
from urllib.parse import urlparse
from typing import Optional
import git

@dataclass
class RepoInfo:
    """Information about a repository."""
    url: str
    branch: str
    subdir: str
    clone_path: str

class RepoCloner:
    """Handles git repository cloning operations."""
    
    def clone(self, github_url: str) -> RepoInfo:
        """Clone a GitHub repository and return its information."""
        repo_url, branch, subdir = self._parse_github_url(github_url)
        clone_path = self._clone_to_temp(repo_url, branch)
        
        return RepoInfo(
            url=repo_url,
            branch=branch,
            subdir=subdir,
            clone_path=clone_path
        )
    
    def cleanup(self, repo_info: RepoInfo) -> None:
        """Clean up cloned repository."""
        if repo_info.clone_path:
            shutil.rmtree(repo_info.clone_path, ignore_errors=True)
    
    def _parse_github_url(self, url: str) -> tuple[str, str, str]:
        """Parse GitHub URL into components."""
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
    
    def _clone_to_temp(self, repo_url: str, branch: str) -> str:
        """Clone repository to temporary directory."""
        tmp_dir = tempfile.mkdtemp(prefix="repo-clone-")
        try:
            git.Repo.clone_from(repo_url, tmp_dir, branch=branch, depth=1)
            return tmp_dir
        except Exception as exc:
            shutil.rmtree(tmp_dir, ignore_errors=True)
            raise RuntimeError(f"Failed to clone repository: {exc}") 