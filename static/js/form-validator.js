/**
 * Form Validator - Professional validation system
 * Handles all form validation rules and error messages
 */

class FormValidator {
    constructor() {
        this.rules = {
            required: (value) => value && value.trim().length > 0,
            email: (value) => /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(value),
            minLength: (value, min) => value && value.length >= min,
            maxLength: (value, max) => !value || value.length <= max,
            password: (value) => /^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]/.test(value),
            phone: (value) => /^[\+]?[1-9][\d]{0,15}$/.test(value.replace(/[\s\-\(\)]/g, '')),
            url: (value) => /^https?:\/\/.+/.test(value),
            numeric: (value) => !isNaN(value) && !isNaN(parseFloat(value)),
            date: (value) => !isNaN(Date.parse(value)),
            match: (value, target) => value === target
        };
        
        this.messages = {
            required: 'This field is required',
            email: 'Please enter a valid email address',
            minLength: (min) => `Must be at least ${min} characters`,
            maxLength: (max) => `Must be no more than ${max} characters`,
            password: 'Password must contain at least one uppercase letter, one lowercase letter, one number, and one special character',
            phone: 'Please enter a valid phone number',
            url: 'Please enter a valid URL',
            numeric: 'Please enter a valid number',
            date: 'Please enter a valid date',
            match: 'Values do not match'
        };
    }
    
    validate(field, value, rules) {
        const errors = [];
        
        for (const [rule, param] of Object.entries(rules)) {
            if (this.rules[rule]) {
                const isValid = this.rules[rule](value, param);
                if (!isValid) {
                    const message = typeof this.messages[rule] === 'function' 
                        ? this.messages[rule](param) 
                        : this.messages[rule];
                    errors.push(message);
                }
            }
        }
        
        return errors;
    }
}

// Export for use in other modules
window.FormValidator = FormValidator;
