# =========================================================
# app.py
# =========================================================

import streamlit as st
import pandas as pd
import json
import PyPDF2

from agents.coding_tutor_agent import CodingTutorAgent
from agents.summary_agent import SummaryAgent
from agents.quiz_generator_agent import QuizGeneratorAgent
from agents.audio_summary_agent import AudioSummaryAgent
from agents.visualization_agent import VisualizationAgent
from agents.evaluator import EvaluatorAgent

# =========================================================
# PAGE CONFIG
# =========================================================

st.set_page_config(
    page_title="AdaptiveSkill AI",
    page_icon="🤖",
    layout="wide"
)

st.title("🤖 AdaptiveSkill AI")
st.subheader(
    "Multi-Agent AI Learning & Evaluation Platform"
)

# =========================================================
# LOAD MODULES
# =========================================================

with open("modules.json") as f:

    modules_data = json.load(f)

# =========================================================
# AGENTS
# =========================================================

coding_agent = CodingTutorAgent()

summary_agent = SummaryAgent()

quiz_agent = QuizGeneratorAgent()

audio_agent = AudioSummaryAgent()

visual_agent = VisualizationAgent()

evaluator_agent = EvaluatorAgent()

# =========================================================
# SESSION STATE
# =========================================================

if "messages" not in st.session_state:
    st.session_state.messages = []

if "quiz_data" not in st.session_state:
    st.session_state.quiz_data = None

if "quiz_answers" not in st.session_state:
    st.session_state.quiz_answers = {}

if "current_module" not in st.session_state:
    st.session_state.current_module = 0

if "module_score" not in st.session_state:
    st.session_state.module_score = 0

# =========================================================
# SIDEBAR
# =========================================================

agent_type = st.sidebar.selectbox(
    "Select Workflow",
    [
        "Learning Orchestrator",
        "Coding Tutor",
        "Summary Agent",
        "Evaluator Agent",
        "Quiz Generator"
    ]
)

# =========================================================
# CLEAR STATE ON SWITCH
# =========================================================

if "last_agent" not in st.session_state:

    st.session_state.last_agent = agent_type

if st.session_state.last_agent != agent_type:

    st.session_state.messages = []

    st.session_state.quiz_data = None

    st.session_state.quiz_answers = {}

    st.session_state.last_agent = agent_type

    st.rerun()

# =========================================================
# DISPLAY CHAT HISTORY
# =========================================================

for msg in st.session_state.messages:

    with st.chat_message(msg["role"]):

        st.markdown(msg["content"])

# =========================================================
# HELPERS
# =========================================================

def read_text_file(file):

    return file.read().decode("utf-8")


def read_pdf_file(file):

    pdf_reader = PyPDF2.PdfReader(file)

    text = ""

    for page in pdf_reader.pages:

        extracted = page.extract_text()

        if extracted:

            text += extracted

    return text


def truncate_text(text, limit=4000):

    if len(text) > limit:

        return text[:limit]

    return text

# =========================================================
# LEARNING ORCHESTRATOR
# =========================================================

if agent_type == "Learning Orchestrator":

    module = modules_data["modules"][
        st.session_state.current_module
    ]

    # -----------------------------------------------------
    # MODULE HEADER
    # -----------------------------------------------------

    st.header(
        f"📘 Module {module['id']} - "
        f"{module['title']}"
    )

    # -----------------------------------------------------
    # MODULE CONTENT
    # -----------------------------------------------------

    st.markdown("## 📖 Learning Content")

    st.markdown(module["content"])

    # -----------------------------------------------------
    # PRACTICE TASK
    # -----------------------------------------------------

    st.markdown("## 💻 Practice Task")

    st.markdown(
        module["practice_question"]
    )

    user_code = st.text_area(
        "Write your code",
        value=module["starter_code"],
        height=300
    )

    # -----------------------------------------------------
    # RUN TEST
    # -----------------------------------------------------

    if st.button("▶ Run Test"):

        if "return" in user_code:

            st.success(
                "✅ Basic test passed"
            )

        else:

            st.error(
                "❌ Test failed"
            )

    # -----------------------------------------------------
    # AI SUMMARY
    # -----------------------------------------------------

    if st.button("🧠 Generate AI Summary"):

        summary = summary_agent.summarize(
            module["content"]
        )

        st.markdown("## 📄 AI Summary")

        st.markdown(summary)

        # Audio Summary

        audio_file, audio_summary = (
            audio_agent.generate_audio_summary(
                summary
            )
        )

        if audio_file:

            audio_bytes = open(
                audio_file,
                "rb"
            ).read()

            st.audio(
                audio_bytes,
                format="audio/mp3"
            )

    # -----------------------------------------------------
    # QUIZ GENERATION
    # -----------------------------------------------------

    if st.button("❓ Generate Quiz"):

        quiz_data = quiz_agent.generate_quiz(
            module["quiz_topic"]
        )

        st.session_state.quiz_data = quiz_data

        st.rerun()

    # -----------------------------------------------------
    # QUIZ DISPLAY
    # -----------------------------------------------------

    if st.session_state.quiz_data:

        st.markdown("# 🧠 Module Quiz")

        for i, question_data in enumerate(
            st.session_state.quiz_data
        ):

            st.markdown(
                f"## Q{i+1}. "
                f"{question_data['question']}"
            )

            options = question_data["options"]

            selected = st.radio(
                "Choose your answer",
                [
                    "Select an option",
                    f"A. {options['A']}",
                    f"B. {options['B']}",
                    f"C. {options['C']}",
                    f"D. {options['D']}"
                ],
                index=0,
                key=f"quiz_{i}"
            )

            selected_letter = None

            if selected != "Select an option":

                selected_letter = selected[0]

            st.session_state.quiz_answers[i] = (
                selected_letter
            )

        # -------------------------------------------------
        # SUBMIT QUIZ
        # -------------------------------------------------

        if st.button("✅ Submit Quiz"):

            score = 0

            st.markdown("# 🎯 Quiz Results")

            for i, question_data in enumerate(
                st.session_state.quiz_data
            ):

                correct_answer = (
                    question_data["correct_answer"]
                )

                explanation = (
                    question_data["explanation"]
                )

                user_answer = (
                    st.session_state.quiz_answers[i]
                )

                if user_answer == correct_answer:

                    score += 1

                    st.success(
                        f"Q{i+1}: Correct"
                    )

                else:

                    st.error(
                        f"Q{i+1}: Incorrect"
                    )

                st.markdown(
                    f"Correct Answer: "
                    f"{correct_answer}"
                )

                st.markdown(
                    f"Explanation: "
                    f"{explanation}"
                )

                st.markdown("---")

            st.session_state.module_score += score

            st.markdown(
                f"# 🏆 Module Score: {score}/5"
            )

            st.markdown(
                f"# 🎖 Overall Program Score: "
                f"{st.session_state.module_score}"
            )

    # -----------------------------------------------------
    # NEXT MODULE
    # -----------------------------------------------------

    st.markdown("---")

    if st.button("➡ Next Module"):

        if (
            st.session_state.current_module
            < len(modules_data["modules"]) - 1
        ):

            st.session_state.current_module += 1

            st.session_state.quiz_data = None

            st.session_state.quiz_answers = {}

            st.rerun()

        else:

            st.success(
                "🎉 Program Completed!"
            )

# =========================================================
# CODING TUTOR
# =========================================================

elif agent_type == "Coding Tutor":

    st.header("💻 Coding Tutor")

    uploaded_file = st.file_uploader(
        "Upload Dataset or Code File",
        type=["csv", "txt", "py"]
    )

    file_content = ""

    df = None

    if uploaded_file is not None:

        if uploaded_file.name.endswith(".csv"):

            df = pd.read_csv(uploaded_file)

            st.dataframe(df.head())

        else:

            file_content = (
                uploaded_file.read()
                .decode("utf-8")
            )

    user_query = st.text_area(
        "Ask your coding question",
        height=180
    )

    if st.button("🚀 Ask Tutor"):

        response = coding_agent.run(
            user_query
        )

        st.markdown(response)

# =========================================================
# SUMMARY AGENT
# =========================================================

elif agent_type == "Summary Agent":

    st.header("📄 Summary Agent")

    uploaded_file = st.file_uploader(
        "Upload Document",
        type=["txt", "md", "py"]
    )

    if uploaded_file is not None:

        file_content = (
            uploaded_file.read()
            .decode("utf-8")
        )

        if st.button("🧠 Generate Summary"):

            response = summary_agent.summarize(
                file_content
            )

            st.markdown(response)

# =========================================================
# EVALUATOR AGENT
# =========================================================

elif agent_type == "Evaluator Agent":

    st.header("🧪 Evaluator Agent")

    problem_statement = st.text_area(
        "Problem Statement",
        height=180
    )

    rubric = st.text_area(
        "Rubric",
        height=180
    )

    submission = st.text_area(
        "Participant Submission",
        height=250
    )

    if st.button("🚀 Evaluate"):

        response = evaluator_agent.evaluate(
            problem_statement,
            rubric,
            submission
        )

        st.markdown(response)

# =========================================================
# QUIZ GENERATOR
# =========================================================

elif agent_type == "Quiz Generator":

    st.header("🧠 Quiz Generator")

    topic = st.text_input(
        "Enter Topic"
    )

    if st.button("❓ Generate Quiz"):

        quiz_data = quiz_agent.generate_quiz(
            topic
        )

        st.json(quiz_data)
