from multiprocessing import Pipe, Process, connection

from sensor import sensor_main
from upgrade import update_and_restart

sensor_processes = {}

def master():
  sensor_conns = {}

  def start_sensor(name, target_fn):
    parent_conn, child_conn = Pipe()
    p = Process(target=target_fn, args=(child_conn, name))
    p.start()
    sensor_conns[name] = parent_conn
    sensor_processes[name] = p

  # Start sensors
  start_sensor('sensor_a', sensor_main)
  start_sensor('sensor_b', sensor_main)

  sensor_data = {}

  while True:
    # Wait for any connection to become ready
    ready_conns = connection.wait(sensor_conns.values())

    for conn in ready_conns:
      # Find which sensor this connection belongs to
      sensor_name = next(name for name, c in sensor_conns.items() if c == conn)

      try:
        msg = conn.recv()
      except EOFError:
        print(f"[{sensor_name}] Connection closed.")
        conn.close()
        sensor_conns.pop(sensor_name)

        start_sensor(sensor_name, sensor_main)
        continue

      if msg['type'] == 'update':
        sensor_data[sensor_name] = msg['value']
      elif msg['type'] == 'query':
        target = msg['target']
        response = sensor_data.get(target, None)
        conn.send({'result': response})


if __name__ == '__main__':
  update_and_restart()
  try:
    master()
  except KeyboardInterrupt:
    print("", end="\r")
    print("Shutting down...")
    for p in sensor_processes.values():
      p.terminate()
