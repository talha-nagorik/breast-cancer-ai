from fastapi import APIRouter, Request, Form, Depends, HTTPException
from fastapi.responses import HTMLResponse, RedirectResponse, JSONResponse
from fastapi.templating import Jinja2Templates
from sqlmodel import Session, select
from pydantic import BaseModel
from typing import Dict, List
import json

from ..models.models import User, BreastCancerPrediction
from ..database.database import get_session
from ..dependencies import get_current_user
from ..ml.breast_cancer_model import predictor

router = APIRouter()
templates = Jinja2Templates(directory="templates")

class PredictionRequest(BaseModel):
    features: Dict[str, float]

class PredictionResponse(BaseModel):
    prediction: str
    confidence: float
    risk_level: str
    probabilities: Dict[str, float]

# Train model endpoint (admin only)
@router.post("/api/train-model")
async def train_model(
    user: User | None = Depends(get_current_user),
    session: Session = Depends(get_session)
):
    """Train the breast cancer prediction model"""
    if not user:
        raise HTTPException(status_code=401, detail="Not authenticated")
    
    # For now, allow any authenticated user to train the model
    # In production, you might want to restrict this to admin users
    
    try:
        results = predictor.train_model()
        return JSONResponse(content={
            "success": True,
            "message": "Model trained successfully",
            "results": results
        })
    except Exception as e:
        return JSONResponse(
            status_code=500,
            content={
                "success": False,
                "message": f"Error training model: {str(e)}"
            }
        )

# Prediction endpoint
@router.post("/api/predict", response_model=PredictionResponse)
async def predict_breast_cancer(
    request: PredictionRequest,
    user: User | None = Depends(get_current_user),
    session: Session = Depends(get_session)
):
    """Make a breast cancer prediction"""
    if not user:
        raise HTTPException(status_code=401, detail="Not authenticated")
    
    try:
        # Make prediction
        result = predictor.predict(request.features)
        
        # Save prediction to database
        prediction_record = BreastCancerPrediction(
            user_id=user.id,
            **request.features,
            prediction=result["prediction"],
            confidence=result["confidence"],
            risk_level=result["risk_level"]
        )
        
        session.add(prediction_record)
        session.commit()
        
        return PredictionResponse(**result)
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Prediction error: {str(e)}")

# Get user's prediction history
@router.get("/api/predictions")
async def get_predictions(
    user: User | None = Depends(get_current_user),
    session: Session = Depends(get_session)
):
    """Get user's prediction history"""
    if not user:
        raise HTTPException(status_code=401, detail="Not authenticated")
    
    predictions = session.exec(
        select(BreastCancerPrediction)
        .where(BreastCancerPrediction.user_id == user.id)
        .order_by(BreastCancerPrediction.created_at.desc())
    ).all()
    
    return [
        {
            "id": pred.id,
            "prediction": pred.prediction,
            "confidence": pred.confidence,
            "risk_level": pred.risk_level,
            "created_at": pred.created_at.isoformat(),
            "notes": pred.notes
        }
        for pred in predictions
    ]

# Get feature importance
@router.get("/api/feature-importance")
async def get_feature_importance(
    user: User | None = Depends(get_current_user)
):
    """Get feature importance from the trained model"""
    if not user:
        raise HTTPException(status_code=401, detail="Not authenticated")
    
    try:
        importance = predictor.get_feature_importance()
        return JSONResponse(content=importance)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error getting feature importance: {str(e)}")

# Breast cancer analysis page
@router.get("/breast-cancer-analysis", response_class=HTMLResponse)
async def breast_cancer_analysis(
    request: Request,
    user: User | None = Depends(get_current_user),
    session: Session = Depends(get_session)
):
    """Breast cancer analysis page"""
    if not user:
        return RedirectResponse(url="/signup")
    
    # Get user's recent predictions
    recent_predictions = session.exec(
        select(BreastCancerPrediction)
        .where(BreastCancerPrediction.user_id == user.id)
        .order_by(BreastCancerPrediction.created_at.desc())
        .limit(5)
    ).all()
    
    context = {
        "request": request,
        "user": user,
        "recent_predictions": [
            {
                "prediction": pred.prediction,
                "confidence": pred.confidence,
                "risk_level": pred.risk_level,
                "created_at": pred.created_at.strftime("%Y-%m-%d %H:%M")
            }
            for pred in recent_predictions
        ]
    }
    
    return templates.TemplateResponse("breast_cancer_analysis.html", context)

# Submit prediction form
@router.post("/submit-prediction")
async def submit_prediction(
    request: Request,
    user: User | None = Depends(get_current_user),
    session: Session = Depends(get_session)
):
    """Submit prediction form data"""
    if not user:
        return RedirectResponse(url="/signup")
    
    # Extract form data (you'll need to create the form fields)
    form_data = await request.form()
    
    # Convert form data to features dictionary
    features = {}
    for field_name in predictor.feature_names:
        if field_name in form_data:
            try:
                features[field_name] = float(form_data[field_name])
            except ValueError:
                return templates.TemplateResponse("breast_cancer_analysis.html", {
                    "request": request,
                    "user": user,
                    "error": f"Invalid value for {field_name}"
                })
    
    # Make prediction
    try:
        result = predictor.predict(features)
        
        # Save to database
        prediction_record = BreastCancerPrediction(
            user_id=user.id,
            **features,
            prediction=result["prediction"],
            confidence=result["confidence"],
            risk_level=result["risk_level"]
        )
        
        session.add(prediction_record)
        session.commit()
        
        return templates.TemplateResponse("breast_cancer_analysis.html", {
            "request": request,
            "user": user,
            "prediction_result": result,
            "success": "Prediction completed successfully"
        })
        
    except Exception as e:
        return templates.TemplateResponse("breast_cancer_analysis.html", {
            "request": request,
            "user": user,
            "error": f"Prediction error: {str(e)}"
        })
