"""File system operations service."""
import os
from typing import List, Dict, Optional, Iterator
from dataclasses import dataclass

@dataclass
class FileInfo:
    """Information about a file."""
    path: str
    relative_path: str
    size: int
    extension: str
    is_binary: bool = False
    is_large: bool = False

class FileSystem:
    """Handles file system operations."""
    
    # Size thresholds
    CHUNK_SIZE = 100 * 1024  # 100KB chunks for large files
    LARGE_FILE_THRESHOLD = 1024 * 1024  # 1MB
    BINARY_CHECK_SIZE = 8000  # Bytes to check for binary content
    
    def __init__(self, max_file_size: int = 5 * 1024 * 1024):
        self.max_file_size = max_file_size
    
    def list_files(self, directory: str) -> List[FileInfo]:
        """List all files in directory recursively."""
        files = []
        
        for root, _, filenames in os.walk(directory):
            for filename in filenames:
                full_path = os.path.join(root, filename)
                try:
                    size = os.path.getsize(full_path)
                    if size > self.max_file_size:
                        continue
                        
                    rel_path = os.path.relpath(full_path, directory)
                    _, ext = os.path.splitext(filename)
                    
                    # Check if file is binary or large
                    is_binary = self._is_binary_file(full_path)
                    is_large = size > self.LARGE_FILE_THRESHOLD
                    
                    # Skip binary files
                    if is_binary:
                        continue
                    
                    files.append(FileInfo(
                        path=full_path,
                        relative_path=rel_path.replace('\\', '/'),
                        size=size,
                        extension=ext.lower(),
                        is_binary=is_binary,
                        is_large=is_large
                    ))
                except OSError:
                    continue
        
        return files
    
    def read_file(self, file_info: FileInfo) -> Optional[str]:
        """Read file content safely, with special handling for large files."""
        try:
            # For large files, read in chunks
            if file_info.is_large:
                return self._read_large_file(file_info.path)
            
            # For normal files, read directly
            with open(file_info.path, 'r', encoding='utf-8', errors='ignore') as f:
                return f.read()
        except Exception:
            return None
    
    def _read_large_file(self, path: str) -> str:
        """Read large file in chunks, focusing on important parts."""
        chunks = []
        total_size = 0
        
        # Read start of file
        with open(path, 'r', encoding='utf-8', errors='ignore') as f:
            # Read first chunk
            chunks.append(f.read(self.CHUNK_SIZE))
            total_size += self.CHUNK_SIZE
            
            # Skip to middle if file is very large
            middle_pos = os.path.getsize(path) // 2
            if middle_pos > self.CHUNK_SIZE:
                f.seek(middle_pos)
                chunks.append("\n... (truncated) ...\n")
                chunks.append(f.read(self.CHUNK_SIZE))
                total_size += self.CHUNK_SIZE
            
            # Read end if there's room
            if total_size < self.LARGE_FILE_THRESHOLD:
                f.seek(-self.CHUNK_SIZE, 2)  # Seek from end
                chunks.append(f.read())
        
        return ''.join(chunks)
    
    def _is_binary_file(self, path: str) -> bool:
        """Check if a file appears to be binary."""
        try:
            with open(path, 'rb') as f:
                chunk = f.read(self.BINARY_CHECK_SIZE)
                return b'\0' in chunk  # Simple binary check
        except Exception:
            return True  # Assume binary on error 