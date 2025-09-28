"""
Wisconsin Breast Cancer Dataset Optimized Ensemble Model
Advanced ensemble methods specifically tuned for Wisconsin dataset characteristics
"""

import numpy as np
import pandas as pd
from typing import Dict, List, Tuple, Optional, Any
from sklearn.ensemble import (
    RandomForestClassifier, 
    GradientBoostingClassifier, 
    VotingClassifier,
    AdaBoostClassifier,
    ExtraTreesClassifier
)
from sklearn.svm import SVC
from sklearn.neural_network import MLPClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import RobustScaler
from sklearn.model_selection import (
    train_test_split, 
    cross_val_score, 
    GridSearchCV,
    StratifiedKFold
)
from sklearn.metrics import (
    accuracy_score, 
    classification_report, 
    confusion_matrix,
    roc_auc_score,
    precision_recall_curve,
    roc_curve
)
import joblib
import os
from datetime import datetime
import warnings
warnings.filterwarnings('ignore')

class WisconsinOptimizedEnsemble:
    """Wisconsin dataset-optimized ensemble model"""
    
    def __init__(self):
        self.models = {}
        self.trained_models = {}
        self.scaler = RobustScaler()  # Better for Wisconsin dataset outliers
        self.feature_names = None
        self.ensemble_weights = {}
        self.model_performance = {}
        
        # Initialize models with Wisconsin-optimized parameters
        self._initialize_models()
        
    def _initialize_models(self):
        """Initialize models with parameters optimized for Wisconsin dataset"""
        
        self.models = {
            'random_forest': RandomForestClassifier(
                n_estimators=200,
                max_depth=12,
                min_samples_split=3,
                min_samples_leaf=1,
                max_features='sqrt',
                bootstrap=True,
                random_state=42,
                n_jobs=-1
            ),
            
            'gradient_boosting': GradientBoostingClassifier(
                n_estimators=200,
                learning_rate=0.1,
                max_depth=6,
                min_samples_split=3,
                min_samples_leaf=1,
                subsample=0.8,
                random_state=42
            ),
            
            'extra_trees': ExtraTreesClassifier(
                n_estimators=200,
                max_depth=15,
                min_samples_split=2,
                min_samples_leaf=1,
                max_features='sqrt',
                bootstrap=True,
                random_state=42,
                n_jobs=-1
            ),
            
            'svm_rbf': SVC(
                kernel='rbf',
                C=1.0,
                gamma='scale',
                probability=True,
                random_state=42
            ),
            
            'svm_linear': SVC(
                kernel='linear',
                C=0.1,
                probability=True,
                random_state=42
            ),
            
            'neural_network': MLPClassifier(
                hidden_layer_sizes=(100, 50, 25),
                activation='relu',
                solver='adam',
                alpha=0.001,
                learning_rate='adaptive',
                max_iter=1000,
                early_stopping=True,
                validation_fraction=0.1,
                random_state=42
            ),
            
            'logistic_regression': LogisticRegression(
                C=1.0,
                max_iter=1000,
                random_state=42,
                solver='liblinear'
            ),
            
            'ada_boost': AdaBoostClassifier(
                n_estimators=100,
                learning_rate=1.0,
                algorithm='SAMME',
                random_state=42
            )
        }
    
    def train_ensemble(self, X: np.ndarray, y: np.ndarray, 
                      feature_names: List[str] = None) -> Dict[str, Any]:
        """Train all models in the ensemble"""
        
        self.feature_names = feature_names
        
        print("Training Wisconsin-optimized ensemble models...")
        print(f"Training data shape: {X.shape}")
        print(f"Class distribution: {np.bincount(y)}")
        
        # Scale features
        X_scaled = self.scaler.fit_transform(X)
        
        # Train each model
        for name, model in self.models.items():
            print(f"Training {name}...")
            
            try:
                # Train the model
                model.fit(X_scaled, y)
                self.trained_models[name] = model
                
                # Evaluate with cross-validation
                cv_scores = cross_val_score(
                    model, X_scaled, y, 
                    cv=StratifiedKFold(n_splits=5, shuffle=True, random_state=42),
                    scoring='accuracy'
                )
                
                self.model_performance[name] = {
                    'mean_accuracy': cv_scores.mean(),
                    'std_accuracy': cv_scores.std(),
                    'cv_scores': cv_scores.tolist()
                }
                
                print(f"{name} - CV Accuracy: {cv_scores.mean():.4f} (+/- {cv_scores.std() * 2:.4f})")
                
            except Exception as e:
                print(f"Error training {name}: {e}")
                continue
        
        # Calculate ensemble weights based on performance
        self._calculate_ensemble_weights()
        
        return {
            'trained_models': len(self.trained_models),
            'model_performance': self.model_performance,
            'ensemble_weights': self.ensemble_weights
        }
    
    def _calculate_ensemble_weights(self):
        """Calculate weights for ensemble based on individual model performance"""
        if not self.model_performance:
            return
        
        # Use accuracy as weight (normalized)
        accuracies = [perf['mean_accuracy'] for perf in self.model_performance.values()]
        total_accuracy = sum(accuracies)
        
        for i, (name, perf) in enumerate(self.model_performance.items()):
            self.ensemble_weights[name] = accuracies[i] / total_accuracy
        
        print("Ensemble weights calculated:")
        for name, weight in self.ensemble_weights.items():
            print(f"  {name}: {weight:.4f}")
    
    def predict_ensemble(self, X: np.ndarray, return_individual: bool = False) -> Dict[str, Any]:
        """Make ensemble predictions with confidence weighting"""
        
        if not self.trained_models:
            raise ValueError("No trained models available. Train the ensemble first.")
        
        # Scale features
        X_scaled = self.scaler.transform(X)
        
        predictions = {}
        confidences = {}
        probabilities = {}
        
        # Get predictions from each model
        for name, model in self.trained_models.items():
            try:
                pred_proba = model.predict_proba(X_scaled)
                pred = model.predict(X_scaled)
                
                predictions[name] = pred
                probabilities[name] = pred_proba
                confidences[name] = np.max(pred_proba, axis=1)
                
            except Exception as e:
                print(f"Error getting prediction from {name}: {e}")
                continue
        
        # Calculate weighted ensemble prediction
        if probabilities:
            # Weighted average of probabilities
            weighted_probs = np.zeros_like(list(probabilities.values())[0])
            total_weight = 0
            
            for name, prob in probabilities.items():
                weight = self.ensemble_weights.get(name, 1.0)
                weighted_probs += weight * prob
                total_weight += weight
            
            if total_weight > 0:
                weighted_probs /= total_weight
            
            # Final prediction
            ensemble_pred = np.argmax(weighted_probs, axis=1)
            ensemble_confidence = np.max(weighted_probs, axis=1)
            
            # Calculate uncertainty (entropy)
            entropy = -np.sum(weighted_probs * np.log(weighted_probs + 1e-10), axis=1)
            uncertainty = entropy / np.log(2)  # Normalize to [0, 1]
            
            result = {
                'prediction': ensemble_pred,
                'confidence': ensemble_confidence,
                'uncertainty': uncertainty,
                'probabilities': weighted_probs,
                'prediction_label': ['Benign' if p == 0 else 'Malignant' for p in ensemble_pred]
            }
            
            if return_individual:
                result['individual_predictions'] = predictions
                result['individual_confidences'] = confidences
                result['individual_probabilities'] = probabilities
            
            return result
        
        raise ValueError("No valid predictions available")
    
    def evaluate_ensemble(self, X_test: np.ndarray, y_test: np.ndarray) -> Dict[str, Any]:
        """Comprehensive evaluation of the ensemble"""
        
        # Get ensemble predictions
        results = self.predict_ensemble(X_test, return_individual=True)
        
        # Calculate metrics
        accuracy = accuracy_score(y_test, results['prediction'])
        
        # ROC AUC
        try:
            roc_auc = roc_auc_score(y_test, results['probabilities'][:, 1])
        except:
            roc_auc = 0.0
        
        # Classification report
        class_report = classification_report(
            y_test, results['prediction'], 
            target_names=['Benign', 'Malignant'],
            output_dict=True
        )
        
        # Confusion matrix
        cm = confusion_matrix(y_test, results['prediction'])
        
        # Individual model performance on test set
        individual_performance = {}
        for name, model in self.trained_models.items():
            try:
                X_scaled = self.scaler.transform(X_test)
                pred = model.predict(X_scaled)
                acc = accuracy_score(y_test, pred)
                individual_performance[name] = acc
            except:
                individual_performance[name] = 0.0
        
        return {
            'ensemble_accuracy': accuracy,
            'ensemble_roc_auc': roc_auc,
            'classification_report': class_report,
            'confusion_matrix': cm.tolist(),
            'individual_performance': individual_performance,
            'average_confidence': np.mean(results['confidence']),
            'average_uncertainty': np.mean(results['uncertainty']),
            'model_weights': self.ensemble_weights
        }
    
    def get_feature_importance(self) -> Dict[str, Dict[str, float]]:
        """Get feature importance from all models that support it"""
        
        importance_dict = {}
        
        for name, model in self.trained_models.items():
            if hasattr(model, 'feature_importances_'):
                importance_dict[name] = dict(zip(
                    self.feature_names or [f'feature_{i}' for i in range(len(model.feature_importances_))],
                    model.feature_importances_
                ))
            elif hasattr(model, 'coef_'):
                # For linear models, use absolute coefficients
                coef = np.abs(model.coef_[0])
                importance_dict[name] = dict(zip(
                    self.feature_names or [f'feature_{i}' for i in range(len(coef))],
                    coef
                ))
        
        return importance_dict
    
    def save_models(self, model_dir: str = "models"):
        """Save all trained models and scaler"""
        
        os.makedirs(model_dir, exist_ok=True)
        
        # Save individual models
        for name, model in self.trained_models.items():
            model_path = os.path.join(model_dir, f"wisconsin_{name}.joblib")
            joblib.dump(model, model_path)
            print(f"Saved {name} to {model_path}")
        
        # Save scaler
        scaler_path = os.path.join(model_dir, "wisconsin_scaler.joblib")
        joblib.dump(self.scaler, scaler_path)
        print(f"Saved scaler to {scaler_path}")
        
        # Save ensemble metadata
        metadata = {
            'ensemble_weights': self.ensemble_weights,
            'model_performance': self.model_performance,
            'feature_names': self.feature_names,
            'trained_at': datetime.now().isoformat(),
            'model_count': len(self.trained_models)
        }
        
        metadata_path = os.path.join(model_dir, "wisconsin_ensemble_metadata.joblib")
        joblib.dump(metadata, metadata_path)
        print(f"Saved ensemble metadata to {metadata_path}")
    
    def load_models(self, model_dir: str = "models") -> bool:
        """Load all trained models and scaler"""
        
        try:
            # Load metadata
            metadata_path = os.path.join(model_dir, "wisconsin_ensemble_metadata.joblib")
            if os.path.exists(metadata_path):
                metadata = joblib.load(metadata_path)
                self.ensemble_weights = metadata.get('ensemble_weights', {})
                self.model_performance = metadata.get('model_performance', {})
                self.feature_names = metadata.get('feature_names', None)
                print(f"Loaded ensemble metadata from {metadata_path}")
            
            # Load scaler
            scaler_path = os.path.join(model_dir, "wisconsin_scaler.joblib")
            if os.path.exists(scaler_path):
                self.scaler = joblib.load(scaler_path)
                print(f"Loaded scaler from {scaler_path}")
            
            # Load individual models
            loaded_count = 0
            for name in self.models.keys():
                model_path = os.path.join(model_dir, f"wisconsin_{name}.joblib")
                if os.path.exists(model_path):
                    self.trained_models[name] = joblib.load(model_path)
                    loaded_count += 1
                    print(f"Loaded {name} from {model_path}")
            
            print(f"Successfully loaded {loaded_count} models")
            return loaded_count > 0
            
        except Exception as e:
            print(f"Error loading models: {e}")
            return False
    
    def hyperparameter_tuning(self, X: np.ndarray, y: np.ndarray, 
                            model_name: str = 'random_forest') -> Dict[str, Any]:
        """Perform hyperparameter tuning for a specific model"""
        
        if model_name not in self.models:
            raise ValueError(f"Model {model_name} not found")
        
        # Define parameter grids for different models
        param_grids = {
            'random_forest': {
                'n_estimators': [100, 200, 300],
                'max_depth': [10, 12, 15, None],
                'min_samples_split': [2, 3, 5],
                'min_samples_leaf': [1, 2, 4]
            },
            'gradient_boosting': {
                'n_estimators': [100, 200, 300],
                'learning_rate': [0.05, 0.1, 0.15],
                'max_depth': [4, 6, 8],
                'min_samples_split': [2, 3, 5]
            },
            'svm_rbf': {
                'C': [0.1, 1, 10, 100],
                'gamma': ['scale', 'auto', 0.001, 0.01, 0.1, 1]
            },
            'neural_network': {
                'hidden_layer_sizes': [(50,), (100,), (100, 50), (100, 50, 25)],
                'alpha': [0.0001, 0.001, 0.01],
                'learning_rate': ['constant', 'adaptive']
            }
        }
        
        if model_name not in param_grids:
            print(f"No parameter grid defined for {model_name}")
            return {}
        
        print(f"Performing hyperparameter tuning for {model_name}...")
        
        # Scale features
        X_scaled = self.scaler.fit_transform(X)
        
        # Grid search with cross-validation
        grid_search = GridSearchCV(
            self.models[model_name],
            param_grids[model_name],
            cv=StratifiedKFold(n_splits=5, shuffle=True, random_state=42),
            scoring='accuracy',
            n_jobs=-1,
            verbose=1
        )
        
        grid_search.fit(X_scaled, y)
        
        # Update the model with best parameters
        self.models[model_name] = grid_search.best_estimator_
        
        return {
            'best_params': grid_search.best_params_,
            'best_score': grid_search.best_score_,
            'cv_results': grid_search.cv_results_
        }

# Global instance
wisconsin_ensemble = WisconsinOptimizedEnsemble()
