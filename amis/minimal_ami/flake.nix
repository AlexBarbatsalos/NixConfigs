{
  description = "Custom NixOS AMI Builder with Correct Disk Size";

  inputs.nixpkgs.url = "github:NixOS/nixpkgs/nixos-unstable";

  outputs = { self, nixpkgs, ... }: {
    nixosConfigurations.my-system = nixpkgs.lib.nixosSystem {
      modules = [
          "${nixpkgs}/nixos/maintainers/scripts/ec2/amazon-image.nix"
          ./configuration.nix

        ];
    };

    
  };
}



