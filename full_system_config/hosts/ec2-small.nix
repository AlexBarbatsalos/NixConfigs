{
  imports = [
    
    ../modules/base.nix
    ../modules/user.nix
    ../modules/ssh.nix
    ../roles/devtools.nix
    #../roles/python_dataScience
  ];

  networking.hostName = "ec2-small";

  boot.loader.grub = {
    enable = true;
    version = 2;
    device = "/dev/nvme0n1"; # or "/dev/xvda" for older EC2 instances
    efiSupport = false;
  };

  boot.loader.timeout = 0;
  boot.kernelParams = [ "console=ttyS0" "boot.shell_on_fail" ];

  # Add common modules used on EC2 instances
  boot.initrd.availableKernelModules = [ "nvme" "xen_blkfront" "ext4" ];
  boot.initrd.kernelModules = [ ];

  # Adjust this block based on `lsblk` or `mount` output inside your EC2 instance
  fileSystems."/" = {
    device = "/dev/nvme0n1p1";
    fsType = "ext4";
  };

  # Optional EC2-specific tweaks
  virtualisation.amazonGuest.enable = true;
  
}
