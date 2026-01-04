import vertexai
from vertexai.generative_models import GenerativeModel

vertexai.init(
    project="adk-ops-copilot",
    location="us-central1"   # IMPORTANT
)

model = GenerativeModel("gemini-1.0-pro")

