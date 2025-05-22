{ pkgs }:

let
  inherit (import ./common.nix { inherit pkgs; })  networkingTools commonTools;
in
pkgs.mkShell {
  name = "networking-shell";
  packages = networkingTools ++ commonTools;
  shellHook = ''
    export STARSHIP_CONFIG="${./snippets/starship-config.toml}"
    export PS1=""

    if command -v starship >/dev/null; then
      eval "$(starship init bash)"
    else
      echo "󰀧  Starship not found, using fallback prompt"
      export PS1="[\u@\h \W]\$ "
    fi
    

    echo " Switching to relaxed dev firewall..."
    toggle-firewall.sh dev

    source ${./snippets/exit_gc.sh} 
  '';
}
