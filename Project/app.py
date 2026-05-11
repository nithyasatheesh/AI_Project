# =========================
# app.py
# =========================

import streamlit as st
import pandas as pd
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
    page_title="Multi-Agent AI Learning Platform",
    page_icon="🤖",
    layout="wide"
)

st.title("🤖 Multi-Agent AI Learning Platform")

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

# =========================================================
# SIDEBAR
# =========================================================

agent_type = st.sidebar.selectbox(
    "Select Agent",
    [
        "Coding Tutor",
        "Summary Agent",
        "Evaluator Agent",
        "Quiz Generator"
    ]
)

# =========================================================
# CLEAR CHAT WHEN AGENT CHANGES
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
# EVALUATOR AGENT
# =========================================================

if agent_type == "Evaluator Agent":

    st.header("🧪 Evaluator Agent")

    # -----------------------------------------------------
    # PROBLEM STATEMENT
    # -----------------------------------------------------

    st.subheader("📄 Problem Statement")

    typed_problem_statement = st.text_area(
        "Type Problem Statement (Optional)",
        height=180
    )

    uploaded_problem = st.file_uploader(
        "Upload Problem Statement",
        type=[
            "txt",
            "pdf",
            "py",
            "html",
            "docx"
        ],
        key="problem_statement"
    )

    # -----------------------------------------------------
    # RUBRIC
    # -----------------------------------------------------

    st.subheader("📋 Evaluation Rubric")

    typed_rubric = st.text_area(
        "Type Rubric (Optional)",
        height=180
    )

    uploaded_rubric = st.file_uploader(
        "Upload Rubric",
        type=[
            "txt",
            "pdf",
            "csv",
            "xlsx"
        ],
        key="rubric"
    )

    # -----------------------------------------------------
    # PARTICIPANT SUBMISSION
    # -----------------------------------------------------

    st.subheader("💻 Participant Submission")

    typed_submission = st.text_area(
        "Type Submission (Optional)",
        height=220
    )

    uploaded_submission = st.file_uploader(
        "Upload Submission",
        type=[
            "txt",
            "py",
            "html",
            "sql",
            "csv",
            "xlsx"
        ],
        key="submission"
    )

    # -----------------------------------------------------
    # OPTIONAL DATASET
    # -----------------------------------------------------

    st.subheader("📊 Optional Dataset")

    uploaded_dataset = st.file_uploader(
        "Upload Dataset",
        type=[
            "csv",
            "xlsx"
        ],
        key="dataset"
    )

    # =====================================================
    # PROCESS FILES
    # =====================================================

    problem_statement = typed_problem_statement

    rubric = typed_rubric

    participant_submission = typed_submission

    dataset_info = ""

    # -----------------------------------------------------
    # PROBLEM FILE
    # -----------------------------------------------------

    if uploaded_problem is not None:

        if uploaded_problem.name.endswith(".pdf"):

            problem_statement += (
                "\n\n"
                + read_pdf_file(uploaded_problem)
            )

        else:

            problem_statement += (
                "\n\n"
                + read_text_file(uploaded_problem)
            )

        st.success(
            f"Problem statement uploaded: "
            f"{uploaded_problem.name}"
        )

    # -----------------------------------------------------
    # RUBRIC FILE
    # -----------------------------------------------------

    if uploaded_rubric is not None:

        if uploaded_rubric.name.endswith(".txt"):

            rubric += (
                "\n\n"
                + read_text_file(uploaded_rubric)
            )

        elif uploaded_rubric.name.endswith(".pdf"):

            rubric += (
                "\n\n"
                + read_pdf_file(uploaded_rubric)
            )

        elif uploaded_rubric.name.endswith(".csv"):

            rubric_df = pd.read_csv(
                uploaded_rubric
            )

            rubric += (
                "\n\n"
                + rubric_df.to_string()
            )

        elif uploaded_rubric.name.endswith(".xlsx"):

            rubric_df = pd.read_excel(
                uploaded_rubric
            )

            rubric += (
                "\n\n"
                + rubric_df.to_string()
            )

        st.success(
            f"Rubric uploaded: "
            f"{uploaded_rubric.name}"
        )

    # -----------------------------------------------------
    # SUBMISSION FILE
    # -----------------------------------------------------

    if uploaded_submission is not None:

        if (
            uploaded_submission.name.endswith(".txt")
            or uploaded_submission.name.endswith(".py")
            or uploaded_submission.name.endswith(".html")
            or uploaded_submission.name.endswith(".sql")
        ):

            participant_submission += (
                "\n\n"
                + read_text_file(uploaded_submission)
            )

        elif uploaded_submission.name.endswith(".csv"):

            df = pd.read_csv(
                uploaded_submission
            )

            participant_submission += (
                "\n\n"
                + df.head(20).to_string()
            )

        elif uploaded_submission.name.endswith(".xlsx"):

            df = pd.read_excel(
                uploaded_submission
            )

            participant_submission += (
                "\n\n"
                + df.head(20).to_string()
            )

        st.success(
            f"Submission uploaded: "
            f"{uploaded_submission.name}"
        )

    # -----------------------------------------------------
    # OPTIONAL DATASET
    # -----------------------------------------------------

    if uploaded_dataset is not None:

        if uploaded_dataset.name.endswith(".csv"):

            dataset_df = pd.read_csv(
                uploaded_dataset
            )

        else:

            dataset_df = pd.read_excel(
                uploaded_dataset
            )

        st.markdown("### 📊 Dataset Preview")

        st.dataframe(dataset_df.head())

        dataset_info = (
            dataset_df.head(10)
            .to_string()
        )

    # =====================================================
    # TRUNCATE CONTENT
    # =====================================================

    problem_statement = truncate_text(
        problem_statement,
        4000
    )

    rubric = truncate_text(
        rubric,
        3000
    )

    participant_submission = truncate_text(
        participant_submission,
        6000
    )

    dataset_info = truncate_text(
        dataset_info,
        2000
    )

    # =====================================================
    # RUN EVALUATION
    # =====================================================

    if st.button("🚀 Evaluate Submission"):

        if not problem_statement.strip():

            st.warning(
                "Please provide problem statement."
            )

        elif not rubric.strip():

            st.warning(
                "Please provide rubric."
            )

        elif not participant_submission.strip():

            st.warning(
                "Please provide participant submission."
            )

        else:

            with st.spinner(
                "Evaluating submission..."
            ):

                response = evaluator_agent.evaluate(
                    problem_statement,
                    rubric,
                    participant_submission,
                    dataset_info
                )

            st.markdown("## 📊 Evaluation Result")

            st.markdown(response)

            # ---------------------------------------------
            # AUDIO SUMMARY
            # ---------------------------------------------

            st.markdown("## 🔊 Audio Summary")

            audio_file, summary = (
                audio_agent.generate_audio_summary(
                    response
                )
            )

            st.markdown(summary)

            if audio_file:

                audio_bytes = open(
                    audio_file,
                    "rb"
                ).read()

                st.audio(
                    audio_bytes,
                    format="audio/mp3"
                )

# =========================================================
# OTHER AGENTS
# =========================================================

else:

    uploaded_file = st.file_uploader(
        "📂 Upload Dataset or Code File",
        type=[
            "csv",
            "txt",
            "py",
            "md"
        ]
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
        "💬 Enter your question",
        height=160
    )

    if st.button("🚀 Run Agent"):

        st.session_state.messages.append({
            "role": "user",
            "content": user_query
        })

        response = ""

        # ------------------------------------------------
        # CODING TUTOR
        # ------------------------------------------------

        if agent_type == "Coding Tutor":

            response = coding_agent.run(
                user_query
            )

        # ------------------------------------------------
        # SUMMARY AGENT
        # ------------------------------------------------

        elif agent_type == "Summary Agent":

            if file_content:

                response = summary_agent.summarize(
                    file_content
                )

            else:

                response = (
                    "Please upload a document."
                )

        # ------------------------------------------------
        # QUIZ GENERATOR
        # ------------------------------------------------

        elif agent_type == "Quiz Generator":

            quiz_data = quiz_agent.generate_quiz(
                user_query
            )

            st.session_state.quiz_data = quiz_data

            response = (
                f"Quiz generated on: {user_query}"
            )

        st.session_state.messages.append({
            "role": "assistant",
            "content": response
        })

        st.rerun()

# =========================================================
# QUIZ DISPLAY
# =========================================================

if (
    agent_type == "Quiz Generator"
    and st.session_state.quiz_data
):

    st.markdown("# 🧠 Interactive Quiz")

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
                f"Correct Answer: {correct_answer}"
            )

            st.markdown(
                f"Explanation: {explanation}"
            )

            st.markdown("---")

        st.markdown(
            f"# 🏆 Final Score: {score}/5"
        )
