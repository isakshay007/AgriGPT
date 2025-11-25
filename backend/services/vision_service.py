# backend/services/vision_service.py
"""
FINAL Vision Service – Python 3.13 Safe
---------------------------------------
- Removes deprecated imghdr
- Uses magic-byte detection (PNG/JPEG only)
- Always returns pure string (OpenAPI safe)
- No dictionary or list output EVER
"""

from __future__ import annotations
import base64
import os
import time

from groq import Groq
from backend.core.config import settings

MAX_RETRIES = 3
BACKOFF = [1, 2, 4]   # retry delays


# ---------------------------------------------------------
# MIME Detection (No imghdr, Python 3.13 safe)
# ---------------------------------------------------------
def _detect_mime(image_path: str) -> str:
    """
    Detect PNG / JPEG using magic bytes.
    No imghdr (removed in Python 3.13).
    """
    try:
        with open(image_path, "rb") as f:
            header = f.read(10)
    except Exception:
        return "unknown"

    # PNG magic bytes: 89 50 4E 47
    if header.startswith(b"\x89PNG"):
        return "image/png"

    # JPEG magic bytes: FF D8
    if header.startswith(b"\xFF\xD8"):
        return "image/jpeg"

    return "unknown"


# ---------------------------------------------------------
# Normalize response to ALWAYS string
# ---------------------------------------------------------
def _normalize_output(o) -> str:
    if not o:
        return ""

    if isinstance(o, str):
        return o.strip()

    # Lists → join lines
    if isinstance(o, list):
        try:
            return "\n".join(_normalize_output(x) for x in o)
        except:
            return str(o)

    # Dict → flatten
    if isinstance(o, dict):
        try:
            return "\n".join(f"{k}: {v}" for k, v in o.items())
        except:
            return str(o)

    return str(o).strip()


# ---------------------------------------------------------
# MAIN VISION FUNCTION (SAFE)
# ---------------------------------------------------------
def query_groq_image(image_path: str, prompt: str) -> str:
    """
    Always returns a clean string — never dict/list.
    Works with Python 3.13 (no imghdr).
    """

    # Validate file existence
    if not os.path.exists(image_path):
        return "Error: Image file does not exist."

    # Validate file size
    if os.path.getsize(image_path) > 8 * 1024 * 1024:
        return "Error: Image too large (max 8MB)."

    # Detect MIME type
    mime = _detect_mime(image_path)
    if mime not in ("image/png", "image/jpeg"):
        return "Unsupported image format. Please upload PNG or JPG."

    # Load bytes
    try:
        with open(image_path, "rb") as f:
            raw = f.read()
    except Exception:
        return "Error reading image file."

    if not raw:
        return "Error: Image file is empty."

    # Base64 encode
    b64 = base64.b64encode(raw).decode("utf-8")
    image_url = f"data:{mime};base64,{b64}"

    # Retry loop
    for attempt in range(MAX_RETRIES):
        try:
            client = Groq(
                api_key=settings.GROQ_API_KEY,
                timeout=30,
            )

            completion = client.chat.completions.create(
                model=settings.VISION_MODEL_NAME,
                messages=[
                    {
                        "role": "system",
                        "content": (
                            "You are AgriGPT Vision, an expert crop disease classifier."
                        ),
                    },
                    {
                        "role": "user",
                        "content": [
                            {"type": "text", "text": prompt.strip()},
                            {"type": "image_url", "image_url": {"url": image_url}},
                        ],
                    },
                ],
                max_tokens=900,
                temperature=0.4,
                top_p=1.0,
            )

            msg = ""
            try:
                msg = completion.choices[0].message.content
            except:
                msg = "Could not analyze the image."

            return _normalize_output(msg)

        except Exception as e:
            if attempt < MAX_RETRIES - 1:
                time.sleep(BACKOFF[attempt])
                continue

            return f"Groq vision model error: {str(e)}"
