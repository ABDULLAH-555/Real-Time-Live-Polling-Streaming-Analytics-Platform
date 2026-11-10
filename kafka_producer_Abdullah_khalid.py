import time
import json
from kafka import KafkaProducer
from poll_response_api import PollResponseAPI

BOOTSTRAP_SERVERS = ['localhost:9092']
TOPIC_NAME = 'poll_responses_v2'

def get_kafka_producer():
    return KafkaProducer(
        bootstrap_servers=BOOTSTRAP_SERVERS,
        value_serializer=lambda v: json.dumps(v).encode('utf-8')
    )

def main():
    producer = get_kafka_producer()
    api = PollResponseAPI()
    print(f"--- Kafka Producer Started on '{TOPIC_NAME}' ---")

    try:
        while True:
            raw_data = api.poll_response_api()
            payload = json.loads(raw_data) if isinstance(raw_data, str) else raw_data
            
            producer.send(TOPIC_NAME, value=payload)
            producer.flush()
            
            print(f"[PRODUCED] ID: {payload.get('answer_id')}")
            time.sleep(1.5)  
            
    except KeyboardInterrupt:
        print("\nStopping producer...")
    finally:
        producer.close()

if __name__ == "__main__":
    main()