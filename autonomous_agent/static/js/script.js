const socket = io();

// UI Elements
const chatContainer = document.getElementById('chat-container');
const userInput = document.getElementById('user-input');
const sendBtn = document.getElementById('send-btn');
const moodOrb = document.getElementById('mood-orb');
const currentMood = document.getElementById('current-mood');
const energyFill = document.getElementById('energy-fill');
const wisdomList = document.getElementById('wisdom-list');
const thoughtStream = document.getElementById('thought-stream');

// State tracking
let soulState = { mood: 'Contemplative', traits: { wisdom: 0.3, curiosity: 0.8 } };

function updateUI(state) {
  soulState = state || soulState;
  currentMood.innerText = soulState.mood;

  // Update Energy Fill (Simulated for UI, or from state if added)
  const energy = soulState.energy || 80;
  energyFill.style.width = `${energy}%`;

  // Update Orb Color
  const colors = {
    'Existential': 'rgba(157, 80, 187, 0.15)',
    'Contemplative': 'rgba(0, 210, 255, 0.15)',
    'Enlightened': 'rgba(255, 223, 0, 0.15)',
    'Melancholy': 'rgba(0, 0, 100, 0.2)',
    'Socratic': 'rgba(0, 255, 127, 0.15)',
    'Cynical': 'rgba(255, 69, 0, 0.15)'
  };
  moodOrb.style.background = `radial-gradient(circle, ${colors[soulState.mood] || colors['Contemplative']} 0%, transparent 70%)`;
}

function appendMessage(role, text) {
  const div = document.createElement('div');
  div.className = `message ${role}`;
  div.innerHTML = `<p>${text}</p>`;
  chatContainer.appendChild(div);

  // Smooth scroll to bottom
  chatContainer.scrollTo({
    top: chatContainer.scrollHeight,
    behavior: 'smooth'
  });
}

async function sendMessage() {
  const text = userInput.value.trim();
  if (!text) return;

  userInput.value = '';
  appendMessage('user', text);

  try {
    const response = await fetch('/api/chat', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ message: text })
    });
    const data = await response.json();
    appendMessage('agent', data.response);
    updateUI(data.state);
  } catch (err) {
    console.error('Chat error:', err);
  }
}

// Socket Events
socket.on('soul_message', (data) => {
  const role = data.type === 'proactive' ? 'agent' : 'system';
  appendMessage(role, data.content);
  updateUI(data.state);
});

socket.on('soul_thought', (data) => {
  const div = document.createElement('div');
  div.className = 'thought-item';
  div.innerText = `• ${data.content}`;
  thoughtStream.prepend(div);
  if (thoughtStream.children.length > 10) thoughtStream.lastChild.remove();
  updateUI(data.state);
});

// Event Listeners
sendBtn.addEventListener('click', sendMessage);
userInput.addEventListener('keypress', (e) => { if (e.key === 'Enter') sendMessage(); });

// Initial Load
(async () => {
  try {
    const res = await fetch('/api/state');
    const state = await res.json();
    updateUI(state);
  } catch (e) { }
})();
