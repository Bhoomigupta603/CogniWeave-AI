import re
from core.llm_setup import get_llm_response

DOMAIN_RULES = {
    "machine learning": {
        "allowed": "model training, dataset preparation, feature engineering, "
                   "evaluation metrics, scikit-learn, PyTorch, Jupyter notebooks, "
                   "data preprocessing, hyperparameter tuning",
        "banned":  "business strategy, marketing, product planning, stakeholder management, "
                   "market research, OKRs, sales, monetization",
    },
    "ai": {
        "allowed": "machine learning, deep learning, NLP, computer vision, "
                   "datasets, model training, neural networks, Python, "
                   "scikit-learn, PyTorch, Hugging Face",
        "banned":  "business strategy, marketing, product planning, stakeholder management, "
                   "market research, OKRs, sales, monetization",
    },
    "web development": {
        "allowed": "frontend components, backend APIs, database design, "
                   "authentication, deployment, React, Node.js, Flask, SQL",
        "banned":  "business strategy, market research, product roadmap planning, "
                   "investor pitches, monetization",
    },
    "data science": {
        "allowed": "data cleaning, exploratory analysis, visualization, "
                   "SQL queries, statistical analysis, dashboards, Python, Pandas",
        "banned":  "business strategy, marketing, product planning, sales, OKRs",
    },
    "devops": {
        "allowed": "CI/CD pipelines, Docker, Kubernetes, infrastructure automation, "
                   "monitoring, bash scripting, cloud deployment, Git workflows",
        "banned":  "business strategy, market research, product planning, sales",
    },
    "cybersecurity": {
        "allowed": "penetration testing, vulnerability scanning, CTF challenges, "
                   "network analysis, secure coding, Nmap, Burp Suite, TryHackMe",
        "banned":  "business strategy, marketing, product planning, sales",
    },
    "cloud": {
        "allowed": "AWS services, Terraform, infrastructure as code, "
                   "cloud networking, serverless functions, IAM, cost optimization",
        "banned":  "business strategy, market research, product planning, sales",
    },
    "android": {
        "allowed": "Kotlin, Android Studio, UI components, REST API integration, "
                   "local storage, MVVM architecture, testing",
        "banned":  "business strategy, app store marketing, monetization strategy",
    },
    "ios": {
        "allowed": "Swift, SwiftUI, UIKit, CoreData, REST API integration, "
                   "TestFlight, Xcode, local notifications",
        "banned":  "business strategy, app store marketing, monetization strategy",
    },
    "blockchain": {
        "allowed": "Solidity, smart contracts, testnet deployment, "
                   "Hardhat, wallet integration, ERC standards, gas optimization",
        "banned":  "tokenomics business strategy, ICO planning, investor relations",
    },
    "data engineering": {
        "allowed": "ETL pipelines, Airflow DAGs, SQL transformations, "
                   "Snowflake, dbt models, data quality checks, Python",
        "banned":  "business strategy, market research, product planning, sales",
    },
}

# ─── Level-based task complexity guidance ────────────────────────────────────
LEVEL_TASK_GUIDANCE = {
    "beginner": (
        "Tasks must be small and achievable in 1–3 days. "
        "Use only simple tools (Python, Pandas, scikit-learn, Flask). "
        "No deployment, no auth, no advanced systems. "
        "Example good task: 'Build a CSV data cleaner using Pandas and export results.'"
    ),
    "intermediate": (
        "Tasks should involve real projects with APIs, databases, and deployment. "
        "Each task should produce a working component. "
        "Example good task: 'Build and deploy a REST API with FastAPI and PostgreSQL on Render.'"
    ),
    "advanced": (
        "Tasks should involve production-grade systems, optimization, or research. "
        "Include architecture decisions, scaling, or open-source contributions. "
        "Example good task: 'Optimize transformer inference latency using ONNX quantization.'"
    ),
}


def _extract_roadmap_bullets(roadmap: str) -> list[str]:
    """
    Returns all bullet point lines from the roadmap.
    Strips the leading "- " so the LLM sees clean action phrases.

    Example input line:  "- Train XGBoost model on Titanic dataset using scikit-learn"
    Example output item: "Train XGBoost model on Titanic dataset using scikit-learn"
    """
    bullets = []
    for line in roadmap.splitlines():
        stripped = line.strip()
        
        if stripped.startswith("- ") or stripped.startswith("➤"):
            # cleaned = stripped.replace("➤", "").replace("- ", "").strip()
            #better version
            cleaned = stripped.replace("➤", "").lstrip("- ").strip()

            if cleaned:   # avoid empty lines
                bullets.append(cleaned)
        
    return bullets


def _calculate_task_range(roadmap: str) -> tuple[int, int]:
    """
    Returns (min_tasks, max_tasks) based on the number of roadmap steps.

    Examples:
        6-month roadmap  →  (6, 10)
        4-month roadmap  →  (4, 8)
        3-week roadmap   →  (3, 6)   ← floor applied
        2-week roadmap   →  (3, 6)   ← floor applied
    """
    # Count lines that look like "Month N:" or "Week N:"
    header_pattern = re.compile(r'^\s*(month|week)\s+\d+\s*:', re.IGNORECASE)
    step_count = sum(1 for line in roadmap.splitlines() if header_pattern.match(line))

    if step_count == 0:
        step_count = 4   # safe fallback if roadmap has no recognised headers

    min_tasks = max(3, step_count)
    max_tasks = min(12, step_count + 4)
    return (min_tasks, max_tasks)


def _get_domain_context(goal_type: str):

    mapping = {

        "ai_ml": {
            "allowed": "Python, datasets, scikit-learn, PyTorch, ML models, training, evaluation",
            "banned": "HTML, CSS, React, APIs, databases, DevOps tools"
        },

        "frontend": {
            "allowed": "HTML, CSS, JavaScript, React, UI components, responsive design",
            "banned": "Python, Flask, APIs, databases, DevOps, machine learning"
        },

        "backend": {
            "allowed": "APIs, Node.js, Express, Flask, databases, authentication",
            "banned": "HTML design, CSS styling, React UI, machine learning"
        },

        "devops": {
            "allowed": "Docker, Kubernetes, CI/CD, cloud deployment, monitoring",
            "banned": "HTML, CSS, React, ML models, datasets"
        },

        "generic": {
            "allowed": "learning, practice, skill building, real-world tasks",
            "banned": "business strategy, marketing, product planning"
        }
    }

    rules = mapping.get(goal_type, mapping["generic"])
    return rules["allowed"], rules["banned"]


def _sanitize_tasks(text: str) -> str:
    """
    Keeps only lines matching "Task N: ..." and discards everything else.
    Preserves original task text after the colon exactly as written.
    """
    task_pattern = re.compile(r'^Task\s+\d+\s*:', re.IGNORECASE)
    kept = [line.strip() for line in text.splitlines() if task_pattern.match(line.strip())]
    return "\n".join(kept)



def generate_tasks(goal, roadmap, user_level, goal_type):
    """
    Generates dynamic, roadmap-driven tasks.

    Parameters:
        goal       : user's original goal string
        roadmap    : full roadmap text from generate_goal_plan()
        user_level : "beginner" | "intermediate" | "advanced"

    Returns:
        Clean string of "Task 1: ...\nTask 2: ..." lines only.
    """

    # ── Extract context from roadmap ──────────────────────────────────────────
    bullets          = _extract_roadmap_bullets(roadmap)
    min_t, max_t     = _calculate_task_range(roadmap)
    allowed, banned = _get_domain_context(goal_type)
    level_guidance   = LEVEL_TASK_GUIDANCE.get(
                           user_level.lower().strip(),
                           LEVEL_TASK_GUIDANCE["beginner"]
                       )

    bullets_text = "\n".join(
        f"  {i+1}. {b}" for i, b in enumerate(bullets)
    ) if bullets else "  (no bullet points extracted — use goal and domain to create tasks)"

    prompt = f"""
You are a technical task planner for a career roadmap.

━━━━━━━━━━━━━━━━━━━━
USER CONTEXT
━━━━━━━━━━━━━━━━━━━━
Goal       : {goal}
Level      : {user_level}
Domain     : {goal_type}
Task count : generate between {min_t} and {max_t} tasks

━━━━━━━━━━━━━━━━━━━━
ROADMAP ACTIONS (use these to generate tasks)
━━━━━━━━━━━━━━━━━━━━
{bullets_text}

━━━━━━━━━━━━━━━━━━━━
LEVEL GUIDANCE
━━━━━━━━━━━━━━━━━━━━
{level_guidance}

━━━━━━━━━━━━━━━━━━━━
DOMAIN RULES
━━━━━━━━━━━━━━━━━━━━
Tasks MUST come from these categories only:
{allowed}

NEVER include tasks from:
{banned}

━━━━━━━━━━━━━━━━━━━━
TASK RULES
━━━━━━━━━━━━━━━━━━━━
Each task must be directly derived from a roadmap action above
Each task must name a specific tool or dataset
Each task must state a concrete output (e.g. "and push to GitHub")
Each task MUST include tool + action + output   
Each task max 15 words
Generate between {min_t} and {max_t} tasks

No generic tasks ("research the topic", "understand the concept")
No business/product/marketing tasks
No intro text, no headings, no explanation — ONLY tasks

━━━━━━━━━━━━━━━━━━━━
OUTPUT FORMAT — FOLLOW EXACTLY
━━━━━━━━━━━━━━━━━━━━
Task 1: [action + tool + output]
Task 2: [action + tool + output]
Task 3: [action + tool + output]
...up to Task {max_t}
"""

    raw = get_llm_response(prompt)

    # ── Sanitize: keep only "Task N: ..." lines ───────────────────────────────
    return _sanitize_tasks(raw)

