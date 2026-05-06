#!/bin/bash

# Cleanup Script - Remove duplicate/extra files
# Keeps the essential files and removes redundant ones

set -e

echo "=================================================="
echo "🧹 Cleaning up project structure"
echo "=================================================="
echo ""

PROJECT_DIR="/home/user/PycharmProjects/adminPanelWebAutomation"
cd "$PROJECT_DIR"

# Files to remove (duplicates and extra files)
EXTRA_FILES=(
    "generate-sample-report.py"
    "run-sample-report.sh"
    "generate-html-report.js"
    "generate-excel-report.js"
    "inspect-logged-in.js"
    "inspect-page.js"
    "test-logout-popup.js"
    "admin-panel-tests.spec.js"
    "logged-in-page.html"
    "page-structure.html"
    "report.html"
)

echo "📋 Files to remove:"
for file in "${EXTRA_FILES[@]}"; do
    if [ -f "$file" ]; then
        echo "   - $file"
        rm -f "$file"
        echo "   ✅ Removed"
    fi
done

echo ""
echo "✅ Cleanup complete!"
echo ""
echo "📁 Project structure optimized:"
ls -la | grep -E "\.py$|\.sh$|\.md$|\.ini$|\.txt$" | awk '{print "   " $NF}'

echo ""
echo "=================================================="
