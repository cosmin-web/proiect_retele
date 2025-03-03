import socket
from Protocol.packet_utils import decode_snmp_message
from Utils.mib_utils import MIB
from tkinter import messagebox


def ReceiveTrap():

    bufferSize = 1024
    conn = ('127.0.0.1', 162)
    UDPclient = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)

    UDPclient.bind(conn)

    print(f"[INFO] Waiting for SNMP traps on {conn}...")

    while True:
        try:
            data, _ = UDPclient.recvfrom(bufferSize)
            decoded_message = decode_snmp_message(data)

            # Parcurge fiecare variabilă binding
            for oid, value in decoded_message['variable_bindings']:
                if oid == "1.3.6.1.4.1.0":  # Trap pentru RAM
                    print(f"TRAP: RAM % IS: {value}")
                    messagebox.showwarning(
                            "TRAP - RAM",
                            f"RAM Usage ({value}%) depășește pragul definit ({MIB.get_check_ram()}%)!"
                        )
                elif oid == "1.3.6.1.4.1.1":  # Trap pentru CPU
                    print(f"TRAP: CPU % IS: {value}")
                    messagebox.showwarning(
                            "TRAP - CPU",
                            f"CPU Usage ({value}%) depășește pragul definit ({MIB.get_check_cpu()}%)!"
                        )
        except Exception as e:
            print(f"[ERROR] Eroare la procesarea trap-ului: {e}")
