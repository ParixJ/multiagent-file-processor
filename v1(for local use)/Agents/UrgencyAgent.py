from dotenv import load_dotenv
import os
import httpx
from utils.decorators import decorator_urgency

class UrgencyAgent:
    """
    UrgencyAgent determines the urgency of provided text content
    using a zero-shot classification model via an external API.

    Attributes:
    ----------
    CANDIDATE_LABELS : list of str
        Labels representing urgency levels, loaded from environment.
    API_KEY : str
        Authorization key for the external model API.
    API_URL : str
        Endpoint URL for the model API.

    Methods:
    -------
    get_data(content: str):
        Asynchronously sends content to the model and retrieves urgency classification.
    """

    def __init__(self):
        """
        Initialize the UrgencyAgent.
        Loads environment variables for candidate labels, API key, and URL.
        """
        load_dotenv()  # Load environment variables from .env file
        self.CANDIDATE_LABELS = os.getenv('CANDIDATE_LABELS_URGENCY').split(',')
        self.API_KEY = os.getenv('API_KEY')
        self.API_URL = os.getenv('API_URL')

    @decorator_urgency
    async def get_data(self, content: str):
        """
        Classify the urgency level of the given content using a zero-shot model.

        Parameters:
        ----------
        content : str
            The input text to classify (e.g., email body or document text).

        Returns:
        -------
        dict
            The JSON response from the model API, including predicted labels and scores.
            Example:
            {
                'labels': ['High', 'Low', 'Medium'],
                'scores': [0.85, 0.1, 0.05]
            }

        Raises:
        ------
        Exception
            If the HTTP request fails or times out.
        """
        headers = {'Authorization': f'Bearer {self.API_KEY}'}
        payload = {
            'inputs': content,
            'parameters': {
                'candidate_labels': self.CANDIDATE_LABELS,
                'multi_label': True
            }
        }

        async with httpx.AsyncClient(timeout=60.0) as client:
            response = await client.post(self.API_URL, headers=headers, json=payload)

        return response.json()
