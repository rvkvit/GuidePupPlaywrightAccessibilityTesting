*** Settings ***
Documentation    Accessibility testing for LähiTapiola site using NVDA screen reader
Resource    ${EXECDIR}${/}keywords${/}accessibility_keywords.robot
Suite Setup    Setup Suite
Suite Teardown    Teardown Suite
Test Setup    Test Setup
Test Teardown    Test Teardown

*** Variables ***
${URL}    https://sitaksasiointi.lahitapiola.fi/developer/rls-mock-redirection
${BROWSER}    chromium

*** Test Cases ***
Verify Page Title Accessibility
    [Documentation]    Verifies that the page title is properly announced by NVDA
    Wait For Elements State    css=duet-heading >> text=RLS    visible    timeout=10s
    Test Header Accessibility    css=duet-heading >> text=RLS    website_title
    
Verify Year Of Birth Field Accessibility
    [Documentation]    Verifies that the year of birth field is properly announced by NVDA
    ${input_selector}=    Set Variable    css=[name="yearOfBirth"][type="text"]
    Wait For Elements State    ${input_selector}    visible    timeout=10s
    Test Textbox Accessibility    ${input_selector}    username_field    1990
    
Verify Application ID Field Accessibility
    [Documentation]    Verifies that the application ID field is properly announced by NVDA
    ${input_selector}=    Set Variable    css=[name="applicationId"].duet-input
    Wait For Elements State    ${input_selector}    visible    timeout=10s
    Test Textbox Accessibility    ${input_selector}    username_field    12345
    
Verify Submit Button Accessibility
    [Documentation]    Verifies that the submit button is properly announced by NVDA
    ${button_selector}=    Set Variable    css=duet-card button.primary
    Wait For Elements State    ${button_selector}    visible    timeout=10s
    Test Button Accessibility    ${button_selector}    submit_button
    
Verify Checkbox Accessibility
    [Documentation]    Verifies that checkboxes are properly announced by NVDA
    ${checkbox_selector}=    Set Variable    css=input#life_insurance
    Wait For Elements State    ${checkbox_selector}    visible    timeout=10s
    Test Button Accessibility    ${checkbox_selector}    checkbox
    
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