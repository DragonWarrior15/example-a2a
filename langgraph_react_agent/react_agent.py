"""Quick React Agent in Langchain."""

from langchain.agents import create_agent

# we are not using ChatLiteLLM because it is not able to run tool calls
# from langchain_litellm.chat_models import ChatLiteLLM
from langchain_ollama import ChatOllama
from langgraph_react_agent.tools import add_numbers, multiply_numbers

from opentelemetry import trace
from phoenix.otel import register
from phoenix.otel import SpanAttributes

tracer_provider = register(
    protocol="http/protobuf", project_name="sample-agent-trace", auto_instrument=True
)
tracer = tracer_provider.get_tracer(__name__)

chat_model = ChatOllama(model="qwen3.5:9b", base_url="http://localhost:11434")

graph = create_agent(
    model=chat_model,
    tools=[add_numbers, multiply_numbers],
)

user_query = "Given a list of numbers [11, 56, 43], find the sum of the sum of the list and the product of the list"

inputs = {
    "messages": [
        {
            "role": "system",
            "content": "You are a top notch mathematician with access to math tools.",
        },
        {
            "role": "user",
            "content": user_query,
        },
    ]
}

if __name__ == "__main__":
    # build a custom span here so that everything is captured under
    # a single parent span

    with tracer.start_as_current_span(
        "sample-react-agent",
        attributes={
            SpanAttributes.OPENINFERENCE_SPAN_KIND: "AGENT",
            SpanAttributes.INPUT_VALUE: user_query,
        },
    ) as agent_span:
        try:
            # All LLM calls, tool executions, and embeddings inside here
            # will appear as children of this span
            output = graph.invoke(inputs)
            messages = output.get("messages", [])
            if messages:
                output_message = messages[-1].content
                print(output_message)

            # custom trace handling here
            agent_span.set_attribute(SpanAttributes.OUTPUT_VALUE, output_message)
            agent_span.set_status(trace.Status(trace.StatusCode.OK))

        except Exception as error:
            agent_span.set_status(trace.Status(trace.StatusCode.ERROR))
            raise
