{
  description = "Minimal flake shell for Mermaid conversion";

  inputs.nixpkgs.url = "github:NixOS/nixpkgs";

  outputs =
    { self, nixpkgs }:
    {
      devShells = {
        x86_64-linux =
          let
            pkgs = import nixpkgs { system = "x86_64-linux"; };
          in
          {
            default = pkgs.mkShell {
              name = "mermaid-converter-env";

              buildInputs = with pkgs; [
                (python3.withPackages (
                  ps: with ps; [
                    pip
                    setuptools
                  ]
                ))
                nodejs_20
                nodePackages.npm
                nodePackages.mermaid-cli
                which
                coreutils
                gnused
                chromium
              ];

              shellHook = ''
                export PUPPETEER_SKIP_CHROMIUM_DOWNLOAD=true
                export PUPPETEER_EXECUTABLE_PATH="${pkgs.chromium}/bin/chromium"
                export PATH="$PATH:${pkgs.nodePackages.mermaid-cli}/bin"
              '';
            };
          };
      };
    };
}
