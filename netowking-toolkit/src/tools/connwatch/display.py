import json
import re


def parse_tcpdump_line(line):
    """
    Parse a single line of tcpdump output and extract relevant fields.
    """
    # Skip header lines
    if "listening on" in line or len(line.strip()) == 0:
        return None

    # Extract IP addresses and ports
    ip_pattern = r"(\d+\.\d+\.\d+\.\d+)\.(\d+) > (\d+\.\d+\.\d+\.\d+)\.(\d+)"
    ip_match = re.search(ip_pattern, line)
    
    if not ip_match:
        return None

    # Extract flags
    flags_pattern = r"Flags \[([^\]]+)\]"
    flags_match = re.search(flags_pattern, line)
    
    # Extract length
    length_pattern = r"length (\d+)"
    length_match = re.search(length_pattern, line)

    if ip_match:
        return {
            "SourceIP": f"{ip_match.group(1)}:{ip_match.group(2)}",
            "TargetIP": f"{ip_match.group(3)}:{ip_match.group(4)}",
            "Type": flags_match.group(1) if flags_match else "Unknown",
            "Size": int(length_match.group(1)) if length_match else 0
        }
    return None