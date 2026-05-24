# Setup Ollama locally
## Local Setup
- Get the latest download instructions from [Ollama repository](https://github.com/ollama/ollama)

## Download a model
- We will be using a small model for local testing: `qwen3.5:9b`
- Details of this model are avaialble [here](https://ollama.com/library/qwen3.5:9b)
- Download the model using `ollama pull qwen3.5:9b`

## Test the model (CLI)
- All models are served on the URL: `http://localhost:11434/api`
- Test with the below snippet
    ```bash
    curl http://localhost:11434/api/generate -d '{
    "model": "qwen3.5:9b",
    "prompt": "What is 3 + 7",
    "stream": false
    }'
    ```
- This gives a response
    ```json
    {
        "model": "qwen3.5:9b",
        "created_at": "YYYY-MM-DDTHH:MM:SS.ssssssZ",
        "response": "3 + 7 = 10",
        "thinking": "Thinking Process:\n\n1.  **Analyze the Request:** The user is asking a simple arithmetic question: \"What is 3 + 7\".\n\n2.  **Calculate the Answer:** 3 + 7 = 10.\n\n3.  **Formulate the Output:** The answer is straightforward. I should just state the result clearly.\n\n4.  **Final Check:** Is there any trick? No. Is it a test of reasoning? No. Just basic addition.\n\n5.  **Construct Response:** \"3 + 7 = 10\".",
        "done": true,
        "done_reason": "stop",
        "context": [
        # list of integers
        ],
        "total_duration": # int,
        "load_duration": # int,
        "prompt_eval_count": 17,
        "prompt_eval_duration": # int,
        "eval_count": 131,
        "eval_duration": # int
    }
    ```

## Test the model (Python)
- Run the script `python ollama_sample.py`
- Prints the final response `3 + 7 = 10`

## Test Tool Calling via cURL
`qwen3.5:9b` natively supports tool calling, and the same can be verified from below.

```bash
curl http://localhost:11434/api/chat -d '{
  "model": "qwen3.5:9b",
  "messages": [
    {"role": "user", "content": "What is 11 plus 56?"}
  ],
  "tools": [
    {
      "type": "function",
      "function": {
        "name": "add_numbers",
        "description": "Add two numbers together",
        "parameters": {
          "type": "object",
          "properties": {
            "a": {"type": "number"},
            "b": {"type": "number"}
          },
          "required": ["a", "b"]
        }
      }
    }
  ],
  "stream": false
}'
```

must return an output like

```json
{
    "model": "qwen3.5:9b",
    "created_at": "some_timestamp",
    "message": {
        "role": "assistant",
        "content": "",
        "thinking": "The user is asking me to add 11 and 56. I can use the add_numbers function to help with this calculation. I need to provide the two numbers as parameters a and b.",
        "tool_calls": [
            {
                "id": "tool_call_id",
                "function": {
                    "index": 0,
                    "name": "add_numbers",
                    "arguments": {
                        "a": 11,
                        "b": 56
                    }
                }
            }
        ]
    },
    "done": true,
    "done_reason": "stop",
    "total_duration": int,
    "load_duration": int,
    "prompt_eval_count": int,
    "prompt_eval_duration": int,
    "eval_count": int,
    "eval_duration": int
}
```

Since this is not a native ReAct setup, we can feed back the output in another curl command

```bash
curl http://localhost:11434/api/chat -d '{
  "model": "qwen3.5:9b",
  "messages": [
    {
      "role": "user", 
      "content": "What is 11 plus 56?"
    },
    {
      "role": "assistant",
      "tool_calls": [
        {
          "id": "call_abc123",
          "type": "function",
          "function": {
            "name": "add_numbers",
            "arguments": {"a": 11, "b": 56}
          }
        }
      ]
    },
    {
      "role": "tool",
      "name": "add_numbers",
      "content": "67"
    }
  ],
  "stream": false
}'
```

which should give the final output
```json
{
    "model": "qwen3.5:9b",
    "created_at": "timestamp",
    "message": {
        "role": "assistant",
        "content": "11 plus 56 equals **67**.",
        "thinking": "Thinking Process:\n\n1.  **Identify the user's request**: The user is asking for the sum of two numbers: 11 and 56.\n2.  **Perform the calculation**:\n    *   $11 + 56$\n    *   $1 + 6 = 7$ (ones place)\n    *   $1 + 5 = 6$ (tens place)\n    *   Total = 67\n3.  **Verify with provided tool output**: The tool output confirms the result is 67.\n4.  **Formulate the final answer**: State the result clearly.\n\nResult: 67.cw"
    },
    "done": true,
    "done_reason": "stop",
    "total_duration": int,
    "load_duration": int,
    "prompt_eval_count": int,
    "prompt_eval_duration": int,
    "eval_count": int,
    "eval_duration": int
}
```
