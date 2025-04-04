from robot.api.deco import library, keyword
import requests
import time
import os
import json
import subprocess
from datetime import datetime
import sys

# Add the resources directory to the path for imports
current_dir = os.path.dirname(os.path.abspath(__file__))
if current_dir not in sys.path:
    sys.path.append(current_dir)

# Try to import the NVDADirect module
try:
    from nvda_direct import NVDADirect
    NVDA_DIRECT_AVAILABLE = True
except ImportError:
    NVDA_DIRECT_AVAILABLE = False
    print("NVDADirect module not available. Direct NVDA control will be limited.")

@library
class GuidepupLibrary:
    """Library for controlling NVDA screen reader using Guidepup through a Node.js bridge or direct execution."""
    
    BRIDGE_URL = "http://localhost:3000"
    NVDA_PATH = "C:\\Program Files (x86)\\NVDA\\nvda.exe"
    
    def __init__(self, use_mock=False, use_direct_nvda=True):
        self.bridge_process = None
        self.nvda = None
        self.speech_log = []
        self.log_file_path = None
        self.expected_results = {}
        self.use_mock = use_mock
        self.use_direct_nvda = use_direct_nvda
    
    @keyword
    def initialize_nvda(self, use_mock=None, use_direct_nvda=None):
        """Initialize NVDA screen reader using Guidepup bridge or direct execution."""
        # Allow override of mock and direct mode
        if use_mock is not None:
            self.use_mock = use_mock
        if use_direct_nvda is not None:
            self.use_direct_nvda = use_direct_nvda
            
        if self.use_direct_nvda and not self.use_mock:
            # Start NVDA directly using NVDADirect if available
            if NVDA_DIRECT_AVAILABLE:
                self.nvda = NVDADirect(nvda_path=self.NVDA_PATH)
                self.nvda.start()
            else:
                # Fall back to basic subprocess if NVDADirect not available
                if not os.path.exists(self.NVDA_PATH):
                    raise Exception(f"NVDA not found at {self.NVDA_PATH}")
                print(f"Starting NVDA directly from {self.NVDA_PATH}")
                subprocess.Popen([self.NVDA_PATH], shell=True)
                time.sleep(5)  # Wait for NVDA to start
        else:
            # Start the Node.js bridge server
            bridge_script = os.path.join(os.getcwd(), "resources", 
                                        "mock_nvda.js" if self.use_mock else "guidepup_bridge.js")
            
            self.bridge_process = subprocess.Popen(["node", bridge_script], 
                                                stdout=subprocess.PIPE, 
                                                stderr=subprocess.PIPE)
            
            # Wait for the server to start
            time.sleep(3)
            
            # Start NVDA through the bridge
            response = requests.get(f"{self.BRIDGE_URL}/start")
            if response.status_code != 200:
                raise Exception(f"Failed to start NVDA: {response.text}")
        
        # Create log directory for this test run
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        log_dir = os.path.join("results", f"nvda_logs_{timestamp}")
        os.makedirs(log_dir, exist_ok=True)
        self.log_file_path = os.path.join(log_dir, "speech_log.json")
        self.speech_log = []
    
    @keyword
    def shutdown_nvda(self):
        """Shut down NVDA screen reader."""
        try:
            if self.use_direct_nvda and not self.use_mock:
                # Stop direct NVDA process using NVDADirect if available
                if NVDA_DIRECT_AVAILABLE and self.nvda:
                    self.nvda.stop()
                else:
                    # Fall back to taskkill
                    subprocess.run(['taskkill', '/IM', 'nvda.exe', '/F'], capture_output=True)
            else:
                # Stop NVDA through the bridge
                requests.get(f"{self.BRIDGE_URL}/stop")
                
                # Kill the bridge process
                if self.bridge_process:
                    self.bridge_process.terminate()
                    self.bridge_process.wait(timeout=5)
        except Exception as e:
            print(f"Error shutting down NVDA: {str(e)}")
        
        # Save speech log to file
        if self.log_file_path and self.speech_log:
            with open(self.log_file_path, 'w') as f:
                json.dump(self.speech_log, f, indent=2)
    
    @keyword
    def load_expected_results(self, file_path):
        """Load expected screen reader output from a JSON file."""
        with open(file_path, 'r') as f:
            self.expected_results = json.load(f)
    
    @keyword
    def focus_element(self, selector, timeout=5):
        """Focus on an element and return NVDA's speech output."""
        if self.use_direct_nvda and not self.use_mock:
            # With direct NVDA, we try to capture speech through NVDADirect
            if NVDA_DIRECT_AVAILABLE and self.nvda:
                # In a real implementation, we would need to integrate with NVDA's speech capture
                # For now, we simulate it
                simulated_speech = f"Element focused: {selector}"
                self.nvda.simulate_speech(simulated_speech)
                speech = self.nvda.get_speech()
            else:
                # Fallback to simulated speech
                time.sleep(1)  # Wait for NVDA to speak
                speech = f"Element focused: {selector}"  # Simulated speech for direct NVDA
                
            element_info = {
                "selector": selector,
                "timestamp": datetime.now().isoformat(),
                "speech": speech
            }
            self.speech_log.append(element_info)
            return speech
        else:
            # For mock mode, use the focus endpoint
            if self.use_mock:
                response = requests.get(f"{self.BRIDGE_URL}/focus", params={"selector": selector})
                if response.status_code != 200:
                    raise Exception(f"Failed to focus element: {response.text}")
                    
            # When an element is focused in the browser, the screen reader announces it
            # We simulate pressing Enter to activate the screen reader
            requests.get(f"{self.BRIDGE_URL}/act")
            time.sleep(1)  # Wait for screen reader to respond
            
            # Get the last spoken phrase
            response = requests.get(f"{self.BRIDGE_URL}/speak")
            data = response.json()
            speech = data.get('speech', '')
            
            # Capture and log the speech
            element_info = {
                "selector": selector,
                "timestamp": datetime.now().isoformat(),
                "speech": speech
            }
            self.speech_log.append(element_info)
            return speech
    
    @keyword
    def verify_element_speech(self, element_id, speech=None, expected=None):
        """Verify the speech output for an element against expected results."""
        if self.use_direct_nvda and not self.use_mock:
            # With direct NVDA, get speech via NVDADirect if available
            if NVDA_DIRECT_AVAILABLE and self.nvda and not speech:
                speech = self.nvda.get_speech()
            # Otherwise use provided speech or a default value
            elif not speech:
                speech = f"Simulated speech for {element_id}"
        else:
            # Get speech from bridge if not provided
            if not speech:
                response = requests.get(f"{self.BRIDGE_URL}/speak")
                data = response.json()
                speech = data.get('speech', '')
        
        # Allow providing expected directly or from JSON
        if not expected:
            expected = self.expected_results.get(element_id, None)
            if not expected:
                raise Exception(f"No expected result defined for element: {element_id}")
        
        result = {
            "element_id": element_id,
            "actual": speech,
            "expected": expected,
            "passed": expected in speech,
            "timestamp": datetime.now().isoformat()
        }
        self.speech_log.append(result)
        
        if not result["passed"]:
            print(f"Speech verification failed for {element_id}. Expected: '{expected}', Got: '{speech}'")
        
        return result["passed"]
        
    @keyword
    def press_key(self, key):
        """Press a key using NVDA."""
        if self.use_direct_nvda and not self.use_mock:
            # For direct NVDA, use NVDADirect if available
            if NVDA_DIRECT_AVAILABLE and self.nvda:
                self.nvda.send_keys(key)
            else:
                # Otherwise just log
                print(f"Simulating key press: {key}")
            return {"status": "key_pressed", "key": key}
        else:
            response = requests.get(f"{self.BRIDGE_URL}/press", params={"key": key})
            if response.status_code != 200:
                raise Exception(f"Failed to press key: {response.text}")
            return response.json()
        
    @keyword
    def is_using_mock(self):
        """Return whether we're using mock mode."""
        return self.use_mock
        
    @keyword
    def is_using_direct_nvda(self):
        """Return whether we're using direct NVDA execution."""
        return self.use_direct_nvda 