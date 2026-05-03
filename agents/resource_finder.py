from core.llm_setup import get_llm_response

def recommend_resources(goal, goal_type):

    domain_rules = {
        "ai_ml": "Python, Machine Learning, datasets, Kaggle, HuggingFace",
        "frontend": "HTML, CSS, JavaScript, React, UI/UX resources ONLY",
        "backend": "Node.js, Express, APIs, databases ONLY",
        "devops": "Docker, Kubernetes, AWS, CI/CD tools ONLY",
        "generic": "general learning platforms like Coursera, YouTube"
    }

    constraint = domain_rules.get(goal_type, "general learning")

    prompt = f"""
You are an expert learning advisor.

Goal: {goal}
Domain: {goal_type}

STRICT DOMAIN RULE:
{constraint}

RULES:
- Give ONLY domain-specific resources
- Max 6 resources
- Each must be REAL and clickable
- Use markdown format ONLY
- No explanation
- No repetition

OUTPUT FORMAT:
- [Resource Title](https://link)
- [Resource Title](https://link)
"""

    return get_llm_response(prompt)