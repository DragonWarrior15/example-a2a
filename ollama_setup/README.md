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
