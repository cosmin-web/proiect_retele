from tkinter import messagebox

from Utils.mib_utils import MIB
from Protocol.packet_utils import *


def GetResponse(decoded_message, address, UDPAgent):
    variable_bindings = decoded_message['variable_bindings']
    oid, _ = variable_bindings[0]

    if oid == "1.1":
        temperature = MIB.get_temperatura(MIB.Temperature)
        if temperature is not None:
            response = encode_snmp_message(
                version=decoded_message['version'],
                community=decoded_message['community'],
                pdu_type=decoded_message['pdu_type'],
                request_id=decoded_message['request_id'],
                error_status=0,
                error_index=0,
                variable_bindings=[("1.1", temperature)]
            )
        else:
            response = encode_snmp_message(
                version=decoded_message['version'],
                community=decoded_message['community'],
                pdu_type=decoded_message['pdu_type'],
                request_id=decoded_message['request_id'],
                error_status=0,
                error_index=0,
                variable_bindings=[("1.1", 0.0)]
            )
    elif oid == "1.2":
        response = encode_snmp_message(
            version=decoded_message['version'],
            community=decoded_message['community'],
            pdu_type=decoded_message['pdu_type'],
            request_id=decoded_message['request_id'],
            error_status=0,
            error_index=0,
            variable_bindings=[("1.2", MIB.Name)]
        )
    elif oid == "1.3":
        ram_percent = MIB.getRamPercent(MIB.getData)
        response = encode_snmp_message(
            version=decoded_message['version'],
            community=decoded_message['community'],
            pdu_type=decoded_message['pdu_type'],
            request_id=decoded_message['request_id'],
            error_status=0,
            error_index=0,
            variable_bindings=[("1.3", ram_percent)]
        )
    elif oid == "1.4":
        ram_gb = MIB.getRamGB(MIB.getData)
        response = encode_snmp_message(
            version=decoded_message['version'],
            community=decoded_message['community'],
            pdu_type=decoded_message['pdu_type'],
            request_id=decoded_message['request_id'],
            error_status=0,
            error_index=0,
            variable_bindings=[("1.4", ram_gb)]
        )
    elif oid == "1.5":
        cpu_percent = MIB.getCPUPercent(MIB.getData)
        response = encode_snmp_message(
            version=decoded_message['version'],
            community=decoded_message['community'],
            pdu_type=decoded_message['pdu_type'],
            request_id=decoded_message['request_id'],
            error_status=0,
            error_index=0,
            variable_bindings=[("1.5", cpu_percent)]
        )
    else:
        response = b"Invalid"

    UDPAgent.sendto(response, address)
