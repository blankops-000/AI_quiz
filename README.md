# AI Quiz Application

A full-stack MERN application with AI integration for text analysis, quiz generation, and intelligent recommendations.

## Features

- **User Authentication**: Secure JWT-based authentication
- **AI Text Analysis**: Analyze text for sentiment, entities, and keywords
- **Quiz Generation**: AI-powered quiz creation on any topic
- **Text Generation**: Generate text based on prompts
- **Recommendations**: Personalized content recommendations
- **Responsive Design**: Works on desktop and mobile devices

## Tech Stack

### Frontend
- React 18
- React Router DOM
- Axios for API calls
- CSS3 with modern styling

### Backend
- Node.js with Express
- MongoDB with Mongoose
- JWT Authentication
- CORS enabled
- Rate limiting
- Input validation

### AI Service
- Python Flask
- HuggingFace Transformers
- OpenAI API integration
- scikit-learn for ML models
- Text preprocessing and analysis

## Prerequisites

- Node.js (v16 or higher)
- Python (v3.8 or higher)
- MongoDB (local or cloud)
- Git

## Quick Start

### Option 1: Automated Setup (Windows)
1. Clone the repository
2. Run `start.bat` - this will install all dependencies and start all services

### Option 2: Manual Setup

#### 1. Install Dependencies
```bash
# Install root dependencies
npm install

# Install backend dependencies
cd ai_backend
npm install
cd ..

# Install frontend dependencies
cd ai_frontend
npm install
cd ..

# Install AI service dependencies
cd ai-service
pip install -r requirements.txt
cd ..
```

#### 2. Environment Configuration

**Backend (.env in ai_backend folder):**
```env
NODE_ENV=development
PORT=5000
MONGO_URI=your_mongodb_connection_string
JWT_SECRET=your_jwt_secret_key
FRONTEND_URL=http://localhost:3000
AI_SERVICE_URL=http://localhost:8000/api
```

**Frontend (.env in ai_frontend folder):**
```env
REACT_APP_API_URL=http://localhost:5000/api
REACT_APP_APP_NAME=AI Quiz App
```

**AI Service (.env in ai-service folder):**
```env
FLASK_ENV=development
PORT=8000
OPENAI_API_KEY=your_openai_api_key (optional)
HUGGINGFACE_API_KEY=your_huggingface_api_key (optional)
```

#### 3. Start Services

**Terminal 1 - AI Service:**
```bash
cd ai-service/src
python app.py
```

**Terminal 2 - Backend:**
```bash
cd ai_backend
npm run dev
```

**Terminal 3 - Frontend:**
```bash
cd ai_frontend
npm start
```

## Service URLs

- **Frontend**: http://localhost:3000
- **Backend API**: http://localhost:5000
- **AI Service**: http://localhost:8000

## API Endpoints

### Authentication
- `POST /api/auth/register` - User registration
- `POST /api/auth/login` - User login
- `GET /api/auth/me` - Get current user

### AI Services
- `POST /api/ai/process` - Process AI requests
- `GET /api/ai/history` - Get AI request history
- `GET /api/ai/health` - AI service health check

### AI Service Endpoints
- `POST /api/analyze/text` - Comprehensive text analysis
- `POST /api/analyze/sentiment` - Sentiment analysis
- `POST /api/generate/text` - Text generation
- `POST /api/generate/quiz` - Quiz generation
- `POST /api/recommendations` - Get recommendations

## Usage

1. **Register/Login**: Create an account or login
2. **Dashboard**: View your activity and stats
3. **AI Assistant**: Access AI-powered features:
   - **Text Analysis**: Analyze any text for insights
   - **Quiz Generation**: Create quizzes on any topic
   - **Text Generation**: Generate content from prompts

## AI Features

### Text Analysis
- Sentiment analysis (positive/negative/neutral)
- Named entity recognition
- Keyword extraction
- Readability scoring
- Text statistics

### Quiz Generation
- Multiple choice questions
- Configurable difficulty levels
- Various topics supported
- Automatic answer generation

### Text Generation
- Prompt-based text creation
- Adjustable parameters (length, creativity)
- Multiple AI models support

## Development

### Project Structure
```
AI_quiz/
├── ai_backend/          # Node.js backend
├── ai_frontend/         # React frontend
├── ai-service/          # Python AI service
├── start.bat           # Windows startup script
└── package.json        # Root package file
```

### Adding New AI Features
1. Add endpoint to `ai-service/src/routes/api_routes.py`
2. Implement controller in `ai-service/src/controllers/`
3. Add service method to `ai_backend/src/services/aiService.js`
4. Create frontend interface in React components

## Troubleshooting

### Common Issues

1. **MongoDB Connection**: Ensure MongoDB is running and connection string is correct
2. **Python Dependencies**: Make sure all Python packages are installed
3. **Port Conflicts**: Check if ports 3000, 5000, 8000 are available
4. **API Keys**: OpenAI and HuggingFace keys are optional but improve AI features

### Logs
- Backend logs: Console output
- AI Service logs: `ai-service/logs/` directory
- Frontend: Browser console

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## License

MIT License - see LICENSE file for details

## Support

For issues and questions, please create an issue in the repository.