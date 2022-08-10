from operator import itemgetter

data = {
  44: 
    {
      "name": "HAM",
      "checkpoints": []
    },
  33:  
    {
      "name": "VER",
      "checkpoints": []
    },
  16:  
    {
      "name": "LEC",
      "checkpoints": [],
    },
  55:  
    {
      "name": "SAI",
      "checkpoints": [],
    },
  11:  
    {
      "name": "PER",
      "checkpoints": [],
    }
}

class Race:
  def __init__(self):
    self.num_checkpoints = 2
    self.fastest_lap = None

  def update(self, car_number, checkpoint, ts):
    if "checkpoints" not in data[car_number]:
      data[car_number]["checkpoints"] = []
    if "lap_times" not in data[car_number]:
      data[car_number]["lap_times"] = []

    if checkpoint != (len(data[car_number]["checkpoints"]))%self.num_checkpoints:
      raise Exception("faulty sensor: data mismatch")
    if len(data[car_number]["checkpoints"]) > 0 and data[car_number]["checkpoints"][-1] > ts:
      raise Exception("faulty sensor: timestamp mismatch on " + str(car_number))

    data[car_number]["checkpoints"].append(ts)

    # add lap time if applicable
    if len(data[car_number]["checkpoints"])%(self.num_checkpoints+1) == 0:
      lap_time = data[car_number]["checkpoints"][-1] - data[car_number]["checkpoints"][-(self.num_checkpoints+1)]
      data[car_number]["lap_times"].append(lap_time)
      if self.fastest_lap == None or self.fastest_lap[1] > lap_time:
        self.fastest_lap = (data[car_number]["name"], lap_time)

  def order(self):
    car_checkpoint_data = [
      {
        "name": data[car]["name"],
        "last_checkpoint": data[car]["checkpoints"][-1] if len(data[car]["checkpoints"]) > 0 else -1,
        "num_checkpoints": len(data[car]["checkpoints"])
      } for car in data.keys()
    ]

    # double sort; cars that have completed the most checkpoints
    # are first. ties broken by time they hit the checkpoint
    car_checkpoint_data.sort(key=itemgetter("last_checkpoint"))
    car_checkpoint_data.sort(key=itemgetter("num_checkpoints"), reverse=True)

    return [y["name"] for y in car_checkpoint_data]

  # assumes car2 is behind
  def interval(self, car1, car2):
    checkpoint = len(data[car2]["checkpoints"])-1
    return data[car2]["checkpoints"][-1] - data[car1]["checkpoints"][checkpoint] + data[car1]["checkpoints"][-1]
