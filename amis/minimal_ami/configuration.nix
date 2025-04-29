# configuration.nix
{ config, pkgs, lib, diskSize, ... }:

{
 

  boot.loader.grub.device = "/dev/xvda";

  fileSystems."/" = {
    device = "/dev/xvda1";
    fsType = "ext4";
  };

  networking.hostName = "nixos-ami";
  networking.useDHCP = false;
  networking.interfaces.eth0.useDHCP = true;

  services.sshd.enable = true;

  users.users.ec2-user = {
    isNormalUser = true;
    extraGroups = [ "wheel" ];
    password = "replace-this-later";
  };

  system.stateVersion = "24.05";
}


