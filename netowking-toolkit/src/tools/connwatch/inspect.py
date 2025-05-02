import subprocess
import shutil

def inspect_connection(ip, port, mode="live", count=25):
    """
    Inspect packets for a given connection IP and port.

    mode: "live" or "snapshot"
    count: number of packets to show (for snapshot)
    """
    print(f"\nInspecting connection to {ip}:{port} [{mode} mode]")
    
    tcpdump_path = shutil.which("tcpdump")
    if tcpdump_path is None:
        print("[ERROR] tcpdump not found in PATH.")
        return

    cmd = [tcpdump_path, "-n", "host", ip, "and", "port", str(port)]

    if mode == "snapshot":
        cmd.insert(1, "-c")
        cmd.insert(2, str(count))
    else:
        cmd.insert(1, "-l")
        
    cmd.insert(0, "sudo")

    print(f"\n[Running command: {' '.join(cmd)}]\n")
    try:
        subprocess.run(cmd)
    except KeyboardInterrupt:
        print("\nLive capture stopped.")
    except Exception as e:
        print(f"[Error running tcpdump: {e}]")



def trace_connection(ip):
    """
    Trace route to a remote IP using traceroute.
    """
    print(f"\nTracing route to {ip}")
    
    traceroute_path = shutil.which("traceroute")
    if traceroute_path is None:
        print("[ERROR] traceroute not found in PATH.")
        return

    cmd = ["sudo", traceroute_path, "-n", ip]

    print(f"\n[Running command: {' '.join(cmd)}]\n")
    try:
        subprocess.run(cmd)
    except KeyboardInterrupt:
        print("\nTrace stopped.")
    except Exception as e:
        print(f"[Error running traceroute: {e}]")
        

def inspect_certificate(ip, port):
    """
    Inspect TLS certificate chain for a given IP and port using openssl.
    """
    print(f"\n\U0001F511 Inspecting TLS certificate chain for {ip}:{port}\n")

    cmd = ["openssl", "s_client", "-connect", f"{ip}:{port}", "-servername", ip, "-showcerts"]
    try:
        subprocess.run(cmd)
    except KeyboardInterrupt:
        print("\nCertificate inspection cancelled.")
    except Exception as e:
        print(f"[Error running openssl: {e}")
