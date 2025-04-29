{
  description = "Custom NixOS AMI Builder with Correct Disk Size";

  inputs.nixpkgs.url = "github:NixOS/nixpkgs/nixos-unstable";

  outputs = { self, nixpkgs, ... }:
    let
      system = "x86_64-linux";
    in {
      nixosConfigurations.first-ami = nixpkgs.lib.nixosSystem {
        inherit system;
        #specialArgs = { diskSize = 8192; }; # Pass diskSize as special argument
        modules = [
          (import "${nixpkgs.outPath}/nixos/maintainers/scripts/ec2/amazon-image.nix")
          ./configuration.nix
          # Apply overlay through a small module here if needed
        ];
      };
    };
}
