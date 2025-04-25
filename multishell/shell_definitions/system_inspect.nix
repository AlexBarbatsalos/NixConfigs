{ pkgs }:

let
  inherit (import ./common.nix { inherit pkgs; }) systemDebugTools;
in
pkgs.mkShell {
  name = "system-shell";
  packages = systemDebugTools;
  shellHook = ''
    export PS1="(sysInspect) $PS1"
    echo "System debug shell: fine-grained inspection tools ready"'';
}