import subprocess
import ipaddress

# import netifaces


def get_interface_name(ip_address):
    """
    Returns the name of the network interface that has the given IP address.

    Args:
        ip_address (str): The IP address to look for.

    Returns:
        str: The name of the network interface, or None if no interface was found.
    """
    interfaces = netifaces.interfaces()
    for interface in interfaces:
        addrs = netifaces.ifaddresses(interface)
        if netifaces.AF_INET in addrs:
            for addr in addrs[netifaces.AF_INET]:
                if addr["addr"] == ip_address:
                    return interface
    return None


def add_ipv4_address(interface, ip_address, netmask):
    """
    Adds an IPv4 address to a network interface using the `ip addr` command.

    Args:
        interface (str): The name of the network interface to add the IP address to.
        ip_address (str): The IPv4 address to add to the interface.
        netmask (int): The netmask in CIDR notation.

    Returns:
        bool: True if the IP address was successfully added, False otherwise.
    """
    try:
        subprocess.check_call(
            ["ip", "addr", "add", "{}/{}".format(ip_address, netmask), "dev", interface]
        )
        return True
    except subprocess.CalledProcessError:
        return False


def get_ipv4_address():
    """
    Returns the IPv4 address of the current machine by parsing the output of the `ip addr` command.

    Returns:
        str: The IPv4 address of the machine.
    """
    output = subprocess.check_output(["ip", "addr"])
    output = output.decode("utf-8")
    for line in output.splitlines():
        if "inet " in line and "127.0.0.1" not in line:
            ipv4_address = line.split()[1].split("/")[0]
            return ipv4_address


def get_ipv6_address():
    """
    Get the primary IPv6 address for the current host.

    Returns:
        str: The primary IPv6 address for the current host.
    """
    interfaces = netifaces.interfaces()
    for interface in interfaces:
        addrs = netifaces.ifaddresses(interface)
        if netifaces.AF_INET6 in addrs:
            for addr in addrs[netifaces.AF_INET6]:
                if "fe80" not in addr["addr"]:
                    return addr["addr"]
    return None


def remove_ipv4_address(interface, address):
    """
    Remove an IPv4 address from the given interface.

    Args:
        interface (str): The name of the interface (e.g. "eth0").
        address (str): The IPv4 address (e.g. "192.168.1.2/24").

    Raises:
        subprocess.CalledProcessError: If the "ip" command fails.

    Returns:
        str: The output of the "ip" command.
    """
    command = ["ip", "addr", "del", address, "dev", interface]
    output = subprocess.check_output(command, stderr=subprocess.STDOUT)
    return output.decode("utf-8")


def change_ip_address(interface, new_ip_address, netmask):
    """
    Change the IP address of a network interface using the `ip` command.

    Args:
        interface (str): The name of the interface to change the IP address of.
        new_ip_address (str): The new IP address to assign to the interface, in the form of "x.x.x.x".
        netmask (str): The netmask for the new IP address, in the form of "x.x.x.x".

    Raises:
        subprocess.CalledProcessError: If the `ip` command fails to execute properly.

    Returns:
        None
    """
    subprocess.run(["ip", "addr", "flush", "dev", interface], check=True)
    subprocess.run(
        ["ip", "addr", "add", f"{new_ip_address}/{netmask}", "dev", interface],
        check=True,
    )


def get_default_route():
    """
    Get the default route IP address.

    Returns:
    - str: Default route IP address.
    """
    output = subprocess.check_output(["ip", "route"])
    output = output.decode("utf-8")
    for line in output.splitlines():
        if "default" in line:
            default_route = line.split()
            return default_route[2]


def disable_interface(interface_name):
    """
    Disable the network interface with the specified name.

    Args:
    - interface_name (str): Name of the network interface to be disabled.
    """
    default_route = get_default_route()
    subprocess.run(["ip", "route", "del", "default", "via", default_route])
    subprocess.run(["ip", "link", "set", interface_name, "down"])


def get_subnet_mask(ip_address):
    """
    Returns the subnet mask for the given IP address.

    :param ip_address: str - the IP address to get the subnet mask for
    :return: str - a message containing the IP address and its subnet mask, or an error message
    """
    try:
        ip = ipaddress.ip_address(ip_address)
        if isinstance(ip, ipaddress.IPv4Address):
            # IPv4
            netmask = ipaddress.IPv4Network(ip_address).netmask
        else:
            # IPv6
            netmask = ipaddress.IPv6Network(ip_address).netmask
        return f"{netmask}"
    except ValueError:
        return "Invalid IP address"


def change_subnet_mask(interface_name: str, new_subnet_mask: str) -> bool:
    """
    Change the subnet mask of a network interface using the `ip addr` command.

    Args:
        interface_name: The name of the network interface to modify.
        new_subnet_mask: The new subnet mask in CIDR notation (e.g. '24').

    Returns:
        True if the subnet mask was successfully changed, False otherwise.
    """
    try:
        command = f"ip addr del {new_subnet_mask} dev {interface_name}"
        subprocess.run(command.split(), check=True)
        command = f"ip addr add {new_subnet_mask} dev {interface_name}"
        subprocess.run(command.split(), check=True)
    except subprocess.CalledProcessError as e:
        print(f"Error: {e}")
