import subprocess
import shutil
import json
from utils.formatting_utils import loading_spinner, print_error, print_cancel
from .display import parse_tcpdump_line

def inspect_connection(ip, port, mode="live", count=25):
    """
    Inspect packets for a given connection IP and port.

    mode: "live" or "snapshot"
    count: number of packets to show (for snapshot)
    """
    
    
    tcpdump_path = shutil.which("tcpdump")
    if tcpdump_path is None:
        print_error("[ERROR] tcpdump not found in PATH.")
        return

    cmd = [tcpdump_path, "-vvn","-l", "host", ip, "and", "port", str(port)]

    if mode == "snapshot":
        cmd.insert(1, "-c")
        cmd.insert(2, str(count))
    else:
        cmd.insert(1, "-l")
        
    cmd.insert(0, "sudo")

    print(f"\nInspecting connection to {ip}:{port} [{mode} mode]...\n\n")
    
    
    
    #### This has to be reworked visually!! And maybe some fields have to be added
    print("Source IP           Target IP           Type     Size")
    print("-" * 55)
    
    try:
        process = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        for line in process.stdout:
            parsed_data = parse_tcpdump_line(line)
            if parsed_data:
                print(f"{parsed_data['SourceIP']:<18} {parsed_data['TargetIP']:<18} {parsed_data['Type']:<8} {parsed_data['Size']}")
    except KeyboardInterrupt:
        print_cancel("\nLive capture stopped.")
    except Exception as e:
        print_error(f"[Error running tcpdump: {e}]")



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
