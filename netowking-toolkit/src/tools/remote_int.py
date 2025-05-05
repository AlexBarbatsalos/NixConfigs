import subprocess
import socket
import ipaddress
import requests
import re
from utils.formatting_utils import print_colored_title, print_error, print_summary_row






### helper functions

def parse_whois(whois_text):
    lines = whois_text.splitlines()
    relevant = {}
    for line in lines:
        for key in ("CIDR", "NetName", "NetHandle", "NetType"):
            if line.startswith(key + ":"):
                relevant[key] = line.split(":", 1)[1].strip()
    return "\n".join(f"{k}: {v}" for k, v in relevant.items()) if relevant else "[WHOIS fields not found]"

def parse_ping(ping_text):
    match = re.search(r"min/avg/max/(?:mdev|stddev) = ([\d.]+)/([\d.]+)/", ping_text)
    if match:
        return f"Average latency: {match.group(2)} ms"
    return "[Could not extract average ping]"


def parse_traceroute(trace_text):
    lines = [line for line in trace_text.splitlines() if re.match(r"\s*\d+\s", line)]
    hops = len(lines)
    last_line = lines[-1] if lines else ""
    times = re.findall(r"(\d+\.\d+)\s*ms", last_line)
    last_rtt = times[-1] if times else "-"
    return f"Hops: {hops}, Final hop RTT: {last_rtt} ms"

def run_cmd(cmd, sudo=False):
    full_cmd = (["sudo"] + cmd) if sudo else cmd
    try:
        return subprocess.run(full_cmd, capture_output=True, text=True, check=True).stdout.strip()
    except subprocess.CalledProcessError:
        return "[Command failed]"




## actual utilities


def reverse_dns(ip):
    try:
        return socket.gethostbyaddr(ip)[0]
    except socket.herror:
        return "[No PTR record]"

def whois_lookup(ip):
    return run_cmd(["whois", ip])

def geoip_lookup(ip):
    try:
        resp = requests.get(f"https://ipinfo.io/{ip}/json", timeout=3)
        if resp.status_code == 200:
            data = resp.json()
            return {
                "City": data.get("city", "-"),
                "Region": data.get("region", "-"),
                "Country": data.get("country", "-"),
                "ASN": data.get("org", "-"),
                "ISP": data.get("org", "-"),
            }
        else:
            return {"Error": f"HTTP {resp.status_code}"}
    except Exception as e:
        return {"Error": str(e)}

def dns_trace(domain):
    print(f"\n[DEBUG] dns_trace() called with domain: {repr(domain)}")
    if not domain or domain.startswith("[No PTR"):
        return "[Invalid domain for DNS trace]"

    def parse_relevant_records(output):
        relevant = []
        for line in output.splitlines():
            if re.match(r"^[^;].*\sIN\s(A|AAAA|CNAME|NS)\s", line):
                relevant.append(line)
        return "\n".join(relevant) if relevant else "[No relevant DNS records found]"

    try:
        result = subprocess.run(["dig", "+trace", domain], capture_output=True, text=True, check=True)
        return parse_relevant_records(result.stdout)
    except subprocess.CalledProcessError as e:
        print("[DEBUG] dig +trace failed — trying fallback @8.8.8.8")
        try:
            fallback = subprocess.run(["dig", domain, "@8.8.8.8"], capture_output=True, text=True, check=True)
            return "[Fallback DNS resolution]\n" + parse_relevant_records(fallback.stdout)
        except Exception as e2:
            return f"[Both DNS trace and fallback failed: {e2}]"



def ping_host(ip):
    return run_cmd(["ping", "-c", "4", ip], sudo=True)

def traceroute(ip):
    return run_cmd(["traceroute", ip])



def tls_info(ip, domain, port=443):
    print(f"\n[DEBUG] tls_info() called with ip={ip}, domain={repr(domain)}, port={port}")
    
    try:
        cmd = [
            "openssl", "s_client",
            "-connect", f"{ip}:{port}",
            "-servername", domain,
            "-showcerts"
        ]
        print(f"[DEBUG] Running: {' '.join(cmd)}")

        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            input="",  # prevents hang
            timeout=10
        )

        # Extract first certificate block
        cert = []
        in_cert = False
        for line in result.stdout.splitlines():
            if "BEGIN CERTIFICATE" in line:
                in_cert = True
            if in_cert:
                cert.append(line)
            if "END CERTIFICATE" in line:
                break

        if not cert:
            return "[No certificate block found]"

        # Pipe cert into openssl x509 for summary
        cert_input = "\n".join(cert)
        x509_proc = subprocess.run(
            ["openssl", "x509", "-noout", "-subject", "-issuer", "-dates"],
            input=cert_input,
            capture_output=True,
            text=True
        )

        return x509_proc.stdout.strip()

    except subprocess.TimeoutExpired:
        return "[TLS connection timed out]"
    except Exception as e:
        return f"[TLS error: {e}]"






### This function calls and collects output of all the functions in this script
def remote_int(ip):
    print_summary_row(f"IP Address:", ip)
    reverse = reverse_dns(ip)
    print_summary_row(f"Reverse DNS:", reverse)

    if not ipaddress.ip_address(ip).is_private:
        geo = geoip_lookup(ip)
        print_summary_row("GeoIP:", f"{geo.get('Country')}, {geo.get('Region')}, {geo.get('City')}")

        print_colored_title("\nWHOIS:")
        print(parse_whois(whois_lookup(ip)))

        print_colored_title("\nPing:")
        print(parse_ping(ping_host(ip)))

        print_colored_title("\nTraceroute:")
        print(parse_traceroute(traceroute(ip)))

        if reverse != "[No PTR record]":
            print_colored_title("\nDNS Trace:")
            print(dns_trace(reverse))

            print_colored_title("\nTLS Certificate:")
            print(tls_info(ip, reverse))
    else:
        print_error("[Private IP address — skipping GeoIP/WHOIS/DNS/TLS]")
