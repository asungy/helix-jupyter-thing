{
  inputs = {
    nixpkgs-unstable.url = "github:nixos/nixpkgs/nixpkgs-unstable";
    nixpkgs-stable.url = "github:nixos/nixpkgs/release-24.11";
    flake-utils.url = "github:numtide/flake-utils";
  };

  outputs = inputs:
    inputs.flake-utils.lib.eachDefaultSystem(system:
      let
        overlays = [];
        pkgs-stable = import inputs.nixpkgs-stable { inherit system overlays; };
        pkgs-unstable = import inputs.nixpkgs-unstable { inherit system overlays; };
      in
      {
        devShells.default = pkgs-unstable.mkShell {
          name = "helix-jupyter-thing";

          packages = with pkgs-unstable; [
            python312Packages.python
          ];

          env.LD_LIBRARY_PATH = pkgs-unstable.lib.makeLibraryPath [
            pkgs-unstable.stdenv.cc.cc.lib
            pkgs-unstable.zlib
          ];

          shellHook = ''
            alias activate='source ./venv/bin/activate'

            VENV_DIR="venv"
            if [ ! -d "$VENV_DIR" ]; then
                echo "Virtual environment not found. Creating at ./$VENV_DIR ..."
                python3 -m venv "$VENV_DIR"
                echo "Virtual environment created."
            fi            
          '';
        };
      }
    );
}
