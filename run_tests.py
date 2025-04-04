#!/usr/bin/env python3
import os
import sys
import subprocess
import datetime

def main():
    current_time = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    output_dir = os.path.join("results", f"run_{current_time}")
    
    os.makedirs(output_dir, exist_ok=True)
    
    # Run Robot Framework tests
    command = [
        "robot",
        "--outputdir", output_dir,
        "--loglevel", "DEBUG",
        "tests"
    ]
    
    try:
        subprocess.run(command, check=True)
        print(f"Tests completed. Results available in {output_dir}")
    except subprocess.CalledProcessError as e:
        print(f"Error running tests: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main() 