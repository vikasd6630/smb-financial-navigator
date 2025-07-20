import vertexai
from vertexai.language_models import TextGenerationModel
from utils.config import settings

vertexai.init(project=settings.GCP_PROJECT_ID, location=settings.GCP_LOCATION)


class VertexAI:
    def __init__(self):
        self.model = TextGenerationModel.from_pretrained("text-bison@001")

    def get_funding_recommendations(self, prompt: str):
        response = self.model.predict(
            prompt,
            temperature=0.3,
            max_output_tokens=1024
        )
        return response.text