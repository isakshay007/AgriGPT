from groq import Groq
from backend.core.config import settings

client = Groq(api_key=settings.GROQ_API_KEY)

def query_groq_text(prompt: str) -> str:
    """Send a text prompt to LLaMA-4 Scout on Groq API"""
    completion = client.chat.completions.create(
        model=settings.MODEL_NAME,
        messages=[
            {"role": "user", "content": prompt}
        ],
        temperature=0.7,
        max_completion_tokens=512,
        top_p=1,
        stream=False
    )
    return completion.choices[0].message.content
