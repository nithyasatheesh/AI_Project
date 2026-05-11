import streamlit as st
import json
from streamlit_ace import st_ace

from agents.summary_agent import SummaryAgent
from agents.quiz_generator_agent import QuizGeneratorAgent
from agents.coding_tutor_agent import CodingTutorAgent


# -----------------------------------------------------
# PAGE CONFIG
# -----------------------------------------------------

st.set_page_config(
    page_title="Multi-Agent AI Learning Platform",
    layout="wide"
)


# -----------------------------------------------------
# LOAD AGENTS
# -----------------------------------------------------

summary_agent = SummaryAgent()
quiz_agent = QuizGeneratorAgent()
coding_agent = CodingTutorAgent()


# -----------------------------------------------------
# LOAD MODULES
# -----------------------------------------------------

with open("modules.json", "r") as f:
    modules_data = json.load(f)


# -----------------------------------------------------
# SESSION STATE
# -----------------------------------------------------

if "current_module" not in st.session_state:
    st.session_state.current_module = 0

if "module_completed" not in st.session_state:
    st.session_state.module_completed = False

if "quiz_completed" not in st.session_state:
    st.session_state.quiz_completed = False

if "quiz_data" not in st.session_state:
    st.session_state.quiz_data = None

if "score" not in st.session_state:
    st.session_state.score = 0


# -----------------------------------------------------
# HEADER
# -----------------------------------------------------

st.title("🤖 Multi-Agent AI Learning & Evaluation Platform")


# -----------------------------------------------------
# SIDEBAR
# -----------------------------------------------------

st.sidebar.header("📚 Learning Orchestrator")

module_titles = [
    module["title"]
    for module in modules_data["modules"]
]

selected_module = st.sidebar.radio(
    "Select Module",
    module_titles,
    index=st.session_state.current_module
)

st.session_state.current_module = module_titles.index(
    selected_module
)


# -----------------------------------------------------
# LOAD CURRENT MODULE
# -----------------------------------------------------

module = modules_data["modules"][
    st.session_state.current_module
]


# -----------------------------------------------------
# MODULE TITLE
# -----------------------------------------------------

st.header(f"📘 {module['title']}")


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

        if st.session_state.current_module < len(modules_data["modules"]) - 1:

            st.session_state.current_module += 1
            st.session_state.module_completed = False
            st.session_state.quiz_completed = False
            st.session_state.quiz_data = None

            st.rerun()


# -----------------------------------------------------
# OBJECTIVE
# -----------------------------------------------------

st.markdown("## 🎯 Objective")

st.info(module["objective"])


# -----------------------------------------------------
# PRACTICE TASK
# -----------------------------------------------------

st.markdown("## 💻 Practice Task")

st.write(module["practice_question"])


# -----------------------------------------------------
# CODE EDITOR
# -----------------------------------------------------

user_code = st_ace(
    value=module["starter_code"],
    language="python",
    theme="monokai",
    height=300,
    key="code_editor"
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

            st.error("❌ Function not found")

        else:

            result = local_env[
                function_name
            ](
                module["test_input"]
            )

            if result == module["expected_output"]:

                st.success("✅ Test Passed")

                st.session_state.module_completed = True

            else:

                st.error(
                    f"❌ Wrong Output: {result}"
                )

    except Exception as e:

        st.error(f"Execution Error: {e}")


# -----------------------------------------------------
# AI HINTS
# -----------------------------------------------------

st.markdown("## 💡 AI Hint")

if st.button("Get Hint"):

    hint_prompt = f"""
    Give ONLY a hint.

    Question:
    {module['practice_question']}

    Do not provide full solution.
    """

    hint = coding_agent.run(hint_prompt)

    st.info(hint)


# -----------------------------------------------------
# AI SUMMARY
# -----------------------------------------------------

if st.session_state.module_completed:

    st.markdown("## 🧠 AI Learning Summary")

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

    user_answers = {}

    score = 0

    for idx, q in enumerate(quiz):

        st.markdown(
            f"### Q{idx+1}. {q['question']}"
        )

        selected = st.radio(
            "Choose your answer",
            options=list(q["options"].values()),
            key=f"quiz_{idx}"
        )

        user_answers[idx] = selected


    # -------------------------------------------------
    # SUBMIT QUIZ
    # -------------------------------------------------

    if st.button("✅ Submit Quiz"):

        for idx, q in enumerate(quiz):

            correct_key = q["correct_answer"]

            correct_value = q["options"][correct_key]

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
                    f"Correct Answer: {correct_value}"
                )

            st.info(
                f"Explanation: {q['explanation']}"
            )

        st.session_state.score = score
        st.session_state.quiz_completed = True

        st.markdown("---")

        st.success(
            f"🎯 Final Score: {score}/{len(quiz)}"
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
