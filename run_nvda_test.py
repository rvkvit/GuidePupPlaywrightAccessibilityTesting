#!/usr/bin/env python3
import os
import sys
import subprocess
import datetime
import time

def main():
    print("Starting accessibility testing with real NVDA...")
    
    # Path to the real NVDA executable
    nvda_path = "C:\\Program Files (x86)\\NVDA\\nvda.exe"
    
    # Check if NVDA exists
    if not os.path.exists(nvda_path):
        print(f"Error: NVDA not found at {nvda_path}")
        return 1
    
    # Check if NVDA is already running
    try:
        nvda_running = subprocess.run(['tasklist', '/FI', 'IMAGENAME eq nvda.exe'], 
                                     capture_output=True, text=True).stdout
        if 'nvda.exe' in nvda_running:
            print("NVDA is already running. Stopping existing instance...")
            subprocess.run(['taskkill', '/IM', 'nvda.exe', '/F'], capture_output=True)
            time.sleep(2)  # Wait for process to terminate
    except Exception as e:
        print(f"Error checking NVDA status: {e}")
    
    nvda_process = None
    try:
        # Start NVDA first
        print(f"Starting NVDA from {nvda_path}...")
        nvda_process = subprocess.Popen([nvda_path], shell=True)
        
        # Give NVDA time to start
        print("Waiting for NVDA to initialize (5 seconds)...")
        time.sleep(5)
        
        # Current time for output directory
        current_time = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        output_dir = os.path.join("results", f"nvda_test_{current_time}")
        os.makedirs(output_dir, exist_ok=True)
        
        # Set environment variable to tell Robot Framework that NVDA is already running
        os.environ["NVDA_ALREADY_RUNNING"] = "true"
        
        # Run Robot Framework test with real NVDA
        print("Running Robot Framework test with real NVDA...")
        robot_cmd = [
            "python", "-m", "robot",
            f"--outputdir={output_dir}",
            "--loglevel=DEBUG",
            "tests/real_nvda_test.robot"
        ]
        
        subprocess.run(robot_cmd, check=True)
        print(f"Test completed. Results available in {output_dir}")
        
    except subprocess.CalledProcessError as e:
        print(f"Error running tests: {e}")
        return 1
    except Exception as e:
        print(f"Unexpected error: {e}")
        return 1
    finally:
        # Always try to stop NVDA when done
        print("Stopping NVDA...")
        try:
            # Clear the environment variable
            if "NVDA_ALREADY_RUNNING" in os.environ:
                del os.environ["NVDA_ALREADY_RUNNING"]
                
            subprocess.run(['taskkill', '/IM', 'nvda.exe', '/F'], capture_output=True)
            
            # Wait for NVDA to fully close
            time.sleep(2)
            
            # Verify NVDA is closed
            nvda_running = subprocess.run(['tasklist', '/FI', 'IMAGENAME eq nvda.exe'], 
                                         capture_output=True, text=True).stdout
            if 'nvda.exe' in nvda_running:
                print("Warning: NVDA is still running. Attempting to force close...")
                subprocess.run(['taskkill', '/IM', 'nvda.exe', '/F', '/T'], capture_output=True)
        except Exception as e:
            print(f"Error stopping NVDA: {e}")
    
    return 0

if __name__ == "__main__":
    sys.exit(main()) 