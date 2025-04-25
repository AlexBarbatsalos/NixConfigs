{ pkgs }:

let
  commonTools = with pkgs; [ neovim git ];
in
pkgs.mkShell {
  name = "default-shell";
  packages = commonTools;
  shellHook = ''
    export PS1="(default) $PS1"
    echo "👋 Default dev shell"

    source ${./snippets/exit_gc.sh}
  '';
}
