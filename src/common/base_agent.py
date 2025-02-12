from abc import ABC, abstractmethod
from typing import List, Dict, Any
from aiokafka import AIOKafkaConsumer, AIOKafkaProducer
import json
from litellm import completion
import os
import asyncio
from pydantic import BaseModel

class Message(BaseModel):
    agent_id: str
    content: str
    metadata: Dict[str, Any] = {}

class BaseAgent(ABC):
    def __init__(self, agent_id: str, kafka_brokers: str, subscribe_topics: List[str]):
        self.agent_id = agent_id
        self.kafka_brokers = kafka_brokers
        self.subscribe_topics = subscribe_topics
        self.consumer = None
        self.producer = None

    async def initialize(self):
        self.consumer = AIOKafkaConsumer(
            *self.subscribe_topics,
            bootstrap_servers=self.kafka_brokers,
            value_deserializer=lambda x: Message.model_validate(json.loads(x.decode('utf-8')))
        )

        self.producer = AIOKafkaProducer(
            bootstrap_servers=self.kafka_brokers,
            value_serializer=lambda x: json.dumps(x.model_dump()).encode('utf-8')
        )

        await self.consumer.start()
        await self.producer.start()

    async def cleanup(self):
        if self.consumer:
            await self.consumer.stop()
        if self.producer:
            await self.producer.stop()

    async def send_message(self, topic: str, content: str, metadata: Dict[str, Any] = {}):
        message = Message(
            agent_id=self.agent_id,
            content=content,
            metadata=metadata
        )
        await self.producer.send_and_wait(topic, message)

    async def run(self):
        try:
            await self.initialize()
            async for message in self.consumer:
                await self.process_message(message.value)
        finally:
            await self.cleanup()

    @abstractmethod
    async def process_message(self, message: Message):
        pass

    async def call_llm(self, prompt: str, model: str = "gpt-3.5-turbo") -> str:
        response = completion(
            model=model,
            messages=[{"role": "user", "content": prompt}]
        )
        return response.choices[0].message.content
