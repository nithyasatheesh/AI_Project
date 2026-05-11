# agents/quiz_generator_agent.py

import json

from openai import OpenAI

client = OpenAI()


class QuizGeneratorAgent:

    def generate_quiz(self, topic):

        prompt = f"""
Generate 5 multiple-choice technical questions on:

{topic}

Return ONLY valid JSON in this exact format:

[
  {{
    "question": "Question text",
    "options": {{
      "A": "Option A",
      "B": "Option B",
      "C": "Option C",
      "D": "Option D"
    }},
    "correct_answer": "A",
    "explanation": "Explanation text"
  }}
]

Do not return markdown.
Do not return extra text.
"""

        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            temperature=0.3
        )

        content = response.choices[0].message.content

        try:

            quiz_data = json.loads(content)

            return quiz_data

        except Exception:

            return []
