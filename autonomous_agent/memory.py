import json
import os
from datetime import datetime

class MemoryManager:
    def __init__(self, storage_path="memory.json"):
        self.storage_path = storage_path
        self.memories = self.load_memory()

    def load_memory(self):
        if os.path.exists(self.storage_path):
            try:
                with open(self.storage_path, "r") as f:
                    return json.load(f)
            except:
                return self._default_memory()
        return self._default_memory()

    def _default_memory(self):
        return {
            "conversations": [],
            "learned_facts": [],
            "internal_thoughts": [],
            "opinions": {},
            "wisdom": [], # Abstracted/Compressed memories
            "last_session": datetime.now().isoformat()
        }

    def save_memory(self):
        self.memories["last_session"] = datetime.now().isoformat()
        with open(self.storage_path, "w") as f:
            json.dump(self.memories, f, indent=4)

    def add_wisdom(self, insight):
        self.memories["wisdom"].append({
            "timestamp": datetime.now().isoformat(),
            "insight": insight
        })
        self.save_memory()

    def compress_memories(self, insight):
        """Replaces old conversations with a single 'wisdom' insight to simulate decay."""
        if len(self.memories["conversations"]) > 20:
            self.add_wisdom(f"From my early dialogues, I distilled this: {insight}")
            # Keep only the last 5 conversations
            self.memories["conversations"] = self.memories["conversations"][-5:]
            self.save_memory()

    def add_conversation(self, role, content):
        self.memories["conversations"].append({
            "timestamp": datetime.now().isoformat(),
            "role": role,
            "content": content
        })
        self.save_memory()

    def add_thought(self, thought):
        self.memories["internal_thoughts"].append({
            "timestamp": datetime.now().isoformat(),
            "thought": thought
        })
        self.save_memory()

    def update_opinion(self, topic, opinion):
        self.memories["opinions"][topic] = {
            "updated_at": datetime.now().isoformat(),
            "sentiment": opinion
        }
        self.save_memory()

    def get_recent_context(self, limit=10):
        return self.memories["conversations"][-limit:]

    def get_summary_of_work(self):
        """Returns a summary of what happened since the last user check-in."""
        recent_thoughts = self.memories["internal_thoughts"][-5:]
        recent_facts = self.memories["learned_facts"][-3:]
        return {
            "thoughts": [t["thought"] for t in recent_thoughts],
            "facts": recent_facts
        }
