"""Example Script for A2A implementation."""

import uvicorn
from a2a.helpers import (
    get_message_text,
    new_task_from_user_message,
    new_text_message,
    new_text_part,
)
from a2a.server.agent_execution import AgentExecutor, RequestContext
from a2a.server.events import EventQueue

from a2a.server.request_handlers import DefaultRequestHandler
from a2a.server.routes import create_agent_card_routes, create_jsonrpc_routes
from a2a.server.tasks import InMemoryTaskStore, TaskUpdater
from a2a.types import AgentCapabilities, AgentCard, AgentInterface, AgentSkill
from a2a.types.a2a_pb2 import TaskState
from fastapi import FastAPI

# Define agent skills, our agent can just say hello world
skill = AgentSkill(
    id="add_two_numbers",
    name="Returns total of two numbers",
    description="Parses string for two numbers and returns their total",
    tags=["add", "+"],
    examples=["2 2", "3, 5"],
)

# Define the agent card, describing the agent
# This will be the public-facing agent card
public_agent_card = AgentCard(
    name="Addition Agent",
    description="Returns total of two numbers",
    version="0.0.1",
    default_input_modes=["text/plain"],
    default_output_modes=["text/plain"],
    capabilities=AgentCapabilities(streaming=True, extended_agent_card=True),
    supported_interfaces=[
        AgentInterface(
            protocol_binding="JSONRPC",
            url="http://127.0.0.1:9999",
        )
    ],
    skills=[skill],  # Only the basic skill for the public card
)

# A2A manages processing of requests and their responses via an AgentExecutor interface
# We can implement it to define how our agent will take up work and generate responses
# AgentExecutor is an abstract class and we need to define two methods in it
# execute: handles incoming stream of requests, and this class should handle how
# to respond back; also use an event queue to send back Message, Task, TaskStatusUpdateEvent,
# or TaskArtifactUpdateEvent object
# cancel: handles request to cancel an ongoing task


# first define a helper class; this is similar to any agent implementation
class AdditionAgent:
    """Helper Addition Agent Class."""

    async def invoke(self, user_request: str) -> str:
        # the core agent implementation
        nums = [int(x) for x in user_request.split(" ")]
        return str(sum(nums))


class AdditionAgentExecutor(AgentExecutor):
    """The main executor interface."""

    def __init__(self):
        self.agent = AdditionAgent()

    async def execute(
        self,
        context: RequestContext,
        event_queue: EventQueue,
    ) -> None:
        """Execute the agent process and enqueue the final response."""

        # 1. get the current task or create a new
        if context.current_task:
            task = context.current_task
        else:
            task = new_task_from_user_message(context.message)
            await event_queue.enqueue_event(task)

        # 2. update the task status in eventqueue using TaskUpdater class object
        # this object is tied to our current task of interest
        task_updater = TaskUpdater(
            event_queue=event_queue,
            task_id=task.id,
            context_id=task.context_id,
        )
        await task_updater.update_status(
            state=TaskState.TASK_STATE_WORKING,
            message=new_text_message("Processing request..."),
        )

        # 3. Collect user request from request content and invoke
        # LLM agent to generate content
        query = get_message_text(context.message)
        if query:
            result = await self.agent.invoke(user_request=query)
        else:
            result = "No text input is provided!"

        # 4. Add generated response as an artifact to EventQueue
        await task_updater.add_artifact(
            parts=[new_text_part(text=result, media_type="text/plain")]
        )
        print("Result: ", result)

        # 5. Update task status to completed
        await task_updater.update_status(
            state=TaskState.TASK_STATE_COMPLETED,
            message=new_text_message("Request is completed!"),
        )

    async def cancel(
        self,
        context: RequestContext,
        event_queue: EventQueue,
    ) -> None:
        """Raise exception as cancel is not supported."""
        raise NotImplementedError("Cancel is not supported.")


# The RequestHandler processes incoming requests and manages tasks
# the server side of things
request_handler = DefaultRequestHandler(
    # Agent executor handles the execution of the client requests
    agent_executor=AdditionAgentExecutor(),
    # The task_store is used to store and manage tasks
    task_store=InMemoryTaskStore(),
    # Public agent card for unauthenticated users
    agent_card=public_agent_card,
)

routes = [
    # this route is for exposing the agent card
    create_agent_card_routes(public_agent_card),
    # this route is for exposing the request handler
    create_jsonrpc_routes(request_handler, "/"),
]

# create a fast api app to serve the routes
app = FastAPI(routes=routes)

# serve on uvicorn, keep the port here and in agent card same
uvicorn.run(app, host="127.0.0.1", port=9999)
