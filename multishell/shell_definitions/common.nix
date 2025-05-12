{ pkgs }:

{
  networkingTools = with pkgs; [
    nmap tcpdump wireshark-cli iftop iperf3
    dig whois traceroute mtr inetutils iproute2
  ];

  systemDebugTools = with pkgs; [
    strace lsof btop dool atop sysstat procps
    gdb perf trace-cmd kernelshark bcc bpftrace
    dmesg kmod systemd systemd-analyze systemd-cgtop
    debugfs xfsprogs btrfs-progs inotify-tools
    journalctl loginctl systemctl udevadm
    nettools psutils psmisc schedtool numactl
    inotify-tools fswatch
  ];

  commonTools = with pkgs; [ neovim git starship];
}
