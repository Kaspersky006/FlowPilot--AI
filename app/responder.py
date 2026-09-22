import time

from google import genai

from app.config import GEMINI_API_KEY, GEMINI_MODEL
from app.models import AnalysisResult, OrderStatus


client = genai.Client(api_key=GEMINI_API_KEY)


def generate_customer_response(
    original_message: str,
    analysis: AnalysisResult,
    order: OrderStatus | None,
    action: str,
) -> str:

    order_information = (
        order.model_dump_json()
        if order
        else "No verified order information is available."
    )

    prompt = f"""
You are a professional customer support assistant.

Write a short customer-facing response.

Original customer message:
{original_message}

Request category:
{analysis.category}

Priority:
{analysis.priority}

Verified order information:
{order_information}

Action selected by the support system:
{action}

Rules:
- Be polite and concise.
- Do not invent information.
- Only use verified information provided above.
- Do not promise refunds, compensation, delivery dates, or actions
  that are not explicitly supported by the provided information.
- If an order was not found, ask the customer to verify the order ID.
- Return only the customer-facing response.
"""

    last_error = None

    for attempt in range(3):
        try:
            response = client.models.generate_content(
                model=GEMINI_MODEL,
                contents=prompt,
            )

            if not response.text:
                raise ValueError(
                    "Gemini returned an empty response."
                )

            return response.text.strip()

        except Exception as error:
            last_error = error

            if attempt < 2:
                time.sleep(2)

    raise RuntimeError(
        f"Response generation failed after 3 attempts: {last_error}"
    )