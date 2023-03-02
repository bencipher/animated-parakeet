from kafka import KafkaConsumer
import json


consumer = KafkaConsumer(
    'registered_user',
    bootstrap_servers=['localhost:9092'],
    auto_offset_reset='earliest',
    enable_auto_commit=True,
    group_id='my-random-id',
    value_deserializer=lambda x: loads(x.decode('utf-8'))
)
for msg in consumer:
    print("Registered User = {}".format(json.loads(msg.value)))