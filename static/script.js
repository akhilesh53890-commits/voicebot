const micBtn = document.getElementById('mic-btn');
const stopBtn = document.getElementById('stop-btn');
const statusText = document.getElementById('status');
const chatHistory = document.getElementById('chat-history');

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

micBtn.addEventListener('click', () => {
    recognition.start();
    micBtn.classList.add('listening');
    statusText.textContent = "Listening...";
});

stopBtn.addEventListener('click', () => {
    SpeechSynthesis.cancel(); // Stop speaking
    statusText.textContent = "Voice stopped.";
    setTimeout(() => {
        statusText.textContent = "Tap to speak";
    }, 2000);
});

recognition.onresult = (event) => {
    const text = event.results[0][0].transcript;
    addMessage(text, 'user-message');

    if (isBookingMode) {
        handleBookingResponse(text);
    } else {
        sendToBackend(text);
    }
};

recognition.onend = () => {
    micBtn.classList.remove('listening');
    statusText.textContent = "Tap to speak";
};

recognition.onerror = (event) => {
    micBtn.classList.remove('listening');
    statusText.textContent = "Error occurred: " + event.error;
};

function addMessage(text, className) {
    const div = document.createElement('div');
    div.classList.add('message', className);

    // Parse simple markdown (bolding and newlines) for display
    let formattedText = text
        .replace(/\*\*(.*?)\*\*/g, '<b>$1</b>') // Bold
        .replace(/\n/g, '<br>'); // Newlines

    div.innerHTML = formattedText;
    chatHistory.appendChild(div);
    chatHistory.scrollTop = chatHistory.scrollHeight;
}

function speak(text) {
    // Strip markdown characters for speech
    const cleanText = text.replace(/\*\*/g, '').replace(/⚠️/g, 'Warning:').replace(/🚨/g, 'Alert:');
    const utterance = new SpeechSynthesisUtterance(cleanText);
    utterance.volume = 0.5; // Decrease volume (0.0 to 1.0)
    SpeechSynthesis.speak(utterance);
}

async function sendToBackend(text) {
    statusText.textContent = "Processing...";

    try {
        const response = await fetch('/api/process', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ text: text })
        });

        const data = await response.json();
        addMessage(data.response_text, 'bot-message');
        speak(data.response_text);

        if (data.booking_prompt) {
            isBookingMode = true;
            // We don't have 'condition' explicitly anymore in the main response, 
            // but we can infer or just pass a generic term if needed for booking.
            // For now, let's just ask.
            setTimeout(() => {
                const followUp = "Would you like me to book an appointment with a doctor?";
                addMessage(followUp, 'bot-message');
                speak(followUp);
            }, 5000); // Wait a bit before asking
        }

    } catch (error) {
        console.error('Error:', error);
        addMessage("Sorry, I encountered an error connecting to the server.", 'bot-message');
        speak("Sorry, I encountered an error connecting to the server.");
    }

    statusText.textContent = "Tap to speak";
}

async function handleBookingResponse(text) {
    isBookingMode = false; // Reset mode

    if (text.toLowerCase().includes('yes')) {
        try {
            const response = await fetch('/api/book', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ condition: "Consultation" }) // Generic condition
            });

            const data = await response.json();
            addMessage(data.response_text, 'bot-message');
            speak(data.response_text);

        } catch (error) {
            console.error('Error:', error);
        }
    } else {
        const msg = "Okay, take care and get well soon!";
        addMessage(msg, 'bot-message');
        speak(msg);
    }
}
