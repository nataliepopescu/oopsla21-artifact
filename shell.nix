{ pkgs ? import <nixpkgs> {} }:
  pkgs.mkShell {
    buildInputs = [
      pkgs.python3
      pkgs.python38Packages.numpy
      pkgs.python38Packages.dash
      pkgs.python38Packages.plotly
      pkgs.python38Packages.orca
      pkgs.python38Packages.tqdm
      pkgs.python38Packages.scipy
      pkgs.python38Packages.psutil
      pkgs.python38Packages.requests
    ];
}
