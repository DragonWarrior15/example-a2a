# Setup a LangGraph based ReAct Agent
## What does not work
- `ChatLiteLLM` does not work and gives an empty response. `ChatOllama` is able to bind better with running tools.

## Usage
- Tools are defined in `tools.py`
- Run `python react_agent.py` to get the below output
```md
The sum of the list [11, 56, 43] is $11 + 56 + 43 = 110$.

The product of the list [11, 56, 43] is $11 \times 56 \times 43 = 26488$.

Finally, the sum of the sum and the product is $110 + 26488 = 26598$.
```

- If we print all the messages, this is how the output looks like (we can see individual tool calls)
```python
[
    SystemMessage(
        content="You are a top notch mathematician with access to math tools.",
        additional_kwargs={},
        response_metadata={},
        id="uuid",
    ),
    HumanMessage(
        content="Given a list of numbers [11, 56, 43], find the sum of the sum of the list and the product of the list",
        additional_kwargs={},
        response_metadata={},
        id="uuid",
    ),
    AIMessage(
        content="",
        additional_kwargs={},
        response_metadata={
            "model": "qwen3.5:9b",
            "created_at": "timestamp",
            "done": True,
            "done_reason": "stop",
            "total_duration": int,
            "load_duration": int,
            "prompt_eval_count": int,
            "prompt_eval_duration": int,
            "eval_count": int,
            "eval_duration": int,
            "logprobs": None,
            "model_name": "qwen3.5:9b",
            "model_provider": "ollama",
        },
        id="lc_run--uuid",
        tool_calls=[
            {
                "name": "add_numbers",
                "args": {"nums": [11, 56, 43]},
                "id": "tool_uuid_1",
                "type": "tool_call",
            },
            {
                "name": "multiply_numbers",
                "args": {"nums": [11, 56, 43]},
                "id": "tool_uuid_2",
                "type": "tool_call",
            },
        ],
        invalid_tool_calls=[],
        usage_metadata={"input_tokens": int, "output_tokens": int, "total_tokens": int},
    ),
    ToolMessage(
        content="110",
        name="add_numbers",
        id="uuid",
        tool_call_id="tool_uuid_1",
    ),
    ToolMessage(
        content="26488",
        name="multiply_numbers",
        id="uuid",
        tool_call_id="tool_uuid_2",
    ),
    AIMessage(
        content="",
        additional_kwargs={},
        response_metadata={
            "model": "qwen3.5:9b",
            "created_at": "timestamp",
            "done": True,
            "done_reason": "stop",
            "total_duration": int,
            "load_duration": int,
            "prompt_eval_count": int,
            "prompt_eval_duration": int,
            "eval_count": int,
            "eval_duration": int,
            "logprobs": None,
            "model_name": "qwen3.5:9b",
            "model_provider": "ollama",
        },
        id="lc_run--uuid",
        tool_calls=[
            {
                "name": "add_numbers",
                "args": {"nums": [110, 26488]},
                "id": "tool_uuid_3",
                "type": "tool_call",
            }
        ],
        invalid_tool_calls=[],
        usage_metadata={"input_tokens": int, "output_tokens": int, "total_tokens": int},
    ),
    ToolMessage(
        content="26598",
        name="add_numbers",
        id="uuid",
        tool_call_id="tool_uuid_3",
    ),
    AIMessage(
        content="The sum of the list [11, 56, 43] is 110.\nThe product of the list [11, 56, 43] is 26488.\n\nThe sum of these two results is:\n$110 + 26488 = 26598$\n\nSo, the final answer is **26598**.",
        additional_kwargs={},
        response_metadata={
            "model": "qwen3.5:9b",
            "created_at": "timestamp",
            "done": True,
            "done_reason": "stop",
            "total_duration": uuid,
            "load_duration": uuid,
            "prompt_eval_count": uuid,
            "prompt_eval_duration": uuid,
            "eval_count": uuid,
            "eval_duration": uuid,
            "logprobs": None,
            "model_name": "qwen3.5:9b",
            "model_provider": "ollama",
        },
        id="lc_run--uuid",
        tool_calls=[],
        invalid_tool_calls=[],
        usage_metadata={"input_tokens": uuid, "output_tokens": uuid, "total_tokens": uuid},
    ),
]
```
- Note that in the above response, tool call UUID is attached when calling the tool and when its output is generated
