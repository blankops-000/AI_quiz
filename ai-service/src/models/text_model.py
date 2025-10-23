import logging
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, classification_report
import pickle
import os

logger = logging.getLogger(__name__)

class TextModel:
    def __init__(self):
        self.vectorizer = TfidfVectorizer(max_features=5000, stop_words='english')
        self.classifier = None
        self.sentiment_analyzer = None
        self.model_path = "models/"
        
        # Create models directory if it doesn't exist
        os.makedirs(self.model_path, exist_ok=True)
    
    def train_classifier(self, texts, labels, parameters=None):
        """Train text classification model"""
        try:
            if parameters is None:
                parameters = {}
            
            # Vectorize texts
            X = self.vectorizer.fit_transform(texts)
            y = np.array(labels)
            
            # Split data
            X_train, X_test, y_train, y_test = train_test_split(
                X, y, test_size=0.2, random_state=42, stratify=y
            )
            
            # Choose classifier based on parameters
            classifier_type = parameters.get('classifier', 'naive_bayes')
            
            if classifier_type == 'logistic_regression':
                self.classifier = LogisticRegression(
                    max_iter=parameters.get('max_iter', 1000),
                    random_state=42
                )
            else:
                self.classifier = MultinomialNB(
                    alpha=parameters.get('alpha', 1.0)
                )
            
            # Train the model
            self.classifier.fit(X_train, y_train)
            
            # Evaluate
            y_pred = self.classifier.predict(X_test)
            accuracy = accuracy_score(y_test, y_pred)
            
            # Save model
            model_filename = f"{self.model_path}text_classifier.pkl"
            with open(model_filename, 'wb') as f:
                pickle.dump({
                    'vectorizer': self.vectorizer,
                    'classifier': self.classifier
                }, f)
            
            logger.info(f"Text classifier trained with accuracy: {accuracy:.3f}")
            
            return {
                'accuracy': accuracy,
                'model_path': model_filename,
                'feature_count': X.shape[1],
                'training_samples': len(texts)
            }
            
        except Exception as e:
            logger.error(f"Text classifier training failed: {str(e)}")
            raise
    
    def train_sentiment_analyzer(self, texts, sentiments, parameters=None):
        """Train sentiment analysis model"""
        try:
            if parameters is None:
                parameters = {}
            
            # Create separate vectorizer for sentiment
            sentiment_vectorizer = TfidfVectorizer(
                max_features=parameters.get('max_features', 3000),
                stop_words='english',
                ngram_range=(1, 2)  # Include bigrams for better sentiment detection
            )
            
            # Vectorize texts
            X = sentiment_vectorizer.fit_transform(texts)
            y = np.array(sentiments)
            
            # Split data
            X_train, X_test, y_train, y_test = train_test_split(
                X, y, test_size=0.2, random_state=42, stratify=y
            )
            
            # Use Logistic Regression for sentiment analysis
            self.sentiment_analyzer = LogisticRegression(
                max_iter=parameters.get('max_iter', 1000),
                random_state=42
            )
            
            # Train the model
            self.sentiment_analyzer.fit(X_train, y_train)
            
            # Evaluate
            y_pred = self.sentiment_analyzer.predict(X_test)
            accuracy = accuracy_score(y_test, y_pred)
            
            # Save model
            model_filename = f"{self.model_path}sentiment_analyzer.pkl"
            with open(model_filename, 'wb') as f:
                pickle.dump({
                    'vectorizer': sentiment_vectorizer,
                    'analyzer': self.sentiment_analyzer
                }, f)
            
            logger.info(f"Sentiment analyzer trained with accuracy: {accuracy:.3f}")
            
            return {
                'accuracy': accuracy,
                'model_path': model_filename,
                'feature_count': X.shape[1],
                'training_samples': len(texts)
            }
            
        except Exception as e:
            logger.error(f"Sentiment analyzer training failed: {str(e)}")
            raise
    
    def predict_text_class(self, text):
        """Predict class of text"""
        try:
            if not self.classifier:
                raise Exception("Text classifier not trained")
            
            # Vectorize text
            X = self.vectorizer.transform([text])
            
            # Predict
            prediction = self.classifier.predict(X)[0]
            probabilities = self.classifier.predict_proba(X)[0]
            
            # Get class names
            classes = self.classifier.classes_
            
            # Create probability dictionary
            prob_dict = dict(zip(classes, probabilities))
            
            return {
                'predicted_class': prediction,
                'confidence': max(probabilities),
                'probabilities': prob_dict
            }
            
        except Exception as e:
            logger.error(f"Text classification prediction failed: {str(e)}")
            raise
    
    def predict_sentiment(self, text):
        """Predict sentiment of text"""
        try:
            if not self.sentiment_analyzer:
                raise Exception("Sentiment analyzer not trained")
            
            # Load model if not in memory
            model_filename = f"{self.model_path}sentiment_analyzer.pkl"
            if os.path.exists(model_filename):
                with open(model_filename, 'rb') as f:
                    model_data = pickle.load(f)
                    vectorizer = model_data['vectorizer']
                    analyzer = model_data['analyzer']
            else:
                raise Exception("Sentiment model not found")
            
            # Vectorize text
            X = vectorizer.transform([text])
            
            # Predict
            prediction = analyzer.predict(X)[0]
            probabilities = analyzer.predict_proba(X)[0]
            
            # Get class names
            classes = analyzer.classes_
            
            # Create probability dictionary
            prob_dict = dict(zip(classes, probabilities))
            
            return {
                'predicted_sentiment': prediction,
                'confidence': max(probabilities),
                'probabilities': prob_dict
            }
            
        except Exception as e:
            logger.error(f"Sentiment prediction failed: {str(e)}")
            raise
    
    def load_model(self, model_path):
        """Load trained model"""
        try:
            with open(model_path, 'rb') as f:
                model_data = pickle.load(f)
                self.vectorizer = model_data['vectorizer']
                self.classifier = model_data['classifier']
            
            logger.info(f"Model loaded from {model_path}")
            
        except Exception as e:
            logger.error(f"Model loading failed: {str(e)}")
            raise
    
    def get_feature_importance(self, top_n=20):
        """Get most important features"""
        try:
            if not self.classifier or not hasattr(self.classifier, 'coef_'):
                raise Exception("Classifier not available or doesn't support feature importance")
            
            # Get feature names
            feature_names = self.vectorizer.get_feature_names_out()
            
            # Get coefficients (for binary classification)
            if len(self.classifier.classes_) == 2:
                coefficients = self.classifier.coef_[0]
            else:
                # For multiclass, use the mean of absolute coefficients
                coefficients = np.mean(np.abs(self.classifier.coef_), axis=0)
            
            # Get top features
            top_indices = np.argsort(np.abs(coefficients))[-top_n:][::-1]
            
            top_features = [
                {
                    'feature': feature_names[i],
                    'importance': float(coefficients[i])
                }
                for i in top_indices
            ]
            
            return top_features
            
        except Exception as e:
            logger.error(f"Feature importance extraction failed: {str(e)}")
            return []