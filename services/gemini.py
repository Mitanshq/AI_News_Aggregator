import logging
from google import genai
from google.genai import types
from typing import Type
from pydantic import BaseModel
from config import settings

logger = logging.getLogger(__name__)

class GeminiService():
    def __init__(self):
        self.client = genai.Client(api_key=settings.GEMINI_API_KEY)
        self.summary_model = settings.MODEL_SUMMARY
        self.newsletter_model = settings.MODEL_NEWSLETTER
        
    async def generate_structured_data(self, prompt: str, schema: Type[BaseModel], model: str = None) -> BaseModel:
        target_model = model or self.summary_model
        try:
            response = await self.client.aio.models.generate_content(
                model=target_model,
                contents=prompt,
                config=types.GenerateContentConfig(
                    response_mime_type="application/json",
                    response_schema=schema,
                    temperature=0.1
                ),
            )
            return schema.model_validate_json(response.text)
        except Exception as e:
            logger.error(f"Error generating structured data from Gemini: {str(e)}")
            raise
        
    async def generate_text(self, prompt: str, model: str = None, temperature: float = 0.7) -> str:
        target_model = model or self.newsletter_model
        try:
            response = await self.client.aio.models.generate_content(
                model=target_model,
                contents=prompt,
                config=types.GenerateContentConfig(
                    temperature=temperature
                )
            )
            return response.text
        except Exception as e:
            logger.error(f"Error generating text from Gemini: {str(e)}")
            raise
        
        
gemini_client = GeminiService()