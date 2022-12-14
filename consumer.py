from kafka import KafkaConsumer
import json
import circuit

consumer = KafkaConsumer('foobar', bootstrap_servers='localhost:9092')
c = circuit.Race()
i = 0
for message in consumer:
    data = json.loads(message.value)
    if "event" in data and data["event"] == "race_concluded":
        print(c.order())
        exit(1)
    i += 1
    c.update(
        data["car"],
        data["checkpoint"],
        data["ts"]
    )
    if i % 5 == 0:
        print(c.order())
