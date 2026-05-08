#!/bin/bash

# Push to Bitbucket Repository Script
# Pushes the admin panel test automation code to Bitbucket as regression test cases

set -e

echo "=================================================="
echo "🚀 Pushing Code to Bitbucket Repository"
echo "=================================================="
echo ""

# Navigate to project directory
cd /home/user/PycharmProjects/adminPanelWebAutomation || exit 1

# Check if git repository exists
if [ ! -d ".git" ]; then
    echo "❌ Git repository not found. Please run git-setup.py first."
    exit 1
fi

echo "📋 Checking current git status..."
git status --short

echo ""
echo "🔗 Setting up Bitbucket remote repository..."

# Remove existing origin if it exists
if git remote get-url origin &> /dev/null; then
    echo "Removing existing remote origin..."
    git remote remove origin
fi

# Add Bitbucket remote
echo "Adding Bitbucket remote..."
git remote add origin https://bitbucket.org/girnarsoftware/b2bauction.git

echo "✅ Remote added: https://bitbucket.org/girnarsoftware/b2bauction.git"

echo ""
echo "🔀 Setting branch to master..."
git branch -M master

echo ""
echo "📤 Pushing code to Bitbucket..."
git push -u origin master

echo ""
echo "=================================================="
echo "✅ Code Successfully Pushed to Bitbucket!"
echo "=================================================="
echo ""
echo "🔗 Repository URL: https://bitbucket.org/girnarsoftware/b2bauction/src/master/"
echo ""
echo "📁 Your code should now be visible in the adminpanelWebAutomation folder"
echo ""
echo "=================================================="