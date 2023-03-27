from flask import Flask, jsonify
from utils.network_utils import get_ipv4_address, get_subnet_mask
from flask_basicauth import BasicAuth

import subprocess
import ipaddress
# import netifaces

app = Flask(__name__)

app.config["BASIC_AUTH_USERNAME"] = "admin"
app.config["BASIC_AUTH_PASSWORD"] = "password"
app.config["BASIC_AUTH_FORCE"] = True
basic_auth = BasicAuth(app)


@app.route("/")
def index():
    ipv4_address = get_ipv4_address()
    return f"My IPv4 address is: {ipv4_address}. The subnet mask is: {get_subnet_mask(ipv4_address)}"

# @app.route("/change_subnet_mask/<string:ip_address>/<string:new_mask>")
# def change_subnet_mask(ip_address, new_mask):
#     """
#     Changes the subnet mask for the network interface associated with the given IP address.

#     :param ip_address: str - the IP address to change the subnet mask for
#     :param new_mask: str - the new subnet mask to set, in CIDR notation (e.g. "24" for a /24 mask)
#     :return: str - a message indicating whether the subnet mask was successfully changed, or an error message
#     """
#     try:
#         interface_name = netifaces.interfaces()[0]  # Assumes the first interface
#         current_netmask = netifaces.ifaddresses(interface_name)[netifaces.AF_INET][0][
#             "netmask"
#         ]

#         ip = ipaddress.ip_address(ip_address)
#         new_subnet = ipaddress.ip_network(f"{ip_address}/{new_mask}", strict=False)

#         netifaces.ifaddresses(interface_name)[netifaces.AF_INET][0]["netmask"] = str(
#             new_subnet.netmask
#         )

#         # Return success message
#         return f"Subnet mask for {ip_address} changed from {current_netmask} to {new_subnet.netmask}"
#     except (ValueError, IndexError):
#         return "Invalid IP address or subnet mask"


@app.route("/admin")
@basic_auth.required
def admin():
    return "Hello Admin!"


if __name__ == "__main__":
    app.run()
