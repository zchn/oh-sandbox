import unittest
import asyncio
from unittest.mock import AsyncMock, patch
from src.agents.qa_agent import QAAgent
from src.common.base_agent import Message

class TestQAAgent(unittest.IsolatedAsyncioTestCase):
    async def asyncSetUp(self):
        self.agent = QAAgent(
            agent_id="test_qa_agent",
            kafka_brokers="localhost:9092",
            subscribe_topics=["questions"]
        )
        self.agent.call_llm = AsyncMock(return_value="Test answer")
        self.agent.send_message = AsyncMock()

    async def test_process_message(self):
        test_message = Message(
            agent_id="test_user",
            content="What is the capital of France?",
            metadata={
                "type": "question",
                "question_id": "123"
            }
        )

        await self.agent.process_message(test_message)

        self.agent.call_llm.assert_awaited_once_with("What is the capital of France?")
        self.agent.send_message.assert_awaited_once_with(
            "answers",
            "Test answer",
            metadata={
                "type": "answer",
                "question_id": "123",
                "original_question": "What is the capital of France?"
            }
        )

if __name__ == '__main__':
    unittest.main()
