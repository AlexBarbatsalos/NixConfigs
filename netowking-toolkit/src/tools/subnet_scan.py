import subprocess
import json
import re
import socket
from utils.formatting_utils import print_colored_title, print_table, print_error, loading_spinner




COMMON_PORTS = {
    22: "SSH", 80: "HTTP", 443: "HTTPS", 3389: "RDP", 139: "NetBIOS",
    445: "SMB", 21: "FTP", 23: "Telnet", 25: "SMTP", 53: "DNS", 3306: "MySQL"
}

def get_local_subnet():
    try:
        result = subprocess.run(["ip", "-j", "route"], capture_output=True, text=True, check=True)
        routes = json.loads(result.stdout)
        for route in routes:
            if route.get("dst") != "default" and route.get("scope") == "link":
                return route["dst"]
        return None
    except Exception as e:
        print_error(f"[Error determining local subnet: {e}]")
        return None



def scan_ports(ip, ports=COMMON_PORTS):
    open_ports = []
    for port in ports:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            sock.settimeout(0.5)  # fast scan, adjust as needed
            try:
                sock.connect((ip, port))
                open_ports.append(port)
            except:
                continue
    return open_ports




def parse_nmap_output(output):
    hosts = []
    current_host = {}

    for line in output.splitlines():
        if line.startswith("Nmap scan report for"):
            if current_host:
                hosts.append(current_host)
                current_host = {}
            match = re.match(r"Nmap scan report for (.+?)( \((.+)\))?$", line)
            if match:
                hostname = match.group(1)
                ip = match.group(3) or hostname
                current_host["IP"] = ip
                current_host["Hostname"] = hostname if hostname != ip else "-"
        elif "MAC Address:" in line:
            parts = line.split("MAC Address:")[1].strip().split(" ", 1)
            current_host["MAC"] = parts[0]
            current_host["Vendor"] = parts[1].strip("()") if len(parts) > 1 else "-"
    if current_host:
        hosts.append(current_host)

    return hosts

def scan_subnet():
    subnet = get_local_subnet()
    if not subnet:
        print_error("[Could not detect local subnet]")
        return

    with loading_spinner(f"Scanning subnet: {subnet}"):
        result = subprocess.run(["nmap", "-sn", subnet], capture_output=True, text=True, check=True)
    try:
        result = subprocess.run(["nmap", "-sn", subnet], capture_output=True, text=True, check=True)
    except Exception as e:
        print_error(f"[Error running nmap: {e}]")
        return

    hosts = parse_nmap_output(result.stdout)

    if not hosts:
        print_error("No active hosts found.")
        return

    print_colored_title("\nSubnet Scan Results")
    print("=" * 80)
    print(f"{'IP':<16} {'MAC':<20} {'Vendor':<18} {'Hostname':<20} Open Ports")
    print("-" * 80)
    for host in hosts:
        ip = host.get("IP", "-")
        ports = scan_ports(ip)
        port_list = ", ".join(str(p) for p in ports) if ports else "-"
        print(f"{ip:<16} {host.get('MAC', '-'): <20} {host.get('Vendor', '-'): <18} {host.get('Hostname', '-'): <20} {port_list}")
