import os
import subprocess
import argparse
from pathlib import Path

def export_mermaid_diagrams(input_folder, output_folder=None, resolution=300):
    """
    Export all Mermaid diagrams in a folder to PNG files using Docker.
    
    Args:
        input_folder (str): Path to folder containing Mermaid diagrams (.mmd files)
        output_folder (str, optional): Path to save PNG files. Defaults to input_folder.
        resolution (int, optional): Image resolution in PPI. Defaults to 300.
    """
    # If no output folder is specified, use the input folder
    if output_folder is None:
        output_folder = input_folder
    
    # Create output folder if it doesn't exist
    os.makedirs(output_folder, exist_ok=True)
    
    # Convert paths to absolute paths
    input_folder = os.path.abspath(input_folder)
    output_folder = os.path.abspath(output_folder)
    
    # Get all .mmd files in the input folder
    mmd_files = list(Path(input_folder).glob("*.mmd"))
    
    if not mmd_files:
        print(f"No .mmd files found in {input_folder}")
        return
    
    print(f"Found {len(mmd_files)} Mermaid diagram files.")
    
    # Process each diagram file
    for mmd_file in mmd_files:
        input_path = str(mmd_file)
        output_filename = mmd_file.stem + ".png"
        output_path = os.path.join(output_folder, output_filename)
        
        print(f"Converting {mmd_file.name} to PNG...")
        
        # Create a temporary config file for high resolution
        config_path = os.path.join(output_folder, "mermaid-config.json")
        with open(config_path, "w") as f:
            f.write("""
            {
              "theme": "dark",
              "themeVariables": {
                "primaryColor": "#6e54bc",
                "primaryTextColor": "#fff",
                "primaryBorderColor": "#8a78d0",
                "lineColor": "#a0a0a0",
                "secondaryColor": "#355c7d",
                "tertiaryColor": "#2a4365"
              }
            }
            """)
        
        # Build the command for mermaid-cli Docker
        cmd = [
            "docker", "run", "--rm",
            "-v", f"{input_folder}:/data/input",
            "-v", f"{output_folder}:/data/output",
            "minlag/mermaid-cli",
            "-i", f"/data/input/{mmd_file.name}",
            "-o", f"/data/output/{output_filename}",
            "-c", "/data/output/mermaid-config.json",
            "-b", "transparent",
            "-s", str(resolution / 72)  # Scale factor based on resolution
        ]
        
        try:
            # Run the command
            result = subprocess.run(cmd, check=True, capture_output=True, text=True)
            print(f"Successfully created {output_filename}")
        except subprocess.CalledProcessError as e:
            print(f"Error converting {mmd_file.name}: {e}")
            print(f"Error output: {e.stderr}")
        except FileNotFoundError:
            print("Error: Docker command not found. Please install Docker.")
            print("Visit https://www.docker.com/products/docker-desktop/ to download Docker Desktop.")
            return

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