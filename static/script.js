const micBtn = document.getElementById('mic-btn');
const stopBtn = document.getElementById('stop-btn');
const sendBtn = document.getElementById('send-btn');
const textInput = document.getElementById('text-input');
const chatHistory = document.getElementById('chat-history');
const typingIndicator = document.getElementById('typing-indicator');
const emergencyBtn = document.getElementById('emergency-btn');
const emergencyMenu = document.getElementById('emergency-menu');

// Check browser support
const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
const SpeechSynthesis = window.speechSynthesis;

if (!SpeechRecognition) {
    alert("Your browser does not support the Web Speech API. Please use Chrome or Edge.");
}

const recognition = new SpeechRecognition();
recognition.continuous = false;
recognition.lang = 'en-US';
recognition.interimResults = false;

let isBookingMode = false;
let lastCondition = null;

// --- Event Listeners ---

micBtn.addEventListener('click', () => {
    recognition.start();
    micBtn.classList.add('listening');
    textInput.placeholder = "Listening...";
});

stopBtn.addEventListener('click', () => {
    SpeechSynthesis.cancel();
    micBtn.classList.remove('listening');
    textInput.placeholder = "Type your symptoms here...";
});

sendBtn.addEventListener('click', () => {
    const text = textInput.value.trim();
    if (text) {
        processUserInput(text);
        textInput.value = '';
    }
});

textInput.addEventListener('keypress', (e) => {
    if (e.key === 'Enter') {
        const text = textInput.value.trim();
        if (text) {
            processUserInput(text);
            textInput.value = '';
        }
    }
});

emergencyBtn.addEventListener('click', () => {
    emergencyMenu.classList.toggle('hidden');
});

// Close menu when clicking outside
document.addEventListener('click', (e) => {
    if (!emergencyBtn.contains(e.target) && !emergencyMenu.contains(e.target)) {
        emergencyMenu.classList.add('hidden');
    }
});

// --- Speech Recognition ---

recognition.onresult = (event) => {
    const text = event.results[0][0].transcript;
    processUserInput(text);
};

recognition.onend = () => {
    micBtn.classList.remove('listening');
    textInput.placeholder = "Type your symptoms here...";
};

recognition.onerror = (event) => {
    micBtn.classList.remove('listening');
    textInput.placeholder = "Error. Try again.";
    console.error(event.error);
};

// --- Logic & UI ---

function processUserInput(text) {
    addMessage(text, 'user-message');

    if (isBookingMode) {
        handleBookingResponse(text);
    } else {
        showTyping();
        // Simulate analysis delay for effect
        setTimeout(() => {
            sendToBackend(text);
        }, 1000);
    }
}

function showTyping() {
    typingIndicator.classList.remove('hidden');
    chatHistory.scrollTop = chatHistory.scrollHeight;
}

function hideTyping() {
    typingIndicator.classList.add('hidden');
}

function addMessage(text, className) {
    const div = document.createElement('div');
    div.classList.add('message', className);

    // Check if it's a bot message with complex content (detected by HTML tags or newlines)
    if (className === 'bot-message' && (text.includes('**') || text.includes('\n'))) {
        div.innerHTML = formatBotResponse(text);
    } else {
        div.textContent = text;
    }

    chatHistory.appendChild(div);
    chatHistory.scrollTop = chatHistory.scrollHeight;
}

function formatBotResponse(text) {
    // Convert the markdown-like string into a nice HTML structure
    // This is a simple parser tailored to the specific output format of medical_logic.js

    let html = text
        .replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>')
        .replace(/\n/g, '<br>');

    // Wrap sections in cards if possible (simple heuristic)
    if (html.includes('1. Detected Symptoms')) {
        html = html.replace('<strong>1. Detected Symptoms</strong>', '<div class="result-section"><h3>Detected Symptoms</h3>');
        html = html.replace('<strong>2. Possible Conditions', '</div><div class="result-section"><h3>Possible Conditions');
        html = html.replace('<strong>3. Safe OTC Medicines', '</div><div class="result-section"><h3>Safe OTC Medicines</h3>');
        html = html.replace('<strong>4. First-Aid Advice', '</div><div class="result-section"><h3>First-Aid Advice</h3>');
        html = html.replace('<strong>5. When to See a Real Doctor', '</div><div class="result-section"><h3>When to See a Doctor</h3>');
        html = html.replace('⚠️', '</div><div class="result-section emergency-alert"><i class="fa-solid fa-triangle-exclamation"></i> ');

        // Wrap the whole thing in a container if needed, but the message div acts as one.
    }

    return html;
}

function speak(text) {
    const cleanText = text.replace(/\*\*/g, '').replace(/⚠️/g, 'Warning:').replace(/🚨/g, 'Alert:');
    const utterance = new SpeechSynthesisUtterance(cleanText);
    utterance.volume = 0.5;
    SpeechSynthesis.speak(utterance);
}

async function sendToBackend(text) {
    try {
        // Local Logic Processing
        const symptoms = extractSymptoms(text);
        const responseText = getMedicalAdvice(symptoms);

        hideTyping();
        addMessage(responseText, 'bot-message');
        speak(responseText);

        if (symptoms.length > 0 && !responseText.includes("EMERGENCY DETECTED")) {
            isBookingMode = true;
            lastCondition = "Consultation";

            setTimeout(() => {
                const followUp = "Would you like me to book an appointment with a doctor?";
                addMessage(followUp, 'bot-message');
                speak(followUp);
            }, 5000);
        }

    } catch (error) {
        hideTyping();
        console.error('Error:', error);
        addMessage("Sorry, I encountered an error processing your request.", 'bot-message');
        speak("Sorry, I encountered an error processing your request.");
    }
}

async function handleBookingResponse(text) {
    isBookingMode = false;

    if (text.toLowerCase().includes('yes')) {
        const msg = "Opening Google Maps to find the nearest hospitals for you.";
        addMessage(msg, 'bot-message');
        speak(msg);

        // Redirect to Google Maps
        setTimeout(() => {
            window.open('https://www.google.com/maps/search/hospitals+near+me', '_blank');
        }, 1500);

    } else {
        const msg = "Okay, take care and get well soon!";
        addMessage(msg, 'bot-message');
        speak(msg);
    }
}
