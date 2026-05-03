from core.llm_setup import get_llm_response
from core.memory import save_to_memory

def give_advice(progress):    
    prompt = f"""
You are an AI career mentor.

User progress:
{progress}

Give actionable advice.

RULES:
- Max 5 points
- Each line max 12 words
- Include improvement + next step
- Keep it practical

FORMAT:
Advice 1:
Advice 2:
"""

    result = get_llm_response(prompt)

    save_to_memory({
        "progress": progress,
        "advice": result
    })

    return result