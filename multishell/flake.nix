{
  description = "Multi-shell flake example";

  inputs.nixpkgs.url = "github:NixOS/nixpkgs/nixos-unstable";
  inputs.flake-utils.url = "github:numtide/flake-utils";

  outputs = { self, nixpkgs, flake-utils, ... }:
    flake-utils.lib.eachDefaultSystem (system:
      let
        pkgs = import nixpkgs { inherit system; };
      in {
        devShells = {
          default = pkgs.mkShell {
            name = "default-shell";
            packages = [ pkgs.neovim pkgs.git ];
            shellHook = ''echo "👋 Default dev shell" '';
          };

          python-data = pkgs.mkShell {
            name = "python-data-shell";
            packages = [ pkgs.python3 pkgs.jupyterlab pkgs.pandas ];
            shellHook = ''echo "🐍 Python data science shell" '';
          };

          haskell = pkgs.mkShell {
            name = "haskell-dev-shell";
            packages = [ pkgs.stack pkgs.git pkgs.ghc ];
            shellHook = ''echo "Haskell dev shell" '';
          };
        };
      });
}
