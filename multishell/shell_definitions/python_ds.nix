{ pkgs }: 

let

  inherit (import ./common.nix { inherit pkgs; }) commonTools;
  
  python_ds = with pkgs; [
    (pkgs.python312.withPackages (ps: with ps; [
        pandas numpy matplotlib jupyterlab
        scikit-learn seaborn ipython
        transformers datasets accelerate sentence-transformers
        langchain openai fastapi
        ]))
  ];
in
pkgs.mkShell {
    name = "python-ds";
    packages = python_ds ++ commonTools;
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