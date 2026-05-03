from core.memory import load_memory

def analyze_user():
    memory = load_memory()

    if not memory:
        return "new user"

    goals = [m.get("goal", "") for m in memory]

    if any("beginner" in g.lower() for g in goals):
        return "beginner"
    elif any("advanced" in g.lower() for g in goals):
        return "advanced"
    
    return "intermediate"