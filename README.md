
# QuizMaster

A full-stack quiz application built with Vue.js frontend and Python backend. 

## 📋 Overview

QuizMaster is an interactive quiz application designed to help users test their knowledge across various topics. The application features a modern, responsive user interface and a robust backend API for managing quiz data and user interactions.

## 🏗️ Project Structure

```
QuizMaster/
├── frontend/              # Vue.js frontend application
│   ├── src/              # Vue components and application logic
│   ├── public/           # Static assets
│   ├── index.html        # Main HTML entry point
│   ├── vite.config.js    # Vite configuration
│   └── package.json      # Frontend dependencies
│
├── backend/              # Python Flask backend
│   ├── app.py           # Main application entry point
│   ├── models/          # Database models
│   ├── routes/          # API route handlers
│   └── requirements. txt # Python dependencies
│
└── package.json         # Root project configuration
```

## 🛠️ Tech Stack

**Frontend:**
- Vue.js - Progressive JavaScript framework
- Vite - Next-generation build tool
- HTML5 & CSS3

**Backend:**
- Python - Backend programming language
- Flask - Lightweight web framework

**Languages Breakdown:**
- Vue:  303,754 bytes (79%)
- Python: 46,406 bytes (12%)
- JavaScript: 3,639 bytes (1%)
- HTML: 730 bytes (<1%)

## 🚀 Getting Started

### Prerequisites
- Node.js and npm (for frontend)
- Python 3.x (for backend)

### Frontend Setup

1. Navigate to the frontend directory:
```bash
cd frontend
```

2. Install dependencies:
```bash
npm install
```

3. Start the development server:
```bash
npm run dev
```

The frontend will be available at `http://localhost:5173` (or the port specified by Vite).

### Backend Setup

1. Navigate to the backend directory:
```bash
cd backend
```

2. Install Python dependencies:
```bash
pip install -r requirements.txt
```

3. Run the Flask application:
```bash
python app.py
```

The backend API will be available at `http://localhost:5000` (or the port specified in app.py).

## 📁 Directory Details

### Frontend (`/frontend`)
- **src/**: Vue components and application logic
- **public/**: Static assets and resources
- **vite.config.js**: Vite build configuration for optimized development and production builds

### Backend (`/backend`)
- **app.py**: Main Flask application with route initialization
- **models/**: Database models for quizzes, questions, and user data
- **routes/**: API endpoints for quiz operations

## 🔧 Configuration

- Frontend is configured to use Vite for fast development and optimized builds
- Backend uses Flask for lightweight API development
- Both frontend and backend can be customized through their respective configuration files

## 📝 Features

- Interactive quiz interface
- Multiple quiz categories and questions
- Real-time quiz progress tracking
- RESTful API backend
- Responsive design for various devices

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request. 

## 📄 License

This project is currently unlicensed.  See the repository for more details. 

## 👤 Author

[ankitkuniyal](https://github.com/ankitkuniyal)

## 📞 Support

For issues, questions, or suggestions, please open an issue in the repository.

---

**Repository**:  [ankitkuniyal/QuizMaster](https://github.com/ankitkuniyal/QuizMaster)  
**Last Updated**: July 25, 2025
```
