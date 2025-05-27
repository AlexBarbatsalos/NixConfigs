{ pkgs }:

let
  inherit (import ./common.nix { inherit pkgs; })  networkingTools pythonNetTools commonTools;
in
pkgs.mkShell {
  name = "networking-shell";
  packages = networkingTools ++ pythonNetTools ++ commonTools;
  env = {
    PYTHONPATH = "./src";
    PATH = "${pkgs.tcpdump}/bin:$PATH";

  };

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