from .connections import get_active_connections
from .inspect import inspect_connection, trace_connection, inspect_certificate
from utils.formatting_utils import print_colored_title, print_table, print_error




from .connections import get_active_connections
from .inspect import inspect_connection, inspect_certificate

def main():
    connections = get_active_connections()
    if isinstance(connections, str):
        print(connections)
        return

    print_colored_title(" Active WAN Connections")
    print("=" * 80)
    print(f"{'ID':<3} {'Proto':<6} {'Local Address':<22} {'Remote Address':<22} {'PID':<6} {'Program'}")
    print("-" * 80)
    for idx, conn in enumerate(connections, start=1):
        print(f"{idx:<3} {conn['proto']:<6} {conn['local']:<22} {conn['remote']:<22} {conn['pid']:<6} {conn['program']}")

    print("""
Options:
 - 'inspect'  : Inspect packets (live/snapshot)
 - 'certs'    : Show TLS certificate chain
 - 'trace'    : (Coming soon) Trace route
""")

    try:
        raw_input = input("\nEnter connection ID and mode (e.g., '1 inspect'): ").strip()
        if not raw_input:
            print("Exiting.")
            return
        parts = raw_input.split()
        if len(parts) != 2:
            print_error("Invalid input format. Use: <ID> <mode>")
            return

        selection = int(parts[0])
        if not (1 <= selection <= len(connections)):
            print_error("Invalid ID.")
            return

        action = parts[1].lower()
        selected = connections[selection - 1]
        remote_ip, remote_port = selected["remote"].rsplit(":", 1)

        if action == "inspect":
            mode = input("Choose packet inspection mode — [l]ive / [s]napshot (default: snapshot): ").strip().lower()
            mode = "live" if mode == "l" else "snapshot"
            inspect_connection(remote_ip, remote_port, mode=mode)

        elif action == "certs":
            inspect_certificate(remote_ip, remote_port)

        elif action == "trace":
            trace_connection(remote_ip)

        else:
            print_error(f"Unknown mode '{action}'.")

    except Exception as e:
        print_error(f"[Error] {e}")
    
    