trap '
 echo

  #  Firewall restore
  echo " Restoring hardened firewall rules..."
  if sudo /usr/bin/nft -f /etc/nftables.conf; then
    echo " Hardened firewall successfully restored."
  else
    echo "❌ Failed to restore firewall — check your config or permissions."
  fi

  # Garbage collection prompt
  echo
  read -r -p "Do you want to run nix-collect-garbage -d on exit? [y/N] " yn
  if [ "$yn" = "y" ] || [ "$yn" = "Y" ]; then
    echo "Running garbage collection..."
    nix-collect-garbage -d
  else
    echo "Skipping garbage collection."
  fi
' EXIT
