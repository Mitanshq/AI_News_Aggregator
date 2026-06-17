import json
from agents.base import BaseAgent
from schemas import AgentSummaryOutput

class SummarizerAgent(BaseAgent):
    async def process(self, content: str, *args, **kwargs) -> AgentSummaryOutput:
        """
        Analyzes the article content and generates a highly structured technical/business summary.
        """
        prompt = f"""
        You are an elite AI research analyst and technology journalist. 
        Analyze the following technical article text and produce a professional, structured analysis.
        
        Focus deeply on extracting:
        1. An executive-level summary of the actual announcement.
        2. Direct technical impact for engineers, architects, and researchers (e.g., architecture changes, context windows, training methods).
        3. Business impact (e.g., market competition, enterprise pricing shifts, cost reduction metrics).
        4. Top actionable key points.

        Article Content:
        {content}
        """
        try:
            # Force structured output matching our strict schema using Gemini 2.5 Flash
            structured_data = await self.ai_service.generate_structured_data(
                prompt=prompt,
                schema=AgentSummaryOutput,
                model=self.ai_service.summary_model
            )
            return structured_data
        except Exception as e:
            self.logger.error(f"Failed to summarize content: {str(e)}")
            # Return an empty/fallback structured object instead of throwing an unhandled exception
            return AgentSummaryOutput(
                executive_summary="Failed to generate summary due to an internal processing error.",
                technical_impact="N/A",
                business_impact="N/A",
                key_points=["Error processing article."]
            )