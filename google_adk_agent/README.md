# Setup an Agent using Google ADK
## LLM Setup
- We are using `ollama/qwen3.5:9b`
- We import `from google.adk.models.lite_llm import LiteLlm` and set it up for `Ollama`
- Basic LiteLLM usage instructions are available [here](https://docs.litellm.ai/docs/)

### LLM Usage
- Listed out in `agent_model.py`; Simply run as `python agent_model.py`
- Should return an output similar to `The value of 3 + 8 is **11**.`

## Testing Agent
- Run `python agent.py`
- Should get an output similar to below
    ```bash
    --- Creating Sessions ---
    --- Testing Agent ---

    >>> Calling Agent: 'addition_agent' | Query: What is 11 + 13 ?
    <<< Agent 'addition_agent' Response: 11 + 13 = 24
    --- Session State ['None']: None
    ------------------------------
    ```
