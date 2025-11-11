import base64
from groq import Groq
from backend.core.config import settings

client = Groq(api_key=settings.GROQ_API_KEY)

def query_groq_image(image_path: str, prompt: str) -> str:
    """Send an image and instruction to LLaMA-4 Scout model"""
    with open(image_path, "rb") as f:
        image_b64 = base64.b64encode(f.read()).decode("utf-8")

    completion = client.chat.completions.create(
        model=settings.MODEL_NAME,
        messages=[
            {
                "role": "user",
                "content": [
                    {"type": "text", "text": prompt},
                    {
                        "type": "image_url",
                        "image_url": f"data:image/jpeg;base64,{image_b64}"
                    }
                ],
            }
        ],
        temperature=0.7,
        max_completion_tokens=512,
        top_p=1,
        stream=False
    )
    return completion.choices[0].message.content
