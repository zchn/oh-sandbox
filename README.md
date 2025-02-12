# Multi-Agent System Powered by LLMs

This project implements a multi-agent system using LLMs (Language Learning Models) for processing and generating responses. The system uses Apache Kafka as the message queue backend for inter-agent communication.

## Features

1. Message queue backend (Apache Kafka) for agent communication
2. Compatible with managed Kafka services on AWS (MSK), GCP (Cloud Pub/Sub), and Azure (Event Hubs)
3. Implemented in Python with async/await support
4. Uses litellm for LLM API calls
5. Containerized agents that can run independently
6. Pub/sub pattern for message processing

## Architecture

- Each agent is a standalone container that subscribes to specific Kafka topics
- Agents process messages using LLMs and publish results back to Kafka
- Messages are structured with agent ID, content, and metadata
- Base agent class provides common functionality for all agents
- Asynchronous processing for better performance

## Getting Started

1. Set up environment variables:
```bash
export OPENAI_API_KEY=your-openai-api-key
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Run tests:
```bash
python -m unittest discover tests
```

4. Run the system using Docker Compose:
```bash
docker-compose up --build
```

## Using Managed Kafka Services

The system is compatible with managed Kafka services from major cloud providers:

1. AWS MSK (Managed Streaming for Apache Kafka):
   - Update KAFKA_BROKERS to point to your MSK cluster endpoints
   - Configure security groups and authentication as needed

2. GCP Cloud Pub/Sub with Kafka Connect:
   - Set up a Pub/Sub topic and subscription
   - Configure Kafka Connect to bridge Pub/Sub and Kafka
   - Update KAFKA_BROKERS accordingly

3. Azure Event Hubs with Kafka endpoint:
   - Create an Event Hubs namespace and hub
   - Enable Kafka endpoint
   - Update KAFKA_BROKERS with the Event Hubs Kafka endpoint

## Adding New Agents

1. Create a new agent class that inherits from BaseAgent:
```python
from src.common.base_agent import BaseAgent, Message

class MyAgent(BaseAgent):
    async def process_message(self, message: Message):
        # Process message and generate response
        response = await self.call_llm(message.content)
        await self.send_message("output_topic", response)
```

2. Add appropriate tests:
```python
class TestMyAgent(unittest.IsolatedAsyncioTestCase):
    async def asyncSetUp(self):
        self.agent = MyAgent(...)

    async def test_process_message(self):
        # Test agent behavior
```

3. Update docker-compose.yml to include your new agent:
```yaml
my-agent:
  build: .
  environment:
    AGENT_ID: my_agent_1
    SUBSCRIBE_TOPICS: input_topic
```

## Message Format

Messages are Pydantic models with the following structure:
```python
class Message(BaseModel):
    agent_id: str          # Unique identifier of the sending agent
    content: str           # Main message content
    metadata: Dict[str, Any] = {}  # Additional metadata
```

Example message flow:
```python
# Question message
{
    "agent_id": "user_1",
    "content": "What is the capital of France?",
    "metadata": {
        "type": "question",
        "question_id": "123"
    }
}

# Answer message
{
    "agent_id": "qa_agent_1",
    "content": "The capital of France is Paris.",
    "metadata": {
        "type": "answer",
        "question_id": "123",
        "original_question": "What is the capital of France?"
    }
}
```
