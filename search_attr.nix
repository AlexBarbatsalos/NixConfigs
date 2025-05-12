
{ lib ? import <nixpkgs/lib>  }:

let
  inherit (builtins) attrNames isAttrs match concatLists map;

  searchAttrPaths = name: set:
    let
      recurse = prefix: s:
        concatLists (
          map
            (key:
              let
                val = s.${key};
                path = prefix ++ [key];
                matchFound = match ".*${name}.*" key != null;
              in
                (if matchFound then [path] else [])
                ++ (if isAttrs val then recurse path val else [])
            )
            (attrNames s)
        );
    in recurse [] set;

in
{
  inherit searchAttrPaths;
}
