import os
from pathlib import Path
from typing import List


class KnowledgeLoader:
    """
    Loads knowledge documents from a directory.
    Supports: .txt, .md, .yaml, .yml, .pdf
    """
    
    SUPPORTED_EXTENSIONS = {'.txt', '.md', '.yaml', '.yml'}
    
    @staticmethod
    def load_knowledge(folder_name: str) -> str:
        """
        Scans the folder ./Knowledgebases/<folder_name>/ (or ./<folder_name>/) 
        for supported documents and returns concatenated content.
        
        Args:
            folder_name: Name of the folder (relative to CWD) to scan.
            
        Returns:
            Concatenated text content of all valid documents.
        """
        # Primary location: Knowledgebases/folder_name
        folder_path = Path("Knowledgebases") / folder_name
        
        # Fallback: ./folder_name (legacy support)
        if not folder_path.exists() or not folder_path.is_dir():
            folder_path_legacy = Path(folder_name)
            if folder_path_legacy.exists() and folder_path_legacy.is_dir():
                folder_path = folder_path_legacy
            else:
                print(f"Knowledge folder for '{folder_name}' not found in 'Knowledgebases/' or root. Skipping local document loading.")
                return ""
            
        print(f"Scanning knowledge folder: {folder_path.absolute()}")
        
        all_content = []
        
        # Walk through the directory
        for root, _, files in os.walk(folder_path):
            for file in files:
                file_path = Path(root) / file
                
                # Check extension
                if file_path.suffix.lower() not in KnowledgeLoader.SUPPORTED_EXTENSIONS:
                    if file_path.suffix.lower() in {'.png', '.jpg', '.jpeg'}:
                        print(f"Warning: Image file '{file}' found but image processing is not yet enabled. Skipping.")
                    continue
                    
                print(f"Loading document: {file_path}")
                content = KnowledgeLoader._read_file(file_path)
                if content:
                    all_content.append(f"\n\n--- Document: {file} ---\n{content}")
                    
        if not all_content:
            return ""
            
        return "\n\n# Local Company Documents\n" + "".join(all_content)

    @staticmethod
    def _read_file(file_path: Path) -> str:
        """Reads a single file based on extension."""
        try:
            suffix = file_path.suffix.lower()
            
            return file_path.read_text(encoding='utf-8', errors='replace')
                
        except Exception as e:
            print(f"Error reading {file_path}: {e}")
            return ""


