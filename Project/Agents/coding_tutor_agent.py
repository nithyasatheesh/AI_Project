from openai import OpenAI

client = OpenAI()


class CodingTutorAgent:

    def __init__(self):

        self.system_prompt = """
        You are an AI Coding Tutor.

        Help users:
        - Learn programming
        - Debug code
        - Understand technical concepts
        - Explain datasets and ML concepts
        """

    def run(self, user_query, chat_history=[]):

        messages = [
            {
                "role": "system",
                "content": self.system_prompt
            }
        ]

        for msg in chat_history:
            messages.append(msg)

        messages.append({
            "role": "user",
            "content": user_query
        })

        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=messages,
            temperature=0.3
        )

        return response.choices[0].message.content