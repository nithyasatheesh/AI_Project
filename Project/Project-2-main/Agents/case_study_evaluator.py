from openai import OpenAI

client = OpenAI()


class CaseStudyEvaluator:

    def evaluate(self, submission):

        prompt = f"""
        Evaluate this technical submission.

        Provide:
        - Score out of 10
        - Strengths
        - Weaknesses
        - Suggested improvements

        Submission:
        {submission}
        """

        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {
                    "role": "user",
                    "content": prompt
                }
            ]
        )

        return response.choices[0].message.content