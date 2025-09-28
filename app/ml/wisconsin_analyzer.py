"""
Wisconsin Breast Cancer Dataset Analyzer
Comprehensive analysis and feature engineering for the Wisconsin dataset
"""

import pandas as pd
import numpy as np
import requests
from io import StringIO
from typing import Dict, List, Tuple, Optional
try:
    import matplotlib.pyplot as plt
    import seaborn as sns
    import plotly.express as px
    import plotly.graph_objects as go
    from plotly.subplots import make_subplots
    PLOTTING_AVAILABLE = True
except ImportError:
    PLOTTING_AVAILABLE = False

from sklearn.preprocessing import RobustScaler
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix

class WisconsinDatasetAnalyzer:
    """Comprehensive analyzer for Wisconsin Breast Cancer Dataset"""
    
    def __init__(self):
        self.dataset_url = "https://archive.ics.uci.edu/ml/machine-learning-databases/breast-cancer-wisconsin/wdbc.data"
        self.feature_names = [
            'radius_mean', 'texture_mean', 'perimeter_mean', 'area_mean',
            'smoothness_mean', 'compactness_mean', 'concavity_mean', 'concave_points_mean',
            'symmetry_mean', 'fractal_dimension_mean',
            'radius_se', 'texture_se', 'perimeter_se', 'area_se',
            'smoothness_se', 'compactness_se', 'concavity_se', 'concave_points_se',
            'symmetry_se', 'fractal_dimension_se',
            'radius_worst', 'texture_worst', 'perimeter_worst', 'area_worst',
            'smoothness_worst', 'compactness_worst', 'concavity_worst', 'concave_points_worst',
            'symmetry_worst', 'fractal_dimension_worst'
        ]
        
        self.feature_groups = {
            'mean': [f for f in self.feature_names if 'mean' in f],
            'se': [f for f in self.feature_names if 'se' in f],
            'worst': [f for f in self.feature_names if 'worst' in f]
        }
        
        self.feature_descriptions = {
            'radius_mean': 'Mean distance from center to points on perimeter',
            'texture_mean': 'Standard deviation of gray-scale values',
            'perimeter_mean': 'Mean perimeter of the nucleus',
            'area_mean': 'Mean area of the nucleus',
            'smoothness_mean': 'Mean local variation in radius lengths',
            'compactness_mean': 'Mean (perimeter² / area - 1.0)',
            'concavity_mean': 'Mean severity of concave portions of the contour',
            'concave_points_mean': 'Mean number of concave portions of the contour',
            'symmetry_mean': 'Mean symmetry of the nucleus',
            'fractal_dimension_mean': 'Mean "coastline approximation" - 1',
            'radius_se': 'Standard error of radius',
            'texture_se': 'Standard error of texture',
            'perimeter_se': 'Standard error of perimeter',
            'area_se': 'Standard error of area',
            'smoothness_se': 'Standard error of smoothness',
            'compactness_se': 'Standard error of compactness',
            'concavity_se': 'Standard error of concavity',
            'concave_points_se': 'Standard error of concave points',
            'symmetry_se': 'Standard error of symmetry',
            'fractal_dimension_se': 'Standard error of fractal dimension',
            'radius_worst': 'Worst (largest) radius',
            'texture_worst': 'Worst (largest) texture',
            'perimeter_worst': 'Worst (largest) perimeter',
            'area_worst': 'Worst (largest) area',
            'smoothness_worst': 'Worst (largest) smoothness',
            'compactness_worst': 'Worst (largest) compactness',
            'concavity_worst': 'Worst (largest) concavity',
            'concave_points_worst': 'Worst (largest) concave points',
            'symmetry_worst': 'Worst (largest) symmetry',
            'fractal_dimension_worst': 'Worst (largest) fractal dimension'
        }
        
        self.feature_ranges = {
            'radius_mean': {'min': 6.981, 'max': 28.11, 'typical': (10, 20)},
            'texture_mean': {'min': 9.71, 'max': 39.28, 'typical': (15, 25)},
            'perimeter_mean': {'min': 43.79, 'max': 188.5, 'typical': (80, 120)},
            'area_mean': {'min': 143.5, 'max': 2501.0, 'typical': (500, 1000)},
            'smoothness_mean': {'min': 0.05263, 'max': 0.1634, 'typical': (0.08, 0.12)},
            'compactness_mean': {'min': 0.01938, 'max': 0.3454, 'typical': (0.05, 0.15)},
            'concavity_mean': {'min': 0.0, 'max': 0.4268, 'typical': (0.0, 0.1)},
            'concave_points_mean': {'min': 0.0, 'max': 0.2012, 'typical': (0.0, 0.05)},
            'symmetry_mean': {'min': 0.106, 'max': 0.304, 'typical': (0.15, 0.25)},
            'fractal_dimension_mean': {'min': 0.04996, 'max': 0.09744, 'typical': (0.06, 0.08)},
            'radius_se': {'min': 0.1115, 'max': 2.873, 'typical': (0.3, 0.8)},
            'texture_se': {'min': 0.3602, 'max': 4.885, 'typical': (1.0, 2.0)},
            'perimeter_se': {'min': 0.757, 'max': 21.98, 'typical': (2.0, 6.0)},
            'area_se': {'min': 6.802, 'max': 542.2, 'typical': (30, 100)},
            'smoothness_se': {'min': 0.001713, 'max': 0.03113, 'typical': (0.005, 0.015)},
            'compactness_se': {'min': 0.002252, 'max': 0.1354, 'typical': (0.01, 0.04)},
            'concavity_se': {'min': 0.0, 'max': 0.396, 'typical': (0.0, 0.05)},
            'concave_points_se': {'min': 0.0, 'max': 0.05279, 'typical': (0.0, 0.02)},
            'symmetry_se': {'min': 0.007882, 'max': 0.07895, 'typical': (0.02, 0.04)},
            'fractal_dimension_se': {'min': 0.0008948, 'max': 0.02984, 'typical': (0.003, 0.01)},
            'radius_worst': {'min': 7.93, 'max': 36.04, 'typical': (12, 25)},
            'texture_worst': {'min': 12.02, 'max': 49.54, 'typical': (20, 35)},
            'perimeter_worst': {'min': 50.41, 'max': 251.2, 'typical': (100, 160)},
            'area_worst': {'min': 185.2, 'max': 4254.0, 'typical': (800, 1500)},
            'smoothness_worst': {'min': 0.07117, 'max': 0.2226, 'typical': (0.1, 0.16)},
            'compactness_worst': {'min': 0.02729, 'max': 1.058, 'typical': (0.1, 0.4)},
            'concavity_worst': {'min': 0.0, 'max': 1.252, 'typical': (0.0, 0.3)},
            'concave_points_worst': {'min': 0.0, 'max': 0.291, 'typical': (0.0, 0.1)},
            'symmetry_worst': {'min': 0.1565, 'max': 0.6638, 'typical': (0.2, 0.4)},
            'fractal_dimension_worst': {'min': 0.05504, 'max': 0.2075, 'typical': (0.08, 0.12)}
        }
    
    def download_dataset(self) -> pd.DataFrame:
        """Download the Wisconsin Breast Cancer Dataset"""
        try:
            print("Downloading Wisconsin Breast Cancer Dataset...")
            response = requests.get(self.dataset_url)
            response.raise_for_status()
            
            # Column names for the dataset
            column_names = ['id', 'diagnosis'] + self.feature_names
            
            # Parse the data
            data = StringIO(response.text)
            df = pd.read_csv(data, header=None, names=column_names)
            
            # Remove the ID column as it's not needed for prediction
            df = df.drop('id', axis=1)
            
            # Convert diagnosis to binary (M=1, B=0)
            df['diagnosis'] = df['diagnosis'].map({'M': 1, 'B': 0})
            
            print(f"Dataset loaded successfully: {len(df)} samples, {len(df.columns)-1} features")
            return df
            
        except Exception as e:
            print(f"Error downloading dataset: {e}")
            return self._create_sample_dataset()
    
    def _create_sample_dataset(self) -> pd.DataFrame:
        """Create a sample dataset for testing when download fails"""
        print("Creating sample dataset for testing...")
        np.random.seed(42)
        n_samples = 569  # Same as real dataset
        
        # Generate synthetic data that mimics the real dataset structure
        data = {}
        data['diagnosis'] = np.random.choice([0, 1], n_samples, p=[0.63, 0.37])  # Real distribution
        
        for feature in self.feature_names:
            range_info = self.feature_ranges[feature]
            if 'mean' in feature:
                if 'radius' in feature:
                    data[feature] = np.random.normal(14, 3, n_samples)
                elif 'texture' in feature:
                    data[feature] = np.random.normal(19, 4, n_samples)
                elif 'perimeter' in feature:
                    data[feature] = np.random.normal(92, 25, n_samples)
                elif 'area' in feature:
                    data[feature] = np.random.normal(655, 350, n_samples)
                else:
                    data[feature] = np.random.uniform(range_info['min'], range_info['max'], n_samples)
            elif 'se' in feature:
                data[feature] = np.random.uniform(range_info['min'], range_info['max'], n_samples)
            else:  # worst
                if 'radius' in feature:
                    data[feature] = np.random.normal(16, 4, n_samples)
                elif 'texture' in feature:
                    data[feature] = np.random.normal(25, 6, n_samples)
                elif 'perimeter' in feature:
                    data[feature] = np.random.normal(107, 33, n_samples)
                elif 'area' in feature:
                    data[feature] = np.random.normal(880, 570, n_samples)
                else:
                    data[feature] = np.random.uniform(range_info['min'], range_info['max'], n_samples)
        
        return pd.DataFrame(data)
    
    def get_dataset_statistics(self) -> Dict:
        """Get comprehensive dataset statistics"""
        df = self.download_dataset()
        
        stats = {
            'dataset_info': {
                'name': 'Wisconsin Breast Cancer Dataset (Diagnostic)',
                'source': 'UCI Machine Learning Repository',
                'url': 'https://archive.ics.uci.edu/ml/datasets/Breast+Cancer+Wisconsin+(Diagnostic)',
                'total_samples': len(df),
                'total_features': len(self.feature_names),
                'missing_values': df.isnull().sum().sum()
            },
            'class_distribution': {
                'malignant_samples': len(df[df['diagnosis'] == 1]),
                'benign_samples': len(df[df['diagnosis'] == 0]),
                'malignant_percentage': (len(df[df['diagnosis'] == 1]) / len(df)) * 100,
                'benign_percentage': (len(df[df['diagnosis'] == 0]) / len(df)) * 100
            },
            'feature_statistics': df.describe().to_dict(),
            'feature_correlations': df.corr()['diagnosis'].drop('diagnosis').sort_values(ascending=False).to_dict(),
            'feature_groups': {
                'mean_features': len(self.feature_groups['mean']),
                'standard_error_features': len(self.feature_groups['se']),
                'worst_features': len(self.feature_groups['worst']),
                'total_features': len(self.feature_names)
            }
        }
        
        return stats
    
    def create_enhanced_features(self, df: pd.DataFrame) -> pd.DataFrame:
        """Create additional features specific to Wisconsin dataset characteristics"""
        df_enhanced = df.copy()
        
        # Feature ratios that are clinically meaningful
        df_enhanced['area_perimeter_ratio'] = df_enhanced['area_mean'] / df_enhanced['perimeter_mean']
        df_enhanced['compactness_smoothness_ratio'] = df_enhanced['compactness_mean'] / df_enhanced['smoothness_mean']
        df_enhanced['concavity_compactness_ratio'] = df_enhanced['concavity_mean'] / df_enhanced['compactness_mean']
        
        # Statistical features
        df_enhanced['mean_se_ratio'] = df_enhanced['radius_mean'] / df_enhanced['radius_se']
        df_enhanced['worst_mean_ratio'] = df_enhanced['radius_worst'] / df_enhanced['radius_mean']
        
        # Combined risk indicators
        df_enhanced['shape_irregularity'] = (df_enhanced['concavity_mean'] + df_enhanced['concave_points_mean']) / 2
        df_enhanced['texture_complexity'] = df_enhanced['texture_mean'] * df_enhanced['fractal_dimension_mean']
        
        # Feature group statistics
        df_enhanced['mean_features_avg'] = df_enhanced[self.feature_groups['mean']].mean(axis=1)
        df_enhanced['se_features_avg'] = df_enhanced[self.feature_groups['se']].mean(axis=1)
        df_enhanced['worst_features_avg'] = df_enhanced[self.feature_groups['worst']].mean(axis=1)
        
        return df_enhanced
    
    def get_feature_importance_analysis(self, model) -> Dict:
        """Analyze feature importance grouped by feature types"""
        if hasattr(model, 'feature_importances_'):
            importance = model.feature_importances_
            feature_names = model.feature_names_in_ if hasattr(model, 'feature_names_in_') else self.feature_names
            
            # Group by feature type
            grouped_importance = {
                'mean_features': [],
                'se_features': [],
                'worst_features': [],
                'enhanced_features': []
            }
            
            for i, feature in enumerate(feature_names):
                if i < len(importance):
                    if 'mean' in feature:
                        grouped_importance['mean_features'].append((feature, importance[i]))
                    elif 'se' in feature:
                        grouped_importance['se_features'].append((feature, importance[i]))
                    elif 'worst' in feature:
                        grouped_importance['worst_features'].append((feature, importance[i]))
                    else:
                        grouped_importance['enhanced_features'].append((feature, importance[i]))
            
            # Sort each group by importance
            for group in grouped_importance:
                grouped_importance[group].sort(key=lambda x: x[1], reverse=True)
            
            return grouped_importance
        
        return {}
    
    def create_correlation_analysis(self) -> Dict:
        """Create comprehensive correlation analysis"""
        df = self.download_dataset()
        
        # Feature correlation with diagnosis
        correlations = df.corr()['diagnosis'].drop('diagnosis').sort_values(ascending=False)
        
        # Group correlations
        group_correlations = {
            'mean_features': correlations[correlations.index.str.contains('mean')].mean(),
            'se_features': correlations[correlations.index.str.contains('se')].mean(),
            'worst_features': correlations[correlations.index.str.contains('worst')].mean()
        }
        
        return {
            'feature_correlations': correlations.to_dict(),
            'group_correlations': group_correlations,
            'top_predictive_features': correlations.head(10).to_dict(),
            'correlation_matrix': df.corr().to_dict()
        }
    
    def validate_feature_input(self, feature_name: str, value: float) -> Dict:
        """Validate feature input against Wisconsin dataset ranges"""
        if feature_name not in self.feature_ranges:
            return {'valid': True, 'message': 'Feature not found in dataset'}
        
        range_info = self.feature_ranges[feature_name]
        
        if value < range_info['min'] or value > range_info['max']:
            return {
                'valid': False,
                'message': f'Value {value} is outside Wisconsin dataset range [{range_info["min"]:.3f}, {range_info["max"]:.3f}]',
                'suggestion': f'Typical range: {range_info["typical"][0]:.3f} - {range_info["typical"][1]:.3f}'
            }
        
        return {'valid': True, 'message': 'Value is within valid range'}
    
    def get_feature_description(self, feature_name: str) -> str:
        """Get clinical description of a feature"""
        return self.feature_descriptions.get(feature_name, 'No description available')
    
    def get_feature_range(self, feature_name: str) -> Dict:
        """Get range information for a feature"""
        return self.feature_ranges.get(feature_name, {})

# Global instance
wisconsin_analyzer = WisconsinDatasetAnalyzer()
