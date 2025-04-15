{
  description = "Dev environment for hacking around";

  inputs = {
    nixpkgs.url = "github:NixOS/nixpkgs/nixos-unstable";
    flake-utils.url = "github:numtide/flake-utils";
  };

  outputs = { self, nixpkgs, flake-utils, ... }:
    flake-utils.lib.eachDefaultSystem (system:
      let
        pkgs = import nixpkgs { inherit system; };
      in {
        devShells.default = pkgs.mkShell {
          name = "my-dev-env";
          packages = [
            pkgs.neovim
            pkgs.git
            pkgs.nodejs
            pkgs.python3
            pkgs.jq
            pkgs.curl
            pkgs.docker
            pkgs.bat      # like `cat` but cooler
            pkgs.fd       # better `find`
            pkgs.ripgrep  # better `grep`
          ];

          shellHook = ''
            echo "👋 Welcome to your Nix dev shell!"
            export EDITOR=nvim
          '';
        };
      });
}
