import json
from typing import List, Dict

class FileHandler:
    """Handles JSONL file operations"""
    
    @staticmethod
    def parse_jsonl(content: str) -> List[Dict]:
        """Parse JSONL content into a list of dictionaries"""
        try:
            return [json.loads(line) for line in content.splitlines() if line.strip()]
        except json.JSONDecodeError as e:
            raise ValueError(f"Invalid JSONL format: {str(e)}")

    @staticmethod
    def extract_code_context(data: List[Dict]) -> str:
        """Extract code content from parsed JSONL data"""
        context = ""
        for item in data:
            if "path" in item and "content" in item:
                context += f"\nFile: {item['path']}\n"
                context += f"Content:\n{item['content']}\n"
        return context
