{
  imports = [
    ../modules/base.nix
    ../modules/user.nix
    ../modules/ssh.nix
    ../roles/gui.nix
  ];

  networking.hostName = "ec2-gui";
  
}
