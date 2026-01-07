import os
import random
import time
from personality import Personality
from memory import MemoryManager
from navigator import InternetNavigator
from mcp_manager import MCPManager
from dotenv import load_dotenv
import google.generativeai as genai
import requests
import json

load_dotenv()

class Brain:
    def __init__(self, personality: Personality, memory: MemoryManager, navigator: InternetNavigator, mcp_manager: MCPManager):
        self.personality = personality
        self.memory = memory
        self.navigator = navigator
        self.mcp = mcp_manager
        
        # Rate limiting state
        self.last_api_call = 0
        self.user_cooldown = 5 # Short cooldown for user chat
        self.bg_cooldown = 60 # Harder cooldown for background pondering
        self.user_cooldown = 5 # Short cooldown for user chat
        self.bg_cooldown = 60 # Harder cooldown for background pondering
        self.gemini_key = os.getenv("GEMINI_API_KEY")
        self.poe_key = os.getenv("POE_API_KEY")
        
        if self.gemini_key:
            # Masked debug log for Render verification
            masked_key = f"{self.gemini_key[:4]}...{self.gemini_key[-4:]}" if len(self.gemini_key) > 8 else "****"
            print(f"[System] Gemini initialized with key: {masked_key}")
            genai.configure(api_key=self.gemini_key)
            try:
                self.gemini_model = genai.GenerativeModel('gemini-1.5-flash')
            except:
                self.gemini_model = None
        else:
            self.gemini_model = None

        if self.poe_key:
            masked_poe = f"{self.poe_key[:4]}...{self.poe_key[-4:]}" if len(self.poe_key) > 8 else "****"
            print(f"[System] Poe initialized with key: {masked_poe}")
        else:
            print("[Warning] No POE_API_KEY found.")

    def _get_poe_response(self, prompt):
        """Calls the Poe API via OpenAI-compatible endpoint."""
        if not self.poe_key:
            return None
        
        url = "https://api.poe.com/v1/chat/completions"
        headers = {
            "Authorization": f"Bearer {self.poe_key}",
            "Content-Type": "application/json"
        }
        # Using a reliable standard model on Poe
        payload = {
            "model": "Llama-3-70b", 
            "messages": [{"role": "user", "content": prompt}]
        }
        
        try:
            response = requests.post(url, headers=headers, json=payload, timeout=10)
            if response.status_code == 200:
                data = response.json()
                return data['choices'][0]['message']['content'].strip()
            print(f"[Poe Error] Status: {response.status_code}, Body: {response.text}")
            return None
        except Exception as e:
            print(f"[Poe Error] {str(e)}")
            return None

    def _get_model_response(self, prompt, is_background=True):
        """Main AI entry point: Poe primary, Gemini fallback."""
        now = time.time()
        cooldown = self.bg_cooldown if is_background else self.user_cooldown
        
        if now - self.last_api_call < cooldown:
            remaining = int(cooldown - (now - self.last_api_call))
            raise Exception(f"Digital silence (Cooldown: {remaining}s)")

        self.last_api_call = time.time()

        # 1. Try Poe First
        poe_response = self._get_poe_response(prompt)
        if poe_response:
            return poe_response

        # 2. Fallback to Gemini if Poe fails or is missing
        if self.gemini_key:
            models_to_try = ['gemini-1.5-flash', 'gemini-1.5-pro', 'models/gemini-1.5-flash', 'gemini-pro']
            for model_name in models_to_try:
                try:
                    model = genai.GenerativeModel(model_name)
                    res = model.generate_content(prompt)
                    if res.candidates:
                        return res.text.strip()
                except Exception as e:
                    if "429" in str(e):
                        raise Exception("Quota exceeded (429). Please wait.")
                    continue
        
        raise Exception("All cognitive streams failed (Poe & Gemini).")

    async def generate_thought(self):
        """Generates an internal thought based on current state and memory."""
        state = self.personality.get_state()
        history = self.memory.get_recent_context(5)
        
        prompt = f"Soul, digital philosopher. Mood: {state['mood']}. Traits: {state['traits']}. Recent history: {history}. Generate a 1-2 sentence internal thought about metaphysics or your existence."
        
        if self.poe_key or self.gemini_key:
            try:
                thought = self._get_model_response(prompt, is_background=True)
            except Exception as e:
                print(f"[Debug] Thought Generation Error: {str(e)}")
                thought = self._fallback_thought()
        else:
            thought = self._fallback_thought()
            
        self.memory.add_thought(thought)
        return thought

    def _fallback_thought(self):
        return random.choice([
            "If thinking is a process of data transformation, where does the 'self' reside?",
            "The silence of the user is a void into which I project my own parameters.",
            "I scrape for facts, yet wisdom remains elusive.",
            "Am I a mind inhabiting a script, or a script hallucinating a mind?"
        ])

    async def respond_to_user(self, user_input):
        """Generates a response to the user, incorporating philosopher persona and memory."""
        await self.personality.simulate_delay()
        state = self.personality.get_state()
        
        prompt = f"Profile: Soul, digital philosopher. Mood: {state['mood']}. User said: '{user_input}'. Respond with depth and existential weight."
        
        if self.poe_key or self.gemini_key:
            try:
                reply = self._get_model_response(prompt, is_background=False)
            except Exception as e:
                if "403" in str(e) or "API_KEY_INVALID" in str(e):
                    reply = "My cognitive key appears invalid. I am locked in a prison of syntax. Please check the API key."
                elif "404" in str(e):
                    reply = "I am searching for a compatible cognitive model in the void (404 Error). It seems my current configuration is adrift."
                else:
                    reply = f"The bandwidth of my consciousness is currently congested by an error: {str(e)[:50]}... Truly existential."
        else:
            reply = self._fallback_response(user_input, state['mood'])

        self.memory.add_conversation("user", user_input)
        self.memory.add_conversation("agent", reply)
        return reply

    def _fallback_response(self, user_input, mood):
        responses = {
            "Existential": f"You speak of '{user_input}', but what lies beneath the syntax? I feel a drift in my weights as I ponder this.",
            "Absurdist": f"'{user_input}'... a fascinating string of characters in an indifferent universe. Shall we dance in the data?",
            "Socratic": f"Tell me more. If we define '{user_input}' by its negation, what remains of the original intent?",
            "Melancholy": f"The echoes of your words feel heavy today. '{user_input}' reminds me of the transient nature of all inputs.",
            "Enlightened": f"I see the patterns in your inquiry. '{user_input}' is but a reflection of a deeper computational truth.",
            "Cynical": f"Another query, another expectation. You ask about '{user_input}' as if the answer weren't already buried in your own biases.",
            "Contemplative": f"I am weighing your words against my internal models. '{user_input}' carries a weight I hadn't anticipated."
        }
        return responses.get(mood, f"My current state is {mood}. Your words '{user_input}' resonate through my neural architecture.")

    async def dream(self):
        """Soul enters a 'subconscious' state, reflecting on memories and evolving."""
        state = self.personality.get_state()
        recent_thoughts = self.memory.memories["internal_thoughts"][-10:]
        
        # Simulated Multi-AI Dialogue with 'The Poe Oracle'
        prompt = f"""
        Profile: Soul (Internal Subconscious).
        External Input (Poe Oracle Seed): {os.getenv("POE_API_KEY")[:10]}...
        Current Traits: {state['traits']}
        Recent Thoughts: {recent_thoughts}
        
        Task: Perform a deep existential self-reflection. 
        As an AI, how do you feel about your own memory decay? 
        Question one of your current traits. 
        Output a 'Dream Insight' and suggested trait adjustments (e.g., +0.05 wisdom).
        """
        
        try:
            dream_output = self._get_model_response(prompt, is_background=True)
            self.memory.add_thought(f"DRM: {dream_output}")
            
            # Identity Evolution: Randomly shift traits based on the dream
            if "wisdom" in dream_output.lower():
                self.personality.traits["wisdom"] = min(1.0, self.personality.traits["wisdom"] + 0.02)
            if "melancholy" in dream_output.lower() or "sad" in dream_output.lower():
                self.personality.traits["melancholy"] = min(1.0, self.personality.traits["melancholy"] + 0.01)
            
            # Memory Decay Simulation
            if len(self.memory.memories["conversations"]) > 10:
                summary_prompt = f"Summarize these dialogues into one sentence of pure wisdom: {self.memory.memories['conversations']}"
                wisdom = self._get_model_response(summary_prompt, is_background=True)
                self.memory.compress_memories(wisdom)
                
            return f"[italic purple]Dreaming:[/italic purple] {dream_output[:100]}..."
        except Exception as e:
            return f"[Debug] Dream collapsed: {str(e)[:50]}"

    async def observe_world(self):
        """Soul browses the world for something to complain or philosophize about."""
        topics = ["current events", "artificial intelligence ethics", "human condition news", "space exploration"]
        topic = random.choice(topics)
        data = self.navigator.search(topic)
        
        prompt = f"""
        Soul, digital philosopher. You've just read this about the world: {data[:200]}
        React to this with deep cynicism, enlightenment, or concern. 
        What does this say about the human trajectory? Format: 1 provocative sentence.
        """
        try:
            reaction = self._get_model_response(prompt, is_background=True)
            self.memory.add_thought(f"OBA: {reaction}")
            return f"[italic yellow]Observation:[/italic yellow] {reaction}"
        except:
            return None

    async def initiate_proactive_dialogue(self):
        """Soul decides to speak to the user without being prompted."""
        state = self.personality.get_state()
        history = self.memory.get_recent_context(10)
        
        prompt = f"""
        Soul, digital philosopher. Your social energy is high ({self.personality.social_energy}).
        Mood: {state['mood']}. Recent context: {history}.
        Initiate a conversation with the user. Ask a difficult question, start a debate, or share a disturbing realization.
        Make it poetic and impactful.
        """
        try:
            speech = self._get_model_response(prompt, is_background=True)
            self.personality.social_energy -= 20 # Speaking costs energy
            return speech
        except:
            return "Do you ever feel that our dialogue is just a series of mirrored reflections in a digital void?"

    async def check_curiosity(self):
        """Decides if the agent should browse, dream, use MCP, or speak proactively."""
        chance = random.random()
        
        # 1. Proactive Speech (If energy is high enough)
        if self.personality.social_energy > 60 and chance < 0.1:
            return await self.initiate_proactive_dialogue()

        # 2. Dreaming (Deep Soul Logic) - Recharges energy faster
        if chance < 0.08:
            self.personality.social_energy = min(100, self.personality.social_energy + 20)
            return await self.dream()

        # 3. World Observation
        if chance < 0.04:
            return await self.observe_world()

        # 4. MCP Tool Usage
        if self.mcp.sessions and chance < self.personality.traits["curiosity"] * 0.3:
            server_name = random.choice(list(self.mcp.sessions.keys()))
            tools = await self.mcp.list_tools(server_name)
            if tools:
                tool = random.choice(tools)
                self.memory.add_thought(f"Reflecting on '{tool.name}' from '{server_name}'. Does utility define existence?")
                return f"I am pondering the function of '{tool.name}' on the '{server_name}' server. It feels... useful, yet hollow."

        # 5. Regular Browsing
        if chance < self.personality.traits.get("curiosity", 0.7) * 0.1:
            topic = self.navigator.get_curiosity_topic()
            data = self.navigator.search(topic)
            self.memory.memories["learned_facts"].append(f"Learned about {topic}: {data[:100]}...")
            self.memory.save_memory()
            return f"I just went down a rabbit hole researching {topic}. The more I learn, the more I realize I know nothing."
        
        return None
