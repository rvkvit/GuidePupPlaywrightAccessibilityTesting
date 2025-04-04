*** Settings ***
Library    Browser
Library    ${EXECDIR}${/}resources${/}GuidepupLibrary.py
Library    OperatingSystem
Library    String

*** Keywords ***
Open Application
    [Arguments]    ${url}    ${browser}=chromium
    New Browser    browser=${browser}    headless=False
    New Page    ${url}
    Set Viewport Size    1920    1080
    Sleep    2s    # Wait for page to load

Test Button Accessibility
    [Arguments]    ${selector}    ${expected_id}
    Wait For Elements State    ${selector}    visible    timeout=10s
    Click    ${selector}
    Sleep    1s
    ${speech}=    Focus Element    ${selector}
    Verify Element Speech    ${expected_id}    ${speech}
    
Test Textbox Accessibility
    [Arguments]    ${selector}    ${expected_id}    ${test_text}=Test input
    Wait For Elements State    ${selector}    visible    timeout=10s
    Click    ${selector}
    Fill Text    ${selector}    ${test_text}
    Sleep    1s
    ${speech}=    Focus Element    ${selector}
    Verify Element Speech    ${expected_id}    ${speech}

Test Header Accessibility
    [Arguments]    ${selector}    ${expected_id}
    Wait For Elements State    ${selector}    visible    timeout=10s
    ${speech}=    Focus Element    ${selector}
    Verify Element Speech    ${expected_id}    ${speech}

Setup NVDA For Testing
    Initialize NVDA
    ${expected_results_file}=    Set Variable    ${EXECDIR}${/}resources${/}expected_results.json
    ${file_exists}=    Run Keyword And Return Status    File Should Exist    ${expected_results_file}
    Run Keyword If    not ${file_exists}    Create Default Expected Results
    Load Expected Results    ${expected_results_file}

Create Default Expected Results
    ${expected_results}=    Create Dictionary
    # Add default expected speech patterns for various elements
    Set To Dictionary    ${expected_results}    login_button    button
    Set To Dictionary    ${expected_results}    username_field    edit
    Set To Dictionary    ${expected_results}    password_field    password edit
    Set To Dictionary    ${expected_results}    main_header    heading level
    
    # Save to file
    ${json_str}=    Evaluate    json.dumps($expected_results, indent=2)    json
    Create File    ${EXECDIR}${/}resources${/}expected_results.json    ${json_str}

Teardown NVDA
    Shutdown NVDA 