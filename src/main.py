import asyncio
import os
from dotenv import load_dotenv
from agents.qa_agent import QAAgent

async def main():
    load_dotenv()

    kafka_brokers = os.getenv("KAFKA_BROKERS", "localhost:9092")
    agent_id = os.getenv("AGENT_ID", "qa_agent_1")
    subscribe_topics = os.getenv("SUBSCRIBE_TOPICS", "questions").split(",")

    agent = QAAgent(
        agent_id=agent_id,
        kafka_brokers=kafka_brokers,
        subscribe_topics=subscribe_topics
    )

    await agent.run()

if __name__ == "__main__":
    asyncio.run(main())
