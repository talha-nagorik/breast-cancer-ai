// Common JavaScript functionality for BreastCare AI with Alpine.js integration

// Alpine.js components and utilities
document.addEventListener('alpine:init', () => {
    // Form handling component
    Alpine.data('formHandler', () => ({
        loading: false,
        errors: {},
        formData: {
            email: '',
            password: '',
            name: '',
            confirmPassword: ''
        },
        
        async handleLogin() {
            // Validate all fields
            const emailValid = this.validateField('email', this.formData.email, { required: true, email: true });
            const passwordValid = this.validateField('password', this.formData.password, { required: true, minLength: 6 });
            
            if (!emailValid || !passwordValid) {
                return;
            }
            
            this.loading = true;
            
            try {
                const formData = new FormData();
                formData.append('email', this.formData.email);
                formData.append('password', this.formData.password);
                
                const response = await fetch('/login', {
                    method: 'POST',
                    body: formData
                });
                
                if (response.ok) {
                    // Redirect to dashboard on successful login
                    window.location.href = '/dashboard';
                } else {
                    const result = await response.text();
                    this.showNotification('Login failed. Please check your credentials.', 'error');
                }
            } catch (error) {
                this.showNotification('Network error occurred', 'error');
            } finally {
                this.loading = false;
            }
        },
        
        async submitForm(formData, url, method = 'POST') {
            this.loading = true;
            this.errors = {};
            
            try {
                const response = await fetch(url, {
                    method: method,
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify(formData)
                });
                
                const result = await response.json();
                
                if (!response.ok) {
                    if (result.errors) {
                        this.errors = result.errors;
                    } else {
                        this.showNotification(result.message || 'An error occurred', 'error');
                    }
                    return false;
                }
                
                this.showNotification(result.message || 'Success!', 'success');
                return result;
            } catch (error) {
                this.showNotification('Network error occurred', 'error');
                return false;
            } finally {
                this.loading = false;
            }
        },
        
        validateField(field, value, rules = {}) {
            const errors = [];
            
            if (rules.required && !value.trim()) {
                errors.push('This field is required');
            }
            
            if (rules.email && value && !this.isValidEmail(value)) {
                errors.push('Please enter a valid email address');
            }
            
            if (rules.minLength && value && value.length < rules.minLength) {
                errors.push(`Must be at least ${rules.minLength} characters`);
            }
            
            if (rules.match && value !== rules.match) {
                errors.push('Values do not match');
            }
            
            if (errors.length > 0) {
                this.errors[field] = errors[0];
            } else {
                delete this.errors[field];
            }
            
            return errors.length === 0;
        },
        
        isValidEmail(email) {
            const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
            return emailRegex.test(email);
        },
        
        showNotification(message, type = 'info') {
            // Use the existing notification system
            if (window.BreastCareAI && window.BreastCareAI.utils) {
                window.BreastCareAI.utils.showNotification(message, type);
            }
        }
    }));
    
    // Notification component
    Alpine.data('notifications', () => ({
        notifications: [],
        
        add(message, type = 'info', duration = 5000) {
            const id = Date.now();
            this.notifications.push({ id, message, type });
            
            setTimeout(() => {
                this.remove(id);
            }, duration);
        },
        
        remove(id) {
            this.notifications = this.notifications.filter(n => n.id !== id);
        }
    }));
    
    // Smooth scrolling component
    Alpine.data('smoothScroll', () => ({
        scrollTo(target) {
            const element = document.querySelector(target);
            if (element) {
                element.scrollIntoView({
                    behavior: 'smooth',
                    block: 'start'
                });
            }
        }
    }));
    
    // Fade-in animation component
    Alpine.data('fadeIn', () => ({
        visible: false,
        
        init() {
            const observer = new IntersectionObserver((entries) => {
                entries.forEach(entry => {
                    if (entry.isIntersecting) {
                        this.visible = true;
                        observer.unobserve(entry.target);
                    }
                });
            }, {
                threshold: 0.1,
                rootMargin: '0px 0px -50px 0px'
            });
            
            observer.observe(this.$el);
        }
    }));
    
    // Medical record form component
    Alpine.data('recordForm', () => ({
        loading: false,
        errors: {},
        formData: {
            date: '',
            type: '',
            doctor: '',
            status: '',
            notes: ''
        },
        
        async handleSubmit() {
            // Validate all fields
            const dateValid = this.validateField('date', this.formData.date, { required: true });
            const typeValid = this.validateField('type', this.formData.type, { required: true });
            const doctorValid = this.validateField('doctor', this.formData.doctor, { required: true });
            const statusValid = this.validateField('status', this.formData.status, { required: true });
            
            if (!dateValid || !typeValid || !doctorValid || !statusValid) {
                return;
            }
            
            this.loading = true;
            
            try {
                const formData = new FormData();
                formData.append('date', this.formData.date);
                formData.append('type', this.formData.type);
                formData.append('doctor', this.formData.doctor);
                formData.append('status', this.formData.status);
                formData.append('notes', this.formData.notes);
                
                const response = await fetch('/add_record', {
                    method: 'POST',
                    body: formData
                });
                
                if (response.ok) {
                    this.showNotification('Record added successfully!', 'success');
                    this.resetForm();
                    // Optionally reload the page to show the new record
                    setTimeout(() => window.location.reload(), 1000);
                } else {
                    this.showNotification('Failed to add record. Please try again.', 'error');
                }
            } catch (error) {
                this.showNotification('Network error occurred', 'error');
            } finally {
                this.loading = false;
            }
        },
        
        resetForm() {
            this.formData = {
                date: '',
                type: '',
                doctor: '',
                status: '',
                notes: ''
            };
            this.errors = {};
        },
        
        validateField(field, value, rules = {}) {
            const errors = [];
            
            if (rules.required && !value.trim()) {
                errors.push('This field is required');
            }
            
            if (errors.length > 0) {
                this.errors[field] = errors[0];
            } else {
                delete this.errors[field];
            }
            
            return errors.length === 0;
        },
        
        showNotification(message, type = 'info') {
            // Use the existing notification system
            if (window.BreastCareAI && window.BreastCareAI.utils) {
                window.BreastCareAI.utils.showNotification(message, type);
            }
        }
    }));
    
    // Signup form component
    Alpine.data('signupForm', () => ({
        loading: false,
        errors: {},
        formData: {
            full_name: '',
            email: '',
            password: '',
            confirm_password: ''
        },
        
        async handleSubmit() {
            // Validate all fields
            const nameValid = this.validateField('full_name', this.formData.full_name, { required: true });
            const emailValid = this.validateField('email', this.formData.email, { required: true, email: true });
            const passwordValid = this.validateField('password', this.formData.password, { required: true, minLength: 6 });
            const confirmValid = this.validateField('confirm_password', this.formData.confirm_password, { required: true, match: this.formData.password });
            
            if (!nameValid || !emailValid || !passwordValid || !confirmValid) {
                return;
            }
            
            this.loading = true;
            
            try {
                const formData = new FormData();
                formData.append('full_name', this.formData.full_name);
                formData.append('email', this.formData.email);
                formData.append('password', this.formData.password);
                formData.append('confirm_password', this.formData.confirm_password);
                
                const response = await fetch('/signup', {
                    method: 'POST',
                    body: formData
                });
                
                if (response.ok) {
                    this.showNotification('Account created successfully!', 'success');
                    setTimeout(() => window.location.href = '/login', 1000);
                } else {
                    this.showNotification('Failed to create account. Please try again.', 'error');
                }
            } catch (error) {
                this.showNotification('Network error occurred', 'error');
            } finally {
                this.loading = false;
            }
        },
        
        validateField(field, value, rules = {}) {
            const errors = [];
            
            if (rules.required && !value.trim()) {
                errors.push('This field is required');
            }
            
            if (rules.email && value && !this.isValidEmail(value)) {
                errors.push('Please enter a valid email address');
            }
            
            if (rules.minLength && value && value.length < rules.minLength) {
                errors.push(`Must be at least ${rules.minLength} characters`);
            }
            
            if (rules.match && value !== rules.match) {
                errors.push('Values do not match');
            }
            
            if (errors.length > 0) {
                this.errors[field] = errors[0];
            } else {
                delete this.errors[field];
            }
            
            return errors.length === 0;
        },
        
        isValidEmail(email) {
            const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
            return emailRegex.test(email);
        },
        
        showNotification(message, type = 'info') {
            // Use the existing notification system
            if (window.BreastCareAI && window.BreastCareAI.utils) {
                window.BreastCareAI.utils.showNotification(message, type);
            }
        }
    }));
});

// Legacy support for existing functionality
document.addEventListener('DOMContentLoaded', function() {
    // Add smooth scrolling for navigation links (fallback)
    document.querySelectorAll('a[href^="#"]').forEach((anchor) => {
        anchor.addEventListener("click", function (e) {
            e.preventDefault();
            const target = document.querySelector(this.getAttribute("href"));
            if (target) {
                target.scrollIntoView({
                    behavior: "smooth",
                });
            }
        });
    });

    // Add fade-in animation to elements (fallback)
    const observerOptions = {
        threshold: 0.1,
        rootMargin: '0px 0px -50px 0px'
    };

    const observer = new IntersectionObserver(function(entries) {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.style.opacity = '1';
                entry.target.style.transform = 'translateY(0)';
            }
        });
    }, observerOptions);

    // Observe elements with fade-in class
    document.querySelectorAll('.fade-in').forEach(el => {
        el.style.opacity = '0';
        el.style.transform = 'translateY(20px)';
        el.style.transition = 'opacity 0.6s ease, transform 0.6s ease';
        observer.observe(el);
    });
});

// Utility functions
const utils = {
    // Format date
    formatDate: function(date) {
        return new Date(date).toLocaleDateString('en-US', {
            year: 'numeric',
            month: 'long',
            day: 'numeric'
        });
    },

    // Show notification
    showNotification: function(message, type = 'info') {
        const notification = document.createElement('div');
        notification.className = `notification notification-${type}`;
        notification.textContent = message;
        
        // Style the notification
        notification.style.cssText = `
            position: fixed;
            top: 20px;
            right: 20px;
            padding: 1rem 1.5rem;
            border-radius: 8px;
            color: white;
            font-weight: 500;
            z-index: 10000;
            transform: translateX(100%);
            transition: transform 0.3s ease;
        `;

        // Set background color based on type
        const colors = {
            success: '#10b981',
            error: '#ef4444',
            warning: '#f59e0b',
            info: '#3b82f6'
        };
        notification.style.backgroundColor = colors[type] || colors.info;

        document.body.appendChild(notification);

        // Animate in
        setTimeout(() => {
            notification.style.transform = 'translateX(0)';
        }, 100);

        // Remove after 5 seconds
        setTimeout(() => {
            notification.style.transform = 'translateX(100%)';
            setTimeout(() => {
                document.body.removeChild(notification);
            }, 300);
        }, 5000);
    },

    // Validate email
    isValidEmail: function(email) {
        const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
        return emailRegex.test(email);
    },

    // Debounce function
    debounce: function(func, wait) {
        let timeout;
        return function executedFunction(...args) {
            const later = () => {
                clearTimeout(timeout);
                func(...args);
            };
            clearTimeout(timeout);
            timeout = setTimeout(later, wait);
        };
    }
};

// Form validation helpers
const formValidation = {
    // Show field error
    showError: function(input, message) {
        const errorElement = input.parentNode.querySelector('.error-message');
        if (errorElement) {
            errorElement.textContent = message;
            errorElement.style.display = 'block';
        }
        input.classList.add('error');
    },

    // Clear field error
    clearError: function(input) {
        const errorElement = input.parentNode.querySelector('.error-message');
        if (errorElement) {
            errorElement.style.display = 'none';
        }
        input.classList.remove('error');
    },

    // Validate required field
    validateRequired: function(input) {
        if (!input.value.trim()) {
            this.showError(input, 'This field is required');
            return false;
        }
        this.clearError(input);
        return true;
    },

    // Validate email field
    validateEmail: function(input) {
        if (input.value && !utils.isValidEmail(input.value)) {
            this.showError(input, 'Please enter a valid email address');
            return false;
        }
        this.clearError(input);
        return true;
    },

    // Validate password field
    validatePassword: function(input, minLength = 6) {
        if (input.value && input.value.length < minLength) {
            this.showError(input, `Password must be at least ${minLength} characters`);
            return false;
        }
        this.clearError(input);
        return true;
    },

    // Validate password confirmation
    validatePasswordConfirm: function(input, passwordInput) {
        if (input.value !== passwordInput.value) {
            this.showError(input, 'Passwords do not match');
            return false;
        }
        this.clearError(input);
        return true;
    }
};

// API helpers
const api = {
    // Make API request
    request: async function(url, options = {}) {
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
    },

    // GET request
    get: function(url) {
        return this.request(url, { method: 'GET' });
    },

    // POST request
    post: function(url, data) {
        return this.request(url, {
            method: 'POST',
            body: JSON.stringify(data),
        });
    },

    // PUT request
    put: function(url, data) {
        return this.request(url, {
            method: 'PUT',
            body: JSON.stringify(data),
        });
    },

    // DELETE request
    delete: function(url) {
        return this.request(url, { method: 'DELETE' });
    }
};

// Export for use in other scripts
window.BreastCareAI = {
    utils,
    formValidation,
    api
};
