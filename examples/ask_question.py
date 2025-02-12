import asyncio
import json
from aiokafka import AIOKafkaProducer, AIOKafkaConsumer
import uuid

async def ask_question(question: str, kafka_brokers: str = "localhost:9092"):
    # Create a unique question ID
    question_id = str(uuid.uuid4())

    # Create producer and consumer
    producer = AIOKafkaProducer(
        bootstrap_servers=kafka_brokers,
        value_serializer=lambda x: json.dumps(x).encode('utf-8')
    )
    consumer = AIOKafkaConsumer(
        "answers",
        bootstrap_servers=kafka_brokers,
        value_deserializer=lambda x: json.loads(x.decode('utf-8'))
    )

    try:
        # Start producer and consumer
        await producer.start()
        await consumer.start()

        # Send question
        message = {
            "agent_id": "user",
            "content": question,
            "metadata": {
                "type": "question",
                "question_id": question_id
            }
        }
        await producer.send_and_wait("questions", message)
        print(f"Question sent: {question}")

        # Wait for answer
        async for msg in consumer:
            answer = msg.value
            if (answer["metadata"].get("question_id") == question_id and
                answer["metadata"].get("type") == "answer"):
                print(f"Answer received: {answer['content']}")
                break

    finally:
        # Cleanup
        await producer.stop()
        await consumer.stop()

async def main():
    questions = [
        "What is the capital of France?",
        "Who wrote Romeo and Juliet?",
        "What is the largest planet in our solar system?"
    ]

    for question in questions:
        await ask_question(question)
        await asyncio.sleep(1)  # Wait a bit between questions

if __name__ == "__main__":
    asyncio.run(main())
