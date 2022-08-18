from operator import itemgetter
from kafka import KafkaProducer
import json
import time

producer = KafkaProducer(bootstrap_servers=['localhost:9092'])

def pub(data):
  x = producer.send('foobar', value=json.dumps(data).encode('ascii'))
  x.get(timeout=10)

events = [
  # CP 1
  ("LEC", 0, 0),
  ("VER", 0, 5),
  ("SAI", 0, 6),
  ("PER", 0, 8),
  ("HAM", 0, 10),
  # CP 2
  ("LEC", 1, 20),
  ("VER", 1, 20),
  ("SAI", 1, 30),
  ("PER", 1, 25),
  ("HAM", 1, 31),
  # CP 1
  ("LEC", 0, 35),
  ("VER", 0, 30),
  ("SAI", 0, 50),
  ("HAM", 0, 41),
]

driver_number_map = {
  "HAM": 44,
  "LEC": 16,
  "VER": 33,
  "SAI": 55,
  "PER": 11
}

def pub_events():
  events.sort(key=itemgetter(2))
  for e in events:
    time.sleep(e[2]/50)
    pub({
      "car": driver_number_map[e[0]],
      "checkpoint": e[1],
      "ts": e[2]
    })
  pub({"event": "race_concluded"})

pub_events()