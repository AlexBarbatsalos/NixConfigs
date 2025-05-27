{
  description = "Networking Toolkit with Unified Output and ASCII Animations";

  inputs = {
    nixpkgs.url = "github:NixOS/nixpkgs/nixos-unstable"; # Still needed
    flake-utils.url = "github:numtide/flake-utils";      # For multiple system support
    multishell.url = "../multishell";                    # <--- your external devshell
  };

  outputs = { self, nixpkgs, flake-utils, multishell }: 
    flake-utils.lib.eachDefaultSystem (system:
      let
        pkgs = import nixpkgs { inherit system; };
      in {
        devShells.default = multishell.devShells.${system}.pyNet;

        packages.default = pkgs.python3Packages.buildPythonApplication {
          pname = "networking-toolkit";
          version = "0.1.0";
          src = ./.;
          propagatedBuildInputs = with pkgs.python3Packages; [
            requests scapy dnspython paramiko netaddr websockets pyshark
          ];
          doCheck = false;
        };

        apps.default = {
          type = "app";
          program = "${self.packages.${system}.default}/bin/networking-toolkit";
        };
      }
    );
}
