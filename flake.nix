{
  description = "Keybinder - Extracts and parses keybinds to markdown";

  inputs = {
    nixpkgs.url = "github:NixOS/nixpkgs/nixos-unstable";
  };

  outputs =
    { self, nixpkgs }:
    let
      system = "x86_64-linux";
      pkgs = import nixpkgs { inherit system; };
      python = pkgs.python312;
      pythonPackages = python.pkgs;
    in
    {
      packages.${system}.default = pythonPackages.buildPythonApplication {
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

      devShells.${system} = {
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

        # ✅ Test shell with pytest configured
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
    };
}
