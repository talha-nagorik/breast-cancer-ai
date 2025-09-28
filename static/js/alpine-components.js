/**
 * Alpine.js Components - All Alpine.js data components and utilities
 * Depends on: form-handler.js, utils.js
 */

document.addEventListener('alpine:init', () => {
    // Professional Form handling component
    Alpine.data('formHandler', () => ({
        loading: false,
        errors: {},
        touched: {},
        formData: {
            email: '',
            password: '',
            name: '',
            confirmPassword: ''
        },
        formHandler: new ProfessionalFormHandler(),
        
        async handleLogin() {
            // Mark all fields as touched for validation display
            this.touched.email = true;
            this.touched.password = true;
            
            // Validate all fields
            const emailErrors = this.formHandler.validateField('email', this.formData.email, { required: true, email: true });
            const passwordErrors = this.formHandler.validateField('password', this.formData.password, { required: true, minLength: 6 });
            
            // Update errors
            this.errors.email = emailErrors.length > 0 ? emailErrors[0] : null;
            this.errors.password = passwordErrors.length > 0 ? passwordErrors[0] : null;
            
            if (emailErrors.length > 0 || passwordErrors.length > 0) {
                this.showNotification('Please fix the errors below', 'error');
                return;
            }
            
            this.loading = true;
            
            const result = await this.formHandler.submitForm(
                {
                    email: this.formData.email.trim(),
                    password: this.formData.password
                },
                '/login',
                {
                    method: 'POST',
                    onSuccess: (data) => {
                        this.showNotification('Login successful! Redirecting...', 'success');
                        setTimeout(() => {
                            window.location.href = '/dashboard';
                        }, 1000);
                    },
                    onError: (error) => {
                        this.showNotification(error.message || 'Login failed. Please check your credentials.', 'error');
                        // Clear password on error for security
                        this.formData.password = '';
                    }
                }
            );
            
            this.loading = false;
        },
        
        validateField(field, value, rules = {}) {
            this.touched[field] = true;
            const errors = this.formHandler.validateField(field, value, rules);
            
            if (errors.length > 0) {
                this.errors[field] = errors[0];
            } else {
                delete this.errors[field];
            }
            
            return errors.length === 0;
        },
        
        validateAllFields() {
            let isValid = true;
            
            // Validate email
            if (this.formData.email) {
                isValid = this.validateField('email', this.formData.email, { required: true, email: true }) && isValid;
            }
            
            // Validate password
            if (this.formData.password) {
                isValid = this.validateField('password', this.formData.password, { required: true, minLength: 6 }) && isValid;
            }
            
            // Validate name
            if (this.formData.name) {
                isValid = this.validateField('name', this.formData.name, { required: true, minLength: 2, maxLength: 50 }) && isValid;
            }
            
            // Validate confirm password
            if (this.formData.confirmPassword) {
                isValid = this.validateField('confirmPassword', this.formData.confirmPassword, { required: true, match: this.formData.password }) && isValid;
            }
            
            return isValid;
        },
        
        clearFieldError(field) {
            delete this.errors[field];
        },
        
        clearAllErrors() {
            this.errors = {};
            this.touched = {};
        },
        
        showNotification(message, type = 'info') {
            if (window.BreastCareAI && window.BreastCareAI.utils) {
                window.BreastCareAI.utils.showNotification(message, type);
            }
        }
    }));
    
    // Enhanced Signup form component
    Alpine.data('signupForm', () => ({
        loading: false,
        errors: {},
        touched: {},
        formData: {
            full_name: '',
            email: '',
            password: '',
            confirm_password: ''
        },
        formHandler: new ProfessionalFormHandler(),
        
        async handleSubmit() {
            // Mark all fields as touched
            this.touched.full_name = true;
            this.touched.email = true;
            this.touched.password = true;
            this.touched.confirm_password = true;
            
            // Validate all fields
            const nameErrors = this.formHandler.validateField('full_name', this.formData.full_name, { required: true, minLength: 2, maxLength: 50 });
            const emailErrors = this.formHandler.validateField('email', this.formData.email, { required: true, email: true });
            const passwordErrors = this.formHandler.validateField('password', this.formData.password, { required: true, minLength: 8 });
            const confirmErrors = this.formHandler.validateField('confirm_password', this.formData.confirm_password, { required: true, match: this.formData.password });
            
            // Update errors
            this.errors.full_name = nameErrors.length > 0 ? nameErrors[0] : null;
            this.errors.email = emailErrors.length > 0 ? emailErrors[0] : null;
            this.errors.password = passwordErrors.length > 0 ? passwordErrors[0] : null;
            this.errors.confirm_password = confirmErrors.length > 0 ? confirmErrors[0] : null;
            
            if (nameErrors.length > 0 || emailErrors.length > 0 || passwordErrors.length > 0 || confirmErrors.length > 0) {
                this.showNotification('Please fix the errors below', 'error');
                return;
            }
            
            this.loading = true;
            
            const result = await this.formHandler.submitForm(
                {
                    full_name: this.formData.full_name.trim(),
                    email: this.formData.email.trim().toLowerCase(),
                    password: this.formData.password,
                    confirm_password: this.formData.confirm_password
                },
                '/signup',
                {
                    method: 'POST',
                    onSuccess: (data) => {
                        this.showNotification('Account created successfully! Redirecting to login...', 'success');
                        setTimeout(() => {
                            window.location.href = '/login';
                        }, 1500);
                    },
                    onError: (error) => {
                        this.showNotification(error.message || 'Failed to create account. Please try again.', 'error');
                        // Clear passwords on error for security
                        this.formData.password = '';
                        this.formData.confirm_password = '';
                    }
                }
            );
            
            this.loading = false;
        },
        
        validateField(field, value, rules = {}) {
            this.touched[field] = true;
            const errors = this.formHandler.validateField(field, value, rules);
            
            if (errors.length > 0) {
                this.errors[field] = errors[0];
            } else {
                delete this.errors[field];
            }
            
            return errors.length === 0;
        },
        
        showNotification(message, type = 'info') {
            if (window.BreastCareAI && window.BreastCareAI.utils) {
                window.BreastCareAI.utils.showNotification(message, type);
            }
        }
    }));
    
    // Enhanced Medical Record form component
    Alpine.data('recordForm', () => ({
        loading: false,
        errors: {},
        touched: {},
        formData: {
            date: '',
            type: '',
            doctor: '',
            status: '',
            notes: ''
        },
        formHandler: new ProfessionalFormHandler(),
        
        async handleSubmit() {
            // Mark all fields as touched
            Object.keys(this.formData).forEach(field => {
                this.touched[field] = true;
            });
            
            // Validate all fields
            const dateErrors = this.formHandler.validateField('date', this.formData.date, { required: true, date: true });
            const typeErrors = this.formHandler.validateField('type', this.formData.type, { required: true });
            const doctorErrors = this.formHandler.validateField('doctor', this.formData.doctor, { required: true, minLength: 2, maxLength: 100 });
            const statusErrors = this.formHandler.validateField('status', this.formData.status, { required: true });
            
            // Update errors
            this.errors.date = dateErrors.length > 0 ? dateErrors[0] : null;
            this.errors.type = typeErrors.length > 0 ? typeErrors[0] : null;
            this.errors.doctor = doctorErrors.length > 0 ? doctorErrors[0] : null;
            this.errors.status = statusErrors.length > 0 ? statusErrors[0] : null;
            
            if (dateErrors.length > 0 || typeErrors.length > 0 || doctorErrors.length > 0 || statusErrors.length > 0) {
                this.showNotification('Please fix the errors below', 'error');
                return;
            }
            
            this.loading = true;
            
            const result = await this.formHandler.submitForm(
                {
                    date: this.formData.date,
                    type: this.formData.type,
                    doctor: this.formData.doctor.trim(),
                    status: this.formData.status,
                    notes: this.formData.notes.trim()
                },
                '/add_record',
                {
                    method: 'POST',
                    onSuccess: (data) => {
                        this.showNotification('Record added successfully!', 'success');
                        this.resetForm();
                        // Optionally reload the page to show the new record
                        setTimeout(() => window.location.reload(), 1000);
                    },
                    onError: (error) => {
                        this.showNotification(error.message || 'Failed to add record. Please try again.', 'error');
                    }
                }
            );
            
            this.loading = false;
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
            this.touched = {};
        },
        
        validateField(field, value, rules = {}) {
            this.touched[field] = true;
            const errors = this.formHandler.validateField(field, value, rules);
            
            if (errors.length > 0) {
                this.errors[field] = errors[0];
            } else {
                delete this.errors[field];
            }
            
            return errors.length === 0;
        },
        
        showNotification(message, type = 'info') {
            if (window.BreastCareAI && window.BreastCareAI.utils) {
                window.BreastCareAI.utils.showNotification(message, type);
            }
        }
    }));
    
    // Dashboard component
    Alpine.data('dashboard', () => ({
        activeTab: 'overview',
        
        setActiveTab(tabName) {
            this.activeTab = tabName;
        },
        
        isActiveTab(tabName) {
            return this.activeTab === tabName;
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
});
