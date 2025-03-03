import struct

INTEGER = 0x02
OCTET_STRING = 0x04
NULL = 0x05
OBJECT_IDENTIFIER = 0x06
SEQUENCE = 0x30
GET_REQUEST = 0xA0
GET_NEXT_REQUEST = 0xA1
GET_RESPONSE = 0xA2
SET_REQUEST = 0xA3
FLOAT = 0x09

def encode_length(length):
    if length < 128:
        return bytes([length])
    else:
        length_bytes = []
        while length > 0:
            length_bytes.insert(0, length & 0xFF)
            length >>= 8
        return bytes([0x80 | len(length_bytes)] + length_bytes)

def encode_integer(value):
    if value == 0:
        return bytes([INTEGER, 1, 0])
    encoded = []
    while value > 0:
        encoded.insert(0, value & 0xFF)
        value >>= 8
    return bytes([INTEGER, len(encoded)] + encoded)

def encode_octet_string(value):
    value_bytes = value.encode('utf-8')
    return bytes([OCTET_STRING]) + encode_length(len(value_bytes)) + value_bytes

def encode_null():
    return bytes([NULL, 0])

def encode_oid(oid):
    elements = [int(x) for x in oid.split('.')]
    encoded = [elements[0] * 40 + elements[1]]
    for value in elements[2:]:
        if value < 128:
            encoded.append(value)
        else:
            bytes_list = []
            while value:
                bytes_list.insert(0, value & 0x7F)
                value >>= 7
            for i in range(len(bytes_list) - 1):
                bytes_list[i] |= 0x80
            encoded.extend(bytes_list)
    return bytes([OBJECT_IDENTIFIER, len(encoded)] + encoded)

def encode_float(value):
    float_bytes = struct.pack('!f', value)  # IEEE 754 single-precision
    return bytes([FLOAT, len(float_bytes)]) + float_bytes

def encode_sequence(value, tag):
    return bytes([tag]) + encode_length(len(value)) + value

def encode_snmp_message(version, community, pdu_type, request_id, error_status, error_index, variable_bindings):
    varbind_contents = b''
    for oid, value in variable_bindings:
        value_encoding = (encode_integer(value) if isinstance(value, int)
                          else encode_octet_string(value) if isinstance(value, str)
                          else encode_float(value) if isinstance(value, float)
                          else encode_null())
        varbind = encode_sequence(encode_oid(oid) + value_encoding, SEQUENCE)
        varbind_contents += varbind
    pdu_contents = (
        encode_integer(request_id) +
        encode_integer(error_status) +
        encode_integer(error_index) +
        encode_sequence(varbind_contents, SEQUENCE)
    )
    message_contents = (
        encode_integer(version) +
        encode_octet_string(community) +
        encode_sequence(pdu_contents, pdu_type)
    )
    return encode_sequence(message_contents, SEQUENCE)

def decode_length(data, offset=0):
    first_byte = data[offset]
    if first_byte < 128:
        return first_byte, offset + 1
    num_bytes = first_byte & 0x7F
    length = 0
    offset += 1
    for _ in range(num_bytes):
        length = (length << 8) | data[offset]
        offset += 1
    return length, offset

def decode_integer(data, offset=0):
    if data[offset] != INTEGER:
        raise ValueError("Not an INTEGER type")
    length, offset = decode_length(data, offset + 1)
    value = 0
    for i in range(length):
        value = (value << 8) | data[offset + i]
    return value, offset + length

def decode_octet_string(data, offset=0):
    if data[offset] != OCTET_STRING:
        raise ValueError("Not an OCTET STRING type")
    length, offset = decode_length(data, offset + 1)
    value = data[offset:offset + length].decode('utf-8')
    return value, offset + length

def decode_oid(data, offset=0):
    if data[offset] != OBJECT_IDENTIFIER:
        raise ValueError("Not an OID type")
    length, offset = decode_length(data, offset + 1)
    end_offset = offset + length
    first_byte = data[offset]
    first = first_byte // 40
    second = first_byte % 40
    oid_components = [str(first), str(second)]
    offset += 1
    while offset < end_offset:
        value = 0
        while offset < end_offset:
            byte = data[offset]
            value = (value << 7) | (byte & 0x7F)
            offset += 1
            if not (byte & 0x80):
                break
        oid_components.append(str(value))
    return '.'.join(oid_components), offset

def decode_float(data, offset=0):
    if data[offset] != FLOAT:
        raise ValueError("Not a FLOAT type")
    length, offset = decode_length(data, offset + 1)
    if length != 4:
        raise ValueError("Invalid FLOAT length")
    value = struct.unpack('!f', data[offset:offset + length])[0]
    return value, offset + length

def decode_snmp_message(data):
    offset = 0
    if data[offset] != SEQUENCE:
        raise ValueError("Invalid SNMP message: expected SEQUENCE tag")
    length, offset = decode_length(data, offset + 1)
    version, offset = decode_integer(data, offset)
    community, offset = decode_octet_string(data, offset)
    pdu_type = data[offset]
    pdu_length, offset = decode_length(data, offset + 1)
    request_id, offset = decode_integer(data, offset)
    error_status, offset = decode_integer(data, offset)
    error_index, offset = decode_integer(data, offset)
    if data[offset] != SEQUENCE:
        raise ValueError("Invalid varbind list: expected SEQUENCE tag")
    varbind_length, offset = decode_length(data, offset + 1)
    varbind_end = offset + varbind_length
    variable_bindings = []
    while offset < varbind_end:
        if data[offset] != SEQUENCE:
            raise ValueError("Invalid varbind: expected SEQUENCE tag")
        _, offset = decode_length(data, offset + 1)
        oid, offset = decode_oid(data, offset)
        value_tag = data[offset]
        if value_tag == INTEGER:
            value, offset = decode_integer(data, offset)
        elif value_tag == OCTET_STRING:
            value, offset = decode_octet_string(data, offset)
        elif value_tag == FLOAT:
            value, offset = decode_float(data, offset)
        elif value_tag == NULL:
            value = None
            offset += 2
        else:
            raise ValueError(f"Unsupported value type: 0x{value_tag:02x}")
        variable_bindings.append((oid, value))
    return {
        'version': version,
        'community': community,
        'pdu_type': pdu_type,
        'request_id': request_id,
        'error_status': error_status,
        'error_index': error_index,
        'variable_bindings': variable_bindings
    }
