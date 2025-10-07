{
  description = "Keybinder - Extracts and parse keybinds to markdown";

  inputs = {
    nixpkgs.url = "github:NixOS/nixpkgs/nixos-unstable";
  };

  outputs = { self, nixpkgs }:
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

      devShells.${system}.default = pkgs.mkShell {
        name = "keybinder-dev";
        packages = with pkgs; [
          python
          ruff
          pythonPackages.pyyaml
        ];
        shellHook = ''
          echo "Entered Keybinder dev shell"
          echo "Run: python keybinder.py"
        '';
      };
    };
}
