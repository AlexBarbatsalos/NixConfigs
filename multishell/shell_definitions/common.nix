{ pkgs }:

{
  networkingTools = with pkgs; [
    nmap tcpdump wireshark-cli iftop iperf3
    dig whois traceroute mtr
  ];

  systemDebugTools = with pkgs; [
    strace lsof btop dstat atop sysstat procps
    gdb perf
  ];
}
