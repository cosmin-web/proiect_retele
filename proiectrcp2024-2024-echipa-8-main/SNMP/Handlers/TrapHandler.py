import time
import socket
import psutil
from Protocol.packet_utils import encode_snmp_message
from Utils.mib_utils import MIB

def checkTrap(agent):
    conn = ('127.0.0.1', 162)

    UDPagent = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)

    while True:
        try:
            ram_percent = psutil.virtual_memory().percent
            if ram_percent > MIB.get_check_ram():
                print(f"[TRAP] RAM Usage depășește pragul: {ram_percent}% (Prag: {MIB.get_check_ram()}%)")
                response = encode_snmp_message(
                    version=1,
                    community="public",
                    pdu_type=0xA4,  # Trap
                    request_id=0,
                    error_status=0,
                    error_index=0,
                    variable_bindings=[("1.3.6.1.4.1.0", ram_percent)]
                )
                UDPagent.sendto(response, conn)

        except Exception as e:
            print(f"Eroare la monitorizarea RAM: {e}")

        try:
            cpu_percent = psutil.cpu_percent(interval=1)
            if cpu_percent > MIB.get_check_cpu():
                print(f"[TRAP] CPU Usage depășește pragul: {cpu_percent}% (Prag: {MIB.get_check_cpu()}%)")
                response = encode_snmp_message(
                    version=1,
                    community="public",
                    pdu_type=0xA4,  # Trap
                    request_id=0,
                    error_status=0,
                    error_index=0,
                    variable_bindings=[("1.3.6.1.4.1.1", cpu_percent)]
                )
                UDPagent.sendto(response, conn)

        except Exception as e:
            print(f"Eroare la monitorizarea CPU: {e}")

        time.sleep(1)
