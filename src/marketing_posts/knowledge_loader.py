import os
from pathlib import Path
from typing import List
import pypdf

class KnowledgeLoader:
    """
    Loads knowledge documents from a directory.
    Supports: .txt, .md, .yaml, .yml, .pdf
    """
    
    SUPPORTED_EXTENSIONS = {'.txt', '.md', '.yaml', '.yml', '.pdf'}
    
    @staticmethod
    def load_knowledge(folder_name: str) -> str:
        """
        Scans the folder ./<folder_name>/ for supported documents and returns concatenated content.
        
        Args:
            folder_name: Name of the folder (relative to CWD) to scan.
            
        Returns:
            Concatenated text content of all valid documents.
        """
        folder_path = Path(folder_name)
        if not folder_path.exists() or not folder_path.is_dir():
            print(f"Knowledge folder '{folder_name}' not found. Skipping local document loading.")
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
            
            if suffix == '.pdf':
                return KnowledgeLoader._read_pdf(file_path)
            else:
                return file_path.read_text(encoding='utf-8', errors='replace')
                
        except Exception as e:
            print(f"Error reading {file_path}: {e}")
            return ""

    @staticmethod
    def _read_pdf(file_path: Path) -> str:
        """Extracts text from a PDF file."""
        text = []
        try:
            with open(file_path, 'rb') as f:
                reader = pypdf.PdfReader(f)
                for page in reader.pages:
                    text.append(page.extract_text())
            return "\n".join(text)
        except Exception as e:
            print(f"Error parsing PDF {file_path}: {e}")
            return ""
