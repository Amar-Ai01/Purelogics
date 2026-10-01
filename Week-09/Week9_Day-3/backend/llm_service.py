import logging
from google import genai
from google.genai import types
from backend.config import GEMINI_API_KEY, GEMINI_MODEL, validate_config

logger = logging.getLogger(__name__)



def generate_email_reply(email_content: str, tone: str) -> str:
    """
    Generates an email reply using Google Gemini AI via the google-genai SDK.
    """
    validate_config()

    client = genai.Client(api_key=GEMINI_API_KEY)

    system_instruction = (
        "You are an expert AI email assistant. "
        "Your task is to write a direct, high-quality reply to the incoming email based strictly on the requested tone. \n"
        "Rules:\n"
        "1. Output ONLY the reply email text (including standard greeting/sign-off as appropriate for the tone).\n"
        "2. Do NOT include any explanations, reasoning, meta-commentary, markdown backticks, or labels like 'Subject:' or 'Reply:'.\n"
        "3. Do NOT make up unverified commitments, false dates, or promises not suggested by the context.\n"
        "4. Strictly match the specified tone."
    )


    tone_guidelines = {
        "Professional": "Polite, formal, well-structured, respectful, and appropriate for workplace or academic settings.",
        "Friendly": "Warm, conversational, approachable, polite, and enthusiastic.",
        "Short and Concise": "Direct, brief, to the point, minimal filler, concise sentences or clear bullet points if applicable."
    }

    selected_guideline = tone_guidelines.get(
        tone, 
        "Clear, polite, and directly responding to the email content."
    )

    prompt = (
        f"Tone: {tone} ({selected_guideline})\n\n"
        f"Incoming Email:\n\"\"\"i{email_content}\n\"\"\"\n\n"
        "Generate the reply email:"
    )


    try:
        response = client.models.generate_content(
            model=GEMINI_MODEL,
            contents=prompt,
            config=types.GenerateContentConfig(
                system_instruction=system_instruction,
                temperature=0.7,
            )
        )

        if not response or not response.text:
            raise RuntimeError("Received an empty response from the II model.")

        return response.text.strip()

    except Exception as e:
        logger.error(f"Error calling Gemini API: {type(e)}")
        raise RuntimeError("Failed to generate email reply due to an upstream AI service error.") from e
