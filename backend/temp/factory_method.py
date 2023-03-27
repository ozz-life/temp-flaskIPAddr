import ipaddress

def create_ip_interface(ip_address, netmask=None):
    """
    Creates an IPv4Interface or IPv6Interface object for the given IP address and netmask.

    :param ip_address: str - the IP address to create the interface for
    :param netmask: str - the netmask to use for the interface (optional)
    :return: IPv4Interface or IPv6Interface - the created interface object
    """
    try:
        ip = ipaddress.ip_address(ip_address)
        if isinstance(ip, ipaddress.IPv4Address):
            # IPv4
            if netmask:
                ip_interface = ipaddress.IPv4Interface(f"{ip_address}/{netmask}")
            else:
                ip_interface = ipaddress.IPv4Interface(ip_address)
        else:
            # IPv6
            if netmask:
                ip_interface = ipaddress.IPv6Interface(f"{ip_address}/{netmask}")
            else:
                ip_interface = ipaddress.IPv6Interface(ip_address)
        return ip_interface
    except ValueError:
        return None

ipv4_interface = create_ip_interface("192.168.1.1", "24")
ipv6_interface = create_ip_interface("fe80::1", "64")