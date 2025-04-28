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
          default      = import "${self}/shell_definitions/default.nix"         { inherit pkgs; };
          networking   = import "${self}/shell_definitions/networking.nix"      { inherit pkgs; };
          system_debug = import "${self}/shell_definitions/system_inspect.nix"  { inherit pkgs; };
          full_debug   = import "${self}/shell_definitions/full_debug.nix"      { inherit pkgs; };
          python_ds    = import "${self}/shell_definitions/python_ds.nix"       { inherit pkgs; };
          haskell      = import "${self}/shell_definitions/haskell.nix"         { inherit pkgs; };
          pentesting   = import "${self}/shell_definitions/pentesting.nix"      { inherit pkgs; };
        };
      });
}



