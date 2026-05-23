# Setup A2A Server
## Basic flow of the setup of the Agent Server (`main.py`)
1. Define an `AgentSkill` which lists our agent's capabilities
2. Define an `AgentCard` which is basically a business card of our agent, specifying where it exists, what skills it has and which type of data exchanges it supports
3. Define a class that represents our `Agent` and encapsulates various tasks that it can do
4. Complete the definition of `AgentExecutor` which imlements one important function `execute` that understands how to create a new task, update its status with various update steps, and also knows how to invoke the agent and update the task with the final output/result
5. `DefaultRequestHandler` handles the server side of things, managing incoming requests and tasks
6. Create `routes` to serve the agent card and incoming requests (via request handler)
7. Serve the app using any web framework of choice

## Getting the Agent Card
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

## Sending a request using the terminal
Did not work, hence continue testing with the sdk functions in `sample_client.py`

## Getting the agent card via SDK
We can use the `get_agent_card` function from `sample_client.py`. In this function, we initialize an `http` client and pass it the URL of our server from `main.py` for discovering the agent card.

```bash
Successfully fetched the public agent card:
====================================================
                     AgentCard                      
====================================================
--- General ---
Name        : Addition Agent
Description : Returns total of two numbers
Version     : 0.0.1

--- Interfaces ---
  [0] http://127.0.0.1:9999  (JSONRPC)

--- Capabilities ---
Streaming           : True
Push notifications  : False
Extended agent card : True

--- I/O Modes ---
Input  : text/plain
Output : text/plain

--- Skills ---
----------------------------------------------------
  ID          : add_two_numbers
  Name        : Returns total of two numbers
  Description : Parses string for two numbers and returns their total
  Tags        : add, +
  Example     : 2 2
  Example     : 3, 5
====================================================
```

## Getting a sample resonse via SDK
We use the `send_message` function, which internally relies on availability of the Agent Card.
```bash
Initializes the A2ACardResolver instance with an HTTP client

Successfully fetched the public agent card:
====================================================
                     AgentCard                      
====================================================
--- General ---
Name        : Addition Agent
Description : Returns total of two numbers
Version     : 0.0.1

--- Interfaces ---
  [0] http://127.0.0.1:9999  (JSONRPC)

--- Capabilities ---
Streaming           : True
Push notifications  : False
Extended agent card : True

--- I/O Modes ---
Input  : text/plain
Output : text/plain

--- Skills ---
----------------------------------------------------
  ID          : add_two_numbers
  Name        : Returns total of two numbers
  Description : Parses string for two numbers and returns their total
  Tags        : add, +
  Example     : 2 2
  Example     : 3, 5
====================================================

--- Public Agent Card - Non-Streaming Call ---

Initializing a non-streaming client.
Response:
task {
  id: "task UUID 1"
  context_id: "context UUID 1"
  status {
    state: TASK_STATE_COMPLETED
    message {
      message_id: "some UUID"
      role: ROLE_AGENT
      parts {
        text: "Request is completed!"
      }
    }
    timestamp {
      seconds: 1779532470
      nanos: 655708000
    }
  }
  artifacts {
    artifact_id: "some UUID"
    parts {
      text: "10"
      media_type: "text/plain"
    }
  }
  history {
    message_id: "some UUID"
    context_id: "context UUID 1"
    task_id: "task UUID 1"
    role: ROLE_USER
    parts {
      text: "3,7"
    }
  }
  history {
    message_id: "some UUID"
    role: ROLE_AGENT
    parts {
      text: "Processing request..."
    }
  }
}
```
