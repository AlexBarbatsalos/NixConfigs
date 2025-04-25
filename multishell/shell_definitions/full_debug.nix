{ pkgs }:

let
  inherit (import ./common.nix { inherit pkgs; }) networkingTools systemDebugTools;

  commonTools = with pkgs; [ neovim git ];
in
pkgs.mkShell {
  name = "full-debug-shell";
  packages = commonTools ++ networkingTools ++ systemDebugTools;
  shellHook = ''
    export PS1="(full-debug) $PS1"
    echo "🛠️ Full debug shell: everything is ready!"

    source ${./snippets/exit_gc.sh}
  '';
}
