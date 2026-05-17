function appendMessage(sender, text) {
    const container = document.getElementById('chat-messages');
    const bubble = document.createElement('div');
    bubble.className = `chat-bubble ${sender}`;
    // Replace newlines with <br> for HTML rendering
    bubble.innerHTML = text.replace(/\n/g, '<br>');
    container.appendChild(bubble);
    container.scrollTop = container.scrollHeight;
}

function showTypingIndicator() {
    const container = document.getElementById('chat-messages');
    const typing = document.createElement('div');
    typing.id = 'typing-indicator';
    typing.className = 'chat-bubble ai';
    typing.innerHTML = '<i>Analizando datos...</i>';
    container.appendChild(typing);
    container.scrollTop = container.scrollHeight;
}

function removeTypingIndicator() {
    const typing = document.getElementById('typing-indicator');
    if (typing) typing.remove();
}

async function sendMessage() {
    const input = document.getElementById('chat-input');
    const btn = document.getElementById('btn-send');
    const text = input.value.trim();

    if (!text) return;

    // UI Updates
    appendMessage('user', text);
    input.value = '';
    input.disabled = true;
    btn.disabled = true;
    showTypingIndicator();

    try {
        const response = await fetch('/api/chat', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ mensaje: text })
        });

        const data = await response.json();
        removeTypingIndicator();
        
        if (data.success) {
            appendMessage('ai', data.respuesta);
        } else {
            appendMessage('ai', `⚠️ Error: ${data.error}`);
        }
    } catch (error) {
        removeTypingIndicator();
        appendMessage('ai', '⚠️ Error de conexión con el servidor.');
    } finally {
        input.disabled = false;
        btn.disabled = false;
        input.focus();
    }
}

// Permitir enviar con la tecla Enter
document.getElementById('chat-input')?.addEventListener('keypress', function (e) {
    if (e.key === 'Enter') sendMessage();
});

// Scroll down on load
window.onload = function() {
    const container = document.getElementById('chat-messages');
    if(container) container.scrollTop = container.scrollHeight;
}
