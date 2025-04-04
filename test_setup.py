#!/usr/bin/env python3
import subprocess
import time
import requests
import os
import signal
import sys
import tempfile

def main():
    print("Testing Accessibility Framework with Mock NVDA...")
    
    # Create log file for bridge output
    log_file = tempfile.NamedTemporaryFile(delete=False, suffix='.log', mode='w+')
    log_path = log_file.name
    log_file.close()
    
    print(f"Bridge logs will be written to: {log_path}")
    
    # Start the Node.js bridge
    bridge_script = os.path.join(os.getcwd(), "resources", "mock_nvda.js")
    bridge_process = subprocess.Popen(
        ["node", bridge_script], 
        stdout=open(log_path, 'w'), 
        stderr=subprocess.STDOUT
    )
    
    try:
        # Wait for the server to start
        print("Starting Node.js mock NVDA bridge server...")
        time.sleep(5)  # Give more time to start
        
        # Test if the server is running
        try:
            # First check version info
            response = requests.get("http://localhost:3000/version")
            print(f"Mock NVDA Version Response: {response.status_code} - {response.text}")
            
            # Try to start NVDA
            print("\nAttempting to start Mock NVDA...")
            response = requests.get("http://localhost:3000/start")
            print(f"Mock NVDA Start Response: {response.status_code} - {response.text}")
            
            # Focus on an element
            print("\nFocusing on a text input element...")
            response = requests.get("http://localhost:3000/focus", params={"selector": "input[type=\"text\"]"})
            print(f"Focus Element Response: {response.status_code} - {response.text}")
            
            # Get speech for the element
            print("\nGetting speech for the element...")
            response = requests.get("http://localhost:3000/speak")
            print(f"Speech Response: {response.status_code} - {response.text}")
            
            # Try another element
            print("\nFocusing on a button element...")
            response = requests.get("http://localhost:3000/focus", params={"selector": "button[type=\"submit\"]"})
            print(f"Focus Button Response: {response.status_code} - {response.text}")
            
            # Get speech for button
            print("\nGetting speech for button...")
            response = requests.get("http://localhost:3000/speak")
            print(f"Button Speech Response: {response.status_code} - {response.text}")
            
            # Stop NVDA
            print("\nStopping Mock NVDA...")
            response = requests.get("http://localhost:3000/stop")
            print(f"Mock NVDA Stop Response: {response.status_code} - {response.text}")
            
            print("\nSetup verification completed successfully!")
            print("You can now run the Robot Framework tests with the mock NVDA.")
            print("\nTo run with real NVDA (if installed):")
            print("1. Make sure NVDA screen reader is installed on your system")
            print("2. Use 'initialize_nvda(False)' in your Robot Framework tests")
            
        except requests.exceptions.RequestException as e:
            print(f"Error connecting to bridge server: {e}")
            return 1
            
    finally:
        # Clean up
        if bridge_process:
            bridge_process.terminate()
            try:
                bridge_process.wait(timeout=5)
            except subprocess.TimeoutExpired:
                if sys.platform == 'win32':
                    bridge_process.kill()
                else:
                    os.kill(bridge_process.pid, signal.SIGKILL)
        
        # Display bridge logs
        print("\nNode.js Bridge Logs:")
        with open(log_path, 'r') as f:
            print(f.read())
    
    return 0

if __name__ == "__main__":
    sys.exit(main()) 