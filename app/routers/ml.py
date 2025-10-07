from fastapi import APIRouter, Request, Depends, HTTPException
from fastapi.responses import HTMLResponse, RedirectResponse, JSONResponse
from fastapi.templating import Jinja2Templates
from sqlmodel import Session, select
from pydantic import BaseModel

from ..models.models import User, BreastCancerPrediction
from ..database.database import get_session
from ..dependencies import get_current_user
from ..ml.breast_cancer_model import predictor

router = APIRouter(
    prefix="/ml",
    tags=["Machine Learning"],
    responses={404: {"description": "Not found"}}
)
templates = Jinja2Templates(directory="templates")


class PredictionRequest(BaseModel):
    features: dict[str, float]


class PredictionResponse(BaseModel):
    prediction: str
    confidence: float
    risk_level: str
    probabilities: dict[str, float]

# Train model endpoint (admin only)


@router.post("/api/train-model",
             summary="Train Breast Cancer Model",
             description="Train the breast cancer prediction model using the Wisconsin dataset")
async def train_model(
    user: User | None = Depends(get_current_user),
    session: Session = Depends(get_session)
):
    """
    Train the breast cancer prediction model.

    Trains a Random Forest classifier on the Wisconsin Breast Cancer Dataset.
    Downloads the dataset, trains the model, and saves it for future predictions.

    Requires authentication.
    """
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


@router.post("/api/predict",
             response_model=PredictionResponse,
             summary="Make Breast Cancer Prediction",
             description="Make a breast cancer prediction using the trained model")
async def predict_breast_cancer(
    request: PredictionRequest,
    user: User | None = Depends(get_current_user),
    session: Session = Depends(get_session)
):
    """
    Make a breast cancer prediction.

    Uses the trained model to predict breast cancer diagnosis based on
    Wisconsin dataset features. Returns prediction with confidence scores
    and risk assessment.

    Requires authentication and trained model.
    """
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
        raise HTTPException(
            status_code=500, detail=f"Prediction error: {str(e)}")

# Get user's prediction history


@router.get("/api/predictions",
            summary="Get User Predictions",
            description="Get the authenticated user's breast cancer prediction history")
async def get_predictions(
    user: User | None = Depends(get_current_user),
    session: Session = Depends(get_session)
):
    """
    Get user's prediction history.

    Returns a list of all breast cancer predictions made by the authenticated user,
    including prediction results, confidence scores, and timestamps.

    Requires authentication.
    """
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


@router.get("/api/feature-importance",
            summary="Get Feature Importance",
            description="Get feature importance analysis from the trained breast cancer model")
async def get_feature_importance(
    user: User | None = Depends(get_current_user)
):
    """
    Get feature importance from the trained model.

    Returns feature importance scores from the trained Random Forest model,
    showing which features are most important for breast cancer prediction.

    Requires authentication and trained model.
    """
    if not user:
        raise HTTPException(status_code=401, detail="Not authenticated")

    try:
        importance = predictor.get_feature_importance()
        return JSONResponse(content=importance)
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Error getting feature importance: {str(e)}")

# Breast cancer analysis page


@router.get("/breast-cancer-analysis",
            response_class=HTMLResponse,
            summary="Breast Cancer Analysis Page",
            description="Interactive page for breast cancer analysis and predictions",
            name="breast_cancer_analysis")
async def breast_cancer_analysis(
    request: Request,
    user: User | None = Depends(get_current_user),
    session: Session = Depends(get_session)
):
    """
    Breast cancer analysis page.

    Provides an interactive interface for breast cancer analysis including
    prediction forms, feature importance visualization, and prediction history.
    """
    if not user:
        return RedirectResponse(url="/users/signup")

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


@router.post("/submit-prediction",
             summary="Submit Prediction Form",
             description="Submit breast cancer prediction form data and get analysis results")
async def submit_prediction(
    request: Request,
    user: User | None = Depends(get_current_user),
    session: Session = Depends(get_session)
):
    """
    Submit prediction form data.

    Processes form data from the breast cancer prediction form, validates features,
    makes predictions using the trained model, and returns results.
    """
    if not user:
        return RedirectResponse(url="/users/signup")

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
