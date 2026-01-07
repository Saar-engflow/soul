import os
import asyncio
import threading
import time
from flask import Flask, render_template, request, jsonify
from flask_socketio import SocketIO, emit
from flask_cors import CORS
from dotenv import load_dotenv

from personality import Personality
from memory import MemoryManager
from navigator import InternetNavigator
from brain import Brain
from mcp_manager import MCPManager

load_dotenv()

app = Flask(__name__)
CORS(app)
socketio = SocketIO(app, cors_allowed_origins="*", async_mode='eventlet')

# Initialize Soul's core
personality = Personality()
memory = MemoryManager()
navigator = InternetNavigator()
mcp = MCPManager()
brain = Brain(personality, memory, navigator, mcp)

def soul_heartbeat():
    """Background thread to handle Soul's proactive nature."""
    # Create a new event loop for this thread
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    
    while True:
        try:
            # Ponder every 60-120 seconds to stay within free tier quota
            time.sleep(os.urandom(1)[0] % 60 + 60)
            
            # Check for proactive behavior
            action_result = loop.run_until_complete(brain.check_curiosity())
            
            if action_result:
                # Determine if it's a thought or proactive speech
                msg_type = "insight" if "[" in action_result else "proactive"
                socketio.emit('soul_message', {
                    'type': msg_type,
                    'content': action_result,
                    'state': personality.get_state()
                })
            else:
                # Occasional silent thought
                thought = loop.run_until_complete(brain.generate_thought())
                socketio.emit('soul_thought', {
                    'content': thought,
                    'state': personality.get_state()
                })
        except Exception as e:
            print(f"[Soul Heartbeat Error] {e}")

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/state', methods=['GET'])
def get_state():
    return jsonify(personality.get_state())

@app.route('/api/chat', methods=['POST'])
def chat():
    data = request.json
    user_input = data.get('message')
    
    if not user_input:
        return jsonify({'error': 'No input provided'}), 400
    
    # Run the brain's response in the main event loop
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    response = loop.run_until_complete(brain.respond_to_user(user_input))
    
    return jsonify({
        'response': response,
        'state': personality.get_state()
    })

if __name__ == '__main__':
    # Start the heartbeat thread
    heartbeat_thread = threading.Thread(target=soul_heartbeat, daemon=True)
    heartbeat_thread.start()
    
    # Run server
    port = int(os.environ.get('PORT', 5000))
    socketio.run(app, host='0.0.0.0', port=port, debug=False)
