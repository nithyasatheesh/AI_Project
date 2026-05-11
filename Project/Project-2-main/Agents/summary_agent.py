from openai import OpenAI

client = OpenAI()


class SummaryAgent:

    def summarize(self, content):

        prompt = f"""
        Summarize the following technical content.

        Include:
        - Key concepts
        - Important takeaways
        - Beginner-friendly explanation

        Content:
        {content}
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