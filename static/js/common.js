// Common JavaScript functionality for BreastCare AI

// Smooth scrolling for anchor links
document.addEventListener('DOMContentLoaded', function() {
    // Add smooth scrolling for navigation links
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

    // Add loading states to forms
    document.querySelectorAll('form').forEach(form => {
        form.addEventListener('submit', function() {
            const submitBtn = form.querySelector('button[type="submit"]');
            if (submitBtn) {
                submitBtn.disabled = true;
                submitBtn.textContent = 'Loading...';
            }
        });
    });

    // Add fade-in animation to elements
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
