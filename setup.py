#!/usr/bin/env python3
import subprocess
import sys
import os

def main():
    print("Setting up Accessibility Testing Framework...")
    
    # Install required packages
    print("Installing dependencies...")
    subprocess.run([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"], check=True)
    
    # Initialize Browser library
    print("Initializing Browser library...")
    subprocess.run(["rfbrowser", "init"], check=True)
    
    # Create required directories if they don't exist
    for directory in ["resources", "keywords", "tests", "results"]:
        os.makedirs(directory, exist_ok=True)
    
    print("\nSetup completed successfully!")
    print("\nTo run tests, use the following command:")
    print("python run_tests.py")
    print("\nNote: Make sure NVDA screen reader is installed on your system.")

if __name__ == "__main__":
    main() 