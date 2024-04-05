import threading
import netifaces as ni
import platform
import socket
from tkinter import messagebox
import re


def team_number_generator():
    team_num = 1
    while True:
        yield team_num
        team_num += 1


class UDP_Server:
    def __init__(self, server_port, server_ip="AUTO", net_mode='INET'):
        self.clients = {}
        self.new_client = False
        self.team_num_gen = team_number_generator()

        # UDP Socket variables
        self.server_port = server_port
        self.socket_run_flag = False

        if server_ip == "AUTO":
            # If server_ip is None then it tries to get the server IP automatically
            self.server_ip = self.getIPv4Address(net_mode)
        else:
            self.server_ip = server_ip
        
        if self.is_valid_ip(str(self.server_ip)):
            # Creates UDP socket
            self.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            self.socket.bind((self.server_ip, self.server_port))
            print(f"Server binded to ({self.server_ip, self.server_port})")
            self.socket_run_flag = True
    
            # Starts thread to receive message from clients
            receive_thread = threading.Thread(target=self.receive_message)
            receive_thread.start()
            print("Started receiving thread")
        

    def getIPv4Address(self, net_mode):
        system = platform.system()
        # print(system)
        if system == 'Windows':
            if net_mode.upper() == 'INET':
                # Get the IPv4 address for the default gateway interface
                gws = ni.gateways()
                default_interface = gws['default'][ni.AF_INET][1]
                addresses = ni.ifaddresses(default_interface)
                server_ip = addresses[ni.AF_INET][0]['addr']
                return server_ip
            elif net_mode.upper() == 'ETH':
                # Get the IPv4 address for the Ethernet interface if available
                interfaces = ni.interfaces()
                for interface in interfaces:
                    if interface.lower().startswith('eth'):
                        addresses = ni.ifaddresses(interface)
                        if ni.AF_INET in addresses:
                            server_ip = addresses[ni.AF_INET][0]['addr']
                            return server_ip
                else:  # End of loop
                    messagebox.askokcancel("Attention","Couldn't find IPv4 address. Try setting the IP manually when constructing the object or another network mode (ETH or INET).")
                raise Exception(
                    "Couldn't find IPv4 address. Try setting the IP manually when constructing the object or another network mode (ETH or INET).")
            else:
                messagebox.askokcancel("Attention","Error: Network mode not valid. Supported modes are INET or ETH.")
                raise Exception("Error: Network mode not valid. Supported modes are INET or ETH.")
        elif system == 'Linux':
            if net_mode.upper() == 'INET':
                # Get the IPv4 address for the default gateway interface
                interfaces = ni.interfaces()
                for interface in interfaces:
                    if interface != 'lo':
                        addresses = ni.ifaddresses(interface)
                        if ni.AF_INET in addresses:
                            server_ip = addresses[ni.AF_INET][0]['addr']
                            return server_ip
                else:  # End of loop
                    messagebox.askokcancel("Attention","Couldn't find IPv4 address. Try setting the IP manually when constructing the object or another network mode (ETH or INET).")
                    raise Exception( "Couldn't find IPv4 address. Try setting the IP manually when constructing the object or another network mode (ETH or INET).")
            elif net_mode.upper() == 'ETH':
                # Get the IPv4 address for the Ethernet interface if available
                interfaces = ni.interfaces()
                for interface in interfaces:
                    if interface.lower().startswith('eth'):
                        addresses = ni.ifaddresses(interface)
                        if ni.AF_INET in addresses:
                            server_ip = addresses[ni.AF_INET][0]['addr']
                            return server_ip
                else:  # End of loop
                    messagebox.askokcancel("Attention","Couldn't find IPv4 address. Try setting the IP manually when constructing the object or another network mode (ETH or INET).")
                    raise Exception(
                        "Couldn't find IPv4 address. Try setting the IP manually when constructing the object or "
                        "another network mode (ETH or INET).")
            else:
                messagebox.askokcancel("Attention","Error: Network mode not valid. Supported modes are INET or ETH.")
                raise Exception("Error: Network mode not valid. Supported modes are INET or ETH.")
        else:
            messagebox.askokcancel(f"Unsupported operating system: {system}")
            raise OSError(f"Unsupported operating system: {system}")

    def is_valid_ip(self, address):
        # Rgular expression pattern for IP address
        self.pattern = r'^(\d{1,3}\.){3}\d{1,3}$'
        if re.match(self.pattern, address):
            return True
        else:
            return False
        
    def handle_message(self, message, address):
        if message.count("#") == 3:
            message = message.split("#")[1:-1]
            ip_address = address[0]

            if ip_address not in self.clients:
                self.clients[ip_address] = {'etape': message[1], 'time': message[0],
                                            'team_num': next(self.team_num_gen), 'address': address}
                self.new_client = True
            else:
                self.clients[ip_address]['etape'] = message[1]
                self.clients[ip_address]['time'] = message[0]

    def send_message(self, message, ip_address):
        print(f"Sending message {message} to {self.clients[ip_address]['address']}")
        self.socket.sendto(message.encode(), self.clients[ip_address]['address'])

    def receive_message(self):
        while self.socket_run_flag:
            try:
                # Receive data from a client
                data, address = self.socket.recvfrom(1024)

                # Creates a new thread to handle the message
                handle_thread = threading.Thread(target=self.handle_message, args=(data.decode(), address))
                handle_thread.start()
            except:
                pass
