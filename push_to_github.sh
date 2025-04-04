#!/bin/bash
# Script to push the Accessibility Testing Framework to GitHub
# Usage: ./push_to_github.sh "Your commit message here"

# Configuration
REPO_URL="https://github.com/rvkvit/AccessibilityTestAutomationWithGuidePup.git"

# Check if git is installed
if ! command -v git &> /dev/null; then
    echo "Error: git is not installed. Please install git first."
    exit 1
fi

# Check for commit message
if [ -z "$1" ]; then
    echo "Please provide a commit message"
    echo "Usage: ./push_to_github.sh \"Your commit message here\""
    exit 1
fi

COMMIT_MESSAGE="$1"

# Check if this is a git repository
if [ ! -d .git ]; then
    echo "Initializing git repository..."
    git init
    git remote add origin $REPO_URL
    if [ $? -ne 0 ]; then
        echo "Error: Failed to add remote repository. Please check if you have access to $REPO_URL"
        exit 1
    fi
fi

# Check if remote exists
if ! git remote | grep -q "origin"; then
    echo "Adding remote repository..."
    git remote add origin $REPO_URL
fi

# Add all files
echo "Adding files to git..."
git add .

# Commit changes
echo "Committing changes with message: '$COMMIT_MESSAGE'"
git commit -m "$COMMIT_MESSAGE"

# Pull latest changes to avoid conflicts
echo "Pulling latest changes from remote..."
git pull --rebase origin main

# Push to GitHub
echo "Pushing changes to GitHub..."
git push origin main

if [ $? -eq 0 ]; then
    echo "Success! Your changes have been pushed to GitHub"
    echo "Repository URL: $REPO_URL"
else
    echo "Error: Failed to push changes to GitHub"
    echo "Please check your GitHub credentials and repository access"
    exit 1
fi 