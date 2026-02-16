from groq import Groq
from app.utils.config import GROQ_API_KEY


client = None
if GROQ_API_KEY:
    try:
        client = Groq(api_key=GROQ_API_KEY)
    except Exception as e:
        print("Groq client init error:", e)


def generate_explanation(
    risk_percentage: int,
    hotspot_hits: int,
    weather: str,
    hazard_hits: int = 0
) -> str:

    if not client:
        return fallback_text(risk_percentage)

    try:
        prompt = f"""
You are a road safety assistant.
Generate a short, clear explanation for a user about route risk.

Risk Percentage: {risk_percentage}
Hotspots: {hotspot_hits}
Weather: {weather}
Hazards: {hazard_hits}

Rules:
- 1–2 sentences only
- Simple English
- No technical terms
- Mention main risk reasons
"""

        response = client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=[
                {"role": "system", "content": "You are a helpful safety assistant."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.4,
            max_tokens=80
        )

        return response.choices[0].message.content.strip()

    except Exception as e:
        print("LLM explanation error:", e)
        return fallback_text(risk_percentage)


def fallback_text(risk_percentage: int) -> str:
    if risk_percentage > 70:
        return "This route is risky due to multiple danger factors."
    elif risk_percentage > 40:
        return "This route has moderate risk. Stay cautious."
    else:
        return "This route appears relatively safe."
