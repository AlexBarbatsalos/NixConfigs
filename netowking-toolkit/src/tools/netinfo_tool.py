import subprocess
import os
import json
from utils.formatting_utils import print_colored_title, print_table, print_error

# Helper functions --> could be a separate module later!!
## checks if system is wsl (just as placeholder for now)
def is_wsl():
    return "WSL_INTEROP" in os.environ or "WSLENV" in os.environ

## later for hypervisors
def is_vm():
    return True



## actual functions for netinfo


def get_routing_table():
    try:
        result = subprocess.run(["ip", "-j", "route", "show"], capture_output=True, text=True, check=True)
        routes = json.loads(result.stdout)
    except Exception as e:
        return f"[Failed to retrieve routing table: {e}]"

    def classify(entry):
        if entry.get("dst") == "default":
            return "default"
        elif entry.get("scope") == "link":
            return "subnet"
        else:
            return "other"

    def format_route(entry):
        return {
            "dst": entry.get("dst", "-"),
            "gateway": entry.get("gateway", "-"),
            "dev": entry.get("dev", "-"),
            "src": entry.get("prefsrc", "-"),
            "scope": entry.get("scope", "-"),
            "proto": entry.get("protocol", "-")
        }

    groups = {
        "default": [],
        "subnet": [],
        "other": []
    }

    for route in routes:
        route_type = classify(route)
        groups[route_type].append(format_route(route))

    def print_group(title, entries):
        print(f"\n[{title}]")
        print(f"{'Destination':<18} {'Gateway':<18} {'Interface':<10} {'Source IP':<18} {'Scope':<8} {'Proto'}")
        print("-" * 85)
        for entry in entries:
            print(f"{entry['dst']:<18} {entry['gateway']:<18} {entry['dev']:<10} {entry['src']:<18} {entry['scope']:<8} {entry['proto']}")

    output_lines = ["Routing Table", "="*30]

    if groups["default"]:
        print_group("Default Route", groups["default"])
    if groups["subnet"]:
        print_group("Subnet Routes", groups["subnet"])
    if groups["other"]:
        print_group("Additional Routes", groups["other"])

    return ""




def get_interfaces():
    try:
        result = subprocess.run(["ip", "-j", "addr", "show"], capture_output=True, text=True, check=True)
        interfaces = json.loads(result.stdout)

        lines = []
        for iface in interfaces:
            name = iface["ifname"]
            # default to none, then override if an IP is found
            ip_address = "<none>"
            for addr in iface.get("addr_info", []):
                if addr.get("family") == "inet":
                    ip_address = addr.get("local")
                    break
            lines.append(f"{name:<10}: {ip_address}")
        
        return "\n".join(lines)

    except Exception as e:
        return f"[Failed to retrieve interface list: {e}]"
    
    
def get_open_ports():
    try:
        result = subprocess.run(["ss", "-tuln"], capture_output=True, text=True, check=True)
        lines = result.stdout.strip().split("\n")
        if len(lines) <= 1:
            return "[No open ports found]"

        output = ["Proto  Local Address       Port"]
        output.append("-" * 35)

        for line in lines[1:]:  # skip header
            parts = line.split()
            proto = parts[0]
            local_addr = parts[4]  # e.g., 0.0.0.0:22
            if ":" in local_addr:
                addr, port = local_addr.rsplit(":", 1)
            else:
                addr, port = local_addr, "?"

            output.append(f"{proto:<6} {addr:<18} {port}")

        return "\n".join(output)

    except Exception as e:
        return f"[Failed to get open ports: {e}]"




def get_firewall_rules():
    
    # if --host flag is set, query host system instead.
    if is_wsl():
        try:
            cmd = [
                "powershell.exe",
                "-Command",
                "[Console]::OutputEncoding = [System.Text.Encoding]::UTF8; " +
                "Get-NetFirewallRule | Where { $_.Enabled -eq 'True' } | " +
                "Group-Object -Property Direction | Sort-Object Count -Descending | " +
                "Select-Object Name,Count | Format-Table -AutoSize"
            ]

            result = subprocess.run(cmd, capture_output=True, text=True, encoding="latin-1")
            return result.stdout.replace('\r\n', '\n').strip()
        
        except Exception as e:
            return f"[Error querying Windows firewall: {e}]"
        
        
    try:
        result = subprocess.run(["iptables", "-L"], capture_output=True, text=True)
        return result.stdout.strip()
    except FileNotFoundError:
        return "[iptables not found — skipping firewall rules]"
    
    


def get_windows_routes():
    try:
        cmd = [
            "powershell.exe",
            "-Command",
            "[Console]::OutputEncoding = [System.Text.Encoding]::UTF8; " +
            "Get-NetRoute | Sort-Object DestinationPrefix | " +
            "Format-Table -Property DestinationPrefix,NextHop,InterfaceAlias,RouteMetric -AutoSize"
        ]
        result = subprocess.run(cmd, capture_output=True)
        try:
            output = result.stdout.decode('utf-8')
        except UnicodeDecodeError:
            output = result.stdout.decode('latin-1')
        return output.replace('\r\n', '\n').strip()
    except Exception as e:
        return f"[Error fetching Windows routes: {e}]"

def netinfo_summary(show_host_info=False):
    print_colored_title("Network Information Snapshot")
    print("="*40)

    print_colored_title("\nRouting Table:")
    print("-"*30)
    get_routing_table()

    print_colored_title("\n\nInterfaces:")
    print("-"*30)
    print(get_interfaces())
    
    print_colored_title("\n\nOpen Ports:")
    print("-"*30)
    print(get_open_ports())

    print_colored_title("\n\n Firewall Rules:")
    print("-"*30)
    print(get_firewall_rules())
    
    
    ## checks for --host flag
    
    if show_host_info:
        if not is_wsl():
            print("\n[--host ignored — not in WSL]")
        else:
            print("\n🪟 Windows Host Firewall Summary")
            print("=" * 60)
            print(get_firewall_rules())

            print_colored_title("\n🗺 Windows Routing Table")
            print("=" * 60)
            print(get_windows_routes())
            
