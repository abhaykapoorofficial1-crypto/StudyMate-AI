import sys
import os
import json
from pathlib import Path
import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# Ensure project root is in sys.path
root_path = Path(__file__).resolve().parent.parent
if str(root_path) not in sys.path:
    sys.path.insert(0, str(root_path))

from agents.router_agent import router_agent
from agents.explain_agent import explain_agent
from agents.quiz_agent import quiz_agent
from agents.notes_agent import notes_agent
from agents.planner_agent import planner_agent
from agents.flashcard_agent import flashcard_agent
from agents.progress_agent import progress_agent
from agents.memory_agent import memory_agent
from mcp.file_server import file_mcp_server
from mcp.pdf_server import pdf_mcp_server
from memory.sqlite_memory import memory_db

# Page Configuration
st.set_page_config(
    page_title="StudyMate AI - Multi-Agent Assistant",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for Dark Mode Aesthetics
st.markdown("""
<style>
    .main {
        background-color: #0E1117;
        color: #FFFFFF;
    }
    .stApp {
        background: linear-gradient(135deg, #0f172a 0%, #1e1b4b 50%, #0f172a 100%);
    }
    .metric-card {
        background: rgba(30, 41, 59, 0.7);
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 12px;
        padding: 20px;
        backdrop-filter: blur(10px);
        box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.37);
    }
    .badge {
        background: linear-gradient(90deg, #6366f1 0%, #a855f7 100%);
        color: white;
        padding: 4px 12px;
        border-radius: 20px;
        font-weight: bold;
        font-size: 0.85rem;
        display: inline-block;
        margin: 4px;
    }
    .chat-bubble-user {
        background-color: #2563eb;
        color: white;
        padding: 12px 16px;
        border-radius: 18px 18px 2px 18px;
        margin-bottom: 10px;
        max-width: 80%;
        float: right;
        clear: both;
    }
    .chat-bubble-agent {
        background-color: #1e293b;
        border: 1px solid #334155;
        color: #f8fafc;
        padding: 12px 16px;
        border-radius: 18px 18px 18px 2px;
        margin-bottom: 10px;
        max-width: 85%;
        float: left;
        clear: both;
    }
</style>
""", unsafe_allow_html=True)

# Session State Initialization
if "chat_history" not in st.session_state:
    st.session_state.chat_history = memory_db.get_chat_history(limit=20)
if "selected_doc" not in st.session_state:
    st.session_state.selected_doc = None

# Sidebar Setup
with st.sidebar:
    st.title("🎓 StudyMate AI")
    st.caption("Secure Multi-Agent Assistant (Google ADK & MCP)")
    
    # Mode indicator
    api_key_status = "🟢 Online Gemini API" if os.getenv("GEMINI_API_KEY") else "⚡ 100% Offline AI Engine"
    st.info(f"Execution Mode: {api_key_status}")
    
    st.divider()
    st.subheader("📤 Document Vault")
    uploaded_file = st.file_uploader("Upload Study Material (PDF, DOCX, TXT)", type=["pdf", "docx", "txt"])
    
    if uploaded_file is not None:
        file_bytes = uploaded_file.read()
        res = file_mcp_server.upload(uploaded_file.name, file_bytes)
        if res.get("success"):
            st.success(f"Uploaded: {uploaded_file.name}")
        else:
            st.error(f"Upload Error: {res.get('error')}")

    # Display Uploaded Files
    docs = file_mcp_server.list_files()
    if docs:
        st.markdown("**Uploaded Files:**")
        doc_names = [d["filename"] for d in docs]
        selected = st.selectbox("Active Context Document", ["None"] + doc_names)
        if selected != "None":
            st.session_state.selected_doc = selected
        else:
            st.session_state.selected_doc = None
    else:
        st.caption("No documents uploaded yet.")

    st.divider()
    st.subheader("🔥 Gamification")
    metrics = memory_db.get_user_metrics()
    gami = metrics["gamification"]
    prog = metrics["progress"]
    
    st.metric("Daily Study Streak", f"{gami['streak']} Days", delta="🔥 Active")
    st.metric("Total XP", f"{gami['xp']} XP", delta="⚡ Level 3")
    
    st.markdown("**Badges Earned:**")
    badge_html = "".join([f"<span class='badge'>{b}</span>" for b in gami["badges"]])
    st.markdown(badge_html, unsafe_allow_html=True)

# Main Navigation Tabs
tab_chat, tab_notes, tab_quiz, tab_flashcards, tab_planner, tab_dashboard, tab_settings = st.tabs([
    "💬 AI Chat", "📝 Notes & Mind Maps", "🧠 Interactive Quiz", 
    "🎴 Flashcards", "📅 Study Planner", "📊 Analytics Dashboard", "⚙️ Settings"
])

# ---------------------------------------------------------
# TAB 1: AI Chat
# ---------------------------------------------------------
with tab_chat:
    st.header("💬 Multi-Agent AI Study Chat")
    st.caption("Ask questions, request explanations, summaries, or quizzes. The Router Agent will automatically delegate to specialized agents.")

    if st.session_state.selected_doc:
        st.info(f"📄 Active Context Document: **{st.session_state.selected_doc}**")

    # Render Chat History
    chat_container = st.container()
    with chat_container:
        for msg in st.session_state.chat_history:
            role = msg["role"]
            agent = msg["agent"]
            text = msg["message"]
            
            with st.chat_message(role, avatar="🤖" if role=="assistant" else "👤"):
                st.markdown(f"**{agent}**" if role=="assistant" else "**You**")
                st.markdown(text)

    # Chat Input
    user_query = st.chat_input("Ask StudyMate AI anything (e.g., 'Explain binary search', 'Quiz me on OS')...")
    if user_query:
        # Append User Message to UI
        with st.chat_message("user", avatar="👤"):
            st.markdown(user_query)

        # Prepare Context
        ctx = {}
        if st.session_state.selected_doc:
            ctx["document_text"] = memory_db.get_document_content(st.session_state.selected_doc)

        # Process with Router Agent
        with st.chat_message("assistant", avatar="🤖"):
            with st.spinner("Multi-Agent orchestration in progress..."):
                response = router_agent.route_and_process(user_query, context=ctx)
                st.markdown(response)

        # Refresh History
        st.session_state.chat_history = memory_db.get_chat_history(limit=30)
        st.rerun()

# ---------------------------------------------------------
# TAB 2: Notes & Mind Maps
# ---------------------------------------------------------
with tab_notes:
    st.header("📝 Smart Notes & Mind Map Generator")
    col1, col2 = st.columns([1, 2])
    
    with col1:
        topic_input = st.text_input("Enter Note Topic or Concept:", value="Operating System Security")
        if st.button("🚀 Generate Revision Notes"):
            ctx = {"document_text": memory_db.get_document_content(st.session_state.selected_doc)} if st.session_state.selected_doc else None
            with st.spinner("NotesAgent compiling high-yield revision sheet..."):
                note_res = notes_agent.process_request(topic_input, context=ctx)
                st.session_state.current_note = note_res

    with col2:
        if "current_note" in st.session_state:
            st.markdown(st.session_state.current_note)
        else:
            all_notes = memory_db.get_all_notes()
            if all_notes:
                st.subheader("📚 Saved Notes in Memory")
                for n in all_notes[:3]:
                    with st.expander(f"📝 {n['title']} ({n['created_at']})"):
                        st.markdown(n["content"])
            else:
                st.info("Generate your first revision sheet using the panel on the left!")

# ---------------------------------------------------------
# TAB 3: Interactive Quiz Test Engine
# ---------------------------------------------------------
with tab_quiz:
    st.header("🧠 Interactive Knowledge Test Engine")
    q_topic = st.text_input("Quiz Subject / Topic:", value="Data Structures & Algorithms", key="q_topic_key")
    q_type = st.selectbox("Quiz Question Format:", ["MCQ", "True/False"])
    
    if st.button("🎯 Generate Live Quiz Test"):
        with st.spinner("QuizAgent generating structured questions..."):
            st.session_state.active_quiz = quiz_agent.generate_quiz_json(q_topic, q_type)
            st.session_state.user_answers = {}

    if "active_quiz" in st.session_state and st.session_state.active_quiz:
        quiz = st.session_state.active_quiz
        st.subheader(f"Test Paper: {quiz['topic']} ({quiz['quiz_type']})")
        
        with st.form("quiz_form"):
            for q in quiz["questions"]:
                st.markdown(f"**Q{q['id']}. {q['question']}**")
                user_ans = st.radio(f"Select your answer for Q{q['id']}:", q["options"], key=f"q_rad_{q['id']}")
                st.session_state.user_answers[q["id"]] = user_ans
                st.divider()
            
            submitted = st.form_submit_button("🏆 Submit & Grade Test")
            if submitted:
                correct_count = 0
                for q in quiz["questions"]:
                    if st.session_state.user_answers.get(q["id"]) == q["answer"]:
                        correct_count += 1
                
                score_pct = (correct_count / len(quiz["questions"])) * 100
                memory_db.update_quiz_result(quiz["quiz_id"], score_pct)
                memory_db.update_study_hours(0.5) # Add study effort
                
                st.balloons()
                st.success(f"🎉 Test Completed! Score: **{correct_count}/{len(quiz['questions'])} ({score_pct:.1f}%)**")
                
                for q in quiz["questions"]:
                    ans = st.session_state.user_answers.get(q["id"])
                    is_correct = ans == q["answer"]
                    st.markdown(f"**Q{q['id']}**: {'✅ Correct' if is_correct else '❌ Incorrect'}")
                    st.caption(f"Explanation: {q['explanation']}")

# ---------------------------------------------------------
# TAB 4: Flashcards Deck Player
# ---------------------------------------------------------
with tab_flashcards:
    st.header("🎴 Spaced Repetition Flashcards Deck")
    fc_topic = st.text_input("Flashcard Deck Subject:", value="Computer Networks", key="fc_topic_key")
    
    if st.button("✨ Generate Deck"):
        cards = flashcard_agent.generate_cards(fc_topic)
        st.session_state.cards = cards
        st.session_state.card_idx = 0

    if "cards" in st.session_state and st.session_state.cards:
        cards = st.session_state.cards
        idx = st.session_state.get("card_idx", 0)
        curr_card = cards[idx]
        
        st.progress((idx + 1) / len(cards), text=f"Card {idx+1} of {len(cards)}")
        
        col_a, col_b = st.columns([1, 1])
        with col_a:
            if st.button("◀️ Previous Card") and idx > 0:
                st.session_state.card_idx -= 1
                st.rerun()
        with col_b:
            if st.button("Next Card ▶️") and idx < len(cards) - 1:
                st.session_state.card_idx += 1
                st.rerun()

        st.markdown(f"""
        <div class="metric-card" style="text-align: center; min-height: 200px; display: flex; flex-direction: column; justify-content: center;">
            <h3 style="color: #6366f1;">❓ FRONT</h3>
            <h2>{curr_card['front']}</h2>
        </div>
        """, unsafe_allow_html=True)
        
        with st.expander("🔍 Click to Flip & Reveal Answer"):
            st.markdown(f"""
            <div class="metric-card" style="text-align: center; background: rgba(16, 185, 129, 0.1); border-color: #10b981;">
                <h3 style="color: #10b981;">💡 BACK</h3>
                <h3>{curr_card['back']}</h3>
            </div>
            """, unsafe_allow_html=True)

# ---------------------------------------------------------
# TAB 5: Study Planner & Exam Countdown
# ---------------------------------------------------------
with tab_planner:
    st.header("📅 Personalized Study Timetable & Planner")
    col1, col2 = st.columns([1, 1])
    
    with col1:
        exam_title = st.text_input("Target Exam Title:", value="Database Management Systems Exam")
        target_date = st.date_input("Exam Date:")
        if st.button("🗓️ Generate Optimized Schedule"):
            with st.spinner("PlannerAgent generating multi-day timetable..."):
                plan_res = planner_agent.process_request(f"planner for {exam_title} on {target_date.strftime('%Y-%m-%d')}")
                st.session_state.current_plan = plan_res

    with col2:
        if "current_plan" in st.session_state:
            st.markdown(st.session_state.current_plan)
        else:
            st.info("Set your target exam date on the left to build a structured revision schedule!")

# ---------------------------------------------------------
# TAB 6: Analytics Dashboard
# ---------------------------------------------------------
with tab_dashboard:
    st.header("📊 Learning Analytics & Mastery Dashboard")
    metrics = memory_db.get_user_metrics()
    prog = metrics["progress"]
    gami = metrics["gamification"]
    quizzes = memory_db.get_quiz_history()

    col1, col2, col3, col4 = st.columns(4)
    col1.metric("⏱️ Study Hours", f"{prog['study_hours']:.1f} hrs", delta="+1.5 hrs this week")
    col2.metric("🎯 Quizzes Completed", len(quizzes))
    col3.metric("🔥 Daily Streak", f"{gami['streak']} Days")
    col4.metric("⚡ Total XP Points", gami['xp'])

    st.divider()
    col_chart1, col_chart2 = st.columns([1, 1])
    
    with col_chart1:
        st.subheader("📈 Quiz Performance History")
        if quizzes:
            df_q = pd.DataFrame(quizzes)
            fig = px.bar(df_q, x="topic", y="score", color="quiz_type", title="Quiz Scores by Topic (%)",
                         template="plotly_dark", labels={"score": "Score (%)", "topic": "Topic"})
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.caption("No quiz history recorded yet.")

    with col_chart2:
        st.subheader("🎯 Mastery vs. Weak Areas Distribution")
        categories = ["Mastered Topics", "Weak Areas Pending", "In Progress"]
        counts = [len(prog["topics_covered"]), len(prog["weak_areas"]), 2]
        fig_pie = px.pie(names=categories, values=counts, hole=0.4, template="plotly_dark",
                         color_discrete_sequence=["#10b981", "#ef4444", "#6366f1"])
        st.plotly_chart(fig_pie, use_container_width=True)

# ---------------------------------------------------------
# TAB 7: Settings & Audit Logs
# ---------------------------------------------------------
with tab_settings:
    st.header("⚙️ System Architecture & Security Audit Settings")
    st.markdown("StudyMate AI implements Google ADK standards, RBAC permissions, and sliding window rate limiting.")
    
    st.subheader("🛡️ Active Security Guardrails")
    st.json({
        "Prompt Injection Defense": "Enabled (10+ RegEx patterns)",
        "Allowed File Formats": [".pdf", ".docx", ".txt"],
        "Max File Upload Size": "15 MB",
        "Rate Limiting": "60 requests/minute",
        "Audit Logging": "Loguru active (logs/audit.log)"
    })

    st.subheader("🤖 Active Multi-Agent Roster")
    agent_info = [
        {"Agent": "RouterAgent", "Role": "Master Orchestrator & Intent Classifier", "Status": "Active"},
        {"Agent": "ExplainAgent", "Role": "Concept Explanations & Analogies", "Status": "Active"},
        {"Agent": "QuizAgent", "Role": "MCQ, True/False & Assessment Generator", "Status": "Active"},
        {"Agent": "NotesAgent", "Role": "Summaries, Bullet Notes & Mind Maps", "Status": "Active"},
        {"Agent": "PlannerAgent", "Role": "Timetables & Exam Countdowns", "Status": "Active"},
        {"Agent": "FlashcardAgent", "Role": "Active Recall Flashcards", "Status": "Active"},
        {"Agent": "ProgressAgent", "Role": "Analytics & Performance Metrics", "Status": "Active"},
        {"Agent": "MemoryAgent", "Role": "Session & Document Retrieval", "Status": "Active"}
    ]
    st.dataframe(pd.DataFrame(agent_info), use_container_width=True)
