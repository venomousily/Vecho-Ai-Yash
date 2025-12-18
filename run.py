"""
Simple script to run the Vecho Ai Flask application
Run this from the project root directory
"""
import os
import sys

# Add backend directory to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'backend'))

from app import app, init_db

if __name__ == '__main__':
    print("=" * 50)
    print("Vecho Ai - Smart AI Chatbot")
    print("=" * 50)
    print("\nInitializing database...")
    init_db()
    print("✅ Database initialized!")
    print("\nStarting Flask server...")
    print("🌐 Open http://localhost:5000 in your browser")
    print("=" * 50)
    print("\nPress Ctrl+C to stop the server\n")
    
    app.run(debug=True, port=5000, host='127.0.0.1')

