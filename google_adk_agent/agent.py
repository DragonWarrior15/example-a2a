"""Create an Agent using Google ADK."""

from agent_model import model

import asyncio

from google.adk.agents.llm_agent import LlmAgent
from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService
from google.genai.types import Content, Part


APP_NAME = "my_app"
USER_ID = "test_user_1"
SESSION_ID = "test_session_1"

addition_agent = LlmAgent(
    model=model,
    name="addition_agent",
    description="Add together numbers.",
    instruction="You are a helpful assistant that adds together numbers.",
    tools=[],
)

# setting up a memory store to run a session with this agent
session_service = InMemorySessionService()

# a runner for the session
runner = Runner(
    agent=addition_agent, app_name=APP_NAME, session_service=session_service
)


# a helper function to print output from the agent
async def call_agent_and_print(
    runner_instance: Runner,
    agent_instance: LlmAgent,
    session_id: str,
    query: str,
    session: InMemorySessionService,
):
    """Sends a query to the specified agent/runner and prints results."""
    print(f"\n>>> Calling Agent: '{agent_instance.name}' | Query: {query}")

    user_content = Content(role="user", parts=[Part(text=query)])

    final_response_content = "No final response received."
    async for event in runner_instance.run_async(
        user_id=USER_ID, session_id=session_id, new_message=user_content
    ):
        # print(f"Event: {event.type}, Author: {event.author}") # Uncomment for detailed logging
        if event.is_final_response() and event.content and event.content.parts:
            # For output_schema, the content is the JSON string itself
            final_response_content = event.content.parts[0].text

    print(f"<<< Agent '{agent_instance.name}' Response: {final_response_content}")

    current_session = await session.get_session(
        app_name=APP_NAME, user_id=USER_ID, session_id=session_id
    )
    stored_output = current_session.state.get(agent_instance.output_key)

    print(f"--- Session State ['{agent_instance.output_key}']: ", end="")
    print(stored_output)
    print("-" * 30)

# main function with all services initialized
async def main():
    print("--- Creating Sessions ---")
    await session_service.create_session(app_name=APP_NAME, user_id=USER_ID, session_id=SESSION_ID)

    print("--- Testing Agent ---")
    await call_agent_and_print(runner, addition_agent, SESSION_ID, "What is 11 + 13 ?", session_service)


if __name__ == "__main__":
    asyncio.run(main())
