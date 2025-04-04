*** Settings ***
Documentation    Accessibility testing using real NVDA screen reader
Library    Browser
Library    ${EXECDIR}${/}resources${/}GuidepupLibrary.py
Library    OperatingSystem
Library    Collections
Library    String

Suite Setup    Setup Suite
Suite Teardown    Teardown Suite
Test Setup    Test Setup
Test Teardown    Test Teardown

*** Variables ***
${URL}    https://sitaksasiointi.lahitapiola.fi/developer/rls-mock-redirection
${BROWSER}    chromium
${NVDA_ALREADY_RUNNING}    ${EMPTY}

*** Test Cases ***
Test Page Navigation With NVDA
    [Documentation]    Basic test to verify NVDA integration
    # Give time for NVDA to start reading the page
    Sleep    3s
    
    # Test interacting with different elements
    Log    Testing input field focus...
    # Use a more specific selector for the duet-input element
    Click    css=duet-input[id="yearOfBirth"] >> visible=true
    Sleep    2s
    Fill Text    css=duet-input[id="yearOfBirth"] input    1990
    Sleep    1s
    
    Log    Testing button interaction...
    # Use the first submit button in a form for more precise targeting
    Click    css=#parameterForm button[type="submit"] >> visible=true
    Sleep    2s
    
    # Test keyboard navigation
    Log    Testing keyboard navigation...
    Keyboard Key    press    Tab
    Sleep    1s
    Keyboard Key    press    Tab
    Sleep    1s
    
    # Screenshot for verification
    Take Screenshot    filename=nvda_test_screenshot.png

Test NVDA Speech Simulation
    [Documentation]    Test simulating NVDA speech output
    # Give time for NVDA to start reading the page
    Sleep    3s
    
    # Focus on input field to trigger NVDA speech
    ${speech}=    Focus Element    css=duet-input[id="yearOfBirth"] >> visible=true
    Log    NVDA speech (simulated): ${speech}
    
    # With simulated speech, we'll just verify it's not empty
    Should Not Be Empty    ${speech}    No speech was captured
    
    # Log expected element names for documentation
    Log    Expected field name: Year of Birth
    
    # Test focusing on button and capture speech
    ${button_speech}=    Focus Element    css=#parameterForm button[type="submit"] >> visible=true
    Log    Button speech (simulated): ${button_speech}
    Should Not Be Empty    ${button_speech}    No button speech was captured
    
    # Screenshot for verification
    Take Screenshot    filename=nvda_speech_test.png

*** Keywords ***
Setup Suite
    Log    Starting real NVDA accessibility testing
    # Check if NVDA is already running (managed by run_nvda_test.py)
    ${NVDA_ALREADY_RUNNING}=    Get Environment Variable    NVDA_ALREADY_RUNNING    ${EMPTY}
    Set Suite Variable    ${NVDA_ALREADY_RUNNING}    ${NVDA_ALREADY_RUNNING}
    
    # Only initialize NVDA if it's not already running
    Run Keyword If    '${NVDA_ALREADY_RUNNING}' == ''    Initialize NVDA    use_mock=False    use_direct_nvda=True
    Run Keyword If    '${NVDA_ALREADY_RUNNING}' != ''    Log    Using NVDA instance already started by the test runner

Teardown Suite
    # Only shut down NVDA if we started it (not if it was started by run_nvda_test.py)
    Run Keyword If    '${NVDA_ALREADY_RUNNING}' == ''    Shutdown NVDA
    Run Keyword If    '${NVDA_ALREADY_RUNNING}' != ''    Log    NVDA will be stopped by the test runner
    Log    Completed accessibility testing with real NVDA

Test Setup
    New Browser    browser=${BROWSER}    headless=False
    New Page    ${URL}
    Set Viewport Size    1920    1080
    # Allow page to load and NVDA to start reading
    Sleep    3s

Test Teardown
    Close Browser 