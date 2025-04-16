{
  imports = [
    ../modules/base.nix
    ../modules/user.nix
    ../modules/ssh.nix
    ../roles/devtools.nix
    #../roles/python_dataScience
  ];

  networking.hostName = "ec2-small";
  
}
