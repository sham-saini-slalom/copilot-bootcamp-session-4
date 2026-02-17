# User Authentication & Authorization System

This implementation adds secure user authentication to the Slalom Capabilities Management System.

## Features Implemented

### 🔐 Security Features
- **Password Hashing**: Uses bcrypt with 12+ rounds for secure password storage
- **JWT Tokens**: Stateless authentication with 24-hour token expiration
- **Protected Endpoints**: Capability registration/unregistration now require authentication
- **User-Specific Actions**: Users can only register/unregister themselves

### 📋 New API Endpoints

#### Authentication Endpoints

**POST /auth/register**
- Register a new user account
- Request body:
  ```json
  {
    "email": "user@slalom.com",
    "password": "securepassword123",
    "first_name": "John",
    "last_name": "Doe"
  }
  ```
- Password must be at least 8 characters
- Returns user information (without password)

**POST /auth/login**
- Authenticate and receive JWT token
- Request body:
  ```json
  {
    "email": "user@slalom.com",
    "password": "securepassword123"
  }
  ```
- Returns:
  ```json
  {
    "access_token": "eyJ0eXAiOiJKV1QiLCJhbGc...",
    "token_type": "bearer",
    "user": {
      "email": "user@slalom.com",
      "first_name": "John",
      "last_name": "Doe",
      "created_at": "2026-02-17T23:30:00"
    }
  }
  ```

**GET /auth/me**
- Get current authenticated user information
- Requires: `Authorization: Bearer <token>` header
- Returns current user details

#### Protected Endpoints (Now Require Authentication)

**POST /capabilities/{capability_name}/register**
- Registers the authenticated user for a capability
- Requires: `Authorization: Bearer <token>` header
- No longer needs email in request body (uses authenticated user)

**DELETE /capabilities/{capability_name}/unregister**
- Unregisters the authenticated user from a capability
- Requires: `Authorization: Bearer <token>` header
- No longer needs email in request body (uses authenticated user)

## Usage Examples

### 1. Register a New User
```bash
curl -X POST http://localhost:8000/auth/register \
  -H "Content-Type: application/json" \
  -d '{
    "email": "alice@slalom.com",
    "password": "MySecurePass123",
    "first_name": "Alice",
    "last_name": "Smith"
  }'
```

### 2. Login
```bash
curl -X POST http://localhost:8000/auth/login \
  -H "Content-Type: application/json" \
  -d '{
    "email": "alice@slalom.com",
    "password": "MySecurePass123"
  }'
```

Save the `access_token` from the response.

### 3. Register for a Capability (Authenticated)
```bash
curl -X POST http://localhost:8000/capabilities/Cloud%20Architecture/register \
  -H "Authorization: Bearer <your_token_here>"
```

### 4. Get Current User Info
```bash
curl -X GET http://localhost:8000/auth/me \
  -H "Authorization: Bearer <your_token_here>"
```

### 5. Unregister from a Capability (Authenticated)
```bash
curl -X DELETE http://localhost:8000/capabilities/Cloud%20Architecture/unregister \
  -H "Authorization: Bearer <your_token_here>"
```

## Technical Implementation

### Files Added/Modified

**New Files:**
- `src/auth.py` - Authentication utilities (JWT, password hashing)
- `src/models.py` - Pydantic models for requests/responses
- `src/AUTH_README.md` - This documentation

**Modified Files:**
- `src/app.py` - Added auth endpoints and protected routes
- `requirements.txt` - Added authentication dependencies

### Dependencies Added
- `python-jose[cryptography]` - JWT token handling
- `passlib[bcrypt]` - Password hashing
- `python-multipart` - Form data parsing
- `pydantic[email]` - Email validation

### Security Configuration
- **Secret Key**: Currently hardcoded (TODO: Move to environment variable)
- **Token Expiration**: 24 hours
- **Password Requirements**: Minimum 8 characters
- **Algorithm**: HS256 for JWT signing

## Installation

Install the new dependencies:
```bash
pip install -r requirements.txt
```

## Production Considerations

⚠️ **Before deploying to production:**

1. **Move SECRET_KEY to environment variable**
   ```python
   SECRET_KEY = os.getenv("JWT_SECRET_KEY")
   ```

2. **Use HTTPS** - JWT tokens should only be transmitted over HTTPS

3. **Add rate limiting** on authentication endpoints to prevent brute force attacks

4. **Implement database persistence** - Currently using in-memory storage

5. **Add password reset functionality** via email

6. **Consider adding refresh tokens** for longer sessions

7. **Add account lockout** after multiple failed login attempts

8. **Implement proper logging** for security events

## Testing

You can test the authentication flow using the FastAPI interactive docs at:
`http://localhost:8000/docs`

The Swagger UI includes an "Authorize" button where you can enter your JWT token for testing protected endpoints.

## Related Issues

This implementation addresses:
- ✅ Issue #10: Add User Authentication & Authorization System

Dependencies:
- 🔴 Still needs Issue #9 (Database Persistence) for production use
