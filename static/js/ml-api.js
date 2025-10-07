/**
 * ML API Integration - Breast Cancer Analysis
 */

// Simple fetch wrapper
async function apiRequest(url, options = {}) {
    const defaultOptions = {
        headers: {
            'Content-Type': 'application/json',
        },
    };

    const config = { ...defaultOptions, ...options };

    try {
        const response = await fetch(url, config);
        const data = await response.json();

        if (!response.ok) {
            throw new Error(data.message || 'An error occurred');
        }

        return data;
    } catch (error) {
        console.error('API request failed:', error);
        throw error;
    }
}

const mlAPI = {
    // Train the model
    trainModel: async function() {
        try {
            const response = await apiRequest('/ml/api/train-model', {
                method: 'POST',
                body: JSON.stringify({})
            });
            return response;
        } catch (error) {
            console.error('Model training failed:', error);
            throw error;
        }
    },

    // Make prediction via JSON API
    predict: async function(features) {
        try {
            const response = await apiRequest('/ml/api/predict', {
                method: 'POST',
                body: JSON.stringify({ features })
            });
            return response;
        } catch (error) {
            console.error('Prediction failed:', error);
            throw error;
        }
    },

    // Get user's prediction history
    getPredictions: async function() {
        try {
            const response = await apiRequest('/ml/api/predictions', {
                method: 'GET'
            });
            return response;
        } catch (error) {
            console.error('Failed to fetch predictions:', error);
            throw error;
        }
    },

    // Get feature importance
    getFeatureImportance: async function() {
        try {
            const response = await apiRequest('/ml/api/feature-importance', {
                method: 'GET'
            });
            return response;
        } catch (error) {
            console.error('Failed to fetch feature importance:', error);
            throw error;
        }
    },

    // Convert form data to features object
    formToFeatures: function(formData) {
        const features = {};
        const featureNames = [
            'radius_mean', 'texture_mean', 'perimeter_mean', 'area_mean',
            'smoothness_mean', 'compactness_mean', 'concavity_mean', 'concave_points_mean',
            'symmetry_mean', 'fractal_dimension_mean',
            'radius_se', 'texture_se', 'perimeter_se', 'area_se',
            'smoothness_se', 'compactness_se', 'concavity_se', 'concave_points_se',
            'symmetry_se', 'fractal_dimension_se',
            'radius_worst', 'texture_worst', 'perimeter_worst', 'area_worst',
            'smoothness_worst', 'compactness_worst', 'concavity_worst', 'concave_points_worst',
            'symmetry_worst', 'fractal_dimension_worst'
        ];

        featureNames.forEach(feature => {
            const value = formData.get(feature);
            if (value !== null && value !== '') {
                features[feature] = parseFloat(value);
            }
        });

        return features;
    }
};

// Export for use in other modules
window.BreastCareAI = window.BreastCareAI || {};
window.BreastCareAI.mlAPI = mlAPI;
