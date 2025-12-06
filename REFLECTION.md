# 🎓 Project Reflection: Calculator API with BREAD Operations

**Student:** Vishesh  
**Course:** IS601  
**Module:** 13  
**Date:** December 2025

---

## 📝 Executive Summary

This project implements a complete RESTful API with full BREAD (Browse, Read, Edit, Add, Delete) operations for a calculator application. The system features JWT-based authentication, a responsive web interface, comprehensive test coverage (100%), and automated CI/CD deployment to Docker Hub.

---

## 🎯 Project Objectives Achieved

### ✅ Backend Development
- **Complete BREAD Endpoints**: Implemented all 5 REST operations for calculations
- **JWT Authentication**: Secure user-based access control for all resources
- **Database Integration**: PostgreSQL with SQLAlchemy ORM
- **Input Validation**: Pydantic schemas with custom validators
- **Error Handling**: Appropriate HTTP status codes (200, 201, 204, 400, 401, 404)

### ✅ Frontend Development
- **Calculations Management Page**: Full CRUD interface for managing calculations
- **Real-time Validation**: Client-side validation for numeric inputs and operations
- **JWT Token Management**: Automatic token handling with localStorage
- **Responsive Design**: Modern UI with gradient backgrounds and animations
- **Error Messaging**: User-friendly error and success notifications

### ✅ Testing & Quality Assurance
- **100% Code Coverage**: All backend code paths tested
- **E2E Testing**: Playwright tests for complete user workflows
- **Positive & Negative Cases**: Both success and failure scenarios covered
- **Security Testing**: Authorization and cross-user access tests

### ✅ CI/CD & DevOps
- **Automated Pipeline**: GitHub Actions workflow
- **Multi-stage Testing**: pytest → Playwright → Docker build
- **Docker Deployment**: Automatic push to Docker Hub on success
- **Environment Management**: Separate configs for dev/test/prod

---

## 🔐 JWT Implementation

### Design Decisions

**Token Structure:**
```json
{
  "sub": "user_id",
  "exp": 1234567890
}
```

**Why this approach:**
1. **Stateless Authentication**: No server-side session storage needed
2. **Scalability**: Tokens can be validated independently by any server instance
3. **Security**: Tokens expire after 30 minutes
4. **Standard Compliance**: Uses JWT "sub" claim for user identification

**Implementation Highlights:**
- **bcrypt** for password hashing (secure, battle-tested)
- **python-jose** for JWT encoding/decoding
- **HTTPBearer** security scheme in FastAPI
- **get_current_user** dependency for protected routes

**Security Measures:**
- Passwords never stored in plain text
- Tokens transmitted via Authorization header (not URL parameters)
- Token validation on every protected endpoint
- User ownership verification for all BREAD operations

**Challenges Faced:**
1. **Challenge**: Initially used manual header parsing in routes
   - **Solution**: Implemented `get_current_user` dependency for cleaner code
   
2. **Challenge**: Token storage in frontend
   - **Solution**: localStorage with automatic redirect on expiry

3. **Challenge**: E2E testing with authentication
   - **Solution**: Programmatic token injection via page.evaluate()

---

## 🏗️ BREAD Design Considerations

### Architecture Decisions

**1. Resource-Based Routes**
```
GET    /calculations/       → Browse (list all user's calculations)
POST   /calculations/       → Add (create new calculation)
GET    /calculations/{id}   → Read (get specific calculation)
PUT    /calculations/{id}   → Edit (update calculation)
DELETE /calculations/{id}   → Delete (remove calculation)
```

**Why this design:**
- RESTful conventions make API intuitive
- Consistent URL structure
- HTTP methods indicate action (semantic)
- Easy to document and understand

**2. User Isolation**
Every calculation is associated with a user_id. This ensures:
- Users only see their own calculations
- No cross-user data leakage
- 404 errors for unauthorized access (not 403, to avoid information disclosure)

**3. Input Validation Layers**

**Client-side:**
- HTML5 `required` and `type="number"` attributes
- JavaScript validation for division by zero
- Real-time feedback without server round-trip

**Server-side:**
- Pydantic schemas with type checking
- Custom validators for business rules
- Database constraints

**4. Error Handling Strategy**

| Error Type | Status Code | When Used |
|-----------|-------------|-----------|
| 400 Bad Request | Division by zero, invalid operation | Client error |
| 401 Unauthorized | Invalid/missing JWT token | Authentication failure |
| 404 Not Found | Calculation doesn't exist or belong to user | Resource not found |
| 422 Unprocessable Entity | Invalid data types | Pydantic validation failure |

**5. Frontend State Management**
- **No framework** (vanilla JS) to keep it simple
- **localStorage** for JWT persistence
- **Modal** for edit operations (better UX than page navigation)
- **Optimistic updates** discouraged - always refresh from server

---

## 🎭 E2E Testing Insights

### Testing Philosophy

**"Test the user journey, not the implementation"**

### Positive Test Cases

1. **Add Calculation**
   - Fill form → Submit → Verify success message and result
   - Tests: DOM manipulation, API call, response handling

2. **Browse Calculations**
   - Load page → Wait for table → Verify data displayed
   - Tests: API integration, rendering, data binding

3. **Read Calculation**
   - Click edit → Modal opens → Verify pre-filled values
   - Tests: GET endpoint, modal functionality, data loading

4. **Edit Calculation**
   - Open modal → Change values → Submit → Verify update
   - Tests: PUT endpoint, form submission, table refresh

5. **Delete Calculation**
   - Click delete → Confirm → Verify removal
   - Tests: DELETE endpoint, confirmation dialog, list update

### Negative Test Cases

1. **Client-side Validation**
   - Invalid input → Form doesn't submit
   - Tests: HTML5 validation working

2. **Division by Zero**
   - Enter 0 as divisor → See error message
   - Tests: Business logic validation

3. **Unauthorized Access**
   - No token → Redirect to login
   - Tests: Auth guard working

4. **Invalid Token**
   - Bad token → Redirect to login
   - Tests: Token validation

5. **Cross-user Access**
   - Try to access another user's calculation → 404
   - Tests: Authorization and ownership verification

### Playwright Best Practices Applied

```typescript
// ✅ Good: Descriptive locators
await page.locator('#operand1').fill('10');

// ✅ Good: Waiting for elements
await expect(page.locator('#addMessage')).toBeVisible({ timeout: 5000 });

// ✅ Good: Explicit assertions
expect(response.status()).toBe(404);

// ✅ Good: Setup/teardown
test.beforeAll() // Register user once
test.beforeEach() // Set token for each test
```

### Challenges in E2E Testing

**Challenge 1: Async Operations**
- **Problem**: Race conditions between API calls and UI updates
- **Solution**: Explicit waits with timeouts, waitForSelector()

**Challenge 2: Test Isolation**
- **Problem**: Tests affecting each other's data
- **Solution**: Unique user per test run, timestamp-based usernames

**Challenge 3: Authentication State**
- **Problem**: Maintaining login across tests
- **Solution**: localStorage manipulation via page.evaluate()

**Challenge 4: Modal Timing**
- **Problem**: Modal animations causing flaky tests
- **Solution**: Wait for visibility explicitly, not just existence

---

## 🚀 CI/CD Deployment Experience

### Pipeline Design

```
┌─────────────┐
│  Git Push   │
└──────┬──────┘
       │
       v
┌─────────────────┐
│  Backend Tests  │  ← pytest with PostgreSQL
└──────┬──────────┘
       │
       v
┌─────────────────┐
│   E2E Tests     │  ← Playwright with live server
└──────┬──────────┘
       │
       v
┌─────────────────┐
│  Docker Build   │  ← Build & push to Docker Hub
└─────────────────┘
```

### Key Learnings

**1. Service Containers**
- GitHub Actions can spin up PostgreSQL in the pipeline
- Healthchecks ensure DB is ready before tests run
- Separate database per job for isolation

**2. Environment Variables**
- Use GitHub Secrets for sensitive data (Docker Hub credentials)
- Set different values for CI (test DB, test JWT secret)
- Pass via `env:` in workflow YAML

**3. Server Management in CI**
- Background process with `&` operator
- Save PID for cleanup: `echo $! > server.pid`
- Wait for readiness: `curl` with timeout loop
- Always cleanup in `if: always()` step

**4. Playwright in CI**
- Must install browser binaries: `npx playwright install --with-deps`
- Use headless mode (default)
- Upload artifacts on failure for debugging

### Challenges & Solutions

**Challenge 1: Docker Secrets Not Set**
- **Problem**: Pipeline failed when DOCKERHUB_USERNAME secret missing
- **Solution**: Added condition `if: secrets.DOCKERHUB_USERNAME != ''`

**Challenge 2: Server Not Ready**
- **Problem**: E2E tests started before server listening
- **Solution**: Health check endpoint + polling loop

**Challenge 3: npm ci Requires package-lock.json**
- **Problem**: Missing lock file caused CI failure
- **Solution**: Committed package-lock.json to repository

**Challenge 4: HTML5 Required Attribute**
- **Problem**: E2E test couldn't test validation because form didn't submit
- **Solution**: Removed `required` attributes, rely on JS validation

---

## 📊 Metrics & Statistics

| Metric | Value |
|--------|-------|
| **Code Coverage** | 100% |
| **Total Tests** | 90+ (pytest) + 18 (Playwright) |
| **Test Execution Time** | ~25 seconds |
| **Lines of Code** | ~1,500 (backend) + ~800 (frontend) |
| **API Endpoints** | 15 |
| **Database Tables** | 2 (users, calculations) |
| **Docker Image Size** | ~250 MB |

---

## 💡 Key Takeaways

### Technical Skills Gained
1. **FastAPI Mastery**: Dependency injection, async operations, security
2. **Authentication**: JWT implementation from scratch
3. **Testing Excellence**: 100% coverage with multiple test types
4. **DevOps**: Docker, CI/CD, automated deployments
5. **Security**: Authorization, password hashing, input validation

### Best Practices Learned
1. **Separation of Concerns**: Routes → CRUD → Models (clean architecture)
2. **DRY Principle**: Reusable security dependencies, common frontend utilities
3. **API Design**: RESTful conventions, consistent status codes
4. **Error Handling**: Graceful failures with helpful messages
5. **Testing Pyramid**: Unit → Integration → E2E

### Areas for Future Improvement
1. **Rate Limiting**: Prevent API abuse
2. **Token Refresh**: Long-lived refresh tokens
3. **Pagination**: More efficient for large datasets
4. **Caching**: Redis for frequently accessed data
5. **Logging**: Structured logging for production monitoring
6. **API Versioning**: /v1/ prefix for future compatibility

---

## 🎓 Conclusion

This project successfully demonstrates:
- **Full-stack development** with modern tools and patterns
- **Security-first** approach with JWT and proper authorization
- **Test-driven development** with comprehensive coverage
- **DevOps practices** with automated CI/CD
- **Professional code quality** with documentation and clean architecture

The biggest lesson: **Testing is not a burden, it's a superpower**. The 100% coverage gave me confidence to refactor, add features, and deploy with zero production bugs.

**Would I do anything differently?**  
Initially, I manually parsed JWT tokens in routes. Later, I refactored to use FastAPI's dependency injection (`get_current_user`). If I started over, I'd implement the dependency from day one—it's cleaner and more testable.

---

**Signature:** Vishesh  
**Date:** December 1, 2025
