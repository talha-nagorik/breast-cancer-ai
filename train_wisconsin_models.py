#!/usr/bin/env python3
"""
Wisconsin Breast Cancer Dataset Training Pipeline
Complete training script for Wisconsin-optimized ensemble models
"""

import sys
import os
import argparse
import json
from datetime import datetime
from pathlib import Path

# Add the app directory to the Python path
sys.path.append(str(Path(__file__).parent / "app"))

from ml.wisconsin_analyzer import wisconsin_analyzer
from ml.wisconsin_ensemble import wisconsin_ensemble
from sklearn.model_selection import train_test_split
import numpy as np

def main():
    parser = argparse.ArgumentParser(description='Train Wisconsin Breast Cancer Ensemble Models')
    parser.add_argument('--output-dir', default='models', help='Output directory for trained models')
    parser.add_argument('--test-size', type=float, default=0.2, help='Test set size (default: 0.2)')
    parser.add_argument('--random-state', type=int, default=42, help='Random state for reproducibility')
    parser.add_argument('--hyperparameter-tuning', action='store_true', help='Perform hyperparameter tuning')
    parser.add_argument('--verbose', action='store_true', help='Verbose output')
    
    args = parser.parse_args()
    
    print("=" * 60)
    print("WISCONSIN BREAST CANCER DATASET TRAINING PIPELINE")
    print("=" * 60)
    print(f"Started at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"Output directory: {args.output_dir}")
    print(f"Test size: {args.test_size}")
    print(f"Random state: {args.random_state}")
    print()
    
    try:
        # Step 1: Load and analyze dataset
        print("Step 1: Loading Wisconsin Breast Cancer Dataset...")
        df = wisconsin_analyzer.download_dataset()
        print(f"✓ Dataset loaded: {len(df)} samples, {len(df.columns)-1} features")
        
        # Get dataset statistics
        stats = wisconsin_analyzer.get_dataset_statistics()
        print(f"✓ Class distribution: {stats['class_distribution']['benign_samples']} benign, {stats['class_distribution']['malignant_samples']} malignant")
        print()
        
        # Step 2: Enhanced feature engineering
        print("Step 2: Applying enhanced feature engineering...")
        df_enhanced = wisconsin_analyzer.create_enhanced_features(df)
        print(f"✓ Enhanced features created: {len(df_enhanced.columns)-1} total features")
        print(f"✓ Added {len(df_enhanced.columns) - len(df.columns)} new features")
        print()
        
        # Step 3: Prepare data
        print("Step 3: Preparing data for training...")
        X = df_enhanced.drop('diagnosis', axis=1)
        y = df_enhanced['diagnosis']
        
        # Split data
        X_train, X_test, y_train, y_test = train_test_split(
            X.values, y.values, 
            test_size=args.test_size, 
            random_state=args.random_state, 
            stratify=y.values
        )
        
        print(f"✓ Training set: {X_train.shape[0]} samples")
        print(f"✓ Test set: {X_test.shape[0]} samples")
        print(f"✓ Features: {X_train.shape[1]}")
        print()
        
        # Step 4: Train ensemble
        print("Step 4: Training Wisconsin-optimized ensemble...")
        training_results = wisconsin_ensemble.train_ensemble(
            X_train, y_train, 
            feature_names=X.columns.tolist()
        )
        
        print(f"✓ Trained {training_results['trained_models']} models")
        print("✓ Model performance:")
        for model_name, performance in training_results['model_performance'].items():
            print(f"  - {model_name}: {performance['mean_accuracy']:.4f} ± {performance['std_accuracy']:.4f}")
        print()
        
        # Step 5: Hyperparameter tuning (optional)
        if args.hyperparameter_tuning:
            print("Step 5: Performing hyperparameter tuning...")
            tuning_results = {}
            
            # Tune key models
            models_to_tune = ['random_forest', 'gradient_boosting', 'svm_rbf']
            for model_name in models_to_tune:
                if model_name in wisconsin_ensemble.models:
                    print(f"  Tuning {model_name}...")
                    try:
                        result = wisconsin_ensemble.hyperparameter_tuning(
                            X_train, y_train, model_name
                        )
                        tuning_results[model_name] = result
                        print(f"    Best score: {result['best_score']:.4f}")
                        print(f"    Best params: {result['best_params']}")
                    except Exception as e:
                        print(f"    Error tuning {model_name}: {e}")
            
            print("✓ Hyperparameter tuning completed")
            print()
        
        # Step 6: Evaluate ensemble
        print("Step 6: Evaluating ensemble performance...")
        evaluation_results = wisconsin_ensemble.evaluate_ensemble(X_test, y_test)
        
        print(f"✓ Ensemble accuracy: {evaluation_results['ensemble_accuracy']:.4f}")
        print(f"✓ Ensemble ROC AUC: {evaluation_results['ensemble_roc_auc']:.4f}")
        print(f"✓ Average confidence: {evaluation_results['average_confidence']:.4f}")
        print(f"✓ Average uncertainty: {evaluation_results['average_uncertainty']:.4f}")
        print()
        
        # Step 7: Save models
        print("Step 7: Saving trained models...")
        os.makedirs(args.output_dir, exist_ok=True)
        wisconsin_ensemble.save_models(args.output_dir)
        print(f"✓ Models saved to {args.output_dir}")
        print()
        
        # Step 8: Generate training report
        print("Step 8: Generating training report...")
        report = {
            'training_info': {
                'timestamp': datetime.now().isoformat(),
                'dataset_info': stats['dataset_info'],
                'class_distribution': stats['class_distribution'],
                'feature_groups': stats['feature_groups']
            },
            'data_preparation': {
                'original_features': len(df.columns) - 1,
                'enhanced_features': len(df_enhanced.columns) - 1,
                'training_samples': X_train.shape[0],
                'test_samples': X_test.shape[0],
                'feature_names': X.columns.tolist()
            },
            'model_performance': training_results['model_performance'],
            'ensemble_evaluation': evaluation_results,
            'ensemble_weights': training_results['ensemble_weights']
        }
        
        if args.hyperparameter_tuning and 'tuning_results' in locals():
            report['hyperparameter_tuning'] = tuning_results
        
        # Save report
        report_path = os.path.join(args.output_dir, 'training_report.json')
        with open(report_path, 'w') as f:
            json.dump(report, f, indent=2, default=str)
        
        print(f"✓ Training report saved to {report_path}")
        print()
        
        # Step 9: Feature importance analysis
        print("Step 9: Analyzing feature importance...")
        feature_importance = wisconsin_ensemble.get_feature_importance()
        
        # Save feature importance
        importance_path = os.path.join(args.output_dir, 'feature_importance.json')
        with open(importance_path, 'w') as f:
            json.dump(feature_importance, f, indent=2, default=str)
        
        print(f"✓ Feature importance saved to {importance_path}")
        print()
        
        # Final summary
        print("=" * 60)
        print("TRAINING COMPLETED SUCCESSFULLY!")
        print("=" * 60)
        print(f"Final ensemble accuracy: {evaluation_results['ensemble_accuracy']:.4f}")
        print(f"Models trained: {training_results['trained_models']}")
        print(f"Output directory: {args.output_dir}")
        print(f"Completed at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print()
        
        if args.verbose:
            print("DETAILED RESULTS:")
            print("-" * 40)
            print("Individual Model Performance:")
            for model_name, performance in training_results['model_performance'].items():
                print(f"  {model_name}: {performance['mean_accuracy']:.4f} ± {performance['std_accuracy']:.4f}")
            
            print("\nEnsemble Weights:")
            for model_name, weight in training_results['ensemble_weights'].items():
                print(f"  {model_name}: {weight:.4f}")
            
            print(f"\nClassification Report:")
            print(evaluation_results['classification_report'])
        
        return 0
        
    except Exception as e:
        print(f"\n❌ Training failed with error: {e}")
        if args.verbose:
            import traceback
            traceback.print_exc()
        return 1

if __name__ == "__main__":
    exit_code = main()
    sys.exit(exit_code)
