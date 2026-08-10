// Smooth scrolling for navigation links
document.querySelectorAll('a[href^="#"]').forEach(anchor => {
    anchor.addEventListener('click', function (e) {
        e.preventDefault();
        const target = document.querySelector(this.getAttribute('href'));
        if (target) {
            target.scrollIntoView({
                behavior: 'smooth',
                block: 'start'
            });
        }
    });
});

// Project card click handlers
document.querySelectorAll('.project-card.clickable').forEach(card => {
    card.addEventListener('click', function() {
        // Check if it's a certificate card
        if (this.classList.contains('certificate-card')) {
            const certUrl = this.getAttribute('data-cert-url');
            if (certUrl) {
                window.open(certUrl, '_blank');
            }
        } else {
            // Regular project page
            const projectName = this.getAttribute('data-project');
            window.location.href = `projects/${projectName}.html`;
        }
    });
});

// Fade in animation on scroll
const observerOptions = {
    threshold: 0.1,
    rootMargin: '0px 0px -50px 0px'
};

const observer = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
        if (entry.isIntersecting) {
            entry.target.classList.add('visible');
        }
    });
}, observerOptions);

document.querySelectorAll('.fade-in').forEach(el => {
    observer.observe(el);
});

// Header background change on scroll
window.addEventListener('scroll', () => {
    const header = document.querySelector('header');
    if (window.scrollY > 100) {
        header.style.background = 'rgba(6, 12, 28, 0.97)';
    } else {
        header.style.background = 'rgba(6, 12, 28, 0.85)';
    }
});

const chatToggle = document.getElementById('chat-toggle');
const chatPanel = document.getElementById('chat-panel');
const chatClose = document.getElementById('chat-close');
const chatForm = document.getElementById('chat-form');
const chatMessages = document.getElementById('chat-messages');
const chatInput = document.getElementById('chat-input');

chatToggle.addEventListener('click', () => {
    chatPanel.classList.toggle('open');
    chatPanel.setAttribute('aria-hidden', chatPanel.classList.contains('open') ? 'false' : 'true');
    if (chatPanel.classList.contains('open')) {
        chatInput.focus();
    }
});

chatClose.addEventListener('click', () => {
    chatPanel.classList.remove('open');
    chatPanel.setAttribute('aria-hidden', 'true');
});

const portfolioText = document.body.innerText.toLowerCase();

function addMessage(text, sender) {
    const message = document.createElement('div');
    message.className = `chat-message ${sender}`;
    message.textContent = text;
    chatMessages.appendChild(message);
    chatMessages.scrollTop = chatMessages.scrollHeight;
}

function findRelevantAnswer(question) {
    const normalizedQuestion = question.toLowerCase();
    const answers = [];

    if (/projects|worked on|project(s)?/.test(normalizedQuestion)) {
        answers.push(
            'This portfolio highlights projects like Surveillance Anomaly Detection, Retail Sales Prediction System, and Cairo2Capital Transportation System.'
        );
    }

    if (/technolog(y|ies)|python|pytorch|tensorflow|xgboost|sql|mysql|html|css|javascript|php/.test(normalizedQuestion)) {
        answers.push(
            'Technologies mentioned include Python, PyTorch, TensorFlow, scikit-learn, XGBoost, pandas, HTML, CSS, JavaScript, PHP, and MySQL.'
        );
    }

    if (/internship|internships|interned/.test(normalizedQuestion)) {
        answers.push(
            'The portfolio does not list a specific internship employer, but it highlights project-based experience and certifications linked to AI, data science, and cloud technologies.'
        );
    }

    if (/certificate|certificates|credential/.test(normalizedQuestion)) {
        answers.push(
            'Certificates include Digital Egyptian Pioneers Initiative, AWS Cloud Foundations, and Introduction to MongoDB.'
        );
    }

    if (/surveillance anomaly detection|anomaly detection/.test(normalizedQuestion)) {
        answers.push(
            'Surveillance Anomaly Detection is a weakly supervised pipeline on the UCF-Crime dataset using a pretrained 3D two-stream CNN backbone, with a custom image processing pipeline and a paper under review at CESS 2026.'
        );
    }

    if (/retail sales prediction|retail prediction|xgboost/.test(normalizedQuestion)) {
        answers.push(
            'Retail Sales Prediction System is an end-to-end XGBoost forecasting pipeline built on 58.5M rows of retail data, achieving MAE 0.36 and R² 0.88 across store segments.'
        );
    }

    if (/cairo2capital|transportation|ticket/.test(normalizedQuestion)) {
        answers.push(
            'Cairo2Capital is a transportation website with OOP logic for ticket pricing, receipts, and a multi-phase system showcased at Deep Minds 4.'
        );
    }

    if (answers.length === 0) {
        return 'I am happy to help with questions about projects, skills, courses, certificates, education, and experience from this portfolio.';
    }

    return answers.join(' ');
}

async function sendQuestionToBot(userQuestion) {
    const localAnswer = findRelevantAnswer(userQuestion);
    if (localAnswer && !localAnswer.includes('I am happy to help')) {
        return localAnswer;
    }

    const endpoints = [
        '/api/chat',
        'http://127.0.0.1:8000/api/chat',
        'https://your-app-name.vercel.app/api/chat'
    ];

    for (const endpoint of endpoints) {
        try {
            const response = await fetch(endpoint, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({ message: userQuestion })
            });

            if (!response.ok) {
                continue;
            }

            const text = await response.text();
            if (text) {
                return text.trim();
            }
        } catch (error) {
            console.warn(`Chat endpoint failed: ${endpoint}`, error);
        }
    }

    return 'Sorry, I am having trouble connecting right now. Please email David directly at davidhalim2004@gmail.com.';
}

chatForm.addEventListener('submit', async (event) => {
    event.preventDefault();
    const question = chatInput.value.trim();
    if (!question) return;

    addMessage(question, 'user');
    chatInput.value = '';

    const loadingMessage = document.createElement('div');
    loadingMessage.className = 'chat-message bot';
    loadingMessage.textContent = 'Thinking...';
    chatMessages.appendChild(loadingMessage);
    chatMessages.scrollTop = chatMessages.scrollHeight;

    const answer = await sendQuestionToBot(question);
    loadingMessage.textContent = answer;
    chatMessages.scrollTop = chatMessages.scrollHeight;
});