from dotenv import load_dotenv
import os
import httpx
from utils.decorators import decorator_intent

class IntentAgent:
    
    def __init__(self):
        load_dotenv()
        
        self.CANDIDATE_LABELS = os.getenv('CANDIDATE_LABELS_INTENT').split(',')
        self.API_KEY = os.getenv('API_KEY')
        self.API_URL = os.getenv('API_URL')

    @decorator_intent
    async def get_data(self,content: str):
        """
        Determines Intent of the file content.

        Attributes:
        content: Must be a type string. Should contain user input(prompt).

        labels: Must be a string of cantidate labels.

        Returns :
        --------
        API response from huggingface api for zero shot classification.
        """
        headers = {'Authorization': f'Bearer {self.API_KEY}'}
        # Content to provide to the API
        payload = {
            'inputs': content,
            'parameters': {
                        'candidate_labels':self.CANDIDATE_LABELS,
                        'multi_label': True
                           }
        }

        async with httpx.AsyncClient(timeout=30.0) as client:
            response = await client.post(self.API_URL,headers=headers, json=payload)

        return response.json()