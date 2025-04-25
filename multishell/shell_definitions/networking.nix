{ pkgs }:

let
  inherit (import ./common.nix { inherit pkgs; })  networkingTools;
in
pkgs.mkShell {
  name = "networking-shell";
  packages = networkingTools;
  shellHook = ''
    export PS1="(networking) $PS1"
    echo "🌐 Networking shell: all net tools loaded"

    source ${./snippets/exit_gc.sh}
  '';
}
