import subprocess
import shutil
import os
import json
from utils.formatting_utils import loading_spinner, print_error, print_cancel
from .display import parse_tcpdump_line



### helpers

def get_default_interface():
    import re
    try:
        result = subprocess.run(["ip", "route", "get", "8.8.8.8"], capture_output=True, text=True)
        match = re.search(r'dev (\w+)', result.stdout)
        return match.group(1) if match else None
    except Exception:
        return None
    
    

### actual utilities

def inspect_connection(ip, port, mode="live", count=25):
    """
    Inspect packets for a given connection IP and port.

    mode: "live" or "snapshot"
    count: number of packets to show (for snapshot)
    """
    
    
    tcpdump_path = shutil.which("tcpdump")
    print(f"[DEBUG] tcpdump_path: {tcpdump_path}")                          ###debug
    if not tcpdump_path:
        print_error("[ERROR] tcpdump not found.")
        return

    
    iface = get_default_interface()
    if not iface:
        print_error("[ERROR] Could not determine network interface.")
        return
    
    cmd = ["sudo", tcpdump_path]

    if mode == "snapshot":
        cmd += ["-c", str(count)]

    cmd += [
        "-i", iface,                                                 
        "-n", "-l", "-tttt",
        "host", ip, 
        "and", "port", str(port)                        
]

   

    print(f"\nInspecting connection to {ip}:{port} [{mode} mode]\n")
    print(f"{'Time':<15} {'Source':<21} {'Destination':<21} {'Flags':<10} {'Len'}")
    print("-" * 75)

    try:
        print("[DEBUG] Final command:", " ".join(cmd))
        print(f"[DEBUG] tcpdump_path: {tcpdump_path}")
        process = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        stdout, stderr = process.communicate()                                                              ####debug start

        print("[DEBUG] STDERR:")
        print(stderr)

        print("[DEBUG] STDOUT:")
        print(stdout)                                                                                       ####### debug end
        
        for line in process.stdout:
            parsed = parse_tcpdump_line(line)
            if parsed:
                print(f"{parsed['Time']:<15} {parsed['Source']:<21} {parsed['Destination']:<21} {parsed['Flags']:<10} {parsed['Length']}")
    except KeyboardInterrupt:
        print("\nCapture Stopped.")
    except Exception as e:
        print_error(f"[ERROR] {e}")


def trace_connection(ip):
    """
    Trace route to a remote IP using traceroute.
    """
    print(f"\nTracing route to {ip}")
    
    traceroute_path = shutil.which("traceroute")
    if traceroute_path is None:
        print_error("[ERROR] traceroute not found in PATH.")
        return

    cmd = ["sudo", traceroute_path, "-n", ip]

    print(f"\n[Running command: {' '.join(cmd)}]\n")
    try:
        subprocess.run(cmd)
    except KeyboardInterrupt:
        print_cancel("\nTrace stopped.")
    except Exception as e:
        print_error(f"[Error running traceroute: {e}]")
        

def inspect_certificate(ip, port):
    """
    Inspect TLS certificate chain for a given IP and port using openssl.
    """
    print(f"Inspecting TLS certificate chain for {ip}:{port}\n")

    cmd = ["openssl", "s_client", "-connect", f"{ip}:{port}", "-servername", ip, "-showcerts"]
    try:
        subprocess.run(cmd)
    except KeyboardInterrupt:
        print_cancel("\nCertificate inspection cancelled.")
    except Exception as e:
        print_error(f"[Error running openssl: {e}")
