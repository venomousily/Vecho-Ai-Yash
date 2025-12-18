# Quick Start Guide - Vecho Ai

## 🚀 Quick Setup (3 Steps)

### Step 1: Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 2: Run the Application
```bash
python run.py
```

Or alternatively:
```bash
cd backend
python app.py
```

### Step 3: Open in Browser
Navigate to: **http://localhost:5000**

## ✅ That's it!

The application will:
- ✅ Automatically create the database
- ✅ Initialize all tables
- ✅ Start the Flask server
- ✅ Be ready to chat!

## 🎯 Try It Out

1. Select a mode (Q&A, Explanation, or Summary)
2. Type a message like "What is Python?"
3. Press Enter or click Send
4. Get instant AI responses!

## 🐛 Troubleshooting

**Port 5000 already in use?**
- Change the port in `backend/app.py` or `run.py`:
  ```python
  app.run(debug=True, port=5001)  # Use port 5001 instead
  ```

**Module not found?**
- Make sure you installed requirements: `pip install -r requirements.txt`

**API errors?**
- Check your internet connection
- Verify the Gemini API key is correct in `backend/gemini_client.py`

---

**Happy Chatting! 🤖**

