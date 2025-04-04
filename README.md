# Accessibility Testing Framework with NVDA

This framework provides automated accessibility testing using the NVDA screen reader on Windows, integrating Playwright, Guidepup, and Robot Framework.

## Features

- Direct control of installed NVDA screen reader
- Automated UI element interaction with speech capture
- Integration with Robot Framework and Playwright
- Screenshot capture for visual verification
- Speech output simulation and validation
- Proper NVDA lifecycle management (start before tests, close after completion)

## Prerequisites

1. Windows machine with NVDA screen reader installed at default location (`C:\Program Files (x86)\NVDA\nvda.exe`)
2. Python 3.7+ installed
3. Node.js (optional - for mock NVDA mode)
4. Git (for version control)

## Installation

1. Clone the repository:

```bash
git clone https://github.com/rvkvit/AccessibilityTestAutomationWithGuidePup.git
cd AccessibilityTestAutomationWithGuidePup
```

2. Create a virtual environment:

```bash
python -m venv accessibility_venv
accessibility_venv\Scripts\activate
```

3. Install the dependencies:

```bash
pip install -r requirements.txt
```

4. Initialize the Playwright browser:

```bash
python -m playwright install
rfbrowser init
```

## Running Tests

To run the accessibility tests with the real NVDA screen reader:

```bash
python run_nvda_test.py
```

This will:
- Start NVDA screen reader (if not already running)
- Run the Robot Framework tests
- Capture NVDA speech output (simulated in current version)
- Generate test reports and screenshots
- Automatically stop NVDA when tests complete

## Framework Structure

- `resources/`: Contains the GuidepupLibrary and NVDA integration modules
  - `GuidepupLibrary.py`: Main library for controlling NVDA
  - `nvda_direct.py`: Direct NVDA control module
  - `mock_nvda.js`: (Optional) Mock NVDA implementation for development
- `tests/`: Test case files
  - `real_nvda_test.robot`: Tests using real NVDA
- `results/`: Test results, logs, and screenshots
- Helper scripts:
  - `push_to_github.bat`: Windows script for pushing to GitHub
  - `push_to_github.sh`: Bash script for pushing to GitHub

## NVDA Integration Modes

The framework supports two modes:

1. **Direct NVDA Mode** - Controls the actual installed NVDA screen reader (current implementation)
2. **Mock NVDA Mode** - Uses a Node.js bridge to simulate NVDA (for development without NVDA)

## Customizing Tests

To add new test cases:
1. Create a new Robot Framework test file or add tests to existing files
2. Use the provided keywords from Browser and GuidepupLibrary
3. Run the tests using the provided script

## NVDA Lifecycle Management

The framework ensures proper NVDA lifecycle management:

1. Before tests start:
   - Checks if NVDA is already running
   - If running, stops the existing instance
   - Starts a fresh NVDA instance
   
2. After tests complete:
   - Automatically stops NVDA
   - Verifies NVDA process is terminated
   - Forces termination if needed

This ensures tests run with a clean NVDA instance and don't leave NVDA running after completion.

## Contributing to the Repository

To contribute to this project:

1. Fork the repository on GitHub
2. Create a new branch for your changes
3. Make your changes and commit them
4. Push your changes to your fork
5. Submit a pull request

## Deploying Changes to GitHub

After making changes to the framework, you can use one of the provided scripts:

### Windows:
```
push_to_github.bat "Your commit message here"
```

### Linux/Mac:
```
./push_to_github.sh "Your commit message here"
```

Or manually with these commands:

```bash
# Add all changed files
git add .

# Commit the changes
git commit -m "Description of changes made"

# Push to GitHub repository
git push origin main
```

## Future Enhancements

- Improved speech capture from real NVDA
- Support for additional screen readers
- Comparison of expected vs. actual speech patterns
- Integration with CI/CD pipelines

## Troubleshooting

- **NVDA Not Found**: Ensure NVDA is installed at the default location or update the path in the code
- **Test Failures**: Check the selector specificity - make sure selectors target exactly one element
- **Speech Not Captured**: Current implementation uses simulated speech - future versions will capture real NVDA output
- **NVDA Doesn't Close**: If NVDA remains running after tests, manually terminate it through Task Manager 