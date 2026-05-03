import streamlit as st
from agents.goal_planner import generate_goal_plan
from agents.task_generator import generate_tasks
from agents.resource_finder import recommend_resources
from agents.progress_advisor import give_advice
import speech_recognition as sr
from fpdf import FPDF
import random
from core.memory import load_memory   


def analyze_intelligence(goal, level, domain):
    goal = goal.lower()

    # Difficulty
    if level == "Beginner":
        difficulty = "🟢 Easy"
    elif level == "Intermediate":
        difficulty = "🟡 Medium"
    else:
        difficulty = "🔴 Hard"

    # Speed detection
    if "fast" in goal or "quick" in goal:
        speed = "Fast Track"
    else:
        speed = "Normal Pace"

    # Career suggestions
    if domain == "ai_ml":
        careers = "ML Engineer, Data Scientist, AI Engineer"
    elif domain == "frontend":
        careers = "Frontend Developer, UI Engineer"
    elif domain == "backend":
        careers = "Backend Developer, API Engineer"
    else:
        careers = "DevOps Engineer, Cloud Engineer"

    # Focus area
    if "job" in goal:
        focus = "Job + Projects"
    elif "project" in goal:
        focus = "🛠 Projects"
    else:
        focus = "Learning + Practice"

    return difficulty, speed, careers, focus

# NEW: Theme state
if "theme" not in st.session_state:
    st.session_state.theme = "dark"

# NEW FIX (ADDED)
def clean_text(text):
    return (
        text.replace("—", "-")
            .replace("–", "-")
            .replace("→", "->")
            .replace("“", '"')
            .replace("”", '"')
            .replace("’", "'")
    )


# ---------------- CONFIG ----------------
st.set_page_config(page_title="CogniWeave AI", layout="centered")


def generate_pdf(plan, tasks, resources):
    pdf = FPDF()
    pdf.add_page()

    # Title
    pdf.set_font("Arial", "B", 16)
    pdf.cell(200, 10, "CogniWeave AI - Smart Roadmap", ln=True, align="C")

    pdf.ln(5)

    # ROADMAP
    pdf.set_font("Arial", "B", 14)
    pdf.cell(200, 10, "Roadmap", ln=True)

    pdf.set_font("Arial", size=11)
    for line in plan.split("\n"):
        line = clean_text(line)   # UPDATED
        pdf.multi_cell(0, 8, line)

    pdf.ln(5)

    # TASKS
    pdf.set_font("Arial", "B", 14)
    pdf.cell(200, 10, "Tasks", ln=True)

    pdf.set_font("Arial", size=11)
    for line in tasks.split("\n"):
        line = clean_text(line)   # UPDATED
        pdf.multi_cell(0, 8, line)

    pdf.ln(5)

    # RESOURCES
    pdf.set_font("Arial", "B", 14)
    pdf.cell(200, 10, "Resources", ln=True)

    pdf.set_font("Arial", size=11)
    for line in resources.split("\n"):
        line = clean_text(line)   # UPDATED
        pdf.multi_cell(0, 8, line)

    file_path = "roadmap.pdf"
    pdf.output(file_path)

    return file_path


st.markdown("""
<style>

/* ===== BACKGROUND (DEPTH EFFECT) ===== */
.stApp {
    background:
        radial-gradient(circle at 20% 20%, rgba(99,102,241,0.15), transparent),
        radial-gradient(circle at 80% 80%, rgba(34,211,238,0.15), transparent),
        linear-gradient(135deg, #020617, #020617);
    color: white;
}

/* ===== CENTER CONTAINER ===== */
.block-container {
    max-width: 820px;
    margin: auto;
}

/* ===== GLASS CARD ===== */
.glass {
    background: rgba(255,255,255,0.05);
    border-radius: 18px;
    padding: 25px;
    backdrop-filter: blur(18px);
    border: 1px solid rgba(255,255,255,0.08);
    margin-top: 25px;
    box-shadow: 0 0 40px rgba(99,102,241,0.15);
}

/* ===== HEADINGS ===== */
h1 {
    font-weight: 700;
}

/* ===== BUTTON ===== */
.stButton>button {
    border-radius: 12px;
    background: linear-gradient(90deg, #6366f1, #22d3ee);
    color: white;
    font-weight: 600;
    border: none;
    transition: all 0.3s ease;
}

.stButton>button:hover {
    transform: scale(1.05);
    box-shadow: 0 0 25px #22d3ee;
}

/* ===== DOWNLOAD BUTTON ===== */
.stDownloadButton>button {
    border-radius: 12px;
    background: linear-gradient(90deg, #22d3ee, #6366f1);
    color: white;
    font-weight: 600;
    border: none;
}

/* ===== INPUT ===== */
input, textarea {
    background-color: rgba(255,255,255,0.08) !important;
    color: #white !important;
    border: 1px solid rgba(255,255,255,0.2) !important;
}

/* ===== METRIC CARDS ===== */
[data-testid="stMetric"] {
    background: rgba(255,255,255,0.08);
    padding: 15px;
    border-radius: 12px;
    border: 1px solid rgba(255,255,255,0.15);
}

/* ADD THIS BELOW */
[data-testid="stMetric"] {
    background: linear-gradient(135deg, rgba(30,41,59,0.95), rgba(15,23,42,0.95)) !important;
    border: 1px solid rgba(99,102,241,0.4) !important;
    border-radius: 16px !important;
    padding: 18px !important;
    box-shadow: 0 0 25px rgba(99,102,241,0.2);
}

[data-testid="stMetricLabel"] {
    color: #94a3b8 !important;
    font-size: 14px !important;
}

[data-testid="stMetricValue"] {
    color: #ffffff !important;
    font-size: 22px !important;
    font-weight: 700 !important;
}

/* ===== PROGRESS BAR ===== */
.stProgress > div > div > div {
    background: linear-gradient(90deg, #6366f1, #22d3ee);
}

/* ===== CARD HOVER ANIMATION ===== */
[data-testid="stMetric"] {
    transition: all 0.25s ease;
}

[data-testid="stMetric"]:hover {
    transform: translateY(-5px) scale(1.02);
    box-shadow: 0 12px 35px rgba(99,102,241,0.5);
}

/* ===== BUTTON HOVER IMPROVEMENT ===== */
.stButton>button:hover {
    transform: scale(1.07);
    box-shadow: 0 0 30px #22d3ee;
}

/* ===== FADE-IN EFFECT ===== */
@keyframes fadeIn {
    from {opacity: 0; transform: translateY(10px);}
    to {opacity: 1; transform: translateY(0);}
}

.block-container {
    animation: fadeIn 0.6s ease-in-out;
}

</style>
""", unsafe_allow_html=True)

# ---------------- HEADER ----------------
st.markdown("""
<div style='text-align:center; margin-top:40px; margin-bottom:20px;'>

<h1 style='font-size:52px;
background: linear-gradient(90deg,#6366f1,#22d3ee);
-webkit-background-clip: text;
color: transparent;
letter-spacing:1px;'>
🧠 CogniWeave AI
</h1>

<p style='color:#94a3b8; font-size:18px;'>
AI-Powered Goal Planning for Students
</p>

</div>
""", unsafe_allow_html=True)

st.write("")
st.write("")


# ================= MEMORY DISPLAY =================
history = load_memory()

if history:
    st.markdown("### Your Recent Goals")    
    
    for item in reversed(history[-3:]):
        goal_text = item.get("goal", "").strip()

    if goal_text:  # removes empty bullet
        st.markdown(f"""
        <div style="
            background: rgba(99,102,241,0.08);
            padding:10px;
            margin-bottom:8px;
            border-radius:10px;
            border-left:3px solid #6366f1;">
            {goal_text}
        </div>
        """, unsafe_allow_html=True)
        
st.markdown("---")        


# ---------------- SESSION ----------------
if "goal" not in st.session_state:
    st.session_state.goal = ""

# ---------------- INPUT CARD ----------------
col1, col2 = st.columns(2)

with col1:
   domain = st.selectbox("🌐 Select Domain", [
    "ai_ml",
    "frontend",
    "backend",
    "devops"
    ]) 
with col2:
    user_level = st.selectbox("📊 Level", [
        "Beginner","Intermediate","Advanced"
    ])
    
st.markdown("<div style='margin-top:15px'></div>", unsafe_allow_html=True)    

st.markdown("### Enter Your Goal")

if "goal" not in st.session_state:
    st.session_state.goal = ""
    
goal = st.text_input(
    "Enter Goal",
    value=st.session_state.goal,
    placeholder="e.g. Become AI Engineer in 2 months",
    label_visibility="collapsed"
)

st.session_state.goal = goal

# ================= VOICE FIX =================
def voice_input():
    r = sr.Recognizer()

    try:
        with sr.Microphone() as source:
            r.adjust_for_ambient_noise(source, duration=1)
            audio = r.listen(source, timeout=5, phrase_time_limit=5)

        text = r.recognize_google(audio)
        return text

    except sr.WaitTimeoutError:
        return "❌ No voice detected. Try again."

    except sr.UnknownValueError:
        return "❌ Couldn't understand. Speak clearly."

    except Exception as e:
        return f"❌ Mic error: {str(e)}"
        

st.write("")

st.markdown("#### Voice Assistant")

# CENTERED BUTTONS
c1, c2, c3 = st.columns([1,1,1])

with c1:
    if st.button("Speak Goal"):
        with st.spinner("Listening..."):
            spoken = voice_input()

        if "❌" in spoken:
            st.error(spoken)
        else:
            st.success(f"✔ Goal detected: {spoken}")
            st.session_state.goal = spoken
        
with c2:
    if st.button("Reset", use_container_width=True):
        st.session_state.goal = ""
        st.rerun()        

with c3:  
    generate_clicked = st.button("Generate Plan", use_container_width=True)

# ---------------- OUTPUT ----------------
if generate_clicked:
    if goal:       
        goal_type = domain
        progress_bar = st.progress(0)
        status = st.empty()

        try:
            status.text("Analyzing your goal...")
            progress_bar.progress(20)

            plan = generate_goal_plan(goal, user_level, goal_type)

            status.text("Building your roadmap...")
            progress_bar.progress(60)

            tasks = generate_tasks(goal, plan, user_level, goal_type)
            resources = recommend_resources(goal, goal_type)

            status.text("Finalizing your plan...")
            progress_bar.progress(100)

            status.empty()
            progress_bar.empty()

            st.success("Plan generated successfully!")
            difficulty, speed, careers, focus = analyze_intelligence(goal, user_level, goal_type)

        except:
            st.warning("AI busy. Showing demo.")
            plan = "Week 1: Basics\nWeek 2: Practice\nWeek 3: Project"
            tasks = "Practice daily\nBuild projects"
            resources = "YouTube\nKaggle"
            
            difficulty, speed, careers, focus = analyze_intelligence(goal, user_level, goal_type)


        st.write("")
        
        st.markdown("### AI Insights")
       
        col1, col2 = st.columns(2)

        with col1:
            st.metric("Difficulty", difficulty)
            st.caption("Suitable based on your current level")

            st.metric("Speed", speed)
            st.caption("Learning pace detected from your goal")

        with col2:
            st.metric("Career Paths", careers)
            st.caption("Possible roles after completion")

            st.metric("Focus", focus)
            st.caption("Main area you should prioritize")
        
        
        st.write("")
        clean_goal = goal.lower().replace("roadmap", "").replace("road map", "").strip()
        
        st.markdown(f"### {clean_goal.title()} Learning Roadmap ({user_level})")        
       
        st.write("")

        pdf_file = generate_pdf(plan, tasks, resources)

        with open(pdf_file, "rb") as f:
            st.download_button(
                "Download Plan",
                data=f,
                file_name="CogniWeave_Roadmap.pdf",
                mime="application/pdf"
            )

        for line in plan.split("\n"):
            if not line.strip():
                continue
            
            if "Month" in line:
                html = f"""
        <div style="font-size:20px; font-weight:700; margin-top:20px; margin-bottom:8px; display:flex; align-items:center;">
            <span style="width:10px; height:10px; background:#6366f1; border-radius:50%; display:inline-block; margin-right:10px;"></span>
            {line}
        </div>
        """
                st.markdown(html, unsafe_allow_html=True)

            else:
                html = f"""
        <div style="margin-left:25px; margin-bottom:6px; color:#cbd5f5; font-size:15px;">
            ➤ {line}
        </div>
        """
                st.markdown(html, unsafe_allow_html=True)
                
        progress_score = random.randint(70, 95)

        st.markdown("<div style='margin-top:20px'></div>", unsafe_allow_html=True)
        st.progress(progress_score / 100)
        st.caption(f"Estimated Completion Readiness: {progress_score}%")  
        
        if user_level == "Beginner":
            tip = "Start slow and stay consistent."
        elif user_level == "Intermediate":
            tip = "Focus on real-world projects."
        else:
            tip = "Optimize and deploy production-ready systems."

        st.info(f"Smart Tip: {tip}")      
                
        st.write("")
        st.markdown("### Tasks")
        
        for line in tasks.split("\n"):
            if line.strip():
                st.markdown(f"""
                <div style="
                    background: rgba(34,197,94,0.08);
                    padding: 12px;
                    margin-bottom: 8px;
                    border-radius: 10px;
                    border-left: 4px solid #22c55e;">
                    ✔ {line}
                </div>
                """, unsafe_allow_html=True)

        st.write("")
        
        st.markdown("### Resources")
        st.markdown(resources)        
        
    else:
        st.warning("Enter a goal")
        

st.write("")
st.markdown("### Track Your Progress")
progress = st.text_input("Your Progress", label_visibility="collapsed")

if st.button("💡 Get AI Advice"):
    if progress:

        progress_lower = progress.lower()

        # simple intelligent scoring
        if any(word in progress_lower for word in ["completed", "done", "finished"]):
            score = 80
        elif any(word in progress_lower for word in ["learning", "practicing"]):
            score = 60
        else:
            score = 40
               
        if score < 50:
            st.progress(score / 100, text="🔴 Beginner Level")
        elif score < 75:
            st.progress(score / 100, text="🟡 Intermediate Progress")
        else:
            st.progress(score / 100, text="🟢 Almost Job Ready")

        st.caption(f"Progress Score: {score}%")

        # Stage detection
        if score >= 75:
            stage = "Job Ready"
        elif score >= 50:
            stage = "In Progress"
        else:
            stage = "Beginner Stage"

        st.metric("Current Stage", stage)

        # Advice
        advice = give_advice(progress)
        st.success("Advice generated!")
        st.info(advice)

    else:
        st.warning("Enter progress first")
        

   