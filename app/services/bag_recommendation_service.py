import json
import os
from typing import Dict
import openai
from fastapi import HTTPException
from sqlalchemy.orm import Session
from app.models.bag_recommendations import BagRecommendation

class BagRecommendationService:
    def __init__(self, openai_client: openai.Client):
        self.openai_client = openai_client

    def _load_satisfaction_data(self, file_path: str) -> Dict:
        """Load and validate the bag satisfaction data from JSON file."""
        try:
            with open(file_path, 'r') as file:
                return json.load(file)
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Error loading satisfaction data: {str(e)}")

    def _prepare_prompt(self, satisfaction_data: Dict) -> str:
        """Prepare a prompt for OpenAI based on the satisfaction data."""
        products = satisfaction_data.get("product_satisfaction_data", [])
        prompt = "Based on the following customer satisfaction data for bags:\n\n"

        for product in products:
            prompt += f"Product: {product['product_name']}\n"
            prompt += f"Price: ${product['price']}\n"
            prompt += "Customer Feedback:\n"
            metrics = product['satisfaction_metrics']
            prompt += f"- Average Rating: {metrics['average_rating']}/5\n"
            prompt += f"- Satisfaction Score: {metrics['satisfaction_score']}/100\n"
            prompt += "Key Feedback:\n"
            for aspect, score in metrics['key_feedback'].items():
                prompt += f"  * {aspect.replace('_', ' ').title()}: {score}/5\n"
            prompt += "\n"

        prompt += "\nBased on this customer satisfaction data, please provide:\n"
        prompt += "1. Specific recommendations for improved bag specifications\n"
        prompt += "2. Key features to focus on for better customer satisfaction\n"
        prompt += "3. Suggested improvements for each current product category\n"
        prompt += "Please be specific and practical in your recommendations."

        print(f"prompt:\n{prompt}")

        return prompt

    async def get_bag_recommendations(self, db: Session, data_file_path: str) -> Dict:
        """
        Analyze bag satisfaction data and get AI recommendations for improvements.
        """
        try:
            # Load satisfaction data
            satisfaction_data = self._load_satisfaction_data(data_file_path)

            # Prepare the prompt for OpenAI
            prompt = self._prepare_prompt(satisfaction_data)

            # Get recommendations from OpenAI
            response = self.openai_client.chat.completions.create(
                model="gpt-4",  # Using GPT-4 for better analysis
                messages=[
                    {"role": "system", "content": "You are a product design expert specializing in bag manufacturing and customer satisfaction analysis."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.7
            )

            print("Finished getting recommendations from OpenAI")

            # Extract the response
            ai_response = response.choices[0].message.content
            tokens_used = response.usage.total_tokens if response.usage else None

            print(f"AI Response: {ai_response}")

            # Create database record
            db_recommendation = BagRecommendation(
                recommendations=ai_response,
                analyzed_products=len(satisfaction_data["product_satisfaction_data"]),
                tokens_used=tokens_used
            )

            db.add(db_recommendation)
            db.commit()
            db.refresh(db_recommendation)

            return {
                "id": db_recommendation.id,
                "recommendations": ai_response,
                "analyzed_products": db_recommendation.analyzed_products,
                "created_at": db_recommendation.created_at,
                "tokens_used": tokens_used
            }

        except Exception as e:
            raise HTTPException(
                status_code=500,
                detail=f"Error generating bag recommendations: {str(e)}"
            )
