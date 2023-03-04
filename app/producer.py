import contextlib
import time
from json import dumps
from kafka import KafkaProducer
from kafka.errors import NoBrokersAvailable
from faker import Faker
from typing import Optional

fake = Faker()


def create_producer() -> Optional[KafkaProducer]:
    producer = None
    counter = 0
    max_tries = 10
    base_sleep_time = 1
    sleep_time = base_sleep_time
    while counter < max_tries:
        try:
            producer = KafkaProducer(
                bootstrap_servers=['localhost:9092'],
                value_serializer=lambda x: dumps(x).encode('utf-8')
            )
            break
        except NoBrokersAvailable:
            print(f"No brokers available. Retrying in {sleep_time} seconds...")
            counter += 1
            time.sleep(sleep_time)
            sleep_time *= 2
        except Exception as e:
            print(dumps(e))

    if counter == max_tries:
        print("Could not connect to Kafka after 10 attempts.")
    return producer


def get_registered_user():
    return {
        "name": fake.name(),
        "address": fake.address(),
        "created_at": fake.year()
    }


def send_messages(producer, topic, data):
    with contextlib.closing(producer):
        producer.send(topic, data)
        print(data)


def send__test_messages(producer, topic, data):
    exit_producer = False
    counter = 0
    with contextlib.closing(producer):
        while not exit_producer:
            producer.send(topic, data)
            print(data)
            if counter > 9:
                while True:
                    user_input = input('press "1" to continue or any number to exit: ')
                    if user_input.isdigit():
                        break
                if int(user_input) != 1:
                    exit_producer = True
                    counter = 0
            counter += 1
            time.sleep(4)


registered_user = get_registered_user()
