from agents.base import BaseAgent
from typing import List, Dict, Any

class NewsletterAgent(BaseAgent):
    async def process(self, content: str, *args, **kwargs) -> str:
        """
        Overrides baseline process. Expects bundled pre-processed data structures.
        """
        return ""

    async def generate_html_newsletter(self, user_name: str, curated_stories: List[Dict[str, Any]]) -> str:
        """
        Synthesizes multiple processed stories into a premium, clean HTML email campaign.
        """
        # Construct an information-dense payload for Gemini 2.5 Pro
        stories_manifest = ""
        for idx, story in enumerate(curated_stories):
            stories_manifest += f"""
            --- STORY ID: {idx} ---
            Title: {story['title']}
            Source: {story['source']}
            Executive Summary: {story['executive_summary']}
            Technical Impact: {story['technical_impact']}
            Business Impact: {story['business_impact']}
            Key Bullet Points: {', '.join(story['key_points'])}
            Importance Score: {story['importance_score']}
            """

        prompt = f"""
        You are an advanced executive communications editor. Your task is to write a highly professional, mobile-responsive HTML newsletter briefing for {user_name}.
        
        Using the structured insights provided below, organize them into a clean corporate intelligence layout with the following hierarchy:
        1. **Top Story**: Pick the article with the highest global importance score.
        2. **Major Releases & Technical Highlights**: Summarize the secondary highly technical announcements.
        3. **Strategic Business Impact Matrix**: A brief analytical summary section highlighting what these items mean for enterprise investments.

        Use modern, clean typography and inline CSS styling (dark gray text, crisp borders, subtle background accent blocks for major sections). Ensure there are no unrendered markdown blocks or placeholders.

        Curated Stories Manifest Data:
        {stories_manifest}
        
        Return ONLY valid, deployable HTML starting with <html> and ending with </html>. Do not wrap in ```html code fences.
        """
        try:
            html_newsletter = await self.ai_service.generate_text(
                prompt=prompt,
                model=self.ai_service.newsletter_model,
                temperature=0.3
            )
            return html_newsletter
        except Exception as e:
            self.logger.error(f"Failed to synthesize HTML newsletter briefing: {str(e)}")
            return f"<h1>AI Daily Intelligence Report</h1><p>Hello {user_name}, your briefing encountered a formatting extraction error during generation.</p>"