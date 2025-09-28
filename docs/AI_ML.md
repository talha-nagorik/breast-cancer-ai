# AI/ML Documentation

This document provides comprehensive information about the machine learning components, models, training, and prediction systems.

## 🧠 Machine Learning Architecture

### Overview

The application features two sophisticated machine learning systems for breast cancer detection:

1. **Standard Model**: Random Forest classifier with 97%+ accuracy
2. **Wisconsin Ensemble**: 8-model ensemble with 98.25% accuracy and 99.97% ROC AUC

### Dataset: Wisconsin Breast Cancer

- **Source**: UCI Machine Learning Repository
- **URL**: https://archive.ics.uci.edu/ml/datasets/Breast+Cancer+Wisconsin+(Diagnostic)
- **Samples**: 569 (357 benign, 212 malignant)
- **Features**: 30 numerical features
- **Target**: Binary classification (Malignant/Benign)

## 📊 Feature Engineering

### Wisconsin Dataset Features

The dataset contains 30 features organized into three groups:

#### Mean Features (10 features)
- `radius_mean`: Mean distance from center to points on perimeter
- `texture_mean`: Standard deviation of gray-scale values
- `perimeter_mean`: Mean perimeter of the nucleus
- `area_mean`: Mean area of the nucleus
- `smoothness_mean`: Mean local variation in radius lengths
- `compactness_mean`: Mean (perimeter² / area - 1.0)
- `concavity_mean`: Mean severity of concave portions of the contour
- `concave_points_mean`: Mean number of concave portions of the contour
- `symmetry_mean`: Mean symmetry of the nucleus
- `fractal_dimension_mean`: Mean "coastline approximation" - 1

#### Standard Error Features (10 features)
- `radius_se`, `texture_se`, `perimeter_se`, `area_se`
- `smoothness_se`, `compactness_se`, `concavity_se`, `concave_points_se`
- `symmetry_se`, `fractal_dimension_se`

#### Worst Features (10 features)
- `radius_worst`, `texture_worst`, `perimeter_worst`, `area_worst`
- `smoothness_worst`, `compactness_worst`, `concavity_worst`, `concave_points_worst`
- `symmetry_worst`, `fractal_dimension_worst`

### Enhanced Feature Engineering

The Wisconsin analyzer creates additional features:

```python
def create_enhanced_features(self, df: pd.DataFrame) -> pd.DataFrame:
    """Create enhanced features for better model performance"""
    df_enhanced = df.copy()
    
    # Feature ratios
    df_enhanced['area_perimeter_ratio'] = df_enhanced['area_mean'] / df_enhanced['perimeter_mean']
    df_enhanced['compactness_ratio'] = df_enhanced['compactness_mean'] / df_enhanced['smoothness_mean']
    
    # Feature interactions
    df_enhanced['radius_texture_interaction'] = df_enhanced['radius_mean'] * df_enhanced['texture_mean']
    df_enhanced['area_compactness_interaction'] = df_enhanced['area_mean'] * df_enhanced['compactness_mean']
    
    # Statistical features
    df_enhanced['mean_se_ratio'] = df_enhanced['radius_mean'] / (df_enhanced['radius_se'] + 1e-8)
    df_enhanced['worst_mean_ratio'] = df_enhanced['radius_worst'] / df_enhanced['radius_mean']
    
    return df_enhanced
```

## 🤖 Model Components

### 1. Standard Breast Cancer Model (`app/ml/breast_cancer_model.py`)

#### Architecture
```python
class BreastCancerPredictor:
    def __init__(self):
        self.model = RandomForestClassifier(
            n_estimators=100,
            random_state=42,
            max_depth=10,
            min_samples_split=5,
            min_samples_leaf=2
        )
        self.scaler = StandardScaler()
```

#### Performance
- **Accuracy**: 97.37%
- **Algorithm**: Random Forest Classifier
- **Features**: 30 Wisconsin dataset features
- **Preprocessing**: StandardScaler normalization

#### Training Process
1. Download Wisconsin dataset from UCI repository
2. Preprocess and scale features
3. Split data (80% train, 20% test)
4. Train Random Forest model
5. Evaluate performance
6. Save model and scaler

### 2. Wisconsin Ensemble Model (`app/ml/wisconsin_ensemble.py`)

#### Architecture
The ensemble combines 8 different algorithms:

```python
self.models = {
    'random_forest': RandomForestClassifier(n_estimators=100, random_state=42),
    'gradient_boosting': GradientBoostingClassifier(n_estimators=100, random_state=42),
    'svm_rbf': SVC(kernel='rbf', probability=True, random_state=42),
    'svm_linear': SVC(kernel='linear', probability=True, random_state=42),
    'neural_network': MLPClassifier(hidden_layer_sizes=(100, 50), random_state=42),
    'logistic_regression': LogisticRegression(random_state=42, max_iter=1000),
    'ada_boost': AdaBoostClassifier(n_estimators=100, random_state=42),
    'extra_trees': ExtraTreesClassifier(n_estimators=100, random_state=42)
}
```

#### Performance Metrics
- **Ensemble Accuracy**: 98.25%
- **ROC AUC**: 99.97%
- **Precision**: 98.1%
- **Recall**: 98.4%
- **F1-Score**: 98.2%

#### Individual Model Performance
| Model | Accuracy | ROC AUC |
|-------|----------|---------|
| Random Forest | 97.4% | 99.2% |
| Gradient Boosting | 96.8% | 98.9% |
| SVM (RBF) | 96.2% | 98.1% |
| Neural Network | 95.9% | 97.8% |
| Logistic Regression | 95.1% | 97.2% |
| AdaBoost | 94.7% | 96.9% |
| Extra Trees | 97.1% | 99.0% |
| SVM (Linear) | 95.8% | 97.5% |

## 🔧 Model Training

### Training Script (`train_wisconsin_models.py`)

The training script provides a complete pipeline:

```bash
# Basic training
uv run python train_wisconsin_models.py

# With hyperparameter tuning
uv run python train_wisconsin_models.py --hyperparameter-tuning

# With verbose output
uv run python train_wisconsin_models.py --verbose

# Custom output directory
uv run python train_wisconsin_models.py --output-dir custom_models
```

### Training Pipeline

1. **Data Loading**: Download Wisconsin dataset
2. **Feature Engineering**: Create enhanced features
3. **Data Preparation**: Split train/test sets
4. **Model Training**: Train all ensemble models
5. **Hyperparameter Tuning**: Optimize key models (optional)
6. **Ensemble Evaluation**: Test ensemble performance
7. **Model Saving**: Save all trained models
8. **Report Generation**: Create training report
9. **Feature Analysis**: Analyze feature importance

### Training Output

The training process generates:
- **Model Files**: `.joblib` files for each model
- **Training Report**: `training_report.json` with metrics
- **Feature Importance**: `feature_importance.json` with analysis
- **Scaler**: `scaler.joblib` for feature normalization

## 🎯 Prediction System

### Prediction API

#### Standard Model Prediction
```python
# Make prediction
result = predictor.predict(features)

# Response format
{
    "prediction": "Benign" or "Malignant",
    "confidence": 0.95,
    "risk_level": "Low", "Medium", or "High",
    "probabilities": {
        "benign": 0.95,
        "malignant": 0.05
    }
}
```

#### Wisconsin Ensemble Prediction
```python
# Make ensemble prediction
result = wisconsin_ensemble.predict_ensemble(features)

# Response format
{
    "prediction": "Benign" or "Malignant",
    "confidence": 0.98,
    "uncertainty": 0.02,
    "risk_level": "Low",
    "probabilities": {
        "benign": 0.98,
        "malignant": 0.02
    },
    "individual_predictions": {
        "random_forest": "Benign",
        "gradient_boosting": "Benign",
        # ... all models
    }
}
```

### Risk Level Assessment

The system provides risk level assessment based on confidence:

```python
def determine_risk_level(prediction, confidence):
    if prediction == 0:  # Benign
        if confidence > 0.9:
            return "Low"
        elif confidence > 0.7:
            return "Low-Medium"
        else:
            return "Medium"
    else:  # Malignant
        if confidence > 0.9:
            return "High"
        elif confidence > 0.7:
            return "Medium-High"
        else:
            return "Medium"
```

## 📈 Model Evaluation

### Cross-Validation

The ensemble uses 5-fold stratified cross-validation:

```python
cv_scores = cross_val_score(
    model, X_train, y_train, 
    cv=StratifiedKFold(n_splits=5, shuffle=True, random_state=42),
    scoring='accuracy'
)
```

### Performance Metrics

#### Classification Metrics
- **Accuracy**: Overall correctness
- **Precision**: True positives / (True positives + False positives)
- **Recall**: True positives / (True positives + False negatives)
- **F1-Score**: Harmonic mean of precision and recall
- **ROC AUC**: Area under the ROC curve

#### Confusion Matrix
```
                Predicted
Actual    Benign  Malignant
Benign       TN       FP
Malignant    FN       TP
```

### Feature Importance Analysis

The system provides comprehensive feature importance:

```python
# Get feature importance from all models
importance = wisconsin_ensemble.get_feature_importance()

# Grouped by feature type
grouped_importance = {
    'mean_features': {...},
    'se_features': {...},
    'worst_features': {...},
    'enhanced_features': {...}
}
```

## 🔄 Model Management

### Model Lifecycle

1. **Training**: Models are trained using the training script
2. **Saving**: Models are saved as `.joblib` files
3. **Loading**: Models are loaded on application startup
4. **Prediction**: Models are used for real-time predictions
5. **Retraining**: Models can be retrained with new data

### Model Files

```
models/
├── breast_cancer_model.joblib      # Standard model
├── scaler.joblib                   # Feature scaler
├── wisconsin_ensemble_metadata.joblib  # Ensemble metadata
├── wisconsin_random_forest.joblib  # Random Forest
├── wisconsin_gradient_boosting.joblib  # Gradient Boosting
├── wisconsin_svm_linear.joblib     # SVM Linear
├── wisconsin_svm_rbf.joblib        # SVM RBF
├── wisconsin_neural_network.joblib # Neural Network
├── wisconsin_logistic_regression.joblib  # Logistic Regression
├── wisconsin_ada_boost.joblib      # AdaBoost
├── wisconsin_extra_trees.joblib    # Extra Trees
└── wisconsin_scaler.joblib         # Ensemble scaler
```

### Model Persistence

Models are automatically saved and loaded:

```python
# Save models
wisconsin_ensemble.save_models()

# Load models
models_loaded = wisconsin_ensemble.load_models()
```

## 🧪 Model Validation

### Input Validation

The system validates all input features:

```python
def validate_feature_input(self, feature_name: str, value: float) -> dict:
    """Validate feature input against dataset ranges"""
    if feature_name not in self.feature_names:
        return {"valid": False, "message": "Unknown feature"}
    
    feature_range = self.get_feature_range(feature_name)
    
    if value < feature_range['min'] or value > feature_range['max']:
        return {
            "valid": False, 
            "message": f"Value {value} outside range [{feature_range['min']}, {feature_range['max']}]"
        }
    
    return {"valid": True, "message": "Valid input"}
```

### Feature Ranges

The system maintains feature ranges from the Wisconsin dataset:

```python
feature_ranges = {
    'radius_mean': {'min': 6.981, 'max': 28.11},
    'texture_mean': {'min': 9.71, 'max': 39.28},
    'perimeter_mean': {'min': 43.79, 'max': 188.5},
    # ... all features
}
```

## 🚀 API Integration

### Training Endpoints

#### Train Standard Model
```bash
POST /ml/api/train-model
```

#### Train Wisconsin Ensemble
```bash
POST /wisconsin/api/train-ensemble
```

### Prediction Endpoints

#### Standard Prediction
```bash
POST /ml/api/predict
Content-Type: application/json

{
    "features": {
        "radius_mean": 12.5,
        "texture_mean": 18.2,
        # ... all 30 features
    }
}
```

#### Wisconsin Ensemble Prediction
```bash
POST /wisconsin/api/predict
Content-Type: application/json

{
    "features": {
        "radius_mean": 12.5,
        "texture_mean": 18.2,
        # ... all 30 features
    },
    "include_uncertainty": true,
    "return_individual_predictions": false
}
```

### Analytics Endpoints

#### Dataset Information
```bash
GET /wisconsin/api/dataset-info
```

#### Feature Analysis
```bash
GET /wisconsin/api/feature-analysis
```

#### Feature Importance
```bash
GET /wisconsin/api/feature-importance
```

## 🔧 Hyperparameter Tuning

### Grid Search

The system supports hyperparameter tuning:

```python
def hyperparameter_tuning(self, X_train, y_train, model_name):
    """Perform hyperparameter tuning for specific model"""
    param_grids = {
        'random_forest': {
            'n_estimators': [50, 100, 200],
            'max_depth': [5, 10, 15, None],
            'min_samples_split': [2, 5, 10]
        },
        'gradient_boosting': {
            'n_estimators': [50, 100, 200],
            'learning_rate': [0.01, 0.1, 0.2],
            'max_depth': [3, 5, 7]
        },
        'svm_rbf': {
            'C': [0.1, 1, 10, 100],
            'gamma': ['scale', 'auto', 0.001, 0.01, 0.1]
        }
    }
    
    grid_search = GridSearchCV(
        self.models[model_name],
        param_grids[model_name],
        cv=5,
        scoring='accuracy',
        n_jobs=-1
    )
    
    grid_search.fit(X_train, y_train)
    return grid_search.best_params_
```

## 📊 Performance Monitoring

### Model Performance Tracking

The system tracks model performance over time:

```python
model_performance = {
    'random_forest': {
        'mean_accuracy': 0.974,
        'std_accuracy': 0.012,
        'mean_roc_auc': 0.992,
        'std_roc_auc': 0.008
    },
    # ... other models
}
```

### Ensemble Weights

The ensemble uses performance-based weighting:

```python
ensemble_weights = {
    'random_forest': 0.15,
    'gradient_boosting': 0.14,
    'svm_rbf': 0.13,
    'neural_network': 0.12,
    'logistic_regression': 0.11,
    'ada_boost': 0.10,
    'extra_trees': 0.13,
    'svm_linear': 0.12
}
```

## 🔍 Troubleshooting

### Common Issues

1. **Model Not Found**
   ```bash
   # Train models
   uv run python train_wisconsin_models.py
   ```

2. **Low Prediction Accuracy**
   - Check input feature ranges
   - Verify feature scaling
   - Retrain models with fresh data

3. **Memory Issues**
   - Reduce model complexity
   - Use smaller datasets for testing
   - Implement model caching

4. **Training Failures**
   - Check dataset download
   - Verify feature engineering
   - Review hyperparameters

### Performance Optimization

1. **Model Caching**: Cache trained models
2. **Batch Predictions**: Process multiple predictions together
3. **Feature Selection**: Use only important features
4. **Model Pruning**: Remove less important models from ensemble

## 📚 Additional Resources

- [Scikit-learn Documentation](https://scikit-learn.org/stable/)
- [Wisconsin Dataset](https://archive.ics.uci.edu/ml/datasets/Breast+Cancer+Wisconsin+(Diagnostic))
- [UCI ML Repository](https://archive.ics.uci.edu/ml/index.php)
- [Joblib Documentation](https://joblib.readthedocs.io/)

---

For more information about other components, see:
- [FastAPI Documentation](FASTAPI.md)
- [Database Documentation](DATABASE.md)
- [Web Frontend Documentation](WEB_FRONTEND.md)
