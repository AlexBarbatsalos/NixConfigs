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

  commonTools = with pkgs; [ neovim git starship];
}
