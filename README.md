# CogniWeave AI  
### AI-Powered Goal Planning for Students  

CogniWeave AI is an intelligent system that generates **personalized learning roadmaps, tasks, and resources** based on a student's goal, level, and domain.

---

## Features

- Personalized roadmap generation (Beginner / Intermediate / Advanced)
- Structured weekly / monthly learning plan
- Task generation based on roadmap
- Smart resource recommendation system
- Progress tracking with AI advice
- Memory system (stores previous goals)
- Voice input support *(local environment only)*

---

## Tech Stack

- **Frontend:** Streamlit  
- **Backend:** Python  
- **AI Model:** Groq API (LLM)  
- **Storage:** JSON (memory system)  

---

```md id="fix123"
## Project Structure

```bash
CogniWeave-AI/
│
├── app.py
├── requirements.txt
├── README.md
├── memory.json
│
├── agents/
│   ├── goal_planner.py
│   ├── task_generator.py
│   ├── resource_finder.py
│   ├── progress_advisor.py
│
├── core/
│   ├── llm_setup.py
│   ├── memory.py
│
└── utils/
    └── helpers.py

---

## How to Run

```bash
pip install -r requirements.txt
streamlit run app.py   or  python -m streamlit run app.py

---

## Important Notes

- Voice feature works only in **local Python environment**
- `.env` file (API key) is not included for security reasons
- Make sure microphone permissions are enabled

---

## Example Output

- AI-generated roadmap (week/month-wise)  
- Practical tasks using tools & datasets  
- Structured learning progression  
- Curated learning resources  

---

## Future Improvements

- Improve AI intelligence using advanced prompts  
- Add real-time voice support in web  
- Add user authentication  
- Deploy using Flask / FastAPI  

---

## Author

**Bhoomi Gupta**  
MCA (AI/ML) Student  

---

## ⭐ Final Note

This project demonstrates how AI can be used to build a **goal-oriented intelligent learning system** for students.

---
