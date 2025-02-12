from src.common.base_agent import BaseAgent, Message

class QAAgent(BaseAgent):
    async def process_message(self, message: Message):
        if message.metadata.get("type") == "question":
            answer = await self.call_llm(message.content)
            await self.send_message(
                "answers",
                answer,
                metadata={
                    "type": "answer",
                    "question_id": message.metadata.get("question_id"),
                    "original_question": message.content
                }
            )
