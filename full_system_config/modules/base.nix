{ config, pkgs, ... }:

{
  nixpkgs.config.allowUnfree = true;

  # Basic networking (optional if already in host-specific config)
  networking.useDHCP = false;
  networking.interfaces.enp1s0.useDHCP = true;

  # Timezone and locale
  time.timeZone = "Europe/Berlin";

  i18n.defaultLocale = "en_US.UTF-8";

  console = {
    font = "Lat2-Terminus16";
    keyMap = "us";
  };

  # System state version (can be overridden in host if needed)
  system.stateVersion = "23.11";
}
