# mermaid-render-tool

A tool to render Mermaid diagrams to high-quality PNG files.

## Setup Options

### Option 1: Using Docker (Windows/Mac/Linux)

1. Install Docker if you don't have it yet.
2. Start the Docker daemon.
3. Run the script with the path to your diagrams folder:
```bash
python main.py /path/to/diagrams -o /path/to/output
```

### Option 2: Using Nix Shell (NixOS/Linux with Nix)

1. Make sure you have Nix installed.
2. Run the provided Nix shell:
```bash
nix-shell
```
3. Within the Nix shell, run the script:
```bash
python3 main.py /path/to/diagrams -o /path/to/output
```

### Option 3: Using Node.js directly (Any OS)

1. Install Node.js and npm.
2. Install mermaid-cli globally:
```bash
npm install -g @mermaid-js/mermaid-cli
```
3. Run the script:
```bash
python3 main.py /path/to/diagrams -o /path/to/output
```

## Example Usage

```bash
python main.py diagrams -o exported_diagrams -r 300
```

This will:
1. Look for all `.mmd` files in the `diagrams` folder.
2. Export them as PNG files to the `exported_diagrams` folder.
3. Use a resolution of 300 PPI.
4. Maintain transparent backgrounds.
5. Apply a consistent dark theme with custom styling.

## Parameters

- `-o, --output`: Output folder path (optional, defaults to input folder)
- `-r, --resolution`: Image resolution in PPI (optional, defaults to 300)

## Requirements

### For Docker method:
- Python 3.6+
- Docker

### For Nix Shell method:
- Nix package manager
- The provided `shell.nix` file

### For Node.js method:
- Python 3.6+
- Node.js 14+
- npm