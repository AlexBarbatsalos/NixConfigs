import subprocess
import re

def get_active_connections():
    try:
        result = subprocess.run(["ss", "-tupn"], capture_output=True, text=True, check=True)
        lines = result.stdout.strip().splitlines()
        connections = []

        for line in lines[1:]:  # Skip header
            parts = re.split(r"\s+", line)
            if len(parts) < 6:
                continue

            proto = parts[0]
            local = parts[4]
            remote = parts[5]
            pid_info = parts[6] if len(parts) > 6 else "-"

            pid, program = "-", "-"
            if pid_info.startswith("users:"):
                match = re.search(r'users:\(\("([^"]+)",pid=(\d+),', pid_info)
                if match:
                    program = match.group(1)
                    pid = match.group(2)

            # Filter out local-only/loopback
            if remote.startswith("127.") or remote.startswith("[::1]") or remote.startswith("::1"):
                continue

            connections.append({
                "proto": proto,
                "local": local,
                "remote": remote,
                "pid": pid,
                "program": program
            })

        return connections
    except Exception as e:
        return f"[Error fetching connections: {e}]"