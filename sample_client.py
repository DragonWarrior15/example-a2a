"""Sample client for A2A interaction."""

import asyncio

import httpx

from a2a.client import A2ACardResolver, ClientConfig, create_client
from a2a.helpers import display_agent_card, new_text_message
from a2a.types.a2a_pb2 import Role, SendMessageRequest
from a2a.utils.constants import AGENT_CARD_WELL_KNOWN_PATH


async def get_agent_card():
    print("Initializes the A2ACardResolver instance with an HTTP client")

    # Initializes the A2ACardResolver instance with an HTTP client, base URL,
    # and uses the default path for the agent card.
    async with httpx.AsyncClient() as httpx_client:
        resolver = A2ACardResolver(
            httpx_client=httpx_client,
            base_url="http://127.0.0.1:9999",
            agent_card_path=AGENT_CARD_WELL_KNOWN_PATH,
        )

        public_agent_card = await resolver.get_agent_card()
        print("\nSuccessfully fetched the public agent card:")
        display_agent_card(public_agent_card)

    return public_agent_card


async def send_message(text_query: str = "3,7"):
    public_agent_card = await get_agent_card()
    print("\n--- Public Agent Card - Non-Streaming Call ---")

    print("\nInitializing a non-streaming client.")
    config = ClientConfig(streaming=False)
    client = await create_client(agent=public_agent_card, client_config=config)

    # Creates a new text message to be sent to the A2A Server.
    # Ex: text_query = '3,7'
    message = new_text_message(text_query, role=Role.ROLE_USER)
    request = SendMessageRequest(message=message)

    print("Response:")
    async for chunk in client.send_message(request):
        print(chunk)

    await client.close()


if __name__ == "__main__":
    # asyncio.run(get_agent_card())
    asyncio.run(send_message())
