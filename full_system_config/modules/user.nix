{
  users.users.ec2user = {
    isNormalUser = true;
    extraGroups = [ "wheel" ];
    password = "alex";  # dev only
  };
}