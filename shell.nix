{ pkgs ? import <nixpkgs-unstable> {} }:
  pkgs.mkShell {
    nativeBuildInputs = (with pkgs.python312Packages; [
      python
    ]);

    env.LD_LIBRARY_PATH = pkgs.lib.makeLibraryPath [
      pkgs.stdenv.cc.cc.lib
      pkgs.libz
    ];
}
