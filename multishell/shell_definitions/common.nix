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

  commonTools = with pkgs; [ neovim git starship];
}
