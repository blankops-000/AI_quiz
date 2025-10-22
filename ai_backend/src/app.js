// ============================================
// FILE: src/app.js
// ============================================
const express = require('express');
const cors = require('cors');
const helmet = require('helmet');
const morgan = require('morgan');

// Import routes
const authRoutes = require('./routes/authroutes');
const userRoutes = require('./routes/userroutes');
const dataRoutes = require('./routes/dataroutes');
const aiRoutes = require('./routes/airoutes');

// Import middleware
const errorMiddleware = require('./middleware/errormiddleware');

const app = express();

// Security middleware
app.use(helmet());
app.use(cors({
  origin: process.env.FRONTEND_URL || 'http://localhost:3000',
  credentials: true
}));

// Body parser middleware
app.use(express.json({ limit: '10mb' }));
app.use(express.urlencoded({ extended: true, limit: '10mb' }));

// Logging middleware
if (process.env.NODE_ENV === 'development') {
  app.use(morgan('dev'));
}

// Rate limiting middleware
// Fix in app.js
const rateLimiterModule = require('./middleware/rateLimitermiddleware');
const rateLimiter = rateLimiterModule.default || rateLimiterModule;


console.log('Rate limiter type:', typeof rateLimiter);
console.log('Rate limiter content:', rateLimiter);
app.use(rateLimiter);


// API Routes
app.use('/api/auth', authRoutes);
app.use('/api/users', userRoutes);
app.use('/api/data', dataRoutes);
app.use('/api/ai', aiRoutes);

// Health check
app.get('/health', (req, res) => {
  res.status(200).json({
    status: 'OK',
    timestamp: new Date().toISOString(),
    uptime: process.uptime()
  });
});

// 404 handler
app.use((req, res) => {
  res.status(404).json({
    success: false,
    message: 'Route not found'
  });
});

// Error handling middleware (must be last)
app.use(errorMiddleware);

module.exports = app;
