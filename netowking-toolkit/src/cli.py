import argparse
from tools import nmap_tool, traceroute_tool, whois_tool
from utils.ascii_utils import print_logo

def main_cli():
    print_logo()
    parser = argparse.ArgumentParser(description="Networking Toolkit CLI")
    subparsers = parser.add_subparsers(dest='command')

    # Add subcommands  --> Just examples now
    nmap_parser = subparsers.add_parser('nmap', help='Scan with Nmap')
    nmap_parser.add_argument('target', help='Target IP or hostname')

    traceroute_parser = subparsers.add_parser('traceroute', help='Traceroute a target')
    traceroute_parser.add_argument('target', help='Target IP or hostname')

    whois_parser = subparsers.add_parser('whois', help='WHOIS lookup')
    whois_parser.add_argument('domain', help='Domain name to query')

    args = parser.parse_args()

    
    # this is just a very basic draft, this will be revisited for sure
    if args.command == 'nmap':
        nmap_tool.scan(args.target)
    elif args.command == 'traceroute':
        traceroute_tool.trace(args.target)
    elif args.command == 'whois':
        whois_tool.lookup(args.domain)
    else:
        parser.print_help()
