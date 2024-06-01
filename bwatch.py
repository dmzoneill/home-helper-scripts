import curses
from scapy.all import sniff, ARP
import argparse
import socket
import time
from threading import Thread, Lock, Event
import subprocess

# Dictionary to store detected devices
devices = {}

devices_lock = Lock()  # To prevent race conditions

def handle_packet(packet):
    if packet.haslayer(ARP) and packet[ARP].op in (1, 2):  # who-has or is-at (request or response)
        ip_address = packet[ARP].psrc
        mac_address = packet[ARP].hwsrc
        try:
            device_name = socket.gethostbyaddr(ip_address)[0]
        except socket.herror:
            device_name = "Unknown"

        current_time = time.time()
        with devices_lock:
            if mac_address in devices:
                devices[mac_address]['last_seen'] = current_time
                devices[mac_address]['count'] += 1
            else:
                devices[mac_address] = {
                    'ip': ip_address, 'mac': mac_address, 'hostname': device_name, 
                    'last_seen': current_time, 'count': 1, 'ports': [], 'scanning': 'scanning'
                }
                # Start a thread to perform an aggressive port scan
                scan_thread = Thread(target=scan_ports, args=(mac_address,))
                scan_thread.start()

def remove_old_devices():
    current_time = time.time()
    with devices_lock:
        for mac in list(devices):
            if current_time - devices[mac]['last_seen'] > 300:  # 5 minutes
                del devices[mac]

def scan_ports(mac_address):
    with devices_lock:
        if devices[mac_address]['scanning'] == 'scanning':
            ip_address = devices[mac_address]['ip']
            hostname = devices[mac_address]['hostname']
            devices[mac_address]['scanning'] = time.time() + 1800  # 30 minutes from now

    output_file = f"{ip_address}-{hostname}.txt"
    with open(output_file, 'w') as f:
        # Run Nmap command and capture stdout and stderr
        nmap_process = subprocess.Popen(['nmap', '-A', '-oN', '-', ip_address], stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True)
        while True:
            output_line = nmap_process.stdout.readline()
            if not output_line:
                break  # End of output
            f.write(output_line)  # Write to file
            f.flush()  # Flush buffer to ensure real-time writing
            # You can also display the output in the console if needed
            # print(output_line, end='', flush=True)

            # Example: Parse output_line and update devices dictionary
            # if "/tcp" in output_line and "open" in output_line:
            #     port = output_line.split('/')[0]
            #     with devices_lock:
            #         devices[mac_address]['ports'].append(port)

    # Nmap scan complete, parse the output file and update devices dictionary as needed
    # Example: Parse the output file to extract open ports
    with open(output_file, 'r') as f:
        lines = f.readlines()
        ports = []
        for line in lines:
            if "/tcp" in line and "open" in line:
                port = line.split('/')[0]
                ports.append(port)

    with devices_lock:
        devices[mac_address]['ports'] = ports
        devices[mac_address]['scanning'] = time.time() + 1800  # 30 minutes from scan completion


def send_network_messages(stop_event):
    # Create a UDP socket
    udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    udp_socket.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)

    multicast_group = '224.1.1.1'
    multicast_port = 5000

    while not stop_event.is_set():
        # Send unicast message
        unicast_message = b"Hello from unicast"
        unicast_target = ('192.168.1.100', 5000)  # Example unicast target
        udp_socket.sendto(unicast_message, unicast_target)

        # Send broadcast message
        broadcast_message = b"Hello from broadcast"
        broadcast_target = ('<broadcast>', 5000)
        udp_socket.sendto(broadcast_message, broadcast_target)

        # Send multicast message
        multicast_message = b"Hello from multicast"
        udp_socket.sendto(multicast_message, (multicast_group, multicast_port))

        time.sleep(1)  # Send messages every second

    # Close the socket when done
    udp_socket.close()

def display_devices(stdscr):
    curses.curs_set(0)  # Hide cursor
    stdscr.nodelay(1)   # Don't block on getch()
    while True:
        stdscr.clear()
        stdscr.addstr(0, 0, "Detected Devices")
        stdscr.addstr(1, 0, "-" * 80)
        stdscr.addstr(2, 0, "{:<15} {:<18} {:<25} {:<10} {:<15}".format("IP", "MAC", "Hostname", "Count", "Open Ports"))
        stdscr.addstr(3, 0, "-" * 80)
        row = 4
        current_time = time.time()
        with devices_lock:
            for device in devices.values():
                ports = ', '.join(device['ports'])
                scanning_status = device['scanning']
                if isinstance(scanning_status, float) and current_time > scanning_status:
                    device['scanning'] = 'scanning'
                stdscr.addstr(row, 0, "{:<15} {:<18} {:<25} {:<10} {:<15}".format(device['ip'], device['mac'], device['hostname'], str(device['count']), ports))
                row += 1
        stdscr.refresh()
        time.sleep(1)
        remove_old_devices()
        if stdscr.getch() == ord('q'):  # Press 'q' to exit
            break

def sniff_network(interface):
    sniff(iface=interface, filter="arp", prn=handle_packet, store=0)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Listen for broadcast traffic on a network interface.")
    parser.add_argument("interface", help="The network interface to listen on (e.g., eth0, wlan0)")
    args = parser.parse_args()

    # Create a stop event for threads
    stop_event = Event()

    # Start the send_network_messages thread
    network_messages_thread = Thread(target=send_network_messages, args=(stop_event,))
    network_messages_thread.daemon = True
    network_messages_thread.start()

    # Start sniffing in a separate thread
    sniff_thread = Thread(target=sniff_network, args=(args.interface,))
    sniff_thread.daemon = True
    sniff_thread.start()

    # Start the curses interface
    curses.wrapper(display_devices)

    # Set the stop event when the curses interface exits
    stop_event.set()

    # Wait for all threads to exit
    network_messages_thread.join()
    sniff_thread.join()

