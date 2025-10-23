import re
import logging
from typing import List, Dict, Any

logger = logging.getLogger(__name__)

class PreprocessingService:
    def __init__(self):
        self.stop_words = {
            'english': {
                'a', 'an', 'and', 'are', 'as', 'at', 'be', 'by', 'for', 'from',
                'has', 'he', 'in', 'is', 'it', 'its', 'of', 'on', 'that', 'the',
                'to', 'was', 'will', 'with', 'the', 'this', 'but', 'they', 'have',
                'had', 'what', 'said', 'each', 'which', 'she', 'do', 'how', 'their',
                'if', 'up', 'out', 'many', 'then', 'them', 'these', 'so', 'some',
                'her', 'would', 'make', 'like', 'into', 'him', 'time', 'two', 'more',
                'go', 'no', 'way', 'could', 'my', 'than', 'first', 'been', 'call',
                'who', 'oil', 'sit', 'now', 'find', 'down', 'day', 'did', 'get',
                'come', 'made', 'may', 'part'
            }
        }
    
    def clean_text(self, text: str, language: str = 'english') -> str:
        """Clean and preprocess text"""
        try:
            if not text or not isinstance(text, str):
                return ""
            
            # Convert to lowercase
            text = text.lower()
            
            # Remove URLs
            text = re.sub(r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\\(\\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', '', text)
            
            # Remove email addresses
            text = re.sub(r'\S+@\S+', '', text)
            
            # Remove HTML tags
            text = re.sub(r'<[^>]+>', '', text)
            
            # Remove special characters but keep spaces and basic punctuation
            text = re.sub(r'[^a-zA-Z0-9\s\.\,\!\?\;\:]', '', text)
            
            # Remove extra whitespace
            text = re.sub(r'\s+', ' ', text)
            
            # Strip leading/trailing whitespace
            text = text.strip()
            
            return text
            
        except Exception as e:
            logger.error(f"Text cleaning failed: {str(e)}")
            return text if isinstance(text, str) else ""
    
    def tokenize(self, text: str) -> List[str]:
        """Tokenize text into words"""
        try:
            if not text:
                return []
            
            # Simple word tokenization
            tokens = re.findall(r'\b\w+\b', text.lower())
            return tokens
            
        except Exception as e:
            logger.error(f"Tokenization failed: {str(e)}")
            return []
    
    def remove_stop_words(self, tokens: List[str], language: str = 'english') -> List[str]:
        """Remove stop words from token list"""
        try:
            stop_words = self.stop_words.get(language, set())
            return [token for token in tokens if token not in stop_words]
            
        except Exception as e:
            logger.error(f"Stop word removal failed: {str(e)}")
            return tokens
    
    def normalize_text(self, text: str) -> str:
        """Normalize text for consistent processing"""
        try:
            if not text:
                return ""
            
            # Convert to lowercase
            text = text.lower()
            
            # Normalize whitespace
            text = re.sub(r'\s+', ' ', text)
            
            # Remove leading/trailing whitespace
            text = text.strip()
            
            return text
            
        except Exception as e:
            logger.error(f"Text normalization failed: {str(e)}")
            return text if isinstance(text, str) else ""
    
    def extract_features(self, text: str) -> Dict[str, Any]:
        """Extract basic features from text"""
        try:
            if not text:
                return {}
            
            # Clean text
            cleaned_text = self.clean_text(text)
            tokens = self.tokenize(cleaned_text)
            
            # Calculate features
            features = {
                'char_count': len(text),
                'word_count': len(tokens),
                'sentence_count': len(re.split(r'[.!?]+', text)),
                'avg_word_length': sum(len(word) for word in tokens) / len(tokens) if tokens else 0,
                'unique_words': len(set(tokens)),
                'lexical_diversity': len(set(tokens)) / len(tokens) if tokens else 0,
                'uppercase_ratio': sum(1 for c in text if c.isupper()) / len(text) if text else 0,
                'punctuation_count': len(re.findall(r'[^\w\s]', text)),
                'digit_count': len(re.findall(r'\d', text))
            }
            
            return features
            
        except Exception as e:
            logger.error(f"Feature extraction failed: {str(e)}")
            return {}
    
    def prepare_for_model(self, texts: List[str], max_length: int = 512) -> List[str]:
        """Prepare texts for model input"""
        try:
            processed_texts = []
            
            for text in texts:
                # Clean text
                cleaned = self.clean_text(text)
                
                # Truncate if too long
                if len(cleaned) > max_length:
                    cleaned = cleaned[:max_length]
                
                processed_texts.append(cleaned)
            
            return processed_texts
            
        except Exception as e:
            logger.error(f"Model preparation failed: {str(e)}")
            return texts
    
    def detect_language(self, text: str) -> str:
        """Simple language detection (basic implementation)"""
        try:
            if not text:
                return 'unknown'
            
            # Very basic language detection based on common words
            english_indicators = ['the', 'and', 'is', 'in', 'to', 'of', 'a', 'that', 'it', 'with']
            spanish_indicators = ['el', 'la', 'de', 'que', 'y', 'en', 'un', 'es', 'se', 'no']
            french_indicators = ['le', 'de', 'et', 'à', 'un', 'il', 'être', 'et', 'en', 'avoir']
            
            text_lower = text.lower()
            
            english_count = sum(1 for word in english_indicators if word in text_lower)
            spanish_count = sum(1 for word in spanish_indicators if word in text_lower)
            french_count = sum(1 for word in french_indicators if word in text_lower)
            
            if english_count >= spanish_count and english_count >= french_count:
                return 'english'
            elif spanish_count >= french_count:
                return 'spanish'
            elif french_count > 0:
                return 'french'
            else:
                return 'english'  # Default to English
                
        except Exception as e:
            logger.error(f"Language detection failed: {str(e)}")
            return 'english'