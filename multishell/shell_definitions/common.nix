{ pkgs }:

{
  networkingTools = with pkgs; [
    nmap tcpdump wireshark-cli iftop iperf3
    dig whois traceroute mtr inetutils iproute2
  ];

  systemDebugTools = with pkgs; [
    strace lsof btop dool atop sysstat procps
    gdb perf-tools trace-cmd kernelshark bcc bpftrace
    kmod systemd xfsprogs btrfs-progs inotify-tools
    e2fsprogs
    nettools
    psutils psmisc schedtool numactl
    inotify-tools fswatch
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
      rich        # for formatting
    ]))
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
      rich        # for formatting
    ]))
  ];

  commonTools = with pkgs; [ neovim git starship];
}
