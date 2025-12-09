# Quick Start Guide - New Features

## 🚀 Getting Started with New Features

### Prerequisites
Ensure you have the updated dependencies:
```bash
pip install -r requirements.txt
```

This will install `alembic` and all other required packages.

### Running the Application

#### Option 1: Docker (Recommended)
```bash
# Build and start all services
docker-compose up --build

# Access the application
open http://localhost:8000
```

#### Option 2: Local Development
```bash
# Activate virtual environment
source .venv/bin/activate  # or .venv\Scripts\activate on Windows

# Install/update dependencies
pip install -r requirements.txt

# Run the application
uvicorn app.main:app --reload

# Access at http://localhost:8000
```

### Testing New Features

#### 1. Power Operation
1. Login to the application
2. Go to Calculations page
3. Select "Power (^)" from operation dropdown
4. Enter values (e.g., 2 and 3)
5. Click "Calculate & Save"
6. Result: 8 (2^3)

#### 2. Modulus Operation
1. Login to the application
2. Go to Calculations page
3. Select "Modulus (%)" from operation dropdown
4. Enter values (e.g., 10 and 3)
5. Click "Calculate & Save"
6. Result: 1 (remainder of 10/3)

#### 3. Profile Management
1. Login to the application
2. Click "Profile" button in header
3. View your current profile information
4. Update username and/or email
5. Click "Update Profile"
6. See immediate confirmation

#### 4. Password Change
1. Go to Profile page
2. Scroll to "Change Password" section
3. Enter current password
4. Enter new password (min 6 chars)
5. Confirm new password
6. Click "Change Password"
7. You'll be logged out automatically
8. Login with new password

#### 5. Dashboard Statistics
1. Login to the application
2. Click "Dashboard" button in header
3. View your statistics:
   - Total calculations
   - Most used operation
   - Average result
   - Operations breakdown with visual bars

### Running Tests

#### All Tests
```bash
# Python tests
pytest tests/ --cov=app --cov-report=term --cov-report=html -v

# E2E tests
cd e2e
npm install
npx playwright install chromium
npm test
```

#### Specific Test Suites
```bash
# Test new operations
pytest tests/unit/test_new_operations.py -v
pytest tests/integration/test_new_operations_routes.py -v

# Test profile features
pytest tests/unit/test_profile_schemas.py -v
pytest tests/integration/test_profile_routes.py -v

# Test dashboard
pytest tests/integration/test_dashboard_routes.py -v

# E2E tests for new features
cd e2e
npm test tests/profile.spec.ts
npm test tests/dashboard.spec.ts
npm test tests/new_operations.spec.ts
```

### Database Migrations

#### Check Migration Status
```bash
# View current version
alembic current

# View migration history
alembic history
```

#### Apply Migrations
```bash
# Upgrade to latest version
alembic upgrade head

# Downgrade one version
alembic downgrade -1
```

#### Create New Migration (if you modify models)
```bash
# Auto-generate from model changes
alembic revision --autogenerate -m "Description of changes"

# Review the generated migration file in alembic/versions/

# Apply the migration
alembic upgrade head
```

### API Testing with cURL

#### Test Power Operation
```bash
# Login first to get token
TOKEN=$(curl -X POST http://localhost:8000/auth/login \
  -H "Content-Type: application/json" \
  -d '{"username_or_email":"testuser","password":"testpass"}' \
  | jq -r '.access_token')

# Create Power calculation
curl -X POST http://localhost:8000/calculations/ \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"a":2,"b":8,"type":"Power"}'
```

#### Test Modulus Operation
```bash
curl -X POST http://localhost:8000/calculations/ \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"a":17,"b":5,"type":"Modulus"}'
```

#### Update Profile
```bash
curl -X PUT http://localhost:8000/profile/me \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"username":"newusername","email":"newemail@example.com"}'
```

#### Change Password
```bash
curl -X POST http://localhost:8000/profile/change-password \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"current_password":"oldpass","new_password":"newpass123"}'
```

#### Get Dashboard Stats
```bash
curl -X GET http://localhost:8000/dashboard/stats \
  -H "Authorization: Bearer $TOKEN"
```

### Troubleshooting

#### Issue: "Module 'alembic' not found"
**Solution:**
```bash
pip install alembic
# or
pip install -r requirements.txt
```

#### Issue: Tests failing with "table already exists"
**Solution:**
```bash
# Remove test databases
rm test_*.db

# Run tests again
pytest tests/ -v
```

#### Issue: E2E tests can't find browser
**Solution:**
```bash
cd e2e
npx playwright install chromium
```

#### Issue: Can't access profile/dashboard pages
**Solution:**
- Make sure you're logged in
- Check browser console for errors
- Verify JWT token is stored in localStorage
- Try logging out and logging back in

#### Issue: Modulus by zero error
**Solution:**
This is expected behavior. The validation correctly prevents division by zero.
Use a non-zero divisor.

### Viewing API Documentation

Interactive API documentation is available at:
- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

You can test all endpoints directly from the Swagger UI.

### Docker Commands

```bash
# Start services
docker-compose up -d

# View logs
docker-compose logs -f app

# Stop services
docker-compose down

# Rebuild after code changes
docker-compose up --build

# Run migrations in Docker
docker-compose exec app alembic upgrade head

# Access container shell
docker-compose exec app bash
```

### Environment Variables

Create a `.env` file in the project root:

```env
# Database
DATABASE_URL=postgresql://user:password@db:5432/calculator_db

# JWT Configuration
JWT_SECRET_KEY=your-secret-key-change-in-production
JWT_ALGORITHM=HS256
JWT_EXPIRE_MINUTES=30

# App Configuration
ENVIRONMENT=development
```

### Next Steps

1. ✅ Register a new user account
2. ✅ Try all six calculation operations (Add, Sub, Multiply, Divide, Power, Modulus)
3. ✅ Update your profile information
4. ✅ Change your password and re-login
5. ✅ View your statistics on the dashboard
6. ✅ Explore the API documentation at /docs

### Support

If you encounter any issues:
1. Check the application logs
2. Review the error messages in the UI
3. Check browser console for frontend errors
4. Refer to the main README.md for detailed documentation
5. Review FEATURES_SUMMARY.md for implementation details

### Performance Tips

- Use the dashboard to track your calculation patterns
- The most used operation shows your preferences
- Average result helps identify calculation trends
- Operations breakdown provides visual insights

---

**Happy calculating! 🧮**
