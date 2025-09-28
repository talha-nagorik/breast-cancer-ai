# Model Management Guide

## Overview

This document explains how the machine learning models are managed in this application.

## Model Files

The application uses two `.joblib` files for the breast cancer prediction model:

- **`models/breast_cancer_model.joblib`** - Contains the trained Random Forest classifier
- **`models/scaler.joblib`** - Contains the StandardScaler for feature normalization

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

### Training the Model
```bash
# Start the application
uv run uvicorn main:app --reload

# Train the model (requires authentication)
curl -X POST "http://localhost:8000/api/train-model" \
  -H "Content-Type: application/json" \
  -b "session_id=your_session_id"
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

The current model achieves:
- **Accuracy**: 97.37%
- **Algorithm**: Random Forest Classifier
- **Dataset**: Wisconsin Breast Cancer Dataset (569 samples)
- **Features**: 30 numerical features

## Troubleshooting

### Model Not Found Error
If you see "Model not trained or loaded" errors:
1. Ensure the `models/` directory exists
2. Train the model using the API endpoint
3. Check file permissions on the models directory

### Low Prediction Accuracy
If predictions seem inaccurate:
1. Retrain the model with fresh data
2. Check if the input features are properly scaled
3. Verify the feature names match the expected format

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
│   ├── breast_cancer_model.joblib
│   └── scaler.joblib
├── app/
│   └── ml/
│       └── breast_cancer_model.py  # Model training code
└── .gitignore                 # Excludes model files
```
