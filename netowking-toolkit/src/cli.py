import argparse
from utils.ascii_utils import print_logo
from tools import netinfo_tool, subnet_scan

def main_cli():
    print_logo()
    parser = argparse.ArgumentParser(description="Networking Toolkit CLI")
    subparsers = parser.add_subparsers(dest='command')

    # Add subcommands  --> Just examples now
    netinfo_parser = subparsers.add_parser('netinfo', help='Show basic network routing and firewall info')
    netinfo_parser.add_argument('--host', action='store_true', help='Include host system info (for WSL environments)')    ## handles --host flag
    
    subnet_parser = subparsers.add_parser('subnet-scan', help='Scan local subnet and list active hosts')

    args = parser.parse_args()

    
    # this is just a very basic draft, this will be revisited for sure
    if args.command == 'subnet-scan':
        subnet_scan.scan_subnet()
    elif args.command == 'netinfo':
        netinfo_tool.netinfo_summary(show_host_info=args.host)
    else:
        parser.print_help()
