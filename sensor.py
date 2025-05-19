import random
import time

def sensor_process(conn, name):
  print("New Process started:", name)
  while True:
    # Simulate data
    value = random.random()
    conn.send({'type': 'update', 'value': value})

    # Simulate a query (every few loops)
    if random.random() < 0.1:
      target = 'sensor_a' if name == 'sensor_b' else 'sensor_b'
      conn.send({'type': 'query', 'target': target})
      result = conn.recv()
      print(f"[{name}] got {target}'s value: {result['result']}")

    time.sleep(1)
