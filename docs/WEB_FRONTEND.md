# Web Frontend Documentation

This document provides comprehensive information about the web frontend, including templates, static assets, styling, and JavaScript components.

## 🎨 Frontend Architecture

### Technology Stack

- **Backend Templates**: Jinja2 with FastAPI
- **CSS Framework**: Tailwind CSS 4.x
- **JavaScript**: Vanilla JavaScript with Alpine.js components
- **Build Tool**: pnpm with Tailwind CLI
- **Icons**: Emoji-based icons and custom SVG
- **Responsive Design**: Mobile-first approach

### Project Structure

```
static/
├── css/
│   ├── app.css              # Main application styles
│   └── common.css           # Common utility styles
├── js/
│   ├── api.js               # API communication
│   ├── common.js            # Common utilities
│   ├── form-handler.js      # Form handling
│   ├── form-validator.js    # Form validation
│   ├── ml-api.js            # ML API interactions
│   ├── utils.js             # Utility functions
│   └── alpine-components.js # Alpine.js components
└── images/                  # Static images

templates/
├── base.html                # Base template
├── home.html                # Home page
├── login.html               # Login page
├── signup.html              # Registration page
├── dashboard.html           # User dashboard
├── breast_cancer_analysis.html
├── wisconsin_analytics.html
├── wisconsin_prediction.html
└── components/              # Reusable components
    ├── dashboard_nav.html
    ├── medical_records.html
    ├── family_history.html
    ├── profile.html
    └── breast_cancer_analysis.html

tailwindcss/
├── styles/
│   └── app.css              # Tailwind source file
└── package.json             # Node.js dependencies
```

## 🎨 Styling System

### Tailwind CSS Configuration

The application uses Tailwind CSS 4.x with a custom configuration:

```json
{
  "name": "tailwindcss",
  "scripts": {
    "dev": "pnpx @tailwindcss/cli -i ./styles/app.css -o ../static/css/app.css --watch",
    "build": "pnpx @tailwindcss/cli -i ./styles/app.css -o ../static/css/app.css"
  },
  "dependencies": {
    "tailwindcss": "^4.1.13",
    "@tailwindcss/cli": "^4.1.13"
  }
}
```

### CSS Build Process

#### Development Mode
```bash
cd tailwindcss
pnpm run dev
```
- Watches for changes in `styles/app.css`
- Automatically rebuilds CSS
- Outputs to `../static/css/app.css`

#### Production Mode
```bash
cd tailwindcss
pnpm run build
```
- One-time build
- Optimized CSS output
- Minified for production

### Design System

#### Color Palette
```css
/* Primary Colors */
--primary-50: #eff6ff;
--primary-500: #3b82f6;
--primary-900: #1e3a8a;

/* Success Colors */
--success-50: #f0fdf4;
--success-500: #22c55e;
--success-900: #14532d;

/* Warning Colors */
--warning-50: #fffbeb;
--warning-500: #f59e0b;
--warning-900: #78350f;

/* Error Colors */
--error-50: #fef2f2;
--error-500: #ef4444;
--error-900: #7f1d1d;
```

#### Typography
- **Headings**: Inter font family
- **Body**: System font stack
- **Code**: Monaco, Consolas, monospace

#### Spacing System
- **Base Unit**: 4px (0.25rem)
- **Common Spacing**: 1, 2, 4, 6, 8, 12, 16, 20, 24, 32, 48, 64

## 📱 Responsive Design

### Breakpoints

```css
/* Mobile First Approach */
sm: 640px   /* Small devices */
md: 768px   /* Medium devices */
lg: 1024px  /* Large devices */
xl: 1280px  /* Extra large devices */
2xl: 1536px /* 2X large devices */
```

### Layout Components

#### Container
```html
<div class="container mx-auto px-4 sm:px-6 lg:px-8">
  <!-- Content -->
</div>
```

#### Grid System
```html
<div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
  <!-- Grid items -->
</div>
```

#### Flexbox Utilities
```html
<div class="flex flex-col sm:flex-row items-center justify-between">
  <!-- Flex content -->
</div>
```

## 🧩 Template System

### Base Template (`templates/base.html`)

The base template provides the foundation for all pages:

```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{% block title %}AI Medical Records{% endblock %}</title>
    
    <!-- Tailwind CSS -->
    <link href="/static/css/app.css" rel="stylesheet">
    
    <!-- Alpine.js -->
    <script defer src="https://unpkg.com/alpinejs@3.x.x/dist/cdn.min.js"></script>
</head>
<body class="bg-gray-50 min-h-screen">
    <!-- Navigation -->
    {% include 'components/dashboard_nav.html' %}
    
    <!-- Main Content -->
    <main class="container mx-auto px-4 py-8">
        {% block content %}{% endblock %}
    </main>
    
    <!-- Scripts -->
    <script src="/static/js/common.js"></script>
    {% block scripts %}{% endblock %}
</body>
</html>
```

### Template Inheritance

All templates extend the base template:

```html
{% extends "base.html" %}

{% block title %}Dashboard - AI Medical Records{% endblock %}

{% block content %}
<div class="max-w-7xl mx-auto">
    <h1 class="text-3xl font-bold text-gray-900 mb-8">Dashboard</h1>
    <!-- Page content -->
</div>
{% endblock %}

{% block scripts %}
<script src="/static/js/dashboard.js"></script>
{% endblock %}
```

### Component System

#### Dashboard Navigation (`templates/components/dashboard_nav.html`)

```html
<nav class="bg-white shadow-sm border-b border-gray-200">
    <div class="container mx-auto px-4">
        <div class="flex justify-between items-center h-16">
            <div class="flex items-center">
                <a href="/" class="text-xl font-bold text-blue-600">
                    🏥 AI Medical Records
                </a>
            </div>
            
            <div class="flex items-center space-x-4">
                {% if user %}
                    <a href="/users/dashboard" class="text-gray-700 hover:text-blue-600">
                        Dashboard
                    </a>
                    <a href="/users/profile" class="text-gray-700 hover:text-blue-600">
                        Profile
                    </a>
                    <form method="post" action="/users/logout" class="inline">
                        <button type="submit" class="text-gray-700 hover:text-blue-600">
                            Logout
                        </button>
                    </form>
                {% else %}
                    <a href="/users/login" class="text-gray-700 hover:text-blue-600">
                        Login
                    </a>
                    <a href="/users/signup" class="bg-blue-600 text-white px-4 py-2 rounded-md hover:bg-blue-700">
                        Sign Up
                    </a>
                {% endif %}
            </div>
        </div>
    </div>
</nav>
```

## 🎯 Page Templates

### Home Page (`templates/home.html`)

Features:
- Hero section with application overview
- Feature cards with icons
- Statistics display
- Call-to-action buttons
- Responsive design

```html
{% extends "base.html" %}

{% block content %}
<!-- Hero Section -->
<section class="bg-gradient-to-r from-blue-600 to-blue-800 text-white py-20">
    <div class="container mx-auto px-4 text-center">
        <h1 class="text-5xl font-bold mb-6">AI-Powered Medical Records</h1>
        <p class="text-xl mb-8 max-w-3xl mx-auto">
            Comprehensive medical records management with advanced breast cancer detection
        </p>
        <div class="flex flex-col sm:flex-row gap-4 justify-center">
            <a href="/users/signup" class="bg-white text-blue-600 px-8 py-3 rounded-lg font-semibold hover:bg-gray-100">
                Get Started
            </a>
            <a href="/ml/breast-cancer-analysis" class="border-2 border-white text-white px-8 py-3 rounded-lg font-semibold hover:bg-white hover:text-blue-600">
                Try AI Analysis
            </a>
        </div>
    </div>
</section>

<!-- Features Section -->
<section class="py-16">
    <div class="container mx-auto px-4">
        <h2 class="text-3xl font-bold text-center mb-12">Key Features</h2>
        <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8">
            {% for card in about_cards %}
            <div class="bg-white p-6 rounded-lg shadow-md">
                <div class="text-4xl mb-4">{{ card.icon }}</div>
                <h3 class="text-xl font-semibold mb-2">{{ card.title }}</h3>
                <p class="text-gray-600">{{ card.description }}</p>
            </div>
            {% endfor %}
        </div>
    </div>
</section>
{% endblock %}
```

### Dashboard (`templates/dashboard.html`)

Features:
- User overview cards
- Recent medical records
- Family history summary
- Quick action buttons
- Statistics widgets

### Breast Cancer Analysis (`templates/breast_cancer_analysis.html`)

Features:
- Interactive prediction form
- Feature input validation
- Real-time results display
- Confidence visualization
- Risk level indicators

### Wisconsin Analytics (`templates/wisconsin_analytics.html`)

Features:
- Dataset statistics
- Model performance metrics
- Feature importance charts
- Prediction history
- Interactive visualizations

## 🚀 JavaScript Components

### Alpine.js Integration

The application uses Alpine.js for interactive components:

```html
<!-- Example: Interactive form -->
<div x-data="predictionForm()">
    <form @submit.prevent="submitForm">
        <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
            <div>
                <label class="block text-sm font-medium text-gray-700 mb-2">
                    Radius Mean
                </label>
                <input 
                    type="number" 
                    x-model="features.radius_mean"
                    class="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
                    step="0.01"
                    required
                >
            </div>
            <!-- More form fields -->
        </div>
        
        <button 
            type="submit" 
            :disabled="loading"
            class="w-full bg-blue-600 text-white py-2 px-4 rounded-md hover:bg-blue-700 disabled:opacity-50"
        >
            <span x-show="!loading">Make Prediction</span>
            <span x-show="loading">Processing...</span>
        </button>
    </form>
</div>
```

### JavaScript Modules

#### API Communication (`static/js/api.js`)

```javascript
class MedicalAPI {
    constructor() {
        this.baseURL = '/api';
    }
    
    async makePrediction(features) {
        const response = await fetch(`${this.baseURL}/ml/predict`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ features })
        });
        
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        
        return await response.json();
    }
    
    async getPredictions() {
        const response = await fetch(`${this.baseURL}/ml/predictions`);
        return await response.json();
    }
}

// Global instance
window.medicalAPI = new MedicalAPI();
```

#### Form Validation (`static/js/form-validator.js`)

```javascript
class FormValidator {
    constructor(formElement) {
        this.form = formElement;
        this.errors = {};
    }
    
    validateFeature(featureName, value) {
        const ranges = {
            'radius_mean': { min: 6.981, max: 28.11 },
            'texture_mean': { min: 9.71, max: 39.28 },
            // ... other features
        };
        
        const range = ranges[featureName];
        if (!range) {
            return { valid: false, message: 'Unknown feature' };
        }
        
        if (value < range.min || value > range.max) {
            return {
                valid: false,
                message: `Value must be between ${range.min} and ${range.max}`
            };
        }
        
        return { valid: true };
    }
    
    validateForm() {
        this.errors = {};
        let isValid = true;
        
        const inputs = this.form.querySelectorAll('input[type="number"]');
        inputs.forEach(input => {
            const validation = this.validateFeature(input.name, parseFloat(input.value));
            if (!validation.valid) {
                this.errors[input.name] = validation.message;
                isValid = false;
            }
        });
        
        return isValid;
    }
    
    displayErrors() {
        // Clear previous errors
        this.form.querySelectorAll('.error-message').forEach(el => el.remove());
        
        // Display new errors
        Object.entries(this.errors).forEach(([field, message]) => {
            const input = this.form.querySelector(`[name="${field}"]`);
            if (input) {
                const errorDiv = document.createElement('div');
                errorDiv.className = 'error-message text-red-500 text-sm mt-1';
                errorDiv.textContent = message;
                input.parentNode.appendChild(errorDiv);
            }
        });
    }
}
```

#### Alpine.js Components (`static/js/alpine-components.js`)

```javascript
// Prediction form component
function predictionForm() {
    return {
        features: {},
        loading: false,
        result: null,
        error: null,
        
        async submitForm() {
            this.loading = true;
            this.error = null;
            this.result = null;
            
            try {
                const response = await window.medicalAPI.makePrediction(this.features);
                this.result = response;
            } catch (error) {
                this.error = error.message;
            } finally {
                this.loading = false;
            }
        },
        
        getRiskColor(riskLevel) {
            const colors = {
                'Low': 'text-green-600 bg-green-100',
                'Medium': 'text-yellow-600 bg-yellow-100',
                'High': 'text-red-600 bg-red-100'
            };
            return colors[riskLevel] || 'text-gray-600 bg-gray-100';
        }
    };
}

// Dashboard component
function dashboard() {
    return {
        stats: {
            totalRecords: 0,
            recentPredictions: 0,
            familyMembers: 0
        },
        
        async loadStats() {
            try {
                // Load dashboard statistics
                const response = await fetch('/api/dashboard/stats');
                this.stats = await response.json();
            } catch (error) {
                console.error('Failed to load stats:', error);
            }
        },
        
        init() {
            this.loadStats();
        }
    };
}
```

## 🎨 UI Components

### Cards

```html
<div class="bg-white rounded-lg shadow-md p-6">
    <div class="flex items-center justify-between mb-4">
        <h3 class="text-lg font-semibold text-gray-900">Card Title</h3>
        <span class="text-2xl">📊</span>
    </div>
    <p class="text-gray-600">Card content goes here.</p>
</div>
```

### Buttons

```html
<!-- Primary Button -->
<button class="bg-blue-600 text-white px-4 py-2 rounded-md hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-blue-500">
    Primary Action
</button>

<!-- Secondary Button -->
<button class="bg-gray-200 text-gray-800 px-4 py-2 rounded-md hover:bg-gray-300 focus:outline-none focus:ring-2 focus:ring-gray-500">
    Secondary Action
</button>

<!-- Danger Button -->
<button class="bg-red-600 text-white px-4 py-2 rounded-md hover:bg-red-700 focus:outline-none focus:ring-2 focus:ring-red-500">
    Delete
</button>
```

### Forms

```html
<form class="space-y-6">
    <div>
        <label class="block text-sm font-medium text-gray-700 mb-2">
            Field Label
        </label>
        <input 
            type="text" 
            class="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent"
            placeholder="Enter value"
            required
        >
    </div>
    
    <div>
        <label class="block text-sm font-medium text-gray-700 mb-2">
            Select Field
        </label>
        <select class="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500">
            <option value="">Choose option</option>
            <option value="option1">Option 1</option>
            <option value="option2">Option 2</option>
        </select>
    </div>
</form>
```

### Alerts

```html
<!-- Success Alert -->
<div class="bg-green-100 border border-green-400 text-green-700 px-4 py-3 rounded mb-4">
    <strong class="font-bold">Success!</strong>
    <span class="block sm:inline">Operation completed successfully.</span>
</div>

<!-- Error Alert -->
<div class="bg-red-100 border border-red-400 text-red-700 px-4 py-3 rounded mb-4">
    <strong class="font-bold">Error!</strong>
    <span class="block sm:inline">Something went wrong.</span>
</div>

<!-- Warning Alert -->
<div class="bg-yellow-100 border border-yellow-400 text-yellow-700 px-4 py-3 rounded mb-4">
    <strong class="font-bold">Warning!</strong>
    <span class="block sm:inline">Please check your input.</span>
</div>
```

## 📱 Mobile Optimization

### Responsive Navigation

```html
<nav class="bg-white shadow-sm">
    <div class="container mx-auto px-4">
        <div class="flex justify-between items-center h-16">
            <!-- Logo -->
            <div class="flex items-center">
                <a href="/" class="text-xl font-bold text-blue-600">
                    🏥 AI Medical Records
                </a>
            </div>
            
            <!-- Desktop Menu -->
            <div class="hidden md:flex items-center space-x-4">
                <a href="/dashboard" class="text-gray-700 hover:text-blue-600">Dashboard</a>
                <a href="/profile" class="text-gray-700 hover:text-blue-600">Profile</a>
            </div>
            
            <!-- Mobile Menu Button -->
            <button class="md:hidden" @click="mobileMenuOpen = !mobileMenuOpen">
                <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 6h16M4 12h16M4 18h16"></path>
                </svg>
            </button>
        </div>
        
        <!-- Mobile Menu -->
        <div x-show="mobileMenuOpen" class="md:hidden">
            <div class="px-2 pt-2 pb-3 space-y-1">
                <a href="/dashboard" class="block px-3 py-2 text-gray-700 hover:text-blue-600">Dashboard</a>
                <a href="/profile" class="block px-3 py-2 text-gray-700 hover:text-blue-600">Profile</a>
            </div>
        </div>
    </div>
</nav>
```

### Touch-Friendly Interface

- **Button Size**: Minimum 44px touch targets
- **Spacing**: Adequate spacing between interactive elements
- **Gestures**: Support for touch gestures
- **Viewport**: Proper viewport meta tag

## 🎯 Performance Optimization

### CSS Optimization

- **Tailwind Purge**: Remove unused CSS in production
- **Minification**: Compress CSS files
- **Critical CSS**: Inline critical styles

### JavaScript Optimization

- **Code Splitting**: Load scripts only when needed
- **Lazy Loading**: Defer non-critical scripts
- **Caching**: Cache API responses
- **Debouncing**: Optimize form input handling

### Image Optimization

- **WebP Format**: Use modern image formats
- **Lazy Loading**: Load images on demand
- **Responsive Images**: Serve appropriate sizes
- **Compression**: Optimize image file sizes

## 🔧 Development Workflow

### CSS Development

1. **Edit Source**: Modify `tailwindcss/styles/app.css`
2. **Watch Changes**: Run `pnpm run dev` in tailwindcss directory
3. **Auto-reload**: CSS automatically rebuilds
4. **Test**: Refresh browser to see changes

### JavaScript Development

1. **Edit Scripts**: Modify files in `static/js/`
2. **Test**: Refresh browser to load changes
3. **Debug**: Use browser developer tools
4. **Optimize**: Minify for production

### Template Development

1. **Edit Templates**: Modify files in `templates/`
2. **Test**: Restart FastAPI server
3. **Debug**: Check template rendering
4. **Validate**: Ensure proper HTML structure

## 🧪 Testing

### Browser Testing

- **Chrome**: Latest version
- **Firefox**: Latest version
- **Safari**: Latest version
- **Edge**: Latest version

### Mobile Testing

- **iOS Safari**: iPhone and iPad
- **Android Chrome**: Various screen sizes
- **Responsive Design**: Test all breakpoints

### Accessibility Testing

- **Screen Readers**: Test with NVDA/JAWS
- **Keyboard Navigation**: Ensure all functionality accessible
- **Color Contrast**: Verify WCAG compliance
- **Focus Management**: Proper focus indicators

## 📚 Additional Resources

- [Tailwind CSS Documentation](https://tailwindcss.com/docs)
- [Alpine.js Documentation](https://alpinejs.dev/)
- [Jinja2 Documentation](https://jinja.palletsprojects.com/)
- [Web Accessibility Guidelines](https://www.w3.org/WAI/WCAG21/quickref/)

---

For more information about other components, see:
- [FastAPI Documentation](FASTAPI.md)
- [Database Documentation](DATABASE.md)
- [AI/ML Documentation](AI_ML.md)
