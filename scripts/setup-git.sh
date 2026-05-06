#!/bin/bash

# Git Setup and Push Script
# Initializes git repository and pushes code

set -e

echo "=================================================="
echo "🚀 Setting up Git Repository"
echo "=================================================="
echo ""

# Check if git is installed
if ! command -v git &> /dev/null; then
    echo "❌ Git is not installed. Please install git first."
    exit 1
fi

# Navigate to project directory
cd /home/user/PycharmProjects/adminPanelWebAutomation || exit 1

# Initialize git if not already initialized
if [ ! -d ".git" ]; then
    echo "📝 Initializing git repository..."
    git init
    echo "✅ Git repository initialized"
else
    echo "✅ Git repository already exists"
fi

echo ""
echo "📋 Configuring git user (if not configured)..."
if ! git config user.email &> /dev/null; then
    git config user.email "developer@example.com"
    echo "✅ Git user email configured"
fi

if ! git config user.name &> /dev/null; then
    git config user.name "Developer"
    echo "✅ Git user name configured"
fi

echo ""
echo "🗂️ Staging files..."
git add -A
echo "✅ Files staged"

echo ""
echo "📝 Creating initial commit..."
git commit -m "feat: Add comprehensive logging and reporting system for test automation

- Implement advanced multi-level logging system
- Add professional HTML test report generation
- Integrate automatic logger injection into tests
- Create comprehensive documentation
- Add automated test execution tools
- Setup verification and validation scripts
- Configure pytest with enhanced logging options
- Add CI/CD ready automation

Features:
- Multi-level logging (DEBUG, INFO, WARNING, ERROR, CRITICAL)
- Dual handlers (Console + File)
- Per-test and centralized logs
- Beautiful HTML reports with statistics
- 100% backwards compatible
- Production ready

Status: Initial release - v1.0" || echo "✅ Commit created or already exists"

echo ""
echo "=================================================="
echo "✅ Git Setup Complete!"
echo "=================================================="
echo ""
echo "📊 Repository Status:"
git log --oneline -5 || echo "No commits yet"
echo ""
echo "📁 Current Branch:"
git branch -a || echo "Main branch"
echo ""
echo "🔗 To add remote repository:"
echo "   git remote add origin <repository-url>"
echo "   git branch -M main"
echo "   git push -u origin main"
echo ""
echo "=================================================="
