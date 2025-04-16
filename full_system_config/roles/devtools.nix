{ pkgs, ... }:

{
  environment.systemPackages = with pkgs; [
    neovim
    git
    jq
    ripgrep
    bat
    fd
    tmux
    htop
  ];

  programs.zsh.enable = true;
  environment.shells = [ pkgs.zsh ];
  users.defaultUserShell = pkgs.zsh;
}