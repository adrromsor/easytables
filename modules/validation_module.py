def validate_user_input(src_ip, src_port, dst_ip, dst_port, protocol):
    if protocol == 'ALL':
        if src_port or dst_port:
            return "Port numbers require a protocol"

    if src_ip:
        if (validate_ip(src_ip) is False):
            return "Source IP \"{}\" is not valid".format(src_ip)

    if src_port:
        if (validate_port(src_port) is False):
            return "Source port \"{}\" is not valid".format(src_port)

    if dst_ip:
        if (validate_ip(dst_ip) is False):
            return "Destination IP \"{}\" is not valid".format(dst_ip)

    if dst_port:
        if (validate_port(dst_port) is False):
            return "Destination port \"{}\" is not valid".format(dst_port)

    return True

def validate_port(port):
    try:
        if not (1 <= len(port) <= 5):
            raise ValueError
        if not (1 <= int(port) <= 65535):
            raise ValueError

    except ValueError:
        return False

def validate_ip(ip):
    parts = ip.split(".")

    try:
        if len(parts) != 4:
            raise ValueError

        for part in parts:
            if not (1 <= len(part) <= 3):
                raise ValueError
            if not (0 <= int(part) <= 255):
                raise ValueError

    except ValueError:
        return False
