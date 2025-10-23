import logging
import numpy as np
from PIL import Image
import requests
from io import BytesIO

logger = logging.getLogger(__name__)

class ImageModel:
    def __init__(self):
        self.model_loaded = False
        self.supported_formats = ['JPEG', 'PNG', 'GIF', 'BMP', 'WEBP']
    
    def load_image_from_url(self, image_url: str) -> Image.Image:
        """Load image from URL"""
        try:
            response = requests.get(image_url, timeout=10)
            response.raise_for_status()
            
            image = Image.open(BytesIO(response.content))
            
            # Convert to RGB if necessary
            if image.mode != 'RGB':
                image = image.convert('RGB')
            
            logger.info(f"Image loaded from URL: {image_url}")
            return image
            
        except Exception as e:
            logger.error(f"Failed to load image from URL {image_url}: {str(e)}")
            raise
    
    def load_image_from_path(self, image_path: str) -> Image.Image:
        """Load image from local path"""
        try:
            image = Image.open(image_path)
            
            # Convert to RGB if necessary
            if image.mode != 'RGB':
                image = image.convert('RGB')
            
            logger.info(f"Image loaded from path: {image_path}")
            return image
            
        except Exception as e:
            logger.error(f"Failed to load image from path {image_path}: {str(e)}")
            raise
    
    def analyze_image(self, image: Image.Image) -> dict:
        """Analyze image and extract basic information"""
        try:
            analysis = {
                'dimensions': {
                    'width': image.width,
                    'height': image.height
                },
                'format': image.format or 'Unknown',
                'mode': image.mode,
                'size_bytes': len(image.tobytes()),
                'aspect_ratio': round(image.width / image.height, 2),
                'is_grayscale': image.mode in ['L', 'LA'],
                'has_transparency': image.mode in ['RGBA', 'LA'] or 'transparency' in image.info
            }
            
            # Calculate basic statistics
            img_array = np.array(image)
            if len(img_array.shape) == 3:  # Color image
                analysis['color_stats'] = {
                    'mean_rgb': [float(np.mean(img_array[:, :, i])) for i in range(3)],
                    'std_rgb': [float(np.std(img_array[:, :, i])) for i in range(3)]
                }
            else:  # Grayscale
                analysis['brightness'] = {
                    'mean': float(np.mean(img_array)),
                    'std': float(np.std(img_array))
                }
            
            return analysis
            
        except Exception as e:
            logger.error(f"Image analysis failed: {str(e)}")
            raise
    
    def classify_image(self, image: Image.Image) -> dict:
        """Classify image content (basic implementation)"""
        try:
            # This is a simplified classification
            # In a real implementation, you would use a pre-trained model
            
            analysis = self.analyze_image(image)
            
            # Simple heuristic-based classification
            classification = {
                'predicted_class': 'general',
                'confidence': 0.5,
                'categories': []
            }
            
            # Analyze dimensions to guess content type
            width, height = analysis['dimensions']['width'], analysis['dimensions']['height']
            aspect_ratio = analysis['aspect_ratio']
            
            if aspect_ratio > 1.5:
                classification['categories'].append('landscape')
            elif aspect_ratio < 0.7:
                classification['categories'].append('portrait')
            else:
                classification['categories'].append('square')
            
            if width > 1920 or height > 1080:
                classification['categories'].append('high_resolution')
            elif width < 300 or height < 300:
                classification['categories'].append('low_resolution')
            else:
                classification['categories'].append('medium_resolution')
            
            # Analyze color information
            if analysis.get('is_grayscale'):
                classification['categories'].append('grayscale')
            else:
                classification['categories'].append('color')
            
            if analysis.get('has_transparency'):
                classification['categories'].append('transparent')
            
            return classification
            
        except Exception as e:
            logger.error(f"Image classification failed: {str(e)}")
            raise
    
    def detect_objects(self, image: Image.Image) -> dict:
        """Detect objects in image (placeholder implementation)"""
        try:
            # This is a placeholder implementation
            # In a real scenario, you would use models like YOLO, R-CNN, etc.
            
            objects = {
                'detected_objects': [],
                'object_count': 0,
                'confidence_threshold': 0.5
            }
            
            # Placeholder detection based on image properties
            analysis = self.analyze_image(image)
            
            # Simple heuristic detection
            if analysis['dimensions']['width'] > analysis['dimensions']['height']:
                objects['detected_objects'].append({
                    'class': 'landscape_scene',
                    'confidence': 0.6,
                    'bbox': [0, 0, analysis['dimensions']['width'], analysis['dimensions']['height']]
                })
            
            objects['object_count'] = len(objects['detected_objects'])
            
            return objects
            
        except Exception as e:
            logger.error(f"Object detection failed: {str(e)}")
            raise
    
    def extract_features(self, image: Image.Image) -> dict:
        """Extract visual features from image"""
        try:
            # Convert image to numpy array
            img_array = np.array(image)
            
            features = {
                'histogram': {},
                'texture_features': {},
                'color_features': {}
            }
            
            if len(img_array.shape) == 3:  # Color image
                # Color histogram
                for i, color in enumerate(['red', 'green', 'blue']):
                    hist, _ = np.histogram(img_array[:, :, i], bins=32, range=(0, 256))
                    features['histogram'][color] = hist.tolist()
                
                # Color moments
                features['color_features'] = {
                    'mean_rgb': [float(np.mean(img_array[:, :, i])) for i in range(3)],
                    'std_rgb': [float(np.std(img_array[:, :, i])) for i in range(3)],
                    'skew_rgb': [float(self._calculate_skewness(img_array[:, :, i])) for i in range(3)]
                }
            else:  # Grayscale
                hist, _ = np.histogram(img_array, bins=32, range=(0, 256))
                features['histogram']['grayscale'] = hist.tolist()
                
                features['color_features'] = {
                    'mean': float(np.mean(img_array)),
                    'std': float(np.std(img_array)),
                    'skew': float(self._calculate_skewness(img_array))
                }
            
            # Basic texture features
            features['texture_features'] = self._calculate_texture_features(img_array)
            
            return features
            
        except Exception as e:
            logger.error(f"Feature extraction failed: {str(e)}")
            raise
    
    def _calculate_skewness(self, data: np.ndarray) -> float:
        """Calculate skewness of data"""
        try:
            mean = np.mean(data)
            std = np.std(data)
            if std == 0:
                return 0.0
            return float(np.mean(((data - mean) / std) ** 3))
        except:
            return 0.0
    
    def _calculate_texture_features(self, img_array: np.ndarray) -> dict:
        """Calculate basic texture features"""
        try:
            # Convert to grayscale if color
            if len(img_array.shape) == 3:
                gray = np.mean(img_array, axis=2)
            else:
                gray = img_array
            
            # Calculate gradients
            grad_x = np.gradient(gray, axis=1)
            grad_y = np.gradient(gray, axis=0)
            
            # Texture measures
            texture_features = {
                'contrast': float(np.std(gray)),
                'homogeneity': float(1.0 / (1.0 + np.var(gray))),
                'energy': float(np.sum(gray ** 2) / gray.size),
                'gradient_magnitude': float(np.mean(np.sqrt(grad_x**2 + grad_y**2)))
            }
            
            return texture_features
            
        except Exception as e:
            logger.error(f"Texture feature calculation failed: {str(e)}")
            return {}
    
    def resize_image(self, image: Image.Image, target_size: tuple) -> Image.Image:
        """Resize image to target size"""
        try:
            resized_image = image.resize(target_size, Image.Resampling.LANCZOS)
            logger.info(f"Image resized to {target_size}")
            return resized_image
        except Exception as e:
            logger.error(f"Image resizing failed: {str(e)}")
            raise
    
    def validate_image(self, image_data: bytes) -> bool:
        """Validate if data is a valid image"""
        try:
            image = Image.open(BytesIO(image_data))
            return image.format in self.supported_formats
        except:
            return False