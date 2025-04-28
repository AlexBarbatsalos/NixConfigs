{ pkgs }:

let
  inherit (import ./common.nix { inherit pkgs; }) networkingTools systemDebugTools commonTools;

  
in
pkgs.mkShell {
  name = "full-debug-shell";
  packages = commonTools ++ networkingTools ++ systemDebugTools;
  shellHook = ''
    export STARSHIP_CONFIG="${./snippets/starship-config.toml}"
    export PS1=""

    if command -v starship >/dev/null; then
      eval "$(starship init bash)"
    else
      echo "⚠️  Starship not found, using fallback prompt"
      export PS1="[\u@\h \W]\$ "
    fi

    source ${./snippets/exit_gc.sh}
  '';
}
