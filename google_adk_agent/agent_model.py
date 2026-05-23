"""Setup the Local model using adk."""

import asyncio

from google.adk.models.lite_llm import LiteLlm
from google.adk.models.llm_request import LlmRequest
from google.genai.types import UserContent


model = LiteLlm(
    model="ollama/qwen3.5:9b",
    api_base="http://localhost:11434"
)

async def print_response():
    response = model.generate_content_async(
        llm_request=LlmRequest(
            contents=[UserContent("What is the value of 3 + 8 ?")]
        ),
        stream=False,
    )

    async for r in response:
        print(r.content.parts[0].text)

if __name__ == "__main__":
    asyncio.run(print_response())
