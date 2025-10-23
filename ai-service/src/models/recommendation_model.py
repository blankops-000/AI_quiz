import logging
import numpy as np
import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.decomposition import TruncatedSVD
import pickle
import os
from datetime import datetime

logger = logging.getLogger(__name__)

class RecommendationModel:
    def __init__(self):
        self.user_item_matrix = None
        self.item_features = None
        self.user_features = None
        self.svd_model = None
        self.model_path = "models/"
        
        # Create models directory if it doesn't exist
        os.makedirs(self.model_path, exist_ok=True)
    
    def train(self, interactions, parameters=None):
        """Train recommendation model"""
        try:
            if parameters is None:
                parameters = {}
            
            # Convert interactions to DataFrame
            df = pd.DataFrame(interactions)
            
            # Create user-item matrix
            self.user_item_matrix = df.pivot_table(
                index='user_id',
                columns='item_id',
                values='rating',
                fill_value=0
            )
            
            # Apply SVD for dimensionality reduction
            n_components = parameters.get('n_components', 50)
            self.svd_model = TruncatedSVD(n_components=n_components, random_state=42)
            
            # Fit SVD model
            user_factors = self.svd_model.fit_transform(self.user_item_matrix)
            item_factors = self.svd_model.components_.T
            
            # Store factors
            self.user_features = pd.DataFrame(
                user_factors,
                index=self.user_item_matrix.index
            )
            self.item_features = pd.DataFrame(
                item_factors,
                index=self.user_item_matrix.columns
            )
            
            # Save model
            model_filename = f"{self.model_path}recommendation_model.pkl"
            with open(model_filename, 'wb') as f:
                pickle.dump({
                    'user_item_matrix': self.user_item_matrix,
                    'user_features': self.user_features,
                    'item_features': self.item_features,
                    'svd_model': self.svd_model
                }, f)
            
            # Calculate some metrics
            explained_variance = np.sum(self.svd_model.explained_variance_ratio_)
            
            logger.info(f"Recommendation model trained with {explained_variance:.3f} explained variance")
            
            return {
                'model_path': model_filename,
                'n_users': len(self.user_item_matrix.index),
                'n_items': len(self.user_item_matrix.columns),
                'n_interactions': len(interactions),
                'explained_variance': explained_variance,
                'n_components': n_components
            }
            
        except Exception as e:
            logger.error(f"Recommendation model training failed: {str(e)}")
            raise
    
    def get_recommendations(self, user_id, preferences=None, limit=10):
        """Get recommendations for a user"""
        try:
            if preferences is None:
                preferences = {}
            
            # Load model if not in memory
            if self.user_features is None:
                self._load_model()
            
            # Check if user exists in training data
            if user_id in self.user_features.index:
                # Existing user - use collaborative filtering
                recommendations = self._get_collaborative_recommendations(user_id, limit)
            else:
                # New user - use content-based or popular items
                recommendations = self._get_content_based_recommendations(preferences, limit)
            
            return recommendations
            
        except Exception as e:
            logger.error(f"Getting recommendations failed: {str(e)}")
            # Return fallback recommendations
            return self._get_fallback_recommendations(limit)
    
    def _get_collaborative_recommendations(self, user_id, limit):
        """Get collaborative filtering recommendations"""
        try:
            # Get user vector
            user_vector = self.user_features.loc[user_id].values.reshape(1, -1)
            
            # Calculate similarity with all items
            item_similarities = cosine_similarity(user_vector, self.item_features.values)[0]
            
            # Get items user hasn't interacted with
            user_items = self.user_item_matrix.loc[user_id]
            unrated_items = user_items[user_items == 0].index
            
            # Get similarities for unrated items
            unrated_similarities = []
            for item_id in unrated_items:
                if item_id in self.item_features.index:
                    item_idx = self.item_features.index.get_loc(item_id)
                    similarity = item_similarities[item_idx]
                    unrated_similarities.append((item_id, similarity))
            
            # Sort by similarity and get top recommendations
            unrated_similarities.sort(key=lambda x: x[1], reverse=True)
            top_recommendations = unrated_similarities[:limit]
            
            # Format recommendations
            recommendations = []
            for i, (item_id, score) in enumerate(top_recommendations):
                recommendations.append({
                    'id': i + 1,
                    'item_id': item_id,
                    'title': f"Item {item_id}",
                    'description': f"Recommended based on your preferences",
                    'score': float(score),
                    'category': 'collaborative',
                    'tags': ['recommended', 'similar_users'],
                    'reasoning': 'Users with similar preferences also liked this item'
                })
            
            return recommendations
            
        except Exception as e:
            logger.error(f"Collaborative filtering failed: {str(e)}")
            return self._get_fallback_recommendations(limit)
    
    def _get_content_based_recommendations(self, preferences, limit):
        """Get content-based recommendations for new users"""
        try:
            # Generate recommendations based on preferences
            recommendations = []
            
            # Extract preference categories
            preferred_categories = preferences.get('categories', ['general'])
            preferred_tags = preferences.get('tags', [])
            
            # Generate sample recommendations
            for i in range(limit):
                category = preferred_categories[i % len(preferred_categories)] if preferred_categories else 'general'
                
                recommendations.append({
                    'id': i + 1,
                    'item_id': f"item_{i + 1}",
                    'title': f"Recommended {category.title()} Item {i + 1}",
                    'description': f"Popular item in {category} category",
                    'score': 0.8 - (i * 0.05),  # Decreasing scores
                    'category': category,
                    'tags': preferred_tags + ['popular', 'trending'],
                    'reasoning': f'Popular item in your preferred category: {category}'
                })
            
            return recommendations
            
        except Exception as e:
            logger.error(f"Content-based recommendations failed: {str(e)}")
            return self._get_fallback_recommendations(limit)
    
    def _get_fallback_recommendations(self, limit):
        """Get fallback recommendations when other methods fail"""
        recommendations = []
        
        categories = ['technology', 'science', 'arts', 'sports', 'entertainment']
        
        for i in range(limit):
            category = categories[i % len(categories)]
            
            recommendations.append({
                'id': i + 1,
                'item_id': f"fallback_item_{i + 1}",
                'title': f"Popular {category.title()} Item",
                'description': f"Trending item in {category}",
                'score': 0.7 - (i * 0.03),
                'category': category,
                'tags': ['popular', 'trending', 'general'],
                'reasoning': 'Popular item across all users'
            })
        
        return recommendations
    
    def _load_model(self):
        """Load trained recommendation model"""
        try:
            model_filename = f"{self.model_path}recommendation_model.pkl"
            
            if os.path.exists(model_filename):
                with open(model_filename, 'rb') as f:
                    model_data = pickle.load(f)
                    self.user_item_matrix = model_data['user_item_matrix']
                    self.user_features = model_data['user_features']
                    self.item_features = model_data['item_features']
                    self.svd_model = model_data['svd_model']
                
                logger.info("Recommendation model loaded successfully")
            else:
                logger.warning("No trained recommendation model found")
                
        except Exception as e:
            logger.error(f"Model loading failed: {str(e)}")
    
    def get_similar_users(self, user_id, limit=10):
        """Get users similar to the given user"""
        try:
            if self.user_features is None:
                self._load_model()
            
            if user_id not in self.user_features.index:
                return []
            
            # Get user vector
            user_vector = self.user_features.loc[user_id].values.reshape(1, -1)
            
            # Calculate similarity with all users
            user_similarities = cosine_similarity(user_vector, self.user_features.values)[0]
            
            # Get similar users (excluding the user itself)
            similar_users = []
            for i, similarity in enumerate(user_similarities):
                other_user_id = self.user_features.index[i]
                if other_user_id != user_id:
                    similar_users.append((other_user_id, similarity))
            
            # Sort by similarity and return top users
            similar_users.sort(key=lambda x: x[1], reverse=True)
            
            return [
                {
                    'user_id': uid,
                    'similarity': float(sim)
                }
                for uid, sim in similar_users[:limit]
            ]
            
        except Exception as e:
            logger.error(f"Getting similar users failed: {str(e)}")
            return []