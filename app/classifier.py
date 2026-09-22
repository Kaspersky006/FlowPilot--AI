import time

from google import genai

from app.config import GEMINI_API_KEY, GEMINI_MODEL
from app.models import AnalysisResult


client = genai.Client(api_key=GEMINI_API_KEY)


def classify_request(message: str) -> AnalysisResult:

    prompt = f"""
You are a customer support request classifier.

Analyze the following customer message:

{message}

Determine:
- category
- priority
- order_id
- summary

Category must be one of:
- delivery_issue
- refund_request
- payment_issue
- account_support
- product_question
- other

Priority must be:
- low
- medium
- high

If there is no order ID, return null.

Keep the summary short and factual.
"""

    last_error = None

    for attempt in range(3):
        try:
            response = client.models.generate_content(
                model=GEMINI_MODEL,
                contents=prompt,
                config={
                    "response_mime_type": "application/json",
                    "response_json_schema":
                        AnalysisResult.model_json_schema(),
                },
            )

            if not response.text:
                raise ValueError(
                    "Gemini returned an empty classification."
                )

            return AnalysisResult.model_validate_json(
                response.text
            )

        except Exception as error:
            last_error = error

            if attempt < 2:
                time.sleep(2)

    raise RuntimeError(
        f"Classification failed after 3 attempts: {last_error}"
    )