import logging
from fastapi import FastAPI, HTTPException, status
from backend.models import GenerateReplyRequest, GenerateReplyResponse
from backend.llm_service import generate_email_reply

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(
    title="AI Email Reply Assistant API",
    description="Backend API for AI Email Reply Assistant",
    version="0.2.0"
)


@app.get("/")
def read_root():
    return {"message": "AI Email Reply Assistant API is running"}


@app.get("/health")
def health_check():
    return {"status": "healthy"}


@app.post(
    "/api/generate-reply",
    response_model=GenerateReplyResponse,
    status_code=status.HTTP_200_OK,
    summary="Generate Email Reply",
    description="Accepts an incoming email and desired tone, and generates a context-aware reply using Gemini AI.")
def generate_reply_endpoint(request: GenerateReplyRequest) -> GenerateReplyResponse:
    try:
        reply_text = generate_email_reply(
            email_content=request.email_content,
            tone=request.tone.value
        )
        return GenerateReplyResponse(
            reply=reply_text,
            tone=request.tone.value
        )
    except ValueError as ve:
        logger.warning(f"Validation/Configuration error: {ve}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="AI service configuration error. Please ensure the GEMINI_API_KEYe is properly set in the server environment."
        )
    except RuntimeError as re:
        logger.error(f"Runtime error during reply generation: {re}")
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="The AI service is temporarily unavailable or unable to process the request. Please try again in a moment."
        )
    except Exception as e:
        logger.error(f"Unexpected error in generate_reply_endpoint: {type(e).__name__}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An unexpected server error occurred while processing your request."
        )
