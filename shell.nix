{ pkgs ? import <nixpkgs> {} }:

pkgs.mkShell {
  packages = with pkgs; [
    (python3.withPackages (ps: with ps; [
      mido
    ]))
    #alsa-utils # aplay # doesn't work on non-nixos
    gcc
    gnumake
    lame
    sox
  ];
}
