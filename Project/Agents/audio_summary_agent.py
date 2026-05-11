import tempfile

from gtts import gTTS
from openai import OpenAI

client = OpenAI()


class AudioSummaryAgent:

    def generate_audio_summary(self, text):

        prompt = f"""
        Summarize into 3 concise learning points.

        Text:
        {text}
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

        summary = response.choices[0].message.content

        tts = gTTS(summary)

        temp_audio = tempfile.NamedTemporaryFile(
            delete=False,
            suffix=".mp3"
        )

        tts.save(temp_audio.name)

        return temp_audio.name, summary