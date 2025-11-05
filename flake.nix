{
  description = "Keybinder - Extracts and parses keybinds to markdown";

  inputs = {
    nixpkgs.url = "github:NixOS/nixpkgs/nixos-unstable";
    systems.url = "github:nix-systems/default";
    flake-utils = {
      url = "github:numtide/flake-utils";
      inputs.systems.follows = "systems";
    };
  };

  outputs =
    {
      self,
      nixpkgs,
      flake-utils,
      ...
    }:
    flake-utils.lib.eachDefaultSystem (
      system:
      let
        pkgs = nixpkgs.legacyPackages.${system};
        python = pkgs.python313;
        pythonPackages = python.pkgs;
      in
      {
        packages.default = pythonPackages.buildPythonApplication {
          pname = "keybind-extractor";
          version = "0.1.0";
          src = ./.;
          format = "other";

          installPhase = ''
            mkdir -p $out/bin
            cp keybinder.py $out/bin/keybinder.py
            chmod +x $out/bin/keybinder
          '';

          propagatedBuildInputs = with pythonPackages; [
            pyyaml
          ];
        };

        devShells = {
          default = pkgs.mkShell {
            name = "keybinder-dev";
            packages = with pkgs; [
              python313
              ruff
              python313Packages.pydantic
              nil
              nixd
              pyright
            ];
            shellHook = ''
              echo "Entered Keybinder dev shell"
              echo "Run: python keybinder.py"
            '';
          };

          test = pkgs.mkShell {
            name = "keybinder-test";
            packages = with pkgs; [
              ruff
              python313
              python313Packages.pytest
              python313Packages.coverage
              python313Packages.pyyaml
            ];

            shellHook = ''
              echo "Entered Keybinder test shell"
              echo "Run: pytest -v tests/"
            '';
          };
        };
      }
    );
}
