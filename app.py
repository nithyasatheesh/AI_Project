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

if "module_completed" not in st.session_state:
    st.session_state.module_completed = False

if "quiz_completed" not in st.session_state:
    st.session_state.quiz_completed = False

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
    # MODULE TITLE
    # -----------------------------------------------------

    st.header(
        f"📘 Module {module['id']} - "
        f"{module['title']}"
    )

    # -----------------------------------------------------
    # MODULE NAVIGATION
    # -----------------------------------------------------

    col1, col2 = st.columns(2)

    with col1:

        if st.button("⬅ Previous Module"):

            if st.session_state.current_module > 0:

                st.session_state.current_module -= 1

                st.session_state.module_completed = False

                st.session_state.quiz_completed = False

                st.session_state.quiz_data = None

                st.rerun()

    with col2:

        if st.button("Next Module ➡"):

            if (
                st.session_state.current_module
                < len(modules_data["modules"]) - 1
            ):

                st.session_state.current_module += 1

                st.session_state.module_completed = False

                st.session_state.quiz_completed = False

                st.session_state.quiz_data = None

                st.rerun()

    # -----------------------------------------------------
    # LEARNING CONTENT
    # -----------------------------------------------------

    st.markdown("## 🎯 Objective")

    st.info(module["objective"])

    # -----------------------------------------------------
    # PRACTICE TASK
    # -----------------------------------------------------

    st.markdown("## 💻 Practice Task")

    st.markdown(
        module["practice_question"]
    )

    # -----------------------------------------------------
    # CODE EDITOR
    # -----------------------------------------------------

    user_code = st.text_area(
        "Write your code",
        value=module["starter_code"],
        height=300
    )

    # -----------------------------------------------------
    # RUN TEST
    # -----------------------------------------------------

    if st.button("▶ Run Test"):

        try:

            local_env = {}

            exec(user_code, {}, local_env)

            function_name = module["function_name"]

            if function_name not in local_env:

                st.error(
                    "❌ Function not found"
                )

            else:

                result = local_env[
                    function_name
                ](
                    module["test_input"]
                )

                if result == module["expected_output"]:

                    st.success(
                        "✅ Test Passed"
                    )

                    st.session_state.module_completed = True

                else:

                    st.error(
                        f"❌ Wrong Output: {result}"
                    )

        except Exception as e:

            st.error(
                f"Execution Error: {e}"
            )

    # -----------------------------------------------------
    # AI HINT
    # -----------------------------------------------------

    st.markdown("## 💡 AI Hint")

    if st.button("Get Hint"):

        hint_prompt = f"""
        Give ONLY a hint.

        Question:
        {module['practice_question']}

        Do not provide full solution.
        """

        hint = coding_agent.run(
            hint_prompt
        )

        st.info(hint)

    # -----------------------------------------------------
    # AI SUMMARY
    # -----------------------------------------------------

    if st.session_state.module_completed:

        st.markdown(
            "## 🧠 AI Learning Summary"
        )

        if st.button("Generate Summary"):

            summary = summary_agent.summarize(
                module["content"]
            )

            st.success(summary)

    # -----------------------------------------------------
    # QUIZ GENERATION
    # -----------------------------------------------------

    if st.session_state.module_completed:

        st.markdown("## ❓ Quiz")

        if st.button("Generate Quiz"):

            quiz_data = quiz_agent.generate_quiz(
                module["quiz_topic"]
            )

            st.session_state.quiz_data = quiz_data

    # -----------------------------------------------------
    # DISPLAY QUIZ
    # -----------------------------------------------------

    if st.session_state.quiz_data:

        quiz = st.session_state.quiz_data

        score = 0

        user_answers = {}

        st.markdown(
            "## 🧠 Quiz Questions"
        )

        for idx, q in enumerate(quiz):

            st.markdown(
                f"### Q{idx+1}. "
                f"{q['question']}"
            )

            selected = st.radio(
                "Choose an answer",
                options=list(
                    q["options"].values()
                ),
                key=f"quiz_{idx}"
            )

            user_answers[idx] = selected

        # -------------------------------------------------
        # SUBMIT QUIZ
        # -------------------------------------------------

        if st.button("✅ Submit Quiz"):

            for idx, q in enumerate(quiz):

                correct_key = q[
                    "correct_answer"
                ]

                correct_value = q[
                    "options"
                ][correct_key]

                selected = user_answers[idx]

                if selected == correct_value:

                    score += 1

                    st.success(
                        f"Q{idx+1} Correct ✅"
                    )

                else:

                    st.error(
                        f"Q{idx+1} Incorrect ❌"
                    )

                    st.info(
                        f"Correct Answer: "
                        f"{correct_value}"
                    )

                st.info(
                    f"Explanation: "
                    f"{q['explanation']}"
                )

            st.session_state.module_score += score

            st.session_state.quiz_completed = True

            st.markdown("---")

            st.success(
                f"🎯 Final Score: "
                f"{score}/{len(quiz)}"
            )

            st.success(
                f"🏆 Overall Program Score: "
                f"{st.session_state.module_score}"
            )

    # -----------------------------------------------------
    # MODULE COMPLETION
    # -----------------------------------------------------

    if (
        st.session_state.module_completed
        and st.session_state.quiz_completed
    ):

        st.balloons()

        st.success(
            "🎉 Module Completed Successfully"
        )

# =========================================================
# CODING TUTOR
# =========================================================

elif agent_type == "Coding Tutor":

    st.header("💻 Coding Tutor")

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

        st.write(quiz_data)
