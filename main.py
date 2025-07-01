import os
import subprocess
import argparse
from pathlib import Path
import sys

def export_mermaid_diagrams(input_folder, output_folder=None, resolution=300):
    """
    Export all Mermaid diagrams to PNG files using a local npm installation.
    """
    # If no output folder is specified, use the input folder
    if output_folder is None:
        output_folder = input_folder
    
    # Create output folder if it doesn't exist
    os.makedirs(output_folder, exist_ok=True)
    
    # Convert paths to absolute paths
    input_folder = os.path.abspath(input_folder)
    output_folder = os.path.abspath(output_folder)
    
    print(f"Input folder: {input_folder}")
    print(f"Output folder: {output_folder}")
    
    # Get all .mmd files in the input folder
    mmd_files = list(Path(input_folder).glob("*.mmd"))
    
    if not mmd_files:
        print(f"No .mmd files found in {input_folder}")
        return
    
    print(f"Found {len(mmd_files)} Mermaid diagram files.")
    
    # First, try to install mermaid-cli locally if it's not installed
    try:
        print("Checking if mermaid-cli is installed...")
        subprocess.run(["which", "mmdc"], check=True, timeout=5)
        print("mermaid-cli is already installed.")
    except:
        print("Installing mermaid-cli locally...")
        try:
            subprocess.run(["npm", "install", "-g", "@mermaid-js/mermaid-cli"], check=True, timeout=120)
            print("mermaid-cli installed successfully.")
        except Exception as e:
            print(f"Failed to install mermaid-cli: {e}")
            print("You may need to install Node.js first.")
            print("Try running: sudo apt install nodejs npm")
            return
    
    # Process each diagram file using local mmdc
    for mmd_file in mmd_files:
        input_path = str(mmd_file)
        output_filename = mmd_file.stem + ".png"
        output_path = os.path.join(output_folder, output_filename)
        
        print(f"Converting {mmd_file.name} to PNG...")
        
        # Create a temporary config file for high resolution
        config_path = os.path.join(output_folder, "mermaid-config.json")
        with open(config_path, "w") as f:
            f.write("""{
  "theme": "dark",
  "themeVariables": {
    "primaryColor": "#6e54bc",
    "primaryTextColor": "#fff",
    "primaryBorderColor": "#8a78d0",
    "lineColor": "#a0a0a0",
    "secondaryColor": "#355c7d",
    "tertiaryColor": "#2a4365"
  }
}""")
        
        # Build command for local mmdc
        cmd = [
            "mmdc",
            "-i", input_path,
            "-o", output_path,
            "-c", config_path,
            "-b", "transparent",
            "-w", str(int(resolution * 3))  # Width - adjust as needed
        ]
        
        print(f"Executing command: {' '.join(cmd)}")
        
        try:
            # Run the command with a timeout
            result = subprocess.run(cmd, check=True, capture_output=True, text=True, timeout=30)
            print(f"Successfully created {output_filename}")
        except Exception as e:
            print(f"Error converting {mmd_file.name}: {e}")
            if hasattr(e, 'stderr'):
                print(f"Error output: {e.stderr}")
            
            # If local mmdc fails, try with Chrome directly as a last resort
            print("Trying with puppeteer directly...")
            # Create a simple HTML file for the browser
            html_path = os.path.join(output_folder, f"{mmd_file.stem}.html")
            with open(input_path, 'r') as f:
                diagram_content = f.read()
                
            with open(html_path, 'w') as f:
                f.write(f"""<!DOCTYPE html>
<html>
<head>
    <title>Mermaid Diagram</title>
    <script src="https://cdn.jsdelivr.net/npm/mermaid@10/dist/mermaid.min.js"></script>
    <script>
        mermaid.initialize({{
            startOnLoad: true,
            theme: 'dark'
        }});
    </script>
</head>
<body style="background-color: black;">
    <div class="mermaid">
    {diagram_content}
    </div>
</body>
</html>""")
            print(f"Created HTML file at {html_path}")
            print(f"Open this in a browser and take a screenshot manually")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Export Mermaid diagrams to PNG files")
    parser.add_argument("input_folder", help="Folder containing Mermaid diagrams")
    parser.add_argument("-o", "--output", help="Folder to save PNG files")
    parser.add_argument("-r", "--resolution", type=int, default=300,
                        help="Image resolution in PPI (default: 300)")
    
    args = parser.parse_args()
    
    # Export diagrams
    export_mermaid_diagrams(args.input_folder, args.output, args.resolution)
    
    print("Done!")