@echo off
REM Script to push the Accessibility Testing Framework to GitHub
REM Usage: push_to_github.bat "Your commit message here"

setlocal

REM Configuration
set REPO_URL=https://github.com/rvkvit/AccessibilityTestAutomationWithGuidePup.git

REM Check if git is installed
where git >nul 2>nul
if %ERRORLEVEL% neq 0 (
    echo Error: git is not installed. Please install git first.
    exit /b 1
)

REM Check for commit message
if "%~1"=="" (
    echo Please provide a commit message
    echo Usage: push_to_github.bat "Your commit message here"
    exit /b 1
)

set COMMIT_MESSAGE=%~1

REM Check if this is a git repository
if not exist .git (
    echo Initializing git repository...
    git init
    git remote add origin %REPO_URL%
    if %ERRORLEVEL% neq 0 (
        echo Error: Failed to add remote repository. Please check if you have access to %REPO_URL%
        exit /b 1
    )
)

REM Check if remote exists
git remote | findstr "origin" >nul
if %ERRORLEVEL% neq 0 (
    echo Adding remote repository...
    git remote add origin %REPO_URL%
)

REM Add all files
echo Adding files to git...
git add .

REM Commit changes
echo Committing changes with message: '%COMMIT_MESSAGE%'
git commit -m "%COMMIT_MESSAGE%"

REM Pull latest changes to avoid conflicts
echo Pulling latest changes from remote...
git pull --rebase origin main

REM Push to GitHub
echo Pushing changes to GitHub...
git push origin main

if %ERRORLEVEL% equ 0 (
    echo Success! Your changes have been pushed to GitHub
    echo Repository URL: %REPO_URL%
) else (
    echo Error: Failed to push changes to GitHub
    echo Please check your GitHub credentials and repository access
    exit /b 1
)

endlocal 