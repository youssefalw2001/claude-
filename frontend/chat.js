// Configuration
const API_BASE = window.location.origin;
let chatHistory = [];
let currentProvider = 'ollama';
let currentModel = '';
let availableModels = [];

// Initialize on load
document.addEventListener('DOMContentLoaded', () => {
    loadSettings();
    loadModels();
    updateModelIndicator();
    autoResizeTextarea();
});

// Settings Management
function loadSettings() {
    currentProvider = localStorage.getItem('provider') || 'ollama-cloud';
    currentModel = localStorage.getItem('model') || '';
    
    document.getElementById('provider-select').value = currentProvider;
    document.getElementById('ollama-cloud-key').value = localStorage.getItem('ollama_cloud_key') || '';
    document.getElementById('groq-key').value = localStorage.getItem('groq_key') || '';
    document.getElementById('openrouter-key').value = localStorage.getItem('openrouter_key') || '';
    document.getElementById('ollama-url').value = localStorage.getItem('ollama_url') || 'http://localhost:11434';
}

function saveSettings() {
    currentProvider = document.getElementById('provider-select').value;
    currentModel = document.getElementById('model-select').value;
    
    localStorage.setItem('provider', currentProvider);
    localStorage.setItem('model', currentModel);
    localStorage.setItem('ollama_cloud_key', document.getElementById('ollama-cloud-key').value);
    localStorage.setItem('groq_key', document.getElementById('groq-key').value);
    localStorage.setItem('openrouter_key', document.getElementById('openrouter-key').value);
    localStorage.setItem('ollama_url', document.getElementById('ollama-url').value);
    
    updateStatus('Settings saved', 'success');
    updateModelIndicator();
    toggleSettings();
}

function toggleSettings() {
    const panel = document.getElementById('settings-panel');
    panel.classList.toggle('hidden');
}

// Model Management
async function loadModels() {
    try {
        const response = await fetch(`${API_BASE}/api/models`);
        const data = await response.json();
        availableModels = data.models;
        updateModelDropdown();
    } catch (error) {
        console.error('Failed to load models:', error);
        updateStatus('Failed to load models', 'error');
    }
}

function updateModels() {
    currentProvider = document.getElementById('provider-select').value;
    updateModelDropdown();
}

function updateModelDropdown() {
    const select = document.getElementById('model-select');
    const filtered = availableModels.filter(m => m.provider === currentProvider);
    
    select.innerHTML = '';
    
    if (filtered.length === 0) {
        select.innerHTML = '<option value="">No models available</option>';
        return;
    }
    
    filtered.forEach(model => {
        const option = document.createElement('option');
        option.value = model.name;
        option.textContent = `${model.name} ${model.size ? '(' + model.size + ')' : ''}`;
        select.appendChild(option);
    });
    
    if (currentModel && filtered.find(m => m.name === currentModel)) {
        select.value = currentModel;
    } else {
        currentModel = filtered[0].name;
        select.value = currentModel;
    }
}

function updateModelIndicator() {
    const indicator = document.getElementById('model-indicator');
    const providerName = currentProvider === 'ollama-cloud' ? 'Ollama Cloud' : currentProvider;
    indicator.textContent = `${providerName} | ${currentModel || 'No model'}`;
}

// Get API key for current provider from localStorage
function getApiKeyForProvider(provider) {
    switch(provider) {
        case 'ollama-cloud':
            return localStorage.getItem('ollama_cloud_key') || '';
        case 'groq':
            return localStorage.getItem('groq_key') || '';
        case 'openrouter':
            return localStorage.getItem('openrouter_key') || '';
        default:
            return '';
    }
}

// Chat Functions
function sendQuickMessage(message) {
    document.getElementById('message-input').value = message;
    sendMessage();
}

async function sendMessage() {
    const input = document.getElementById('message-input');
    const message = input.value.trim();
    
    if (!message) return;
    
    // Clear welcome message if exists
    const welcome = document.querySelector('.welcome-message');
    if (welcome) welcome.remove();
    
    // Add user message
    addMessage('user', message);
    chatHistory.push({ role: 'user', content: message });
    
    // Clear input
    input.value = '';
    autoResizeTextarea();
    
    // Show typing indicator
    const typingId = addTypingIndicator();
    
    // Disable send button
    const sendBtn = document.getElementById('send-btn');
    sendBtn.disabled = true;
    updateStatus('Fox is thinking...', 'loading');
    
    try {
        const response = await fetch(`${API_BASE}/api/chat`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                message: message,
                provider: currentProvider,
                model: currentModel,
                history: chatHistory.slice(-10), // Keep last 10 messages for context
                api_key: getApiKeyForProvider(currentProvider)
            })
        });
        
        removeTypingIndicator(typingId);
        
        if (!response.ok) {
            throw new Error(`API error: ${response.status}`);
        }
        
        const data = await response.json();
        addMessage('assistant', data.response);
        chatHistory.push({ role: 'assistant', content: data.response });
        
        updateStatus('Ready', 'success');
        
    } catch (error) {
        removeTypingIndicator(typingId);
        console.error('Chat error:', error);
        addMessage('assistant', `Shit, something broke: ${error.message}\n\nCheck if the backend is running and the model is available.`);
        updateStatus('Error - check console', 'error');
    } finally {
        sendBtn.disabled = false;
    }
}

function addMessage(role, content) {
    const container = document.getElementById('chat-container');
    
    const messageDiv = document.createElement('div');
    messageDiv.className = `message ${role}`;
    
    const avatar = document.createElement('div');
    avatar.className = 'message-avatar';
    avatar.textContent = role === 'user' ? '👤' : '🦊';
    
    const contentDiv = document.createElement('div');
    contentDiv.className = 'message-content';
    
    // Format content with code blocks
    const formatted = formatMessage(content);
    contentDiv.innerHTML = formatted;
    
    messageDiv.appendChild(avatar);
    messageDiv.appendChild(contentDiv);
    
    container.appendChild(messageDiv);
    container.scrollTop = container.scrollHeight;
}

function formatMessage(content) {
    // Simple markdown-like formatting
    let formatted = content;
    
    // Code blocks
    formatted = formatted.replace(/```(\w+)?\n([\s\S]+?)```/g, (match, lang, code) => {
        return `<pre><code>${escapeHtml(code.trim())}</code></pre>`;
    });
    
    // Inline code
    formatted = formatted.replace(/`([^`]+)`/g, '<code>$1</code>');
    
    // Bold
    formatted = formatted.replace(/\*\*([^*]+)\*\*/g, '<strong>$1</strong>');
    
    // Line breaks
    formatted = formatted.replace(/\n/g, '<br>');
    
    return formatted;
}

function escapeHtml(text) {
    const div = document.createElement('div');
    div.textContent = text;
    return div.innerHTML;
}

function addTypingIndicator() {
    const container = document.getElementById('chat-container');
    
    const messageDiv = document.createElement('div');
    messageDiv.className = 'message assistant';
    messageDiv.id = 'typing-indicator';
    
    const avatar = document.createElement('div');
    avatar.className = 'message-avatar';
    avatar.textContent = '🦊';
    
    const contentDiv = document.createElement('div');
    contentDiv.className = 'message-content';
    contentDiv.innerHTML = '<div class="typing-indicator"><span></span><span></span><span></span></div>';
    
    messageDiv.appendChild(avatar);
    messageDiv.appendChild(contentDiv);
    
    container.appendChild(messageDiv);
    container.scrollTop = container.scrollHeight;
    
    return 'typing-indicator';
}

function removeTypingIndicator(id) {
    const indicator = document.getElementById(id);
    if (indicator) indicator.remove();
}

function updateStatus(message, type) {
    const indicator = document.getElementById('status-indicator');
    const icons = {
        success: '🟢',
        error: '🔴',
        loading: '🟡'
    };
    indicator.textContent = `${icons[type] || '🟢'} ${message}`;
}

function clearHistory() {
    if (confirm('Clear all chat history?')) {
        chatHistory = [];
        const container = document.getElementById('chat-container');
        container.innerHTML = `
            <div class="welcome-message">
                <h2>👋 Hey Jack, Fox here.</h2>
                <p>Ready to fuck shit up. What are we building today?</p>
                <div class="quick-actions">
                    <button onclick="sendQuickMessage('Write me an AOB scanner in C++')">AOB Scanner</button>
                    <button onclick="sendQuickMessage('Show me how to hook D3D11 Present')">D3D11 Hook</button>
                    <button onclick="sendQuickMessage('Manual map DLL injection example')">Manual Map</button>
                </div>
            </div>
        `;
        updateStatus('History cleared', 'success');
        toggleSettings();
    }
}

// Input Handling
function handleKeyDown(event) {
    if (event.key === 'Enter' && !event.shiftKey) {
        event.preventDefault();
        sendMessage();
    }
}

function autoResizeTextarea() {
    const textarea = document.getElementById('message-input');
    textarea.style.height = 'auto';
    textarea.style.height = Math.min(textarea.scrollHeight, 150) + 'px';
}

document.getElementById('message-input').addEventListener('input', autoResizeTextarea);

// Keyboard shortcut for settings
document.addEventListener('keydown', (event) => {
    if (event.ctrlKey && event.key === ',') {
        event.preventDefault();
        toggleSettings();
    }
});
