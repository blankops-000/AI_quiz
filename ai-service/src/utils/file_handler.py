import os
import json
import logging
from typing import Dict, Any, List
import pickle

logger = logging.getLogger(__name__)

class FileHandler:
    def __init__(self, base_path: str = "./data"):
        self.base_path = base_path
        self.ensure_directory_exists(base_path)
    
    def ensure_directory_exists(self, path: str):
        """Ensure directory exists, create if not"""
        try:
            os.makedirs(path, exist_ok=True)
        except Exception as e:
            logger.error(f"Failed to create directory {path}: {str(e)}")
    
    def save_json(self, data: Dict[str, Any], filename: str) -> bool:
        """Save data as JSON file"""
        try:
            filepath = os.path.join(self.base_path, filename)
            with open(filepath, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
            logger.info(f"JSON data saved to {filepath}")
            return True
        except Exception as e:
            logger.error(f"Failed to save JSON to {filename}: {str(e)}")
            return False
    
    def load_json(self, filename: str) -> Dict[str, Any]:
        """Load data from JSON file"""
        try:
            filepath = os.path.join(self.base_path, filename)
            if not os.path.exists(filepath):
                logger.warning(f"JSON file not found: {filepath}")
                return {}
            
            with open(filepath, 'r', encoding='utf-8') as f:
                data = json.load(f)
            logger.info(f"JSON data loaded from {filepath}")
            return data
        except Exception as e:
            logger.error(f"Failed to load JSON from {filename}: {str(e)}")
            return {}
    
    def save_pickle(self, data: Any, filename: str) -> bool:
        """Save data as pickle file"""
        try:
            filepath = os.path.join(self.base_path, filename)
            with open(filepath, 'wb') as f:
                pickle.dump(data, f)
            logger.info(f"Pickle data saved to {filepath}")
            return True
        except Exception as e:
            logger.error(f"Failed to save pickle to {filename}: {str(e)}")
            return False
    
    def load_pickle(self, filename: str) -> Any:
        """Load data from pickle file"""
        try:
            filepath = os.path.join(self.base_path, filename)
            if not os.path.exists(filepath):
                logger.warning(f"Pickle file not found: {filepath}")
                return None
            
            with open(filepath, 'rb') as f:
                data = pickle.load(f)
            logger.info(f"Pickle data loaded from {filepath}")
            return data
        except Exception as e:
            logger.error(f"Failed to load pickle from {filename}: {str(e)}")
            return None
    
    def save_text(self, text: str, filename: str) -> bool:
        """Save text to file"""
        try:
            filepath = os.path.join(self.base_path, filename)
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(text)
            logger.info(f"Text saved to {filepath}")
            return True
        except Exception as e:
            logger.error(f"Failed to save text to {filename}: {str(e)}")
            return False
    
    def load_text(self, filename: str) -> str:
        """Load text from file"""
        try:
            filepath = os.path.join(self.base_path, filename)
            if not os.path.exists(filepath):
                logger.warning(f"Text file not found: {filepath}")
                return ""
            
            with open(filepath, 'r', encoding='utf-8') as f:
                text = f.read()
            logger.info(f"Text loaded from {filepath}")
            return text
        except Exception as e:
            logger.error(f"Failed to load text from {filename}: {str(e)}")
            return ""
    
    def list_files(self, extension: str = None) -> List[str]:
        """List files in the base directory"""
        try:
            files = []
            for filename in os.listdir(self.base_path):
                filepath = os.path.join(self.base_path, filename)
                if os.path.isfile(filepath):
                    if extension is None or filename.endswith(extension):
                        files.append(filename)
            return files
        except Exception as e:
            logger.error(f"Failed to list files: {str(e)}")
            return []
    
    def delete_file(self, filename: str) -> bool:
        """Delete a file"""
        try:
            filepath = os.path.join(self.base_path, filename)
            if os.path.exists(filepath):
                os.remove(filepath)
                logger.info(f"File deleted: {filepath}")
                return True
            else:
                logger.warning(f"File not found for deletion: {filepath}")
                return False
        except Exception as e:
            logger.error(f"Failed to delete file {filename}: {str(e)}")
            return False
    
    def file_exists(self, filename: str) -> bool:
        """Check if file exists"""
        filepath = os.path.join(self.base_path, filename)
        return os.path.exists(filepath)
    
    def get_file_size(self, filename: str) -> int:
        """Get file size in bytes"""
        try:
            filepath = os.path.join(self.base_path, filename)
            if os.path.exists(filepath):
                return os.path.getsize(filepath)
            return 0
        except Exception as e:
            logger.error(f"Failed to get file size for {filename}: {str(e)}")
            return 0