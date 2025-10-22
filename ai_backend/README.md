// ============================================
// FILE: README.md (Backend)
// ============================================
# MERN Stack Backend

Backend API server for MERN stack application with AI integration.

## Features

- RESTful API with Express.js
- MongoDB database with Mongoose ODM
- JWT authentication & authorization
- Role-based access control
- Input validation
- Error handling middleware
- Rate limiting
- Security headers with Helmet
- AI service integration
- Email service (Nodemailer)
- Logging utility

## Installation

1. Install dependencies:
```bash
npm install
```

2. Create .env file:
```bash
cp .env.example .env
```

3. Update .env with your configuration

4. Start MongoDB:
```bash
mongod
```

5. Run the server:
```bash
# Development
npm run dev

# Production
npm start
```

## API Endpoints

### Authentication
- POST /api/auth/register - Register new user
- POST /api/auth/login - Login user
- GET /api/auth/me - Get current user
- PUT /api/auth/update-password - Update password

### Users
- GET /api/users - Get all users (Admin only)
- GET /api/users/:id - Get user by ID
- PUT /api/users/profile - Update user profile
- DELETE /api/users/:id - Delete user (Admin only)

### Posts/Data
- GET /api/data/posts - Get all posts
- GET /api/data/posts/:id - Get post by ID
- POST /api/data/posts - Create post (Auth required)
- PUT /api/data/posts/:id - Update post (Auth required)
- DELETE /api/data/posts/:id - Delete post (Auth required)
- POST /api/data/posts/:id/like - Like/unlike post (Auth required)

### AI Service
- POST /api/ai/process - Process AI request (Auth required)
- GET /api/ai/history - Get AI request history (Auth required)
- GET /api/ai/requests/:id - Get AI request by ID (Auth required)

## Environment Variables

See `.env.example` for required environment variables.

## Project Structure

```
backend/
├── src/
│   ├── config/          # Configuration files
│   ├── controllers/     # Route controllers
│   ├── middleware/      # Custom middleware
│   ├── models/          # Mongoose models
│   ├── routes/          # Express routes
│   ├── services/        # Business logic
│   ├── utils/           # Utility functions
│   ├── validators/      # Input validation
│   └── app.js           # Express app setup
├── server.js            # Server entry point
├── package.json
└── .env

```

## Testing

```bash
npm test
```

## License

MIT