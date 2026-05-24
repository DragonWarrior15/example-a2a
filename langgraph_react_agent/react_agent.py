"""Quick React Agent in Langchain."""

from langchain.agents import create_agent
# we are not using ChatLiteLLM because it is not able to run tool calls
# from langchain_litellm.chat_models import ChatLiteLLM
from langchain_ollama import ChatOllama
from tools import add_numbers, multiply_numbers

chat_model = ChatOllama(model="qwen3.5:9b", base_url="http://localhost:11434")

graph = create_agent(
    model=chat_model,
    tools=[add_numbers, multiply_numbers],
)

inputs = {
    "messages": [
        {
            "role": "system",
            "content": "You are a top notch mathematician with access to math tools.",
        },
        {
            "role": "user",
            "content": "Given a list of numbers [11, 56, 43], find the sum of the sum of the list and the product of the list",
        }
    ]
}

if __name__ == "__main__":
    output = graph.invoke(inputs)
    messages = output.get("messages", [])
    if messages:
        print(messages[-1].content)
