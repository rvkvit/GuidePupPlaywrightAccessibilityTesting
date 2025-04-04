*** Settings ***
Documentation    Simple accessibility test using mock NVDA
Library    Browser
Library    ${EXECDIR}${/}resources${/}GuidepupLibrary.py
Library    OperatingSystem
Library    Collections
Library    RequestsLibrary

Suite Setup    Setup Suite
Suite Teardown    Teardown Suite

*** Variables ***
${URL}    https://sitaksasiointi.lahitapiola.fi/developer/rls-mock-redirection
${BROWSER}    chromium
${MOCK_URL}    http://localhost:3000

*** Test Cases ***
Test Website Accessibility
    [Documentation]    Tests a single element to confirm the framework is working
    New Browser    browser=${BROWSER}    headless=False
    New Page    ${URL}
    Set Viewport Size    1920    1080
    Sleep    2s
    
    # Log page content for debugging
    ${page_content}=    Get Page Source
    Log    ${page_content}
    
    # Take a screenshot
    Take Screenshot    filename=screenshot.png
    
    # Test just one simple element - any h1 on the page
    ${elements}=    Get Elements    h1
    ${count}=    Get Length    ${elements}
    Log    Number of H1 elements found: ${count}
    
    # Manually use the mock NVDA through our library
    ${params}=    Create Dictionary    selector=h1
    ${response}=    GET    ${MOCK_URL}/focus    params=${params}
    Log    ${response.text}
    
    ${speech_resp}=    GET    ${MOCK_URL}/speak
    Log    ${speech_resp.text}
    
    ${speech_json}=    Evaluate    json.loads('''${speech_resp.text}''')    json
    Should Contain    ${speech_json}[speech]    heading
    
    # Clean up
    Close Browser

*** Keywords ***
Setup Suite
    Log    Starting simple test with mock NVDA
    Initialize NVDA    use_mock=False
    
    # Initialize expected results
    ${expected_results}=    Create Dictionary
    Set To Dictionary    ${expected_results}    heading    heading level
    ${json_str}=    Evaluate    json.dumps($expected_results, indent=2)    json
    Create File    ${EXECDIR}${/}resources${/}expected_results.json    ${json_str}
    Load Expected Results    ${EXECDIR}${/}resources${/}expected_results.json

Teardown Suite
    Shutdown NVDA 