/**
 * Professional Form Handler - Handles form submissions with retry logic and error handling
 * Depends on: form-validator.js
 */

class ProfessionalFormHandler {
    constructor() {
        this.validator = new FormValidator();
        this.retryAttempts = 3;
        this.retryDelay = 1000;
        this.timeout = 30000; // 30 seconds
    }
    
    async submitForm(formData, url, options = {}) {
        const {
            method = 'POST',
            headers = {},
            retryAttempts = this.retryAttempts,
            timeout = this.timeout,
            onProgress = null,
            onSuccess = null,
            onError = null
        } = options;
        
        let attempt = 0;
        
        while (attempt < retryAttempts) {
            try {
                const controller = new AbortController();
                const timeoutId = setTimeout(() => controller.abort(), timeout);
                
                const response = await fetch(url, {
                    method,
                    headers: {
                        'Content-Type': 'application/json',
                        'X-Requested-With': 'XMLHttpRequest',
                        ...headers
                    },
                    body: JSON.stringify(formData),
                    signal: controller.signal
                });
                
                clearTimeout(timeoutId);
                
                if (response.ok) {
                    const result = await response.json();
                    if (onSuccess) onSuccess(result);
                    return { success: true, data: result };
                } else {
                    const errorData = await response.json().catch(() => ({ message: 'Unknown error occurred' }));
                    if (onError) onError(errorData);
                    return { success: false, error: errorData };
                }
            } catch (error) {
                attempt++;
                
                if (error.name === 'AbortError') {
                    const errorMsg = { message: 'Request timeout. Please try again.' };
                    if (onError) onError(errorMsg);
                    return { success: false, error: errorMsg };
                }
                
                if (attempt >= retryAttempts) {
                    const errorMsg = { message: 'Network error. Please check your connection and try again.' };
                    if (onError) onError(errorMsg);
                    return { success: false, error: errorMsg };
                }
                
                // Wait before retry
                await new Promise(resolve => setTimeout(resolve, this.retryDelay * attempt));
            }
        }
    }
    
    validateField(field, value, rules) {
        return this.validator.validate(field, value, rules);
    }
}

// Export for use in other modules
window.ProfessionalFormHandler = ProfessionalFormHandler;
