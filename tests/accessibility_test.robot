*** Settings ***
Documentation    Accessibility testing for LähiTapiola using NVDA screen reader
Resource    ${EXECDIR}${/}keywords${/}accessibility_keywords.robot
Suite Setup    Setup Suite
Suite Teardown    Teardown Suite
Test Setup    Test Setup
Test Teardown    Test Teardown

*** Variables ***
${URL}    https://sitaksasiointi.lahitapiola.fi/developer/rls-mock-redirection
${BROWSER}    chromium

*** Test Cases ***
Verify Header Accessibility
    [Documentation]    Verifies that headers are properly announced by NVDA
    Test Header Accessibility    h1    main_header
    
Verify Input Field Accessibility
    [Documentation]    Verifies that input fields are properly announced by NVDA
    Test Textbox Accessibility    input[type="text"]    username_field    TestUser
    
Verify Password Field Accessibility
    [Documentation]    Verifies that password fields are properly announced by NVDA
    Test Textbox Accessibility    input[type="password"]    password_field    TestPassword123
    
Verify Button Accessibility
    [Documentation]    Verifies that buttons are properly announced by NVDA
    Test Button Accessibility    button[type="submit"]    submit_button
    
Verify Checkbox Accessibility
    [Documentation]    Verifies that checkboxes are properly announced by NVDA
    Test Button Accessibility    input[type="checkbox"]    checkbox
    
*** Keywords ***
Setup Suite
    Log    Starting accessibility testing suite with NVDA
    Setup NVDA For Testing

Teardown Suite
    Teardown NVDA
    Log    Completed accessibility testing suite with NVDA

Test Setup
    Open Application    ${URL}    ${BROWSER}
    
Test Teardown
    Close Browser 