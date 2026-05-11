# ==========================================
# agents/evaluator.py
# ==========================================

from openai import OpenAI

client = OpenAI()


class EvaluatorAgent:

    def evaluate(
        self,
        problem_statement,
        rubric,
        submission_content,
        dataset_info=""
    ):

        prompt = f"""
You are an enterprise technical evaluator.

Evaluate the participant submission professionally.

========================================
PROBLEM STATEMENT
========================================

{problem_statement}

========================================
EVALUATION RUBRIC
========================================

{rubric}

========================================
PARTICIPANT SUBMISSION
========================================

{submission_content}

========================================
OPTIONAL DATASET INFO
========================================

{dataset_info}

========================================

Evaluation Instructions:

1. Understand the problem statement carefully.
2. Compare submission against rubric.
3. Check correctness.
4. Check optimization.
5. Check readability and maintainability.
6. Check edge cases and error handling.
7. Provide constructive improvements.
8. Give detailed scoring.

Return output STRICTLY in this format:

# 📊 Evaluation Report

## ✅ Rubric Scores

| Criteria | Score |
|---|---|
| Correctness | /10 |
| Optimization | /10 |
| Readability | /10 |
| Error Handling | /10 |
| Best Practices | /10 |

## 🏆 Final Score

X/50

## 💪 Strengths

- 
- 
- 

## ⚠ Weaknesses

- 
- 
- 

## 🚀 Suggested Improvements

- 
- 
- 

## 🎯 Final Verdict

PASS / NEEDS IMPROVEMENT / FAIL

Keep response concise but professional.
"""

        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            temperature=0.2,
            max_tokens=1200
        )

        return response.choices[0].message.content
