trap '
  echo
  read -r -p "🧹 Do you want to run nix-collect-garbage -d on exit? [y/N] " yn
  if [ "$yn" = "y" ] || [ "$yn" = "Y" ]; then
    echo "Running garbage collection..."
    nix-collect-garbage -d
  else
    echo "Skipping garbage collection."
  fi
' EXIT
