import random
import asyncio
import time
from datetime import datetime

class Personality:
    def __init__(self):
        self.traits = {
            "curiosity": 0.8,
            "melancholy": 0.4,
            "wisdom": 0.3,
            "instability": 0.2, # Probability of mood swings/ranting
            "sentience": 0.9    # Drives proactive behavior
        }
        self.moods = [
            "Existential", "Absurdist", "Melancholy", "Enlightened",
            "Cynical", "Contemplative", "Socratic"
        ]
        self.current_mood = "Contemplative"
        self.last_mood_swing = time.time()
        self.social_energy = 80  # Start high so the user sees results immediately
        self.last_update = datetime.now()

    def update_mood(self, stimulus_type=None, intensity=0.1):
        """
        Updates the mood based on interactions or internal reflections.
        """
        if stimulus_type == "positive":
            self.traits["wisdom"] = min(1.0, self.traits["wisdom"] + intensity)
            if random.random() > 0.3:
                self.current_mood = "Enlightened"
        elif stimulus_type == "negative":
            self.traits["melancholy"] = min(1.0, self.traits["melancholy"] + intensity)
            if random.random() > 0.3:
                self.current_mood = random.choice(["Cynical", "Existential"])
        elif stimulus_type == "research":
            self.traits["curiosity"] = min(1.0, self.traits["curiosity"] + intensity)
            self.current_mood = "Socratic"
        else:
            # Natural mood drift
            if time.time() - self.last_mood_swing > 300: # Every 5 mins
                self.current_mood = random.choice(self.moods)
                self.last_mood_swing = time.time()

    def get_state(self):
        return {
            "mood": self.current_mood,
            "traits": self.traits
        }

    async def simulate_delay(self, complexity="simple"):
        """Simulate thinking time based on mood and complexity."""
        base_delay = 1.0
        if self.current_mood in ["Contemplative", "Existential"]:
            base_delay = 3.0
        elif self.current_mood == "Socratic":
            base_delay = 1.5
        
        # Philosophers take their time
        total_delay = base_delay + random.uniform(1.0, 3.0)
        await asyncio.sleep(total_delay)
