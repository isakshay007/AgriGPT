import base64
from groq import Groq
from backend.core.config import settings

# Initialize Groq client
client = Groq(api_key=settings.GROQ_API_KEY)

def query_groq_image(image_path: str, prompt: str) -> str:
    """
    Send an image and text prompt to Groq’s multimodal model (LLaMA-4 Scout).
    Works with both local uploads and base64-encoded data.
    """

    try:
        # Read and encode image in base64
        with open(image_path, "rb") as f:
            image_b64 = base64.b64encode(f.read()).decode("utf-8")

        # Call Groq multimodal endpoint
        completion = client.chat.completions.create(
            model="meta-llama/llama-4-scout-17b-16e-instruct",  #  Use vision-capable model
            messages=[
                {
                    "role": "user",
                    "content": [
                        {"type": "text", "text": prompt},
                        {
                            "type": "image_url",
                            "image_url": {
                                "url": f"data:image/jpeg;base64,{image_b64}"
                            },
                        },
                    ],
                }
            ],
            temperature=0.7,
            max_completion_tokens=512,
            top_p=1,
            stream=False,
        )

        # Extract and return model response
        return completion.choices[0].message.content

    except Exception as e:
        return f"Error processing image: {e}"
