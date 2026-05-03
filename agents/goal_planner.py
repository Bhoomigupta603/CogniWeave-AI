import re
from core.llm_setup import get_llm_response
from core.memory import save_to_memory, load_memory
import random

DOMAIN_BLUEPRINT = {

    "ai_ml": {
        "beginner": [
            "Learn Python basics (variables, loops, functions)",
            "Practice Python on small datasets",
            "Learn NumPy fundamentals",
            "Learn Pandas for data handling",
            "Clean and preprocess datasets",
            "Visualize data using Matplotlib",
            "Understand ML basics (supervised vs unsupervised)",
            "Train Linear Regression model",
            "Train Decision Tree model",
            "Evaluate models using accuracy and confusion matrix",
            "Work with real datasets like Iris or Titanic",
            "Build a mini ML project",
            "Upload project to GitHub",
            "Learn basics of model deployment (Streamlit)"
        ],

        "intermediate": [
            "Perform feature engineering on datasets",
            "Handle missing values and outliers",
            "Train Random Forest and SVM models",
            "Use cross-validation techniques",
            "Tune hyperparameters using GridSearchCV",
            "Work with real-world datasets (Kaggle)",
            "Build ML pipeline (data → model → evaluation)",
            "Learn deep learning basics using PyTorch",
            "Build neural network model",
            "Deploy ML model using Flask/Streamlit",
            "Optimize models using feature selection",
            "Participate in Kaggle competitions",
            "Build 2 strong ML projects",
            "Prepare ML interview questions"
        ],

        "advanced": [
            "Build deep learning models using PyTorch",
            "Implement CNN for image classification",
            "Implement RNN/LSTM for sequence modeling",
            "Work with NLP using transformers",
            "Fine-tune pretrained models like BERT",
            "Optimize models using hyperparameter tuning",
            "Use GPU/Colab for faster training",
            "Deploy models using FastAPI",
            "Work with large-scale datasets",
            "Implement model monitoring",
            "Use MLOps tools like MLflow",
            "Build production-level ML system",
            "Optimize inference performance",
            "Create portfolio with advanced projects"
        ]
    },

    "frontend": {
        "beginner": [
            "Learn HTML basics and page structure",
            "Style pages using CSS",
            "Understand Flexbox and Grid",
            "Build responsive layouts",
            "Learn basic JavaScript (variables, functions)",
            "Handle DOM manipulation",
            "Create simple interactive UI",
            "Build a personal portfolio website",
            "Use Bootstrap for styling",
            "Debug using browser dev tools",
            "Host website using GitHub Pages",
            "Improve UI/UX basics",
            "Create 2 small frontend projects",
            "Push projects to GitHub"
        ],

        "intermediate": [
            "Learn advanced JavaScript (closures, promises)",
            "Work with ES6 features",
            "Build apps using React",
            "Understand components and props",
            "Manage state using hooks",
            "Handle API calls using fetch/axios",
            "Implement routing using React Router",
            "Use Tailwind CSS",
            "Optimize UI performance",
            "Build dynamic web apps",
            "Deploy apps on Vercel/Netlify",
            "Work with forms and validation",
            "Build 2 React projects",
            "Prepare frontend interview questions"
        ],

        "advanced": [
            "Build scalable React applications",
            "Use Redux for state management",
            "Optimize performance using memoization",
            "Implement lazy loading",
            "Work with Next.js framework",
            "Build SSR and SSG apps",
            "Handle authentication flows",
            "Improve accessibility (a11y)",
            "Test UI using Jest",
            "Design reusable component systems",
            "Work with design systems",
            "Build production-level frontend apps",
            "Optimize SEO performance",
            "Deploy full production UI system"
        ]
    },

    "backend": {
        "beginner": [
            "Learn backend basics (Node.js/Python)",
            "Understand HTTP and APIs",
            "Build simple REST APIs",
            "Use Express or Flask framework",
            "Handle routing and middleware",
            "Connect to database (MongoDB/SQLite)",
            "Perform CRUD operations",
            "Test APIs using Postman",
            "Handle JSON data",
            "Implement authentication (JWT)",
            "Build secure APIs",
            "Handle error handling and logging",
            "Structure backend project properly",
            "Deploy backend using Render/Heroku",
            "Use environment variables",
            "Build final backend project"
        ],

        "intermediate": [
            "Implement JWT authentication system",
            "Work with PostgreSQL/MySQL",
            "Design scalable API architecture",
            "Use ORM tools (Sequelize/SQLAlchemy)",
            "Handle file uploads",
            "Implement logging system",
            "Optimize API performance",
            "Use caching basics",
            "Deploy backend on AWS",
            "Secure APIs using best practices",
            "Use environment configs",
            "Build 2 backend projects",
            "Write API documentation",
            "Prepare backend interviews"
        ],

        "advanced": [
            "Build microservices architecture",
            "Use Docker for containerization",
            "Implement caching using Redis",
            "Handle message queues (RabbitMQ)",
            "Design scalable backend systems",
            "Work with GraphQL APIs",
            "Implement rate limiting",
            "Monitor backend performance",
            "Use CI/CD pipelines",
            "Scale applications on cloud",
            "Optimize database queries",
            "Implement load balancing",
            "Build high-traffic backend systems",
            "Deploy production-ready backend"
        ]
    },

    "devops": {
        "beginner": [
            "Learn Linux basics and commands",
            "Understand Git and version control",
            "Work with GitHub repositories",
            "Understand CI/CD basics",
            "Install Docker and create containers",
            "Run simple apps in Docker",
            "Understand cloud basics (AWS/GCP)",
            "Deploy simple applications",
            "Monitor basic system logs",
            "Learn shell scripting basics",
            "Use environment variables",
            "Understand networking basics",
            "Build small DevOps pipeline",
            "Practice deployment workflows"
        ],

        "intermediate": [
            "Work with Docker Compose",
            "Build CI/CD pipelines",
            "Deploy apps on AWS/GCP",
            "Use Nginx for server setup",
            "Implement monitoring tools",
            "Handle load balancing",
            "Work with Terraform basics",
            "Manage infrastructure",
            "Automate deployments",
            "Secure cloud services",
            "Handle logs and alerts",
            "Optimize system performance",
            "Build real CI/CD pipeline",
            "Deploy scalable apps"
        ],

        "advanced": [
            "Manage Kubernetes clusters",
            "Deploy microservices using Kubernetes",
            "Use Helm charts",
            "Implement infrastructure as code",
            "Use Prometheus and Grafana",
            "Monitor distributed systems",
            "Optimize cloud cost",
            "Handle high availability systems",
            "Automate scaling",
            "Work with advanced networking",
            "Secure DevOps pipelines",
            "Build production DevOps systems",
            "Implement disaster recovery",
            "Deploy enterprise-level systems"
        ]
    }
}

# # =========================
# # HELPERS
# # =========================
def _detect_duration(goal: str):
    goal = goal.lower()

    # convert words → numbers
    word_to_num = {
        "one": 1, "two": 2, "three": 3,
        "four": 4, "five": 5, "six": 6
    }

    for word, num in word_to_num.items():
        if word in goal:
            goal = goal.replace(word, str(num))

    month_match = re.search(r'(\d+)\s*month', goal)
    week_match = re.search(r'(\d+)\s*week', goal)

    if month_match:
        return "month", int(month_match.group(1))

    if week_match:
        return "week", int(week_match.group(1))

    return "month", 3


def _limit_bullets(text, max_bullets=3):
    lines = text.split("\n")
    result = []
    count = 0

    for line in lines:
        if line.startswith("Month"):
            count = 0
            result.append(line)
        elif line.startswith("- "):
            if count < max_bullets:
                result.append(line)
                count += 1
        else:
            result.append(line)

    return "\n".join(result)


def _fix_common_errors(text):
    fixes = {
        "machine building": "machine learning",
        "Scikit-build": "scikit-learn",
        "build to": "use tools to"
    }

    for k, v in fixes.items():
        text = text.replace(k, v)

    return text

def _analyze_goal(goal: str):
    goal = goal.lower()

    insights = {
        "fast": "fast" in goal or "quick" in goal,
        "job": "job" in goal or "placement" in goal,
        "project": "project" in goal
    }

    return insights

def _convert_to_weekly(plan: str):
    lines = plan.split("\n")
    new_plan = []
    current_tasks = []

    for line in lines:
        if line.startswith("Month"):
            if current_tasks:
                mid = len(current_tasks) // 2
                new_plan.append("  Week 1-2:")
                for t in current_tasks[:mid]:
                    new_plan.append("  " + t)
                new_plan.append("  Week 3-4:")
                for t in current_tasks[mid:]:
                    new_plan.append("  " + t)
                current_tasks = []

            new_plan.append(line)

        elif line.startswith("- "):
            current_tasks.append(line)

    if current_tasks:
        mid = len(current_tasks) // 2
        new_plan.append("  Week 1-2:")
        for t in current_tasks[:mid]:
            new_plan.append("  " + t)
        new_plan.append("  Week 3-4:")
        for t in current_tasks[mid:]:
            new_plan.append("  " + t)

    return "\n".join(new_plan)

# =========================
# MAIN FUNCTION
# =========================
def generate_goal_plan(goal, user_level, goal_type):
    
    # FIX (IMPORTANT)
    user_level = user_level.lower()
    goal_type = goal_type.lower()

    duration_type, duration_count = _detect_duration(goal)

    unit = "Week" if duration_type == "week" else "Month"
    
    # ADD THIS HERE
    is_beginner = user_level == "beginner"

    base_steps = DOMAIN_BLUEPRINT.get(goal_type, {}).get(user_level, [])

    if not base_steps:
        return f"{unit} 1:\n- No roadmap available"

    plan = ""
    step_index = 0

    for i in range(1, duration_count + 1):
        plan += f"{unit} {i}:\n"               
        
        for j in range(3):            
            if step_index < len(base_steps):
                plan += f"- {base_steps[step_index]}\n"
                step_index += 1
            else:
                break
          

        if step_index >= len(base_steps) and i != duration_count:            

            fallbacks = [
                "- Build a mini project using learned concepts",
                "- Work on a real-world dataset and document results",
                "- Practice interview-level problems",
                "- Optimize and improve previous models"
            ]

            plan += random.choice(fallbacks) + "\n"
            
        
        if i == duration_count and step_index >= len(base_steps):
            if is_beginner:
                plan += "- Build a small project\n"
            elif user_level == "intermediate":
                plan += "- Build 2 real-world projects\n"
            else:
                plan += "- Build production-level system\n"
   

        plan += "\n"

    
    plan = plan.strip()

    save_to_memory({
        "goal": goal,
        "level": user_level,
        "domain": goal_type,
        "plan": plan
    })

    return plan

   













