{ pkgs }:

let haskell_stack = with pkgs; [ stack ghc git ];

in 

pkgs.mkShell{
    name = "haskell-dev-shell";
    packages = haskell_stack;
    shellHook = ''
        export PS1="(λ) $PS1"
        echo "λ Haskell dev shell"

        source ${./snippets/exit_gc.sh}
        
    '';
    }