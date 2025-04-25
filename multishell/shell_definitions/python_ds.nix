{ pkgs }: 

let
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
    name = "python-data-shell";
    packages = python_ds;
    shellHook = ''
        export PS1="(python-ds) $PS1"
        echo "Python data science shell"

        source ${./snippets/exit_gc.sh}
        
      '';
    }