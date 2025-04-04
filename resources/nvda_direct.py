"""
Direct NVDA control module for accessibility testing
Uses pywinauto for Windows application interaction
"""

import os
import time
import subprocess
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger("NVDADirect")

class NVDADirect:
    """
    Class for directly controlling NVDA screen reader
    """
    
    def __init__(self, nvda_path="C:\\Program Files (x86)\\NVDA\\nvda.exe"):
        self.nvda_path = nvda_path
        self.nvda_process = None
        self.running = False
        self.last_speech = ""
        
    def start(self):
        """Start NVDA screen reader"""
        if not os.path.exists(self.nvda_path):
            raise FileNotFoundError(f"NVDA not found at {self.nvda_path}")
        
        logger.info(f"Starting NVDA from {self.nvda_path}")
        self.nvda_process = subprocess.Popen([self.nvda_path], shell=True)
        time.sleep(5)  # Give NVDA time to start
        self.running = True
        return True
        
    def stop(self):
        """Stop NVDA screen reader"""
        logger.info("Stopping NVDA")
        if self.running:
            try:
                # Use Windows taskkill to close NVDA
                subprocess.run(['taskkill', '/IM', 'nvda.exe', '/F'], capture_output=True)
                self.nvda_process = None
                self.running = False
                return True
            except Exception as e:
                logger.error(f"Error stopping NVDA: {e}")
                return False
        return True
    
    def get_speech(self):
        """
        Get the last spoken text by NVDA
        
        Note: This is a placeholder. In a real implementation, you would need to:
        1. Access NVDA's speech output through its Python API or
        2. Use a speech recognition system to capture what NVDA speaks, or
        3. Configure NVDA to write speech to a log file and read from it
        """
        logger.info("Getting NVDA speech")
        # In a real implementation, this would capture actual speech
        return self.last_speech
    
    def send_keys(self, keys):
        """Send keyboard input to NVDA"""
        logger.info(f"Sending keys to NVDA: {keys}")
        # In a real implementation, this would send actual keystrokes
        # Using something like pyautogui or pynput
        return True
    
    def simulate_speech(self, text):
        """
        Simulate speech output from NVDA (for testing without actual speech capture)
        """
        logger.info(f"Simulating NVDA speech: {text}")
        self.last_speech = text
        return self.last_speech
        
# Testing code
if __name__ == "__main__":
    nvda = NVDADirect()
    try:
        nvda.start()
        print("NVDA started successfully")
        nvda.simulate_speech("Test speech output")
        speech = nvda.get_speech()
        print(f"NVDA speech: {speech}")
        time.sleep(5)  # Wait to observe NVDA
    finally:
        nvda.stop()
        print("NVDA stopped") 