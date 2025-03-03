import threading
import socket
from Handlers.GetResponse import GetResponse
from Handlers.SetResponse import SetResponse
from Handlers.TrapHandler import *

from Protocol.packet_utils import decode_snmp_message, encode_snmp_message

agents = [
    {'ip': '127.0.0.1', 'port': 161},
    {'ip': '127.0.0.2', 'port': 161},
    {'ip': '127.0.0.3', 'port': 161}
]

bufferSize = 1024
threads = []

def handle_agent(agent):
    UDPAgent = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
    UDPAgent.bind((agent['ip'], agent['port']))

    print(f"Agent listening on {agent['ip']}:{agent['port']}")

    threading.Thread(target=checkTrap, args=(agent,)).start()

    try:
        while True:
            data = UDPAgent.recvfrom(bufferSize)
            decoded_message = decode_snmp_message(data[0])
            print(f"Decoded SNMP message from {agent['ip']}: {decoded_message}")

            address = data[1]
            variable_bindings = decoded_message['variable_bindings']

            if not variable_bindings:
                UDPAgent.sendto(b"Invalid", address)
                continue

            oid, value = variable_bindings[0]

            if oid.startswith("1."):
                GetResponse(decoded_message, address, UDPAgent)
            elif oid.startswith("2."):
                SetResponse(decoded_message, address, UDPAgent, value)
            else:
                UDPAgent.sendto(b"Invalid", address)
    except KeyboardInterrupt:
        print(f"Agent {agent['ip']} stopped manually.")
    finally:
        UDPAgent.close()

for agent in agents:
    t = threading.Thread(target=handle_agent, args=(agent,))
    t.start()
    threads.append(t)

for t in threads:
    t.join()
