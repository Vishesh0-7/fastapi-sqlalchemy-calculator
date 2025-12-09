# 🧮 Calculator API with JWT Authentication

[![Python](https://img.shields.io/badge/Python-3.11-blue?logo=python)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.100+-teal?logo=fastapi)](https://fastapi.tiangolo.com/)
[![PostgreSQL](https://img.shields.io/badge/PostgreSQL-15-blue?logo=postgresql)](https://www.postgresql.org/)
[![Docker](https://img.shields.io/badge/Docker-ready-2496ED?logo=docker)](https://www.docker.com/)
[![Tests](https://img.shields.io/badge/tests-pytest%20%2B%20playwright-green?logo=pytest)](https://pytest.org/)
[![Coverage](https://img.shields.io/badge/coverage-100%25-brightgreen?logo=codecov)](https://codecov.io/)
[![CI/CD](https://github.com/Vishesh0-7/fastapi-sqlalchemy-calculator/actions/workflows/ci.yml/badge.svg)](https://github.com/Vishesh0-7/fastapi-sqlalchemy-calculator/actions)

A professional RESTful API built with FastAPI featuring JWT authentication, calculation history tracking, and a modern responsive web interface.

**🔗 Links:**  
📦 [Docker Hub](https://hub.docker.com/r/vishy211/cicd_calculator) | 💻 [GitHub Repository](https://github.com/Vishesh0-7/fastapi-sqlalchemy-calculator.git)

---

## ✨ Features

### Core Functionality
- 🔐 **JWT Authentication** - Secure user registration and login
- ➕ **Extended Arithmetic Operations** - Add, subtract, multiply, divide, power, modulus with validation
- 📊 **Calculation History** - Track all calculations with user association
- 👤 **User Profile Management** - Update username, email, and change password
- 📈 **Dashboard & Analytics** - View calculation statistics and usage patterns
- 👥 **User Management** - Complete CRUD operations for users
- 🎨 **Modern Web UI** - Responsive frontend with real-time validation

### New Features (Module 14)
- 🔢 **Power Operation** - Exponentiation calculations (a^b)
- ％ **Modulus Operation** - Remainder calculations (a % b)
- 🔑 **Password Change** - Secure password updates with re-authentication
- ✏️ **Profile Updates** - Modify username and email with validation
- 📊 **Usage Dashboard** - Statistics including:
  - Total calculations count
  - Operations breakdown with visual bars
  - Most frequently used operation
  - Average calculation result
- 🔄 **Forced Re-login** - After password change for security

### Technical Excellence
- ✅ **100% Test Coverage** - Unit, integration, and E2E tests
- 🚀 **CI/CD Pipeline** - Automated testing and deployment
- 🐳 **Docker Ready** - Full containerization with Docker Compose
- 📝 **API Documentation** - Auto-generated Swagger/ReDoc docs
- 🔒 **Security** - Password hashing, JWT tokens, input validation
- 🗄️ **Database Migrations** - Alembic for version-controlled schema changes

---

## 🛠 Tech Stack

### Backend
- **[FastAPI](https://fastapi.tiangolo.com/)** - Modern, fast web framework for building APIs
- **[PostgreSQL](https://www.postgresql.org/)** - Advanced open-source relational database
- **[SQLAlchemy](https://www.sqlalchemy.org/)** - Python SQL toolkit and ORM
- **[Pydantic](https://pydantic-docs.helpmanual.io/)** - Data validation using Python type hints
- **[python-jose](https://python-jose.readthedocs.io/)** - JWT token generation and validation
- **[bcrypt](https://github.com/pyca/bcrypt/)** - Secure password hashing
- **[Uvicorn](https://www.uvicorn.org/)** - Lightning-fast ASGI server

### Frontend
- **Vanilla JavaScript** - Clean, dependency-free client-side code
- **HTML5/CSS3** - Modern, responsive design with gradient backgrounds

### Testing & DevOps
- **[pytest](https://pytest.org/)** - Powerful Python testing framework
- **[Playwright](https://playwright.dev/)** - End-to-end browser automation
- **[GitHub Actions](https://github.com/features/actions)** - CI/CD automation
- **[Docker](https://www.docker.com/)** - Container platform for consistent deployments

---

## 📁 Project Structure

```
calculator--FastApi/
│
├── 📂 app/                       # Core application
│   ├── main.py                   # FastAPI app & configuration
│   ├── database.py               # Database connection & session
│   ├── models.py                 # SQLAlchemy database models
│   ├── schemas.py                # Pydantic validation schemas
│   ├── crud.py                   # Database CRUD operations
│   ├── security.py               # JWT & password utilities
│   ├── operations.py             # Calculation business logic (6 operations)
│   ├── routes_auth.py            # Authentication endpoints
│   ├── routes_calculations.py    # Calculation CRUD endpoints
│   ├── routes_users.py           # User management endpoints
│   ├── routes_profile.py         # Profile & password management **NEW**
│   ├── routes_dashboard.py       # Statistics & analytics **NEW**
│   └── 📂 static/
│       └── index.html            # Calculator web interface
│
├── 📂 frontend/                  # Frontend pages
│   ├── index.html                # Landing page
│   ├── login.html                # User login page
│   ├── register.html             # User registration page
│   ├── calculations.html         # Calculation BREAD interface
│   ├── profile.html              # Profile management page **NEW**
│   ├── dashboard.html            # Statistics dashboard **NEW**
│   └── common.js                 # Shared frontend utilities
│
├── 📂 alembic/                   # Database migrations **NEW**
│   ├── env.py                    # Migration environment
│   ├── script.py.mako            # Migration template
│   └── 📂 versions/
│       └── 001_initial.py        # Initial schema migration
│
├── 📂 tests/                     # Python test suite
│   ├── conftest.py               # Pytest fixtures & config
│   ├── test_auth.py              # Authentication tests
│   ├── test_comprehensive.py     # Integration tests
│   ├── 📂 unit/                  # Unit tests
│   │   └── test_operations.py
│   └── 📂 integration/           # Integration tests
│       └── test_api.py
│
├── 📂 e2e/                       # End-to-end tests
│   ├── 📂 tests/
│   │   ├── auth.spec.ts          # Auth flow E2E tests
│   │   └── calculations.spec.ts  # Calculation E2E tests
│   ├── package.json              # Node.js dependencies
│   └── playwright.config.ts      # Playwright configuration
│
├── 📂 .github/
│   └── 📂 workflows/
│       └── ci.yml                # CI/CD pipeline configuration
│
├── docker-compose.yml            # Multi-container Docker setup
├── Dockerfile                    # Application container definition
├── requirements.txt              # Python dependencies
├── pytest.ini                    # Pytest configuration
├── .env.example                  # Environment variables template
└── README.md                     # This file
```

---

## 🚀 Quick Start

### Prerequisites
- Python 3.11+
- Docker & Docker Compose
- PostgreSQL 15+ (or use Docker)

### 1️⃣ Clone the Repository
```bash
git clone https://github.com/Vishesh0-7/fastapi-sqlalchemy-calculator.git
cd fastapi-sqlalchemy-calculator
```

### 2️⃣ Set Up Environment Variables
```bash
cp .env.example .env
# Edit .env with your configuration
```

### 3️⃣ Run with Docker (Recommended)
```bash
# Start all services (app, database, pgAdmin)
docker-compose up -d

# View logs
docker-compose logs -f app

# Stop services
docker-compose down
```

**Access the application:**
- 🌐 Web Interface: http://localhost:8000
- 📚 API Documentation: http://localhost:8000/docs
- 🔧 pgAdmin: http://localhost:5050

### 4️⃣ Run Locally (Development)
```bash
# Create virtual environment
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Set up database (PostgreSQL must be running)
export DATABASE_URL="postgresql://user:pass@localhost:5432/calculator_db"

# Run the server
uvicorn app.main:app --reload

# Server available at http://localhost:8000
```

---

## 🧪 Testing

### Run All Tests
```bash
# Unit + Integration tests with coverage
pytest tests/ --cov=app --cov-report=html

# View coverage report
open htmlcov/index.html
```

### Run E2E Tests
```bash
cd e2e
npm install
npx playwright install chromium
npm test
```

### Run Specific Test Suites
```bash
# Authentication tests only
pytest tests/test_auth.py -v

# Unit tests only
pytest tests/unit/ -v

# New operations tests
pytest tests/unit/test_new_operations.py -v
pytest tests/unit/test_profile_schemas.py -v

# Integration tests only
pytest tests/integration/ -v

# New feature integration tests
pytest tests/integration/test_profile_routes.py -v
pytest tests/integration/test_dashboard_routes.py -v
pytest tests/integration/test_new_operations_routes.py -v

# E2E tests
cd e2e
npm test tests/auth.spec.ts
npm test tests/calculations.spec.ts
npm test tests/profile.spec.ts        # NEW
npm test tests/dashboard.spec.ts      # NEW
npm test tests/new_operations.spec.ts # NEW
```

### Test Coverage

The project maintains comprehensive test coverage:

**Unit Tests:**
- ✅ All calculation operations (including Power & Modulus)
- ✅ Password hashing and verification
- ✅ Schema validations (profiles, password change)
- ✅ Statistics calculations

**Integration Tests:**
- ✅ Profile update routes (username, email)
- ✅ Password change workflow
- ✅ Dashboard statistics endpoints
- ✅ New calculation operations (Power, Modulus)
- ✅ User isolation and data integrity

**E2E Tests (Playwright):**
- ✅ Profile viewing and updates
- ✅ Password change with re-login
- ✅ Dashboard statistics display
- ✅ Power and Modulus operations full workflow
- ✅ Navigation between pages
- ✅ Client-side validations

---

## 🌐 Using the Web Interface

### Landing Page
Navigate to `http://localhost:8000` to access the landing page with options to:
- Login to existing account
- Register new account
- View API documentation

### User Registration
1. Navigate to `http://localhost:8000/frontend/register.html`
2. Fill in email, username, and password
3. Click "Create Account"
4. You'll be automatically logged in and redirected to the calculator

### User Login
1. Navigate to `http://localhost:8000/frontend/login.html`
2. Enter your email/username and password
3. Click "Sign In"
4. You'll be redirected to the calculator interface

### Calculator Interface
**Quick Calculator** (`/static/index.html`):
- Simple calculator for immediate calculations
- Operations: Add, Subtract, Multiply, Divide
- Results displayed instantly
- All calculations saved to your history

### Calculation History Management
**Full BREAD Interface** (`/frontend/calculations.html`):
- **Browse**: View all your past calculations in a table
- **Add**: Create new calculations with instant feedback
- **Read**: Click "Edit" to view calculation details
- **Edit**: Modify operands and operations, results recompute automatically
- **Delete**: Remove calculations with confirmation prompt

**Features:**
- ✅ Client-side validation (no page refresh for errors)
- ✅ Real-time result calculation
- ✅ Success/error messages with auto-dismiss
- ✅ Responsive table design
- ✅ Modal-based editing for better UX
- ✅ Automatic token management (logout on expiry)

**Navigation:**
- Calculations Page → Dashboard/Profile (via header buttons)
- Dashboard → Calculations/Profile (via navigation)
- Profile → Calculations/Dashboard (via navigation)
- Any Page → Logout (via "Logout" button)

---

## 🆕 New Features (Module 14)

### 1. Extended Calculation Operations

#### Power Operation (Exponentiation)
Calculate a number raised to a power: `a^b`

**Examples:**
- `2^3 = 8`
- `10^2 = 100`
- `5^0 = 1`
- `2^-2 = 0.25` (negative exponents supported)

**Usage in UI:**
- Select "Power (^)" from operation dropdown
- Enter base number in operand 1
- Enter exponent in operand 2

**API Endpoint:**
```http
POST /calculations/
Content-Type: application/json
Authorization: Bearer <token>

{
  "a": 2,
  "b": 8,
  "type": "Power"
}

Response: {"result": 256}
```

#### Modulus Operation (Remainder)
Calculate the remainder after division: `a % b`

**Examples:**
- `10 % 3 = 1`
- `20 % 5 = 0`
- `17 % 5 = 2`

**Usage in UI:**
- Select "Modulus (%)" from operation dropdown
- Enter dividend in operand 1
- Enter divisor in operand 2

**Validation:**
- Modulus by zero returns an error

**API Endpoint:**
```http
POST /calculations/
Content-Type: application/json
Authorization: Bearer <token>

{
  "a": 17,
  "b": 5,
  "type": "Modulus"
}

Response: {"result": 2}
```

### 2. User Profile Management

Access your profile at `/frontend/profile.html`

#### View Profile Information
- Current username
- Current email
- User ID
- Account status

#### Update Profile
**Change Username:**
```http
PUT /profile/me
Authorization: Bearer <token>
Content-Type: application/json

{
  "username": "new_username"
}
```

**Change Email:**
```http
PUT /profile/me
Authorization: Bearer <token>
Content-Type: application/json

{
  "email": "newemail@example.com"
}
```

**Update Both:**
```http
PUT /profile/me
Authorization: Bearer <token>
Content-Type: application/json

{
  "username": "new_username",
  "email": "newemail@example.com"
}
```

**Features:**
- ✅ Real-time validation
- ✅ Duplicate username/email detection
- ✅ Immediate UI updates after successful change
- ✅ At least one field must be provided

### 3. Password Change

Secure password update functionality with forced re-login.

**Endpoint:**
```http
POST /profile/change-password
Authorization: Bearer <token>
Content-Type: application/json

{
  "current_password": "oldpass123",
  "new_password": "newpass456"
}
```

**Security Features:**
- ✅ Current password verification required
- ✅ New password must be different from current
- ✅ Minimum 6 characters validation
- ✅ Password confirmation in UI
- ✅ Automatic logout after change
- ✅ Must re-login with new password

**Validation Rules:**
1. Current password must be correct
2. New password ≥ 6 characters
3. New password ≠ current password
4. Confirm password must match new password

**Workflow:**
1. User enters current password
2. User enters new password (validated client-side)
3. User confirms new password
4. Backend verifies current password
5. Backend hashes and stores new password
6. User automatically logged out
7. User must log in with new password

### 4. Dashboard & Statistics

Comprehensive analytics dashboard at `/frontend/dashboard.html`

**Features:**
- 📊 Visual statistics display
- 📈 Operations breakdown with progress bars
- 🎯 Most frequently used operation
- 📉 Average calculation result
- 🔢 Total calculations count

**API Endpoint:**
```http
GET /dashboard/stats
Authorization: Bearer <token>

Response:
{
  "total_calculations": 42,
  "operations_breakdown": {
    "Add": 15,
    "Multiply": 10,
    "Divide": 8,
    "Sub": 5,
    "Power": 3,
    "Modulus": 1
  },
  "most_used_operation": "Add",
  "average_result": 127.5
}
```

**Dashboard UI Components:**

**Stat Cards:**
- Total Calculations (highlighted primary card)
- Most Used Operation
- Average Result (formatted to 2 decimals)

**Operations Breakdown:**
- Visual progress bars for each operation type
- Count displayed on each bar
- Sorted by frequency (most used first)
- Dynamic width based on percentage

**Empty State:**
- Friendly message when no calculations exist
- Call-to-action button to create first calculation

---

## 📖 API Documentation

### Authentication Endpoints

#### Register User
```http
POST /auth/register
Content-Type: application/json

{
  "email": "user@example.com",
  "username": "johndoe",
  "password": "SecurePass123"
}
```

**Response:**
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIs...",
  "token_type": "bearer"
}
```

#### Login
```http
POST /auth/login
Content-Type: application/json

{
  "username_or_email": "user@example.com",
  "password": "SecurePass123"
}
```

### Calculation Endpoints

#### Create Calculation
```http
POST /calculations/
Authorization: Bearer <token>
Content-Type: application/json

{
  "a": 10,
  "b": 5,
  "type": "Add"
}
```

**Response:**
```json
{
  "id": 1,
  "a": 10,
  "b": 5,
  "type": "Add",
  "result": 15,
  "user_id": 1,
  "created_at": "2025-11-30T12:00:00"
}
```

#### Get All Calculations
```http
GET /calculations/
Authorization: Bearer <token>
```

#### Get Calculation by ID
```http
GET /calculations/{id}
Authorization: Bearer <token>
```

#### Update Calculation
```http
PUT /calculations/{id}
Authorization: Bearer <token>
Content-Type: application/json

{
  "a": 20,
  "b": 4,
  "type": "Multiply"
}
```

#### Delete Calculation
```http
DELETE /calculations/{id}
Authorization: Bearer <token>
```

### User Endpoints

#### Get All Users
```http
GET /users/
```

#### Get User by ID
```http
GET /users/{id}
```

#### Update User
```http
PUT /users/{id}
Authorization: Bearer <token>
Content-Type: application/json

{
  "email": "newemail@example.com",
  "username": "newusername"
}
```

#### Delete User
```http
DELETE /users/{id}
Authorization: Bearer <token>
```

---

## 🗄️ Database Migrations (Alembic)

This project uses Alembic for database schema version control.

### Initial Setup

The project includes a pre-configured Alembic setup with an initial migration for the base schema.

```bash
# View current migration status
alembic current

# View migration history
alembic history

# Upgrade to latest version
alembic upgrade head

# Downgrade one version
alembic downgrade -1
```

### Creating New Migrations

When you modify SQLAlchemy models, create a new migration:

```bash
# Auto-generate migration from model changes
alembic revision --autogenerate -m "Add new column to users table"

# Create empty migration (for manual changes)
alembic revision -m "Custom migration"

# Apply the migration
alembic upgrade head
```

### Migration Files

Migrations are stored in `alembic/versions/`:
- `001_initial.py` - Base schema (users & calculations tables)
- Future migrations will be added here

### Configuration

- **alembic.ini**: Main configuration file
- **alembic/env.py**: Migration environment setup
- **alembic/script.py.mako**: Template for new migrations

### Docker and Migrations

When using Docker, migrations can be run inside the container:

```bash
# Run migrations in Docker
docker-compose exec app alembic upgrade head

# Check current version in Docker
docker-compose exec app alembic current
```

### Best Practices

1. **Always test migrations** on a development database first
2. **Review auto-generated migrations** before applying
3. **Add both upgrade and downgrade** functions
4. **Use descriptive migration messages**
5. **Don't modify existing migrations** once applied to production

---

## 🔐 Security Features

- **Password Hashing**: bcrypt with automatic salt generation
- **JWT Tokens**: HS256 algorithm, 30-minute expiration
- **Input Validation**: Pydantic schemas with type checking
- **SQL Injection Protection**: SQLAlchemy ORM parameterized queries
- **CORS Configuration**: Properly configured cross-origin requests
- **Error Handling**: Secure error messages without sensitive data exposure

---

## 🐳 Docker Configuration

### Services

**App (FastAPI)**
- Port: 8000
- Auto-reload on file changes
- Environment variables from .env

**PostgreSQL Database**
- Port: 5432
- Persistent volume storage
- Health checks configured

**pgAdmin**
- Port: 5050
- Web-based database management
- Pre-configured connection

### Docker Commands
```bash
# Build and start
docker-compose up --build

# Start in detached mode
docker-compose up -d

# View logs
docker-compose logs -f

# Stop services
docker-compose down

# Remove volumes (clean slate)
docker-compose down -v

# Rebuild app only
docker-compose build app
docker-compose up -d app
```

---

## 🤝 Contributing

Contributions are welcome! Please follow these steps:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

### Development Guidelines
- Write tests for new features
- Maintain 100% code coverage
- Follow PEP 8 style guide
- Update documentation as needed
- Run tests before committing

---

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## 👤 Author

**Vishesh Patel**

- GitHub: [@Vishesh0-7](https://github.com/Vishesh0-7)
- LinkedIn: [Vishesh Patel](https://linkedin.com/in/vishesh-patel)

---

## 🙏 Acknowledgments

- FastAPI documentation and community
- NJIT IS601 Course Materials
- All contributors and testers

---

## 📞 Support

If you have any questions or issues, please:
- Open an issue on [GitHub](https://github.com/Vishesh0-7/fastapi-sqlalchemy-calculator/issues)
- Check the [API Documentation](http://localhost:8000/docs)
- Review the [QUICKSTART Guide](QUICKSTART.md)

---

**Made with ❤️ using FastAPI**
