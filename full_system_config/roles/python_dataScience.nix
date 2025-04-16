{ pkgs, ... }:

{
  environment.systemPackages = with pkgs; [
    python3
    python3Packages.pip
    python3Packages.numpy
    python3Packages.pandas
    python3Packages.scipy
    python3Packages.matplotlib
    python3Packages.jupyterlab
    python3Packages.scikit-learn
    python3Packages.seaborn
    python312Packages.tensorflow

  ];

  # Optional: enable Jupyter as a service
  services.jupyter.enable = true;
}