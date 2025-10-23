import logging
from services.huggingface_service import HuggingFaceService
from services.preprocessing import PreprocessingService
from services.postprocessing import PostprocessingService

logger = logging.getLogger(__name__)

class AnalysisController:
    def __init__(self):
        self.hf_service = HuggingFaceService()
        self.preprocessing = PreprocessingService()
        self.postprocessing = PostprocessingService()
    
    def analyze_text(self, text):
        """Perform comprehensive text analysis"""
        try:
            # Preprocess text
            processed_text = self.preprocessing.clean_text(text)
            
            # Perform various analyses
            results = {
                'original_text': text,
                'processed_text': processed_text,
                'word_count': len(processed_text.split()),
                'character_count': len(processed_text),
                'sentiment': self.analyze_sentiment(text),
                'entities': self.extract_entities(processed_text),
                'keywords': self.extract_keywords(processed_text),
                'readability_score': self.calculate_readability(processed_text)
            }
            
            return results
            
        except Exception as e:
            logger.error(f"Text analysis failed: {str(e)}")
            raise
    
    def analyze_sentiment(self, text):
        """Analyze sentiment of text"""
        try:
            result = self.hf_service.analyze_sentiment(text)
            
            # Post-process results
            processed_result = self.postprocessing.format_sentiment_result(result)
            
            return processed_result
            
        except Exception as e:
            logger.error(f"Sentiment analysis failed: {str(e)}")
            raise
    
    def extract_entities(self, text):
        """Extract named entities from text"""
        try:
            entities = self.hf_service.extract_entities(text)
            
            # Group entities by type
            grouped_entities = {}
            for entity in entities:
                entity_type = entity.get('entity_group', 'MISC')
                if entity_type not in grouped_entities:
                    grouped_entities[entity_type] = []
                grouped_entities[entity_type].append({
                    'text': entity.get('word', ''),
                    'confidence': entity.get('score', 0.0)
                })
            
            return grouped_entities
            
        except Exception as e:
            logger.error(f"Entity extraction failed: {str(e)}")
            return {}
    
    def extract_keywords(self, text):
        """Extract keywords from text"""
        try:
            # Simple keyword extraction using word frequency
            words = text.lower().split()
            word_freq = {}
            
            # Filter out common stop words
            stop_words = {'the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for', 'of', 'with', 'by', 'is', 'are', 'was', 'were', 'be', 'been', 'being', 'have', 'has', 'had', 'do', 'does', 'did', 'will', 'would', 'could', 'should'}
            
            for word in words:
                if word not in stop_words and len(word) > 2:
                    word_freq[word] = word_freq.get(word, 0) + 1
            
            # Sort by frequency and return top keywords
            keywords = sorted(word_freq.items(), key=lambda x: x[1], reverse=True)[:10]
            
            return [{'word': word, 'frequency': freq} for word, freq in keywords]
            
        except Exception as e:
            logger.error(f"Keyword extraction failed: {str(e)}")
            return []
    
    def calculate_readability(self, text):
        """Calculate readability score"""
        try:
            sentences = text.split('.')
            words = text.split()
            
            if len(sentences) == 0 or len(words) == 0:
                return 0
            
            # Simple readability calculation (Flesch Reading Ease approximation)
            avg_sentence_length = len(words) / len(sentences)
            avg_syllables_per_word = sum(self._count_syllables(word) for word in words) / len(words)
            
            readability_score = 206.835 - (1.015 * avg_sentence_length) - (84.6 * avg_syllables_per_word)
            
            return max(0, min(100, readability_score))
            
        except Exception as e:
            logger.error(f"Readability calculation failed: {str(e)}")
            return 0
    
    def _count_syllables(self, word):
        """Count syllables in a word (simple approximation)"""
        word = word.lower()
        vowels = 'aeiouy'
        syllable_count = 0
        prev_was_vowel = False
        
        for char in word:
            is_vowel = char in vowels
            if is_vowel and not prev_was_vowel:
                syllable_count += 1
            prev_was_vowel = is_vowel
        
        # Handle silent 'e'
        if word.endswith('e'):
            syllable_count -= 1
        
        return max(1, syllable_count)