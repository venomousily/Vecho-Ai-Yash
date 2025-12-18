from flask import Flask, request, jsonify, send_from_directory, send_file
from flask_cors import CORS
import sqlite3
from datetime import datetime
import os
import sys

# Add backend directory to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'backend'))

from gemini_client import GeminiClient

app = Flask(__name__, static_folder='../frontend', template_folder='../frontend')
CORS(app)

# Database path - use /tmp for Vercel serverless (writable directory)
DB_PATH = os.path.join('/tmp', 'chat.db')

def init_db():
    """Initialize the database with required tables"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    # Create users table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            user_id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL,
            email TEXT UNIQUE
        )
    ''')
    
    # Create chats table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS chats (
            chat_id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            user_message TEXT NOT NULL,
            ai_response TEXT NOT NULL,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users(user_id)
        )
    ''')
    
    conn.commit()
    conn.close()

# Initialize database on first import
init_db()

@app.route('/')
def index():
    """Serve the main chat interface"""
    return send_from_directory('../frontend', 'index.html')

@app.route('/<path:path>')
def serve_static(path):
    """Serve static files from frontend directory"""
    if path == 'logo.png':
        logo_path = os.path.join(os.path.dirname(__file__), '..', 'vecho ai logo.png')
        if os.path.exists(logo_path):
            return send_file(logo_path, mimetype='image/png')
        return '', 404
    return send_from_directory('../frontend', path)

@app.route('/api/chat', methods=['POST'])
def chat():
    """Handle chat requests"""
    try:
        data = request.json
        user_message = data.get('message', '').strip()
        user_id = data.get('user_id', 1)
        mode = data.get('mode', 'qa')
        
        if not user_message:
            return jsonify({'error': 'Message cannot be empty'}), 400
        
        # Get Gemini response
        gemini_client = GeminiClient()
        ai_response = gemini_client.get_response(user_message, mode)
        
        # Save to database
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO chats (user_id, user_message, ai_response, timestamp)
            VALUES (?, ?, ?, ?)
        ''', (user_id, user_message, ai_response, datetime.now()))
        conn.commit()
        conn.close()
        
        return jsonify({
            'response': ai_response,
            'timestamp': datetime.now().isoformat()
        })
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/history', methods=['GET'])
def get_history():
    """Get chat history for a user"""
    try:
        user_id = request.args.get('user_id', 1, type=int)
        
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute('''
            SELECT user_message, ai_response, timestamp
            FROM chats
            WHERE user_id = ?
            ORDER BY timestamp DESC
            LIMIT 50
        ''', (user_id,))
        
        history = [
            {
                'user_message': row[0],
                'ai_response': row[1],
                'timestamp': row[2]
            }
            for row in cursor.fetchall()
        ]
        
        conn.close()
        
        return jsonify({'history': history})
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/recent-chats', methods=['GET'])
def get_recent_chats():
    """Get recent chat sessions for a user"""
    try:
        user_id = request.args.get('user_id', 1, type=int)
        limit = request.args.get('limit', 10, type=int)
        
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT chat_id, user_message, timestamp
            FROM chats
            WHERE user_id = ?
            ORDER BY timestamp DESC
        ''', (user_id,))
        
        all_messages = cursor.fetchall()
        
        # Group messages into conversations (messages within 30 minutes are same conversation)
        conversations = []
        current_conversation = None
        
        def parse_timestamp(ts):
            """Parse timestamp from various formats"""
            try:
                if isinstance(ts, str):
                    if 'T' in ts:
                        return datetime.fromisoformat(ts.replace('Z', '+00:00').split('.')[0])
                    return datetime.strptime(ts, '%Y-%m-%d %H:%M:%S')
                return ts
            except:
                return datetime.now()
        
        for chat_id, user_message, timestamp in all_messages:
            if current_conversation is None:
                current_conversation = {
                    'first_message': user_message,
                    'first_timestamp': timestamp,
                    'last_timestamp': timestamp,
                    'message_count': 1
                }
            else:
                try:
                    last_time = parse_timestamp(current_conversation['last_timestamp'])
                    current_time = parse_timestamp(timestamp)
                    
                    time_diff = abs((last_time - current_time).total_seconds() / 60)
                    if time_diff > 30:
                        conversations.append(current_conversation)
                        current_conversation = {
                            'first_message': user_message,
                            'first_timestamp': timestamp,
                            'last_timestamp': timestamp,
                            'message_count': 1
                        }
                    else:
                        current_conversation['last_timestamp'] = timestamp
                        current_conversation['message_count'] += 1
                except Exception as e:
                    conversations.append(current_conversation)
                    current_conversation = {
                        'first_message': user_message,
                        'first_timestamp': timestamp,
                        'last_timestamp': timestamp,
                        'message_count': 1
                    }
        
        if current_conversation:
            conversations.append(current_conversation)
        
        # Format conversations for response
        recent_chats = []
        for conv in conversations[:limit]:
            try:
                def parse_ts(ts):
                    if isinstance(ts, str):
                        if 'T' in ts:
                            return datetime.fromisoformat(ts.replace('Z', '+00:00').split('.')[0])
                        return datetime.strptime(ts, '%Y-%m-%d %H:%M:%S')
                    return ts
                
                timestamp = parse_ts(conv['first_timestamp'])
                now = datetime.now()
                if timestamp.tzinfo:
                    now = datetime.now(timestamp.tzinfo)
                diff = abs((now - timestamp.replace(tzinfo=None) if timestamp.tzinfo else timestamp).total_seconds())
                
                if diff < 60:
                    time_ago = "Just now"
                elif diff < 3600:
                    minutes = int(diff / 60)
                    time_ago = f"{minutes} minute{'s' if minutes != 1 else ''} ago"
                elif diff < 86400:
                    hours = int(diff / 3600)
                    time_ago = f"{hours} hour{'s' if hours != 1 else ''} ago"
                elif diff < 604800:
                    days = int(diff / 86400)
                    time_ago = f"{days} day{'s' if days != 1 else ''} ago"
                else:
                    time_ago = timestamp.strftime("%b %d, %Y")
            except Exception as e:
                time_ago = "Recently"
            
            recent_chats.append({
                'title': conv['first_message'][:50] + ('...' if len(conv['first_message']) > 50 else ''),
                'preview': conv['first_message'],
                'timestamp': conv['first_timestamp'],
                'time_ago': time_ago,
                'message_count': conv['message_count']
            })
        
        conn.close()
        
        return jsonify({'recent_chats': recent_chats})
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/user', methods=['POST'])
def create_user():
    """Create a new user"""
    try:
        data = request.json
        username = data.get('username', 'Guest')
        email = data.get('email', '')
        
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO users (username, email)
            VALUES (?, ?)
        ''', (username, email))
        user_id = cursor.lastrowid
        conn.commit()
        conn.close()
        
        return jsonify({'user_id': user_id, 'username': username})
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Vercel serverless function handler
# This is the entry point for Vercel
handler = app

