"""Pattern matching service for file filtering."""
from typing import List, Set
import os
import pathspec

class PatternMatcher:
    """Handles pattern matching and file filtering using gitignore-style patterns."""
    
    def __init__(self, patterns: List[str]):
        self.raw_patterns = patterns
        self.processed_patterns = self._process_patterns(patterns)
        self.spec = pathspec.PathSpec.from_lines("gitwildmatch", self.processed_patterns)
        
        # Common directory patterns that should always be ignored
        self.force_ignore_dirs = {
            'node_modules',
            'dist',
            'build',
            '.git',
            'coverage',
            '__pycache__',
            '.cache',
            'target',
            'vendor'
        }
    
    def should_ignore(self, path: str) -> bool:
        """
        Check if a file should be ignored based on patterns.
        Implements behavior similar to minimatch with dot=true, matchBase=true, nocase=true
        """
        # Normalize path
        normalized_path = path.replace('\\', '/').lower()
        
        # Force ignore common large directories
        parts = normalized_path.split('/')
        if any(part in self.force_ignore_dirs for part in parts):
            return True
            
        # Check if any part of the path matches a force ignore pattern
        if any(
            part.startswith('.') or  # Hidden files/dirs
            part.endswith('.min.js') or  # Minified files
            part.endswith('.min.css') or
            part.endswith('.map')  # Source maps
            for part in parts
        ):
            return True
        
        return self.spec.match_file(normalized_path)
    
    def _process_patterns(self, patterns: List[str]) -> List[str]:
        """Process patterns to match minimatch behavior."""
        processed: Set[str] = set()
        
        for pattern in patterns:
            # Normalize pattern
            pattern = pattern.replace('\\', '/').lower().rstrip('/')
            
            # Add base pattern
            processed.add(pattern)
            
            # Handle directory patterns (similar to minimatch behavior)
            if not any(c in pattern for c in '*?[]{}'):
                # Add pattern with trailing /**
                processed.add(f"{pattern}/**")
                
                # Add matchBase-like variants (match in any subdirectory)
                if '/' in pattern:
                    base = os.path.basename(pattern)
                    if base:
                        processed.add(f"**/{base}")
                        processed.add(f"**/{base}/**")
            
            # Handle .* patterns (match in root and all subdirs)
            if pattern.endswith('.*'):
                base = pattern[:-2]
                processed.add(f"{base}/**/*.*")
                processed.add(f"**/{base}/**/*.*")
            
            # Always add **/ prefix variant for deep matching
            if not pattern.startswith('**/'):
                processed.add(f"**/{pattern}")
        
        return list(processed) 