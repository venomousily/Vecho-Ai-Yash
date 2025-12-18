const API_BASE_URL = 'http://localhost:5000/api';

// DOM elements
const chatMessages = document.getElementById('chat-messages');
const userInput = document.getElementById('user-input');
const sendBtn = document.getElementById('send-btn');
const modeSelect = document.getElementById('mode');
const loading = document.getElementById('loading');

// User ID (default to 1 for demo)
let userId = 1;

// Initialize
document.addEventListener('DOMContentLoaded', () => {
    // Load chat history
    loadChatHistory();
    
    // Event listeners
    sendBtn.addEventListener('click', sendMessage);
    userInput.addEventListener('keypress', (e) => {
        if (e.key === 'Enter' && !e.shiftKey) {
            e.preventDefault();
            sendMessage();
        }
    });
});

async function sendMessage() {
    const message = userInput.value.trim();
    if (!message) return;

    // Get selected mode
    const mode = modeSelect.value;

    // Disable input and button
    userInput.disabled = true;
    sendBtn.disabled = true;
    loading.style.display = 'block';

    // Add user message to chat
    addMessage(message, 'user');

    // Clear input
    userInput.value = '';

    try {
        // Send request to backend
        const response = await fetch(`${API_BASE_URL}/chat`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                message: message,
                user_id: userId,
                mode: mode
            })
        });

        const data = await response.json();

        if (response.ok) {
            // Add AI response to chat
            addMessage(data.response, 'ai');
        } else {
            // Show error message
            addMessage(`Error: ${data.error}`, 'ai');
        }
    } catch (error) {
        console.error('Error:', error);
        addMessage('Sorry, I encountered an error. Please try again.', 'ai');
    } finally {
        // Re-enable input and button
        userInput.disabled = false;
        sendBtn.disabled = false;
        loading.style.display = 'none';
        userInput.focus();
    }
}

function addMessage(text, sender) {
    // Remove welcome message if it exists
    const welcomeMsg = chatMessages.querySelector('.welcome-message');
    if (welcomeMsg) {
        welcomeMsg.remove();
    }

    const messageDiv = document.createElement('div');
    messageDiv.className = `message ${sender}`;

    const contentDiv = document.createElement('div');
    contentDiv.className = 'message-content';
    contentDiv.textContent = text;

    const timeDiv = document.createElement('div');
    timeDiv.className = 'message-time';
    timeDiv.textContent = new Date().toLocaleTimeString();

    messageDiv.appendChild(contentDiv);
    messageDiv.appendChild(timeDiv);
    chatMessages.appendChild(messageDiv);

    // Scroll to bottom
    chatMessages.scrollTop = chatMessages.scrollHeight;
}

async function loadChatHistory() {
    try {
        const response = await fetch(`${API_BASE_URL}/history?user_id=${userId}`);
        const data = await response.json();

        if (response.ok && data.history && data.history.length > 0) {
            // Remove welcome message
            const welcomeMsg = chatMessages.querySelector('.welcome-message');
            if (welcomeMsg) {
                welcomeMsg.remove();
            }

            // Load messages in reverse order (oldest first)
            data.history.reverse().forEach(chat => {
                addMessage(chat.user_message, 'user');
                addMessage(chat.ai_response, 'ai');
            });
        }
    } catch (error) {
        console.error('Error loading chat history:', error);
    }
}

