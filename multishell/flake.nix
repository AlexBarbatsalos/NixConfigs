{
  description = "Modular multi-shell flake";

  inputs.nixpkgs.url = "github:NixOS/nixpkgs/nixos-unstable";
  inputs.flake-utils.url = "github:numtide/flake-utils";

  outputs = { self, nixpkgs, flake-utils, ... }:
    flake-utils.lib.eachDefaultSystem (system:
      let
        pkgs = import nixpkgs { inherit system; };
      in {
        devShells = {
          default      = import "${self}/shell_definitions/default.nix"      { inherit pkgs; };
          networking   = import "${self}/shell_definitions/networking.nix"   { inherit pkgs; };
          system-debug = import "${self}/shell_definitions/system-debug.nix" { inherit pkgs; };
          full-debug   = import "${self}/shell_definitions/full-debug.nix"   { inherit pkgs; };
          python-data  = import "${self}/shell_definitions/python-data.nix"  { inherit pkgs; };
          haskell      = import "${self}/shell_definitions/haskell.nix"      { inherit pkgs; };
          pentesting   = import "${self}/shell_definitions/pentesting.nix"   { inherit pkgs; };
        };
      });
}



