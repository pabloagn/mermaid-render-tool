{ pkgs ? import <nixpkgs> {} }:

pkgs.mkShell {
  name = "mermaid-converter-env";
  
  buildInputs = with pkgs; [
    # Python environment
    (python3.withPackages (ps: with ps; [
      pip
      setuptools
    ]))
    
    # Node.js and npm
    nodejs_20
    nodePackages.npm
    
    # Include the mermaid-cli package directly
    nodePackages.mermaid-cli
    
    # Utils
    which
    coreutils
    gnused
    
    # Include Chrome/Chromium for puppeteer
    chromium
  ];
  
  shellHook = ''
    export PUPPETEER_SKIP_CHROMIUM_DOWNLOAD=true
    export PUPPETEER_EXECUTABLE_PATH="${pkgs.chromium}/bin/chromium"
    export PATH="$PATH:${pkgs.nodePackages.mermaid-cli}/bin"
    
    echo "Nix shell for Mermaid diagram conversion"
    echo "---------------------------------------"
    echo "This shell includes Python, Node.js, and mermaid-cli (mmdc command)."
    echo ""
    echo "You can run your script with:"
    echo "  python3 main.py /path/to/diagrams -r 300"
    echo ""
    echo "Or use mmdc directly:"
    echo "  mmdc -i input.mmd -o output.png -b transparent"
    echo ""
    
    # Verify mmdc is available
    if command -v mmdc >/dev/null 2>&1; then
      echo "✓ mermaid-cli is available as 'mmdc'"
    else
      echo "✗ mermaid-cli is not in PATH. Please check your Nix configuration."
    fi
  '';
}