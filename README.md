# example-a2a
Repository for a sample setup of Agent to agent (A2A) communication

## Example 1: Setup an A2A Server
### Basic flow of the setup of the Agent Server (`main.py`)
1. Define an `AgentSkill` which lists our agent's capabilities
2. Define an `AgentCard` which is basically a business card of our agent, specifying where it exists, what skills it has and which type of data exchanges it supports
3. Define a class that represents our `Agent` and encapsulates various tasks that it can do
4. Complete the definition of `AgentExecutor` which imlements one important function `execute` that understands how to create a new task, update its status with various update steps, and also knows how to invoke the agent and update the task with the final output/result
5. `DefaultRequestHandler` handles the server side of things, managing incoming requests and tasks
6. Create `routes` to serve the agent card and incoming requests (via request handler)
7. Serve the app using any web framework of choice

### Getting the Agent Card
Once the app is running, we can simply use the below `cURL` command to get the agent card.
```bash
curl 127.0.0.1:9999/.well-known/agent-card.json
```
and the (formatted) response is
```json
{
    "name": "Addition Agent",
    "description": "Returns total of two numbers",
    "supportedInterfaces": [
        {
            "url": "http://127.0.0.1:9999",
            "protocolBinding": "JSONRPC"
        }
    ],
    "version": "0.0.1",
    "capabilities": {
        "streaming": true,
        "extendedAgentCard": true
    },
    "defaultInputModes": [
        "text/plain"
    ],
    "defaultOutputModes": [
        "text/plain"
    ],
    "skills": [
        {
            "id": "add_two_numbers",
            "name": "Returns total of two numbers",
            "description": "Parses string for two numbers and returns their total",
            "tags": [
                "add",
                "+"
            ],
            "examples": [
                "2 2",
                "3, 5"
            ]
        }
    ],
    "preferredTransport": "JSONRPC",
    "protocolVersion": "0.3",
    "supportsAuthenticatedExtendedCard": true,
    "url": "http://127.0.0.1:9999"
}
```

### Sending a request using the terminal
Did not work, hence continue testing with the sdk functions in `sample_client.py`

### Sending a request using the SDK
