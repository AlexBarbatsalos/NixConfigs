{ pkgs, ... }:

{
  services.xserver.enable = true;
  services.xserver.desktopManager.plasma5.enable = true;
  services.xserver.displayManager.sddm.enable = true;

  services.xserver.displayManager.autoLogin.enable = true;
  services.xserver.displayManager.autoLogin.user = "ec2user";

  environment.systemPackages = with pkgs; [
    firefox
    vscode
    chromium
  ];
}