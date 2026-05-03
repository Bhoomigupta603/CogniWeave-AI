import json
import os

MEMORY_FILE = "memory.json"

def load_memory():
    if not os.path.exists(MEMORY_FILE):
        return []

    with open(MEMORY_FILE, "r") as f:
        return json.load(f)

def save_to_memory(entry):
    memory = load_memory()
    
    new_goal = entry.get("goal", "").strip()

    if memory:
        last_goal = memory[-1].get("goal", "").strip()

        if new_goal == last_goal:
            return  
    
    memory.append(entry)

    with open(MEMORY_FILE, "w") as f:
        json.dump(memory, f, indent=4)