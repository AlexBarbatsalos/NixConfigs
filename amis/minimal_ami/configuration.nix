{ config, pkgs, lib, diskSize, ... }:


let
  envFile = builtins.readFile ./.env;                 ### set up your own .env file locally or use environment variables directly
  envVars = builtins.listToAttrs (map (line:
    let parts = builtins.match "([^=]+)=(.*)" line;
    in {
      name = builtins.elemAt parts 0;
      value = builtins.elemAt parts 1;
    }) (lib.splitString "\n" envFile));
in

{ 


  ### Base
  nixpkgs.hostPlatform = "x86_64-linux";
  virtualisation.diskSize = 4096;

  boot.loader.grub.device = "/dev/xvda";

  fileSystems."/" = {
    device = "/dev/xvda1";
    fsType = "ext4";
  };



  ### Networking Config
  networking.hostName = "nixos-ami";
  networking.useDHCP = false;
  networking.interfaces.eth0.useDHCP = true;
  networking.firewall = {
    enable = true;
    allowedTCPPorts = [ 22 80 443 53 ];
    allowedUDPPorts = [ ];
  };



  ### startup services
  services.cockpit.enable = true;
  services.journald.extraConfig = "Storage=persistent";
  services.openssh.enable = true;
  services.nginx.enable = true; # Add or remove based on your need




  ### included packages
  environment.systemPackages = with pkgs; [
    git
    neovim
    htop
    curl
    wget
    traceroute
    mtr
    inetutils  # includes ping, ifconfig, etc.
    lsof
    strace
    iproute2  # includes ip(8), ss, etc.
    dnsutils  # includes dig, nslookup
    tcpdump
    netcat
    bind
    jq
    python3Full
  ];




  ### User Config
  users.users.ec2-user = {
    isNormalUser = true;
    extraGroups = [ "wheel" ];
    password = "$6$eKG/rs9B9Pr28ibC$TxJMKPhBXLFJ7uB/DdtfUSDy.VvwU0kRWwMxFwmSqEE4UxUOS/SD/IfJJTmB43SrBjIP6.dhBhWDRvhoGmweT.";
  };

  users.users.alex = {
  isNormalUser = true;
  description = "Alex Admin";
  extraGroups = [ "wheel" ];  
  password = "$6$EhOT71ytUDRv4sVt$4I0l7uIPRV0nE4a5sVT.zH.W.QyCCeE1xbZSM8wvs2HSITdMI0bRA9xmbT6dBvBQm9iNztnEbWy9QkRG4MxxY.";  
  };

  users.users.root.password ="$6$JFx3nWOb8k.8AgJp$wOsynQlJ98caIoP67IPjWEYAr9ZGzBt32WgwrE1H82Le9ZuKz9HkI4GGF4siAYbGwm/HmVx0ZhR1bg8p5vSqB/";


  system.stateVersion = "24.05";
}



