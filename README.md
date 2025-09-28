# AI Medical Records Application

A comprehensive medical records management system with AI-powered breast cancer detection, built with FastAPI, SQLModel, and advanced machine learning algorithms.

## 🚀 Quick Start

### Prerequisites

Before you begin, ensure you have the following installed:

#### For macOS:
- **Python 3.13+**: [Download from python.org](https://www.python.org/downloads/macos/) or use Homebrew: `brew install python@3.13`
- **uv**: [Install uv package manager](https://docs.astral.sh/uv/getting-started/installation/#macos-and-linux)
- **Node.js 18+**: [Download from nodejs.org](https://nodejs.org/en/download/) or use Homebrew: `brew install node`
- **pnpm**: Install via npm: `npm install -g pnpm`

#### For Windows:
- **Python 3.13+**: [Download from python.org](https://www.python.org/downloads/windows/) or use Windows Store
- **uv**: [Install uv package manager](https://docs.astral.sh/uv/getting-started/installation/#windows)
- **Node.js 18+**: [Download from nodejs.org](https://nodejs.org/en/download/)
- **pnpm**: Install via npm: `npm install -g pnpm`

### Installation Steps

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd ai
   ```

2. **Install Python dependencies**
   ```bash
   uv sync
   ```

3. **Install Node.js dependencies**
   ```bash
   cd tailwindcss
   pnpm install
   cd ..
   ```

4. **Initialize the database**
   ```bash
   uv run python manage_db.py init
   ```

5. **Start the development server**
   
   **Terminal 1 (FastAPI):**
   ```bash
   uv run fastapi dev app/main.py
   ```
   
   **Terminal 2 (Tailwind CSS):**
   ```bash
   cd tailwindcss
   pnpm run dev
   ```

6. **Access the application**
   - Open your browser and go to: http://localhost:8000
   - API documentation: http://localhost:8000/docs

## 🏗️ Project Structure

```
ai/
├── app/                      # Main application package
│   ├── __init__.py
│   ├── main.py              # FastAPI application entry point
│   ├── auth.py              # Authentication utilities
│   ├── dependencies.py      # Dependency injection
│   ├── database/            # Database configuration
│   │   ├── __init__.py
│   │   ├── database.py      # Database connection
│   │   └── init.py          # Database initialization
│   ├── internal/            # Internal/admin routes
│   │   ├── __init__.py
│   │   └── admin.py
│   ├── ml/                  # Machine learning models
│   │   ├── __init__.py
│   │   ├── breast_cancer_model.py
│   │   ├── wisconsin_analyzer.py
│   │   └── wisconsin_ensemble.py
│   ├── models/              # Database models
│   │   ├── __init__.py
│   │   └── models.py
│   └── routers/             # API route modules
│       ├── __init__.py
│       ├── users.py         # User management
│       ├── medical.py       # Medical records
│       ├── ml.py           # ML predictions
│       └── wisconsin.py    # Wisconsin dataset analysis
├── alembic/                 # Database migrations
│   ├── versions/            # Migration files
│   ├── env.py              # Alembic environment
│   └── script.py.mako      # Migration template
├── docs/                    # Documentation
│   ├── FASTAPI.md          # FastAPI and routing guide
│   ├── DATABASE.md         # Database and migrations
│   ├── AI_ML.md            # AI/ML components
│   ├── WEB_FRONTEND.md     # Web frontend guide
│   └── MODEL_MANAGEMENT.md # Model management
├── models/                  # Trained ML models (gitignored)
├── static/                  # Static files (CSS, JS, images)
│   ├── css/
│   ├── js/
│   └── images/
├── tailwindcss/            # Tailwind CSS configuration
│   ├── styles/
│   └── package.json
├── templates/              # Jinja2 HTML templates
│   ├── components/
│   ├── base.html
│   ├── home.html
│   ├── dashboard.html
│   └── ...
├── manage_db.py            # Database management CLI
├── train_wisconsin_models.py # ML model training script
├── pyproject.toml          # Python dependencies
├── alembic.ini            # Alembic configuration
└── README.md              # This file
```

## 🎯 Features

### User Management
- ✅ User registration with email validation
- ✅ Secure login with password hashing
- ✅ Session-based authentication
- ✅ User profile management

### Medical Records
- ✅ Add/edit medical records
- ✅ Track record status (pending/completed)
- ✅ Doctor information and notes
- ✅ Date-based organization

### Family History
- ✅ Add family members
- ✅ Track medical conditions
- ✅ Age and relationship tracking

### AI Breast Cancer Detection
- ✅ **Standard Model**: Random Forest classifier with 97%+ accuracy
- ✅ **Wisconsin Ensemble**: 8-model ensemble with 98.25% accuracy and 99.97% ROC AUC
- ✅ Real-time predictions with confidence scores
- ✅ Feature importance analysis
- ✅ Risk level assessment

### Security
- ✅ Password hashing with pbkdf2_sha256
- ✅ Session management with expiration
- ✅ SQL injection protection via SQLModel
- ✅ Secure cookie handling

## 🚀 Development Commands

### Development Mode
```bash
# Terminal 1: Start FastAPI development server
uv run fastapi dev app/main.py

# Terminal 2: Start Tailwind CSS watcher
cd tailwindcss
pnpm run dev
```

### Production Mode
```bash
# Build Tailwind CSS
cd tailwindcss
pnpm run build
cd ..

# Start production server
uv run fastapi run app/main.py
```

### Database Management
```bash
# Initialize database
uv run python manage_db.py init

# Check migration status
uv run python manage_db.py status

# Apply migrations
uv run python manage_db.py migrate

# Create new migration
uv run python manage_db.py create-migration "Description of changes"

# Show migration history
uv run python manage_db.py history

# Downgrade database
uv run python manage_db.py downgrade
```

### Machine Learning
```bash
# Train Wisconsin ensemble models
uv run python train_wisconsin_models.py

# Train with hyperparameter tuning
uv run python train_wisconsin_models.py --hyperparameter-tuning

# Train with verbose output
uv run python train_wisconsin_models.py --verbose
```

## 📚 Documentation

For detailed information about specific components, see the documentation in the `docs/` folder:

- **[FastAPI & Routing](docs/FASTAPI.md)** - API structure, routing, and endpoints
- **[Database & Migrations](docs/DATABASE.md)** - Database setup, models, and migrations
- **[AI/ML Components](docs/AI_ML.md)** - Machine learning models and training
- **[Web Frontend](docs/WEB_FRONTEND.md)** - Frontend structure and styling
- **[Model Management](docs/MODEL_MANAGEMENT.md)** - ML model lifecycle and management

## 🔧 Configuration

### Environment Variables
- `SECRET_KEY`: JWT secret key (defaults to development key)
- `DATABASE_URL`: Database connection string (defaults to SQLite)

### Database
The application uses SQLite by default, but can be easily configured for PostgreSQL or MySQL by updating the `DATABASE_URL` in `app/database/database.py`.

## 🧪 Testing

### Test Application Imports
```bash
uv run python -c "from app.main import app; print('✅ App imports successfully')"
```

### Test Database Connection
```bash
uv run python -c "from app.database import engine; print('✅ Database connection successful')"
```

## 📝 Sample User

For testing purposes, you can create a sample user:
- **Email**: jane.doe@email.com
- **Password**: password123

## 🛠️ Troubleshooting

### Common Issues

1. **Model not found error**
   - Train the model: `uv run python train_wisconsin_models.py`
   - Or use the API: `POST /ml/api/train-model`

2. **Database connection issues**
   - Check if database exists: `uv run python manage_db.py status`
   - Initialize database: `uv run python manage_db.py init`

3. **Tailwind CSS not updating**
   - Ensure Tailwind watcher is running: `cd tailwindcss && pnpm run dev`
   - Check if CSS files are being generated in `static/css/`

4. **Port already in use**
   - Change port: `uv run fastapi dev app/main.py --port 8001`
   - Or kill existing process: `lsof -ti:8000 | xargs kill -9` (macOS/Linux)

## 📈 Performance Metrics

### Wisconsin Ensemble Model
- **Accuracy**: 98.25%
- **ROC AUC**: 99.97%
- **Precision**: 98.1%
- **Recall**: 98.4%
- **F1-Score**: 98.2%

### Individual Models
- Random Forest: 97.4%
- Gradient Boosting: 96.8%
- SVM (RBF): 96.2%
- Neural Network: 95.9%
- Logistic Regression: 95.1%
- AdaBoost: 94.7%
- Extra Trees: 97.1%
- SVM (Linear): 95.8%

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch: `git checkout -b feature-name`
3. Make your changes
4. Add tests if applicable
5. Commit your changes: `git commit -m 'Add feature'`
6. Push to the branch: `git push origin feature-name`
7. Submit a pull request

## 📄 License

This project is licensed under the MIT License.

## 🆘 Support

If you encounter any issues or have questions:

1. Check the [documentation](docs/) for detailed guides
2. Review the [troubleshooting section](#-troubleshooting)
3. Open an issue on GitHub
4. Contact the development team

---

**Built with ❤️ using FastAPI, SQLModel, and Scikit-learn**