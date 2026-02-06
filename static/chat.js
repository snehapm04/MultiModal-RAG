const pdfInput = document.getElementById('pdfInput');
const uploadStatus = document.getElementById('uploadStatus');
const chatBox = document.getElementById('chatBox');
const chatForm = document.getElementById('chatForm');
const userInput = document.getElementById('userInput');
const sendBtn = document.getElementById('sendBtn');
const docCount = document.getElementById('docCount');

let docsLoaded = false;

// Handle PDF Upload
pdfInput.addEventListener('change', async (e) => {
    const files = Array.from(e.target.files);
    if (files.length === 0) return;

    const formData = new FormData();
    files.forEach(file => formData.append('files', file));

    showStatus(`Uploading ${files.length} file(s)...`, false);

    try {
        const response = await fetch('/api/upload', {
            method: 'POST',
            body: formData
        });

        if (!response.ok) throw new Error('Upload failed');

        const data = await response.json();
        docsLoaded = true;
        userInput.disabled = false;
        sendBtn.disabled = false;

        showStatus(`✅ ${files.length} PDF(s) loaded successfully!`, true);
        docCount.textContent = `${files.length} doc${files.length > 1 ? 's' : ''} loaded`;
        
        // Clear welcome message
        if (chatBox.querySelector('.welcome-message')) {
            chatBox.innerHTML = '';
        }

        pdfInput.value = '';
    } catch (error) {
        console.error('Error:', error);
        showStatus(`❌ Upload failed: ${error.message}`, true, true);
    }
});

// Handle Chat Submission
chatForm.addEventListener('submit', async (e) => {
    e.preventDefault();

    const query = userInput.value.trim();
    if (!query || !docsLoaded) return;

    // Add user message
    addMessage(query, 'user');
    userInput.value = '';
    userInput.focus();

    // Show thinking indicator
    addMessage('Thinking<span class="thinking-dot"></span><span class="thinking-dot"></span><span class="thinking-dot"></span>', 'bot', true);

    try {
        const response = await fetch('/api/chat', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ query })
        });

        if (!response.ok) throw new Error('Chat request failed');

        const data = await response.json();

        // Remove thinking message
        chatBox.lastElementChild.remove();

        // Add bot response
        addMessage(data.answer, 'bot');
    } catch (error) {
        console.error('Error:', error);
        chatBox.lastElementChild.remove();
        addMessage(`❌ Error: ${error.message}`, 'bot');
    }
});

function addMessage(text, role, isThinking = false) {
    const messageDiv = document.createElement('div');
    messageDiv.className = `message ${role}`;

    const bubbleDiv = document.createElement('div');
    bubbleDiv.className = 'message-bubble' + (isThinking ? ' thinking' : '');
    bubbleDiv.innerHTML = text;

    messageDiv.appendChild(bubbleDiv);
    chatBox.appendChild(messageDiv);

    // Auto-scroll to bottom
    chatBox.scrollTop = chatBox.scrollHeight;
}

function showStatus(message, isSuccess = false, isError = false) {
    uploadStatus.innerHTML = message;
    uploadStatus.classList.add('show');
    if (isError) uploadStatus.classList.add('error');
    else uploadStatus.classList.remove('error');

    if (isSuccess || isError) {
        setTimeout(() => {
            uploadStatus.classList.remove('show');
        }, 3000);
    }
}
