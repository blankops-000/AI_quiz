import os
import logging
from transformers import pipeline, AutoTokenizer, AutoModelForSequenceClassification
import torch

logger = logging.getLogger(__name__)

class HuggingFaceService:
    def __init__(self):
        self.sentiment_pipeline = None
        self.text_generation_pipeline = None
        self.ner_pipeline = None
        self._initialize_models()
    
    def _initialize_models(self):
        """Initialize HuggingFace models"""
        try:
            # Initialize sentiment analysis pipeline
            self.sentiment_pipeline = pipeline(
                "sentiment-analysis",
                model="cardiffnlp/twitter-roberta-base-sentiment-latest",
                return_all_scores=True
            )
            
            # Initialize text generation pipeline
            self.text_generation_pipeline = pipeline(
                "text-generation",
                model="gpt2",
                tokenizer="gpt2"
            )
            
            # Initialize NER pipeline
            self.ner_pipeline = pipeline(
                "ner",
                model="dbmdz/bert-large-cased-finetuned-conll03-english",
                aggregation_strategy="simple"
            )
            
            logger.info("HuggingFace models initialized successfully")
            
        except Exception as e:
            logger.error(f"Failed to initialize HuggingFace models: {str(e)}")
            # Initialize fallback models
            self._initialize_fallback_models()
    
    def _initialize_fallback_models(self):
        """Initialize simpler fallback models"""
        try:
            self.sentiment_pipeline = pipeline("sentiment-analysis")
            self.text_generation_pipeline = pipeline("text-generation", model="gpt2")
            self.ner_pipeline = pipeline("ner", aggregation_strategy="simple")
            logger.info("Fallback models initialized")
        except Exception as e:
            logger.error(f"Failed to initialize fallback models: {str(e)}")
    
    def analyze_sentiment(self, text):
        """Analyze sentiment of text"""
        try:
            if not self.sentiment_pipeline:
                raise Exception("Sentiment pipeline not initialized")
            
            results = self.sentiment_pipeline(text)
            
            # Process results
            if isinstance(results[0], list):
                # Multiple scores returned
                sentiment_scores = {}
                for result in results[0]:
                    label = result['label'].lower()
                    if 'positive' in label or label == 'pos':
                        sentiment_scores['positive'] = result['score']
                    elif 'negative' in label or label == 'neg':
                        sentiment_scores['negative'] = result['score']
                    elif 'neutral' in label:
                        sentiment_scores['neutral'] = result['score']
                
                # Determine overall sentiment
                max_sentiment = max(sentiment_scores.items(), key=lambda x: x[1])
                overall_sentiment = max_sentiment[0]
                confidence = max_sentiment[1]
            else:
                # Single result
                overall_sentiment = results[0]['label'].lower()
                confidence = results[0]['score']
                sentiment_scores = {overall_sentiment: confidence}
            
            return {
                'overall_sentiment': overall_sentiment,
                'confidence': confidence,
                'scores': sentiment_scores
            }
            
        except Exception as e:
            logger.error(f"Sentiment analysis failed: {str(e)}")
            # Return neutral sentiment as fallback
            return {
                'overall_sentiment': 'neutral',
                'confidence': 0.5,
                'scores': {'neutral': 0.5}
            }
    
    def generate_text(self, prompt, max_length=100, temperature=0.7):
        """Generate text based on prompt"""
        try:
            if not self.text_generation_pipeline:
                raise Exception("Text generation pipeline not initialized")
            
            # Generate text
            results = self.text_generation_pipeline(
                prompt,
                max_length=max_length,
                temperature=temperature,
                num_return_sequences=1,
                pad_token_id=50256  # GPT-2 pad token
            )
            
            generated_text = results[0]['generated_text']
            
            # Remove the original prompt from the generated text
            if generated_text.startswith(prompt):
                generated_text = generated_text[len(prompt):].strip()
            
            return generated_text
            
        except Exception as e:
            logger.error(f"Text generation failed: {str(e)}")
            # Return a simple fallback response
            return f"This is a generated response based on: {prompt}"
    
    def extract_entities(self, text):
        """Extract named entities from text"""
        try:
            if not self.ner_pipeline:
                raise Exception("NER pipeline not initialized")
            
            entities = self.ner_pipeline(text)
            
            # Process and clean entities
            processed_entities = []
            for entity in entities:
                processed_entities.append({
                    'word': entity.get('word', ''),
                    'entity_group': entity.get('entity_group', 'MISC'),
                    'score': entity.get('score', 0.0),
                    'start': entity.get('start', 0),
                    'end': entity.get('end', 0)
                })
            
            return processed_entities
            
        except Exception as e:
            logger.error(f"Entity extraction failed: {str(e)}")
            return []
    
    def classify_text(self, text, labels):
        """Classify text into given labels"""
        try:
            # Use zero-shot classification
            classifier = pipeline("zero-shot-classification")
            result = classifier(text, labels)
            
            return {
                'predicted_label': result['labels'][0],
                'scores': dict(zip(result['labels'], result['scores']))
            }
            
        except Exception as e:
            logger.error(f"Text classification failed: {str(e)}")
            # Return first label as fallback
            return {
                'predicted_label': labels[0] if labels else 'unknown',
                'scores': {label: 1.0/len(labels) for label in labels} if labels else {}
            }