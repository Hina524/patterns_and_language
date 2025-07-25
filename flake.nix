{
  description = "DevShell with spaCy from PyPI";

  inputs = {
    nixpkgs.url = "github:NixOS/nixpkgs/nixos-unstable";
    flake-utils.url = "github:numtide/flake-utils";
  };

  outputs =
    {
      self,
      nixpkgs,
      flake-utils,
    }:
    flake-utils.lib.eachDefaultSystem (
      system:
      let
        pkgs = import nixpkgs { inherit system; config.allowUnfree = true; };
      in
      {
        devShell = pkgs.mkShell {
          buildInputs = [
            pkgs.python311
            pkgs.python311Packages.pip
            pkgs.claude-code
          ];
          shellHook = ''
            export PYTHONNOUSERSITE="true"
            if [ ! -d .venv ]; then
              python -m venv .venv
            fi
            source .venv/bin/activate
            pip install --upgrade pip
            if [ -f requirements.txt ]; then
              pip install -r requirements.txt
            fi
            echo "🐍 Python venv ready!"
          '';
        };
      }
    );
}
