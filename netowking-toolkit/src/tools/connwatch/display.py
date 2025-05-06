import json
import re


def parse_tcpdump_line(line):
    """
    Extract structured data from a tcpdump line.
    """
    # Sample line (customize if needed):
    # 12:34:56.789012 IP 192.168.1.10.12345 > 8.8.8.8.53: Flags [S], seq 123, win 29200, length 0
    regex = (
        r'^(?P<timestamp>\d{2}:\d{2}:\d{2}\.\d+)\s+'
        r'IP\s+(?P<src_ip>[\d.]+)\.(?P<src_port>\d+)\s+>\s+'
        r'(?P<dst_ip>[\d.]+)\.(?P<dst_port>\d+):\s+'
        r'(Flags\s+\[(?P<flags>[^\]]+)\],\s+)?'
        r'.*length\s+(?P<length>\d+)'
    )

    match = re.match(regex, line)
    if match:
        return {
            "Time": match.group("timestamp"),
            "Source": f"{match.group('src_ip')}:{match.group('src_port')}",
            "Destination": f"{match.group('dst_ip')}:{match.group('dst_port')}",
            "Flags": match.group("flags") or "-",
            "Length": match.group("length")
        }
    return None