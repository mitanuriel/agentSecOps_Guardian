// DOM Elements
const postForm = document.getElementById('postForm');
const generateBtn = document.getElementById('generateBtn');
const resultSection = document.getElementById('resultSection');
const errorSection = document.getElementById('errorSection');
const loadingSection = document.getElementById('loadingSection');
const postOutput = document.getElementById('postOutput');
const errorMessage = document.getElementById('errorMessage');
const modelBadge = document.getElementById('modelBadge');
const copyBtn = document.getElementById('copyBtn');
const newPostBtn = document.getElementById('newPostBtn');
const dismissErrorBtn = document.getElementById('dismissErrorBtn');

// API Configuration
const API_BASE_URL = window.location.origin;

// Local Storage for API Key
const STORAGE_KEY = 'mistral_api_key';

// Custom Cursor
const cursor = document.createElement('div');
cursor.className = 'custom-cursor';
document.body.appendChild(cursor);

const follower = document.createElement('div');
follower.className = 'cursor-follower';
document.body.appendChild(follower);

let mouseX = 0, mouseY = 0;
let followerX = 0, followerY = 0;

document.addEventListener('mousemove', (e) => {
    mouseX = e.clientX;
    mouseY = e.clientY;
    
    // Instant cursor response - no delay
    cursor.style.left = mouseX + 'px';
    cursor.style.top = mouseY + 'px';
    
    // Create sparkle effect more frequently
    if (Math.random() > 0.93) {
        createSparkle(mouseX, mouseY);
    }
});

// Much faster follower animation
function animateFollower() {
    followerX += (mouseX - followerX) * 0.45;
    followerY += (mouseY - followerY) * 0.45;
    
    follower.style.left = followerX + 'px';
    follower.style.top = followerY + 'px';
    
    requestAnimationFrame(animateFollower);
}
animateFollower();

// Sparkle effect
function createSparkle(x, y) {
    const sparkle = document.createElement('div');
    sparkle.className = 'sparkle';
    sparkle.style.left = x + 'px';
    sparkle.style.top = y + 'px';
    sparkle.style.width = '6px';
    sparkle.style.height = '6px';
    sparkle.style.background = 'linear-gradient(135deg, #c084fc, #fbbf24)';
    sparkle.style.borderRadius = '50%';
    sparkle.style.boxShadow = '0 0 10px #c084fc';
    document.body.appendChild(sparkle);
    
    setTimeout(() => sparkle.remove(), 600);
}

// Load saved API key on page load
window.addEventListener('DOMContentLoaded', () => {
    const savedKey = localStorage.getItem(STORAGE_KEY);
    if (savedKey) {
        document.getElementById('apiKey').value = savedKey;
    }
});

// Form submission handler
postForm.addEventListener('submit', async (e) => {
    e.preventDefault();
    
    const apiKey = document.getElementById('apiKey').value.trim();
    const prompt = document.getElementById('prompt').value.trim();
    const model = document.getElementById('model').value;
    
    if (!apiKey || !prompt) {
        showError('Please fill in all required fields');
        return;
    }
    
    // Save API key to local storage
    localStorage.setItem(STORAGE_KEY, apiKey);
    
    // Hide previous results/errors
    hideAllSections();
    
    // Show loading
    loadingSection.classList.remove('hidden');
    generateBtn.disabled = true;
    
    try {
        const response = await fetch(`${API_BASE_URL}/generate-post`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                api_key: apiKey,
                prompt: prompt,
                model: model
            })
        });
        
        if (!response.ok) {
            const errorData = await response.json().catch(() => ({}));
            throw new Error(errorData.detail || `Server error: ${response.status}`);
        }
        
        const data = await response.json();
        displayResult(data);
        
    } catch (error) {
        console.error('Error generating post:', error);
        showError(error.message || 'Failed to generate post. Please check your API key and try again.');
    } finally {
        loadingSection.classList.add('hidden');
        generateBtn.disabled = false;
    }
});

// Display result
function displayResult(data) {
    hideAllSections();
    
    postOutput.textContent = data.post;
    modelBadge.textContent = data.model;
    
    resultSection.classList.remove('hidden');
    
    // Smooth scroll to result
    resultSection.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
}

// Show error
function showError(message) {
    hideAllSections();
    
    errorMessage.textContent = message;
    errorSection.classList.remove('hidden');
    
    // Smooth scroll to error
    errorSection.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
}

// Hide all sections
function hideAllSections() {
    resultSection.classList.add('hidden');
    errorSection.classList.add('hidden');
}

// Copy to clipboard
copyBtn.addEventListener('click', async () => {
    const text = postOutput.textContent;
    
    try {
        await navigator.clipboard.writeText(text);
        
        // Visual feedback
        const originalText = copyBtn.innerHTML;
        copyBtn.innerHTML = '<span>✅ Copied!</span>';
        copyBtn.style.background = 'var(--success)';
        
        setTimeout(() => {
            copyBtn.innerHTML = originalText;
            copyBtn.style.background = '';
        }, 2000);
        
    } catch (error) {
        console.error('Failed to copy:', error);
        showError('Failed to copy to clipboard');
    }
});

// Generate new post
newPostBtn.addEventListener('click', () => {
    hideAllSections();
    document.getElementById('prompt').focus();
    window.scrollTo({ top: 0, behavior: 'smooth' });
});

// Dismiss error
dismissErrorBtn.addEventListener('click', () => {
    errorSection.classList.add('hidden');
});

// Keyboard shortcuts
document.addEventListener('keydown', (e) => {
    // Ctrl/Cmd + Enter to submit form
    if ((e.ctrlKey || e.metaKey) && e.key === 'Enter') {
        postForm.dispatchEvent(new Event('submit'));
    }
});

// Auto-resize textarea
const promptTextarea = document.getElementById('prompt');
promptTextarea.addEventListener('input', function() {
    this.style.height = 'auto';
    this.style.height = (this.scrollHeight) + 'px';
});
