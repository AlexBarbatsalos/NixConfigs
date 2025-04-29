{ pkgs }:

{
  networkingTools = with pkgs; [
    nmap tcpdump wireshark-cli iftop iperf3
    dig whois traceroute mtr inetutils iproute2
  ];

  systemDebugTools = with pkgs; [
    strace lsof btop dool atop sysstat procps
    gdb
  ];


  pythonNetTools = with pkgs; [
    (python3.withPackages (ps: with ps; [
      requests    # HTTP client
      scapy       # Packet crafting/sniffing
      dnspython   # DNS queries
      paramiko    # SSH connections
      netaddr     # IP address manipulation
      websockets  # Async WebSocket client/server
      pyshark     # Wireshark wrapper for packet captures
    ]))
  ];

  commonTools = with pkgs; [ neovim git starship];
}
