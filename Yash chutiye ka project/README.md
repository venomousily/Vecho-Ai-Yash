# Vecho Ai - Smart AI Chatbot using Gemini API

Vecho Ai is a smart conversational assistant designed for students, built using Google's Gemini API. It helps users with answering questions, explaining topics, assisting with assignments, and generating summaries.

## 🎯 Features

- **Smart Q&A**: Get accurate answers to your questions
- **Explanation Mode**: Understand complex topics in simple language
- **Summary Mode**: Generate concise summaries of content
- **Chat History**: All conversations are saved in the database
- **Modern UI**: Beautiful, responsive chat interface

## 🏗️ Architecture

### Design Patterns Used

1. **MVC (Model-View-Controller)**
   - Model: SQLite database (users, chats)
   - View: HTML/CSS/JavaScript frontend
   - Controller: Flask routes handling API requests

2. **Singleton Pattern**
   - Gemini API client initialized once
   - Prevents repeated API setup

3. **Strategy Pattern**
   - Different response strategies for different modes:
     - Q&A mode
     - Explanation mode
     - Summary mode

## 🛠️ Technology Stack

### Frontend
- HTML5
- CSS3 (with modern gradients and animations)
- JavaScript (ES6+)

### Backend
- Python 3.8+
- Flask (Web framework)
- Flask-CORS (Cross-origin resource sharing)

### AI & Database
- Google Gemini API (gemini-pro model)
- SQLite (Lightweight database)

## 📁 Project Structure

```
vecho-ai/
│
├── backend/
│   ├── app.py              # Flask application and routes
│   ├── gemini_client.py     # Gemini API client (Singleton)
│
├── frontend/
│   ├── index.html          # Main chat interface
│   ├── style.css           # Styling
│   ├── script.js           # Frontend logic
│
├── database/
│   └── chat.db             # SQLite database (auto-created)
│
├── requirements.txt        # Python dependencies
└── README.md              # Project documentation
```

## 🗄️ Database Schema

### Table: users
| Field    | Type         |
| -------- | ------------ |
| user_id  | INTEGER (PK) |
| username | TEXT         |
| email    | TEXT         |

### Table: chats
| Field        | Type         |
| ------------ | ------------ |
| chat_id      | INTEGER (PK) |
| user_id      | INTEGER (FK) |
| user_message | TEXT         |
| ai_response  | TEXT         |
| timestamp    | DATETIME     |

## 🚀 Installation & Setup

### Prerequisites
- Python 3.8 or higher
- pip (Python package manager)

### Steps

1. **Clone or download the project**
   ```bash
   cd vecho-ai
   ```

2. **Install Python dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the Flask server**
   ```bash
   cd backend
   python app.py
   ```

4. **Open the application**
   - Open `frontend/index.html` in your browser, OR
   - Navigate to `http://localhost:5000` in your browser

## 📝 Usage

1. **Select Response Mode**
   - **Q&A Mode**: Direct question answering
   - **Explanation Mode**: Detailed explanations in simple language
   - **Summary Mode**: Generate concise summaries

2. **Type your message** in the input field

3. **Press Enter or click Send** to get AI response

4. **View chat history** - All conversations are automatically saved

## 🔌 API Endpoints

### POST `/api/chat`
Send a message to the chatbot.

**Request Body:**
```json
{
  "message": "What is Python?",
  "user_id": 1,
  "mode": "qa"
}
```

**Response:**
```json
{
  "response": "Python is a high-level programming language...",
  "timestamp": "2024-01-01T12:00:00"
}
```

### GET `/api/history?user_id=1`
Get chat history for a user.

**Response:**
```json
{
  "history": [
    {
      "user_message": "Hello",
      "ai_response": "Hi! How can I help you?",
      "timestamp": "2024-01-01T12:00:00"
    }
  ]
}
```

### POST `/api/user`
Create a new user.

**Request Body:**
```json
{
  "username": "John Doe",
  "email": "john@example.com"
}
```

## 🔐 API Key Configuration

The Gemini API key is configured in `backend/gemini_client.py`. The key is already set in the code.

**Note**: In production, consider using environment variables for API keys:
```python
import os
API_KEY = os.getenv('GEMINI_API_KEY', 'your-default-key')
```

## 🎨 Features

- **Responsive Design**: Works on desktop and mobile devices
- **Real-time Chat**: Instant AI responses
- **Mode Selection**: Choose between Q&A, Explanation, or Summary modes
- **Chat History**: Persistent storage of all conversations
- **Modern UI**: Beautiful gradient design with smooth animations

## 🐛 Troubleshooting

1. **Module not found error**
   - Make sure all dependencies are installed: `pip install -r requirements.txt`

2. **CORS errors**
   - Ensure Flask-CORS is installed and configured

3. **Database errors**
   - The database will be created automatically on first run
   - Make sure the `database/` directory exists or can be created

4. **API errors**
   - Verify the Gemini API key is correct
   - Check your internet connection

## 📄 License

This project is created for educational purposes.

## 👥 Team

Solo Project or Group Project (3 Members):
- Member 1: Gemini API & Backend
- Member 2: Frontend & UI
- Member 3: Database & Documentation

---

**Vecho Ai** - *Context-aware AI assistant built using Gemini API to improve student learning productivity.*

