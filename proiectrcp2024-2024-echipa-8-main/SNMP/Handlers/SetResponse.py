from Utils.mib_utils import MIB
from Protocol.packet_utils import *


def SetResponse(decoded_message, address, UDPAgent, text):
    variable_bindings = decoded_message['variable_bindings']
    oid, _ = variable_bindings[0]

    if oid == "2.1":
        MIB.Name = text
        response = encode_snmp_message(
            version=decoded_message['version'],
            community=decoded_message['community'],
            pdu_type=decoded_message['pdu_type'],
            request_id=decoded_message['request_id'],
            error_status=0,
            error_index=0,
            variable_bindings=[("2.1", MIB.Name)]
        )
    elif oid == "2.2":
        MIB.Temperature = text
        response = encode_snmp_message(
            version=decoded_message['version'],
            community=decoded_message['community'],
            pdu_type=decoded_message['pdu_type'],
            request_id=decoded_message['request_id'],
            error_status=0,
            error_index=0,
            variable_bindings=[("2.2", MIB.Temperature)]
        )
    elif oid == "2.3":  # Setare checkRam
        MIB.set_check_ram(float(text))
        response = encode_snmp_message(
            version=decoded_message['version'],
            community=decoded_message['community'],
            pdu_type=decoded_message['pdu_type'],
            request_id=decoded_message['request_id'],
            error_status=0,
            error_index=0,
            variable_bindings=[("2.3", str(MIB.get_check_ram()))]
        )
    elif oid == "2.4":  # Setare checkCpu
        MIB.set_check_cpu(float(text))
        response = encode_snmp_message(
            version=decoded_message['version'],
            community=decoded_message['community'],
            pdu_type=decoded_message['pdu_type'],
            request_id=decoded_message['request_id'],
            error_status=0,
            error_index=0,
            variable_bindings=[("2.4", str(MIB.get_check_cpu()))]
        )
    else:
        response = b"Invalid"

    UDPAgent.sendto(response, address)
