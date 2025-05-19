import random
import time
from multiprocessing import Pipe, Process


def master():
    sensor_conns = {}
    sensor_processes = {}

    def start_sensor(name, target_fn):
        parent_conn, child_conn = Pipe()
        p = Process(target=target_fn, args=(child_conn, name))
        p.start()
        sensor_conns[name] = parent_conn
        sensor_processes[name] = p

    # Start sensors
    start_sensor('sensor_a', sensor_process)
    start_sensor('sensor_b', sensor_process)

    sensor_data = {}

    while True:
        for name, conn in sensor_conns.items():
            if conn.poll():
                msg = conn.recv()
                if msg['type'] == 'update':
                    sensor_data[name] = msg['value']
                elif msg['type'] == 'query':
                    target = msg['target']
                    response = sensor_data.get(target, None)
                    conn.send({'result': response})

def sensor_process(conn, name):
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

if __name__ == '__main__':
    master()
