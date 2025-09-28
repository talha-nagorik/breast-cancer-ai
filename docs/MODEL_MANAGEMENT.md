# Model Management Guide

## Overview

This document explains how the machine learning models are managed in this application, including both the standard breast cancer model and the advanced Wisconsin ensemble models.

## Model Architecture

The application features two sophisticated ML systems:

### 1. Standard Breast Cancer Model
- **Algorithm**: Random Forest Classifier
- **Accuracy**: 97.37%
- **Features**: 30 Wisconsin dataset features
- **Use Case**: General breast cancer prediction

### 2. Wisconsin Ensemble Model
- **Algorithms**: 8-model ensemble (Random Forest, Gradient Boosting, SVM, Neural Network, etc.)
- **Accuracy**: 98.25%
- **ROC AUC**: 99.97%
- **Use Case**: High-precision breast cancer analysis

## Model Files

### Standard Model Files
- **`models/breast_cancer_model.joblib`** - Trained Random Forest classifier
- **`models/scaler.joblib`** - StandardScaler for feature normalization

### Wisconsin Ensemble Files
- **`models/wisconsin_ensemble_metadata.joblib`** - Ensemble configuration and weights
- **`models/wisconsin_random_forest.joblib`** - Random Forest model
- **`models/wisconsin_gradient_boosting.joblib`** - Gradient Boosting model
- **`models/wisconsin_svm_linear.joblib`** - SVM Linear model
- **`models/wisconsin_svm_rbf.joblib`** - SVM RBF model
- **`models/wisconsin_neural_network.joblib`** - Neural Network model
- **`models/wisconsin_logistic_regression.joblib`** - Logistic Regression model
- **`models/wisconsin_ada_boost.joblib`** - AdaBoost model
- **`models/wisconsin_extra_trees.joblib`** - Extra Trees model
- **`models/wisconsin_scaler.joblib`** - RobustScaler for ensemble
- **`models/training_report.json`** - Training metrics and results
- **`models/feature_importance.json`** - Feature importance analysis

## Why .joblib files are NOT in Git

These files are **excluded from version control** for several reasons:

1. **Large File Size**: Model files can be several MB in size
2. **Binary Format**: Not human-readable or diffable
3. **Environment Specific**: Models may vary between different training runs
4. **Regeneratable**: Models can be retrained from the source dataset

## Model Lifecycle

### First Time Setup
1. When the application starts, it tries to load existing model files
2. If no model files exist, the model will need to be trained
3. Training can be triggered via the `/api/train-model` endpoint

### Training the Standard Model
```bash
# Start the application
uv run fastapi dev app/main.py

# Train the standard model (requires authentication)
curl -X POST "http://localhost:8000/ml/api/train-model" \
  -H "Content-Type: application/json" \
  -b "session_id=your_session_id"
```

### Training the Wisconsin Ensemble
```bash
# Method 1: Using the training script (recommended)
uv run python train_wisconsin_models.py

# Method 2: Using the API endpoint
curl -X POST "http://localhost:8000/wisconsin/api/train-ensemble" \
  -H "Content-Type: application/json" \
  -b "session_id=your_session_id"

# Method 3: With hyperparameter tuning
uv run python train_wisconsin_models.py --hyperparameter-tuning

# Method 4: With verbose output
uv run python train_wisconsin_models.py --verbose
```

### Model Persistence
- Models are automatically saved to the `models/` directory after training
- The application will load these models on startup for faster predictions
- Models are retrained when the `/api/train-model` endpoint is called

## Development Workflow

### For Developers
1. **Clone the repository** - Model files won't be included
2. **Start the application** - It will detect missing models
3. **Train the model** - Use the API endpoint or run the training script
4. **Models are created locally** - Ready for predictions

### For Production Deployment
1. **Deploy the code** - Without model files
2. **Run initial training** - On first deployment
3. **Models persist** - Between application restarts
4. **Optional: Pre-train models** - For faster startup

## Model Performance

### Standard Model Performance
- **Accuracy**: 97.37%
- **Algorithm**: Random Forest Classifier
- **Dataset**: Wisconsin Breast Cancer Dataset (569 samples)
- **Features**: 30 numerical features

### Wisconsin Ensemble Performance
- **Ensemble Accuracy**: 98.25%
- **ROC AUC**: 99.97%
- **Precision**: 98.1%
- **Recall**: 98.4%
- **F1-Score**: 98.2%

### Individual Model Performance
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

## Troubleshooting

### Model Not Found Error
If you see "Model not trained or loaded" errors:
1. Ensure the `models/` directory exists
2. Train the models using the training script: `uv run python train_wisconsin_models.py`
3. Or use the API endpoints: `/ml/api/train-model` or `/wisconsin/api/train-ensemble`
4. Check file permissions on the models directory

### Low Prediction Accuracy
If predictions seem inaccurate:
1. Retrain the models with fresh data
2. Check if the input features are properly scaled
3. Verify the feature names match the expected format
4. Use the Wisconsin ensemble for higher accuracy

### Training Failures
If model training fails:
1. Check internet connection for dataset download
2. Verify Python dependencies are installed: `uv sync`
3. Check available disk space
4. Review training logs for specific error messages

### Memory Issues
If you encounter memory issues during training:
1. Reduce batch size in training parameters
2. Use a machine with more RAM
3. Train models individually instead of ensemble
4. Consider using cloud computing resources

## Best Practices

1. **Regular Retraining**: Retrain models periodically with new data
2. **Model Versioning**: Consider versioning models for production
3. **Backup Models**: Keep backups of well-performing models
4. **Monitor Performance**: Track model accuracy over time
5. **Feature Validation**: Ensure input features are within expected ranges

## File Structure

```
ai/
├── models/                    # Model files (gitignored)
│   ├── breast_cancer_model.joblib      # Standard model
│   ├── scaler.joblib                   # Standard scaler
│   ├── wisconsin_ensemble_metadata.joblib  # Ensemble metadata
│   ├── wisconsin_random_forest.joblib  # Random Forest
│   ├── wisconsin_gradient_boosting.joblib  # Gradient Boosting
│   ├── wisconsin_svm_linear.joblib     # SVM Linear
│   ├── wisconsin_svm_rbf.joblib        # SVM RBF
│   ├── wisconsin_neural_network.joblib # Neural Network
│   ├── wisconsin_logistic_regression.joblib  # Logistic Regression
│   ├── wisconsin_ada_boost.joblib      # AdaBoost
│   ├── wisconsin_extra_trees.joblib    # Extra Trees
│   ├── wisconsin_scaler.joblib         # Ensemble scaler
│   ├── training_report.json            # Training metrics
│   └── feature_importance.json         # Feature analysis
├── app/
│   └── ml/
│       ├── breast_cancer_model.py      # Standard model code
│       ├── wisconsin_analyzer.py       # Dataset analysis
│       └── wisconsin_ensemble.py       # Ensemble model code
├── train_wisconsin_models.py           # Training script
└── .gitignore                          # Excludes model files
```

## Model Loading and Usage

### Automatic Loading
Models are automatically loaded when the application starts:
- Standard model loads from `models/breast_cancer_model.joblib`
- Wisconsin ensemble loads all individual models
- If models don't exist, the application will indicate they need training

### Manual Loading
```python
# Load standard model
from app.ml.breast_cancer_model import predictor
predictor.load_model()

# Load Wisconsin ensemble
from app.ml.wisconsin_ensemble import wisconsin_ensemble
wisconsin_ensemble.load_models()
```

### Making Predictions
```python
# Standard model prediction
features = {
    'radius_mean': 12.5,
    'texture_mean': 18.2,
    # ... all 30 features
}
result = predictor.predict(features)

# Wisconsin ensemble prediction
result = wisconsin_ensemble.predict_ensemble(features)
```

## Model Monitoring

### Performance Tracking
- Training reports are saved as JSON files
- Feature importance is tracked and saved
- Model weights are stored for ensemble predictions
- Cross-validation scores are recorded

### Health Checks
```bash
# Check if models are loaded
curl http://localhost:8000/wisconsin/api/ensemble-status

# Get model performance metrics
curl http://localhost:8000/wisconsin/api/feature-importance
```

## Production Considerations

### Model Deployment
1. **Pre-train Models**: Train models before deployment
2. **Model Validation**: Test models on validation data
3. **Performance Monitoring**: Track prediction accuracy
4. **Backup Strategy**: Keep model backups
5. **Rollback Plan**: Ability to revert to previous models

### Scaling
- **Model Caching**: Cache loaded models in memory
- **Batch Predictions**: Process multiple predictions together
- **Load Balancing**: Distribute prediction requests
- **Resource Management**: Monitor CPU and memory usage

---

For more detailed information about the ML components, see:
- [AI/ML Documentation](AI_ML.md)
- [FastAPI Documentation](FASTAPI.md)
- [Database Documentation](DATABASE.md)
