"""
Wisconsin Breast Cancer Dataset API Endpoints
Specialized endpoints for Wisconsin dataset analysis and predictions
"""

from fastapi import APIRouter, Request, Form, Depends, HTTPException
from fastapi.responses import HTMLResponse, RedirectResponse, JSONResponse
from fastapi.templating import Jinja2Templates
from sqlmodel import Session, select
from pydantic import BaseModel
from typing import Dict, List, Optional, Any
import json
import numpy as np

from ..models.models import User, BreastCancerPrediction
from ..database.database import get_session
from ..dependencies import get_current_user
from ..ml.wisconsin_analyzer import wisconsin_analyzer
from ..ml.wisconsin_ensemble import wisconsin_ensemble

router = APIRouter()
templates = Jinja2Templates(directory="templates")

# Pydantic models for Wisconsin API
class WisconsinPredictionRequest(BaseModel):
    features: Dict[str, float]
    include_uncertainty: bool = True
    return_individual_predictions: bool = False

class WisconsinPredictionResponse(BaseModel):
    prediction: str
    confidence: float
    uncertainty: Optional[float] = None
    risk_level: str
    probabilities: Dict[str, float]
    individual_predictions: Optional[Dict[str, Any]] = None
    feature_validation: Dict[str, Any]

class WisconsinDatasetInfo(BaseModel):
    dataset_name: str
    source: str
    url: str
    statistics: Dict[str, Any]
    feature_groups: Dict[str, int]
    clinical_context: Dict[str, str]

# Wisconsin Dataset Information Endpoints
@router.get("/api/wisconsin/dataset-info", response_model=WisconsinDatasetInfo)
async def get_wisconsin_dataset_info():
    """Get comprehensive information about the Wisconsin dataset"""
    try:
        stats = wisconsin_analyzer.get_dataset_statistics()
        
        return WisconsinDatasetInfo(
            dataset_name="Wisconsin Breast Cancer Dataset (Diagnostic)",
            source="UCI Machine Learning Repository",
            url="https://archive.ics.uci.edu/ml/datasets/Breast+Cancer+Wisconsin+(Diagnostic)",
            statistics=stats,
            feature_groups={
                "mean_features": 10,
                "standard_error_features": 10,
                "worst_features": 10,
                "total_features": 30
            },
            clinical_context={
                "description": "Features computed from digitized images of fine needle aspirate (FNA) of breast mass",
                "diagnosis": "Binary classification: Malignant (M) or Benign (B)",
                "sample_size": "569",
                "feature_type": "Real-valued",
                "clinical_relevance": "Features describe characteristics of cell nuclei present in the image"
            }
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error retrieving dataset info: {str(e)}")

@router.get("/api/wisconsin/feature-analysis")
async def get_wisconsin_feature_analysis():
    """Get detailed analysis of Wisconsin dataset features"""
    try:
        correlation_analysis = wisconsin_analyzer.create_correlation_analysis()
        
        # Get feature descriptions and ranges
        feature_info = {}
        for feature in wisconsin_analyzer.feature_names:
            feature_info[feature] = {
                'description': wisconsin_analyzer.get_feature_description(feature),
                'range': wisconsin_analyzer.get_feature_range(feature),
                'group': 'mean' if 'mean' in feature else 'se' if 'se' in feature else 'worst'
            }
        
        return {
            "feature_correlations": correlation_analysis['feature_correlations'],
            "group_correlations": correlation_analysis['group_correlations'],
            "top_predictive_features": correlation_analysis['top_predictive_features'],
            "feature_info": feature_info,
            "feature_groups": wisconsin_analyzer.feature_groups
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error analyzing features: {str(e)}")

@router.get("/api/wisconsin/feature-validation/{feature_name}")
async def validate_wisconsin_feature(feature_name: str, value: float):
    """Validate a single feature value against Wisconsin dataset ranges"""
    try:
        validation_result = wisconsin_analyzer.validate_feature_input(feature_name, value)
        
        return {
            "feature_name": feature_name,
            "value": value,
            "validation": validation_result,
            "description": wisconsin_analyzer.get_feature_description(feature_name),
            "range": wisconsin_analyzer.get_feature_range(feature_name)
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error validating feature: {str(e)}")

# Wisconsin Ensemble Training Endpoints
@router.post("/api/wisconsin/train-ensemble")
async def train_wisconsin_ensemble(
    user: User | None = Depends(get_current_user),
    session: Session = Depends(get_session)
):
    """Train the Wisconsin-optimized ensemble model"""
    if not user:
        raise HTTPException(status_code=401, detail="Not authenticated")
    
    try:
        # Download and prepare dataset
        df = wisconsin_analyzer.download_dataset()
        df_enhanced = wisconsin_analyzer.create_enhanced_features(df)
        
        # Prepare features and target
        X = df_enhanced.drop('diagnosis', axis=1)
        y = df_enhanced['diagnosis']
        
        # Train ensemble
        training_results = wisconsin_ensemble.train_ensemble(
            X.values, y.values, feature_names=X.columns.tolist()
        )
        
        # Evaluate on test set
        X_train, X_test, y_train, y_test = train_test_split(
            X.values, y.values, test_size=0.2, random_state=42, stratify=y.values
        )
        
        evaluation_results = wisconsin_ensemble.evaluate_ensemble(X_test, y_test)
        
        # Save models
        wisconsin_ensemble.save_models()
        
        return JSONResponse(content={
            "success": True,
            "message": "Wisconsin ensemble trained successfully",
            "training_results": training_results,
            "evaluation_results": evaluation_results,
            "dataset_info": {
                "total_samples": len(df),
                "features_used": len(X.columns),
                "enhanced_features": len(X.columns) - len(wisconsin_analyzer.feature_names)
            }
        })
        
    except Exception as e:
        return JSONResponse(
            status_code=500,
            content={
                "success": False,
                "message": f"Error training Wisconsin ensemble: {str(e)}"
            }
        )

@router.get("/api/wisconsin/ensemble-status")
async def get_wisconsin_ensemble_status():
    """Get status of Wisconsin ensemble models"""
    try:
        # Try to load existing models
        models_loaded = wisconsin_ensemble.load_models()
        
        return {
            "models_loaded": models_loaded,
            "trained_models": list(wisconsin_ensemble.trained_models.keys()),
            "model_count": len(wisconsin_ensemble.trained_models),
            "ensemble_weights": wisconsin_ensemble.ensemble_weights,
            "model_performance": wisconsin_ensemble.model_performance
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error checking ensemble status: {str(e)}")

# Wisconsin Prediction Endpoints
@router.post("/api/wisconsin/predict", response_model=WisconsinPredictionResponse)
async def predict_wisconsin_breast_cancer(
    request: WisconsinPredictionRequest,
    user: User | None = Depends(get_current_user),
    session: Session = Depends(get_session)
):
    """Make Wisconsin-optimized breast cancer prediction"""
    if not user:
        raise HTTPException(status_code=401, detail="Not authenticated")
    
    try:
        # Validate all features
        feature_validation = {}
        all_valid = True
        
        for feature_name, value in request.features.items():
            validation = wisconsin_analyzer.validate_feature_input(feature_name, value)
            feature_validation[feature_name] = validation
            if not validation['valid']:
                all_valid = False
        
        if not all_valid:
            return JSONResponse(
                status_code=400,
                content={
                    "error": "Invalid feature values",
                    "feature_validation": feature_validation
                }
            )
        
        # Check if ensemble is trained
        if not wisconsin_ensemble.trained_models:
            if not wisconsin_ensemble.load_models():
                raise HTTPException(
                    status_code=503, 
                    detail="Wisconsin ensemble not trained. Please train the model first."
                )
        
        # Prepare features in correct order
        feature_array = np.array([
            request.features.get(feature, 0.0) 
            for feature in wisconsin_analyzer.feature_names
        ]).reshape(1, -1)
        
        # Make prediction
        result = wisconsin_ensemble.predict_ensemble(
            feature_array, 
            return_individual=request.return_individual_predictions
        )
        
        # Determine risk level
        confidence = result['confidence'][0]
        prediction = result['prediction'][0]
        
        if prediction == 0:  # Benign
            if confidence > 0.9:
                risk_level = "Low"
            elif confidence > 0.7:
                risk_level = "Low-Medium"
            else:
                risk_level = "Medium"
        else:  # Malignant
            if confidence > 0.9:
                risk_level = "High"
            elif confidence > 0.7:
                risk_level = "Medium-High"
            else:
                risk_level = "Medium"
        
        # Save prediction to database
        prediction_record = BreastCancerPrediction(
            user_id=user.id,
            **request.features,
            prediction=result['prediction_label'][0],
            confidence=float(confidence),
            risk_level=risk_level
        )
        
        session.add(prediction_record)
        session.commit()
        
        response_data = {
            "prediction": result['prediction_label'][0],
            "confidence": float(confidence),
            "risk_level": risk_level,
            "probabilities": {
                "benign": float(result['probabilities'][0][0]),
                "malignant": float(result['probabilities'][0][1])
            },
            "feature_validation": feature_validation
        }
        
        if request.include_uncertainty:
            response_data["uncertainty"] = float(result['uncertainty'][0])
        
        if request.return_individual_predictions:
            response_data["individual_predictions"] = result['individual_predictions']
        
        return WisconsinPredictionResponse(**response_data)
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Prediction error: {str(e)}")

@router.get("/api/wisconsin/feature-importance")
async def get_wisconsin_feature_importance(
    user: User | None = Depends(get_current_user)
):
    """Get feature importance from Wisconsin ensemble models"""
    if not user:
        raise HTTPException(status_code=401, detail="Not authenticated")
    
    try:
        if not wisconsin_ensemble.trained_models:
            if not wisconsin_ensemble.load_models():
                raise HTTPException(
                    status_code=503, 
                    detail="Wisconsin ensemble not trained. Please train the model first."
                )
        
        importance = wisconsin_ensemble.get_feature_importance()
        
        # Group importance by feature type
        grouped_importance = {
            'mean_features': {},
            'se_features': {},
            'worst_features': {},
            'enhanced_features': {}
        }
        
        for model_name, model_importance in importance.items():
            for feature, imp in model_importance.items():
                if 'mean' in feature:
                    if feature not in grouped_importance['mean_features']:
                        grouped_importance['mean_features'][feature] = []
                    grouped_importance['mean_features'][feature].append(imp)
                elif 'se' in feature:
                    if feature not in grouped_importance['se_features']:
                        grouped_importance['se_features'][feature] = []
                    grouped_importance['se_features'][feature].append(imp)
                elif 'worst' in feature:
                    if feature not in grouped_importance['worst_features']:
                        grouped_importance['worst_features'][feature] = []
                    grouped_importance['worst_features'][feature].append(imp)
                else:
                    if feature not in grouped_importance['enhanced_features']:
                        grouped_importance['enhanced_features'][feature] = []
                    grouped_importance['enhanced_features'][feature].append(imp)
        
        # Average importance across models
        for group in grouped_importance:
            for feature in grouped_importance[group]:
                grouped_importance[group][feature] = np.mean(grouped_importance[group][feature])
        
        return {
            "individual_model_importance": importance,
            "grouped_importance": grouped_importance,
            "ensemble_weights": wisconsin_ensemble.ensemble_weights
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error getting feature importance: {str(e)}")

# Wisconsin Analytics Dashboard
@router.get("/wisconsin-analytics", response_class=HTMLResponse)
async def wisconsin_analytics_dashboard(
    request: Request,
    user: User | None = Depends(get_current_user),
    session: Session = Depends(get_session)
):
    """Wisconsin dataset analytics dashboard"""
    if not user:
        return RedirectResponse(url="/signup")
    
    try:
        # Get dataset statistics
        dataset_stats = wisconsin_analyzer.get_dataset_statistics()
        
        # Get ensemble status
        ensemble_status = wisconsin_ensemble.load_models()
        
        # Get user's recent predictions
        recent_predictions = session.exec(
            select(BreastCancerPrediction)
            .where(BreastCancerPrediction.user_id == user.id)
            .order_by(BreastCancerPrediction.created_at.desc())
            .limit(10)
        ).all()
        
        context = {
            "request": request,
            "user": user,
            "dataset_stats": dataset_stats,
            "ensemble_status": ensemble_status,
            "recent_predictions": [
                {
                    "prediction": pred.prediction,
                    "confidence": pred.confidence,
                    "risk_level": pred.risk_level,
                    "created_at": pred.created_at.strftime("%Y-%m-%d %H:%M")
                }
                for pred in recent_predictions
            ],
            "feature_groups": wisconsin_analyzer.feature_groups,
            "feature_descriptions": wisconsin_analyzer.feature_descriptions
        }
        
        return templates.TemplateResponse("wisconsin_analytics.html", context)
        
    except Exception as e:
        return templates.TemplateResponse("wisconsin_analytics.html", {
            "request": request,
            "user": user,
            "error": f"Error loading analytics: {str(e)}"
        })

# Wisconsin Enhanced Prediction Form
@router.get("/wisconsin-prediction", response_class=HTMLResponse)
async def wisconsin_prediction_form(
    request: Request,
    user: User | None = Depends(get_current_user)
):
    """Wisconsin-optimized prediction form"""
    if not user:
        return RedirectResponse(url="/signup")
    
    try:
        # Get feature information for the form
        feature_info = {}
        for feature in wisconsin_analyzer.feature_names:
            feature_info[feature] = {
                'description': wisconsin_analyzer.get_feature_description(feature),
                'range': wisconsin_analyzer.get_feature_range(feature),
                'group': 'mean' if 'mean' in feature else 'se' if 'se' in feature else 'worst'
            }
        
        context = {
            "request": request,
            "user": user,
            "feature_info": feature_info,
            "feature_groups": wisconsin_analyzer.feature_groups,
            "dataset_info": wisconsin_analyzer.get_dataset_statistics()
        }
        
        return templates.TemplateResponse("wisconsin_prediction.html", context)
        
    except Exception as e:
        return templates.TemplateResponse("wisconsin_prediction.html", {
            "request": request,
            "user": user,
            "error": f"Error loading form: {str(e)}"
        })

@router.post("/wisconsin-prediction")
async def submit_wisconsin_prediction(
    request: Request,
    user: User | None = Depends(get_current_user),
    session: Session = Depends(get_current_user)
):
    """Submit Wisconsin prediction form data"""
    if not user:
        return RedirectResponse(url="/signup")
    
    try:
        # Extract form data
        form_data = await request.form()
        
        # Convert form data to features dictionary
        features = {}
        validation_errors = []
        
        for feature_name in wisconsin_analyzer.feature_names:
            if feature_name in form_data:
                try:
                    value = float(form_data[feature_name])
                    validation = wisconsin_analyzer.validate_feature_input(feature_name, value)
                    
                    if validation['valid']:
                        features[feature_name] = value
                    else:
                        validation_errors.append(f"{feature_name}: {validation['message']}")
                        
                except ValueError:
                    validation_errors.append(f"{feature_name}: Invalid number format")
        
        if validation_errors:
            return templates.TemplateResponse("wisconsin_prediction.html", {
                "request": request,
                "user": user,
                "validation_errors": validation_errors,
                "form_data": dict(form_data)
            })
        
        # Make prediction using the API
        prediction_request = WisconsinPredictionRequest(
            features=features,
            include_uncertainty=True,
            return_individual_predictions=False
        )
        
        # Call the prediction endpoint
        prediction_result = await predict_wisconsin_breast_cancer(
            prediction_request, user, session
        )
        
        return templates.TemplateResponse("wisconsin_prediction.html", {
            "request": request,
            "user": user,
            "prediction_result": prediction_result.dict(),
            "success": "Prediction completed successfully"
        })
        
    except Exception as e:
        return templates.TemplateResponse("wisconsin_prediction.html", {
            "request": request,
            "user": user,
            "error": f"Prediction error: {str(e)}"
        })
