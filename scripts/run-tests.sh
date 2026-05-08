#!/bin/bash
# Quick start script for running tests with logging and report generation

set -e

echo "=========================================="
echo "🧪 Admin Panel Test Automation"
echo "=========================================="
echo ""

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is not installed"
    exit 1
fi

# Check if pytest is installed
if ! python3 -m pytest --version &> /dev/null; then
    echo "⚠️  Pytest not found. Installing dependencies..."
    python3 -m pip install -r requirements.txt
fi

# Show available options
echo "📋 Available Options:"
echo "  1. Run all tests with logging"
echo "  2. Run smoke tests only"
echo "  3. Run tests with full report generation"
echo "  4. Generate report from existing logs"
echo "  5. Open comprehensive report"
echo ""

read -p "Select option (1-5): " option

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
PROJECT_DIR="$(dirname "$SCRIPT_DIR")"
cd "$PROJECT_DIR"

case $option in
    1)
        echo "🚀 Running all tests with logging..."
        python3 -m pytest tests/ -v --log-cli-level=INFO
        ;;
    2)
        echo "🚀 Running smoke tests..."
        python3 -m pytest -m smoke -v --log-cli-level=INFO
        ;;
    3)
        echo "🚀 Running tests with full report generation..."
        python3 "$SCRIPT_DIR/run-tests-with-report.py"
        ;;
    4)
        echo "📊 Generating report from existing logs..."
        python3 "$PROJECT_DIR/report-generators/generate-comprehensive-report.py"
        ;;
    5)
        echo "🌐 Opening comprehensive report..."
        if [ -f "test-results/comprehensive-test-report.html" ]; then
            if command -v xdg-open &> /dev/null; then
                xdg-open test-results/comprehensive-test-report.html
            elif command -v open &> /dev/null; then
                open test-results/comprehensive-test-report.html
            else
                echo "📁 Report location: test-results/comprehensive-test-report.html"
            fi
        else
            echo "❌ Report not found. Run tests first (option 3)."
        fi
        ;;
    *)
        echo "❌ Invalid option"
        exit 1
        ;;
esac

echo ""
echo "=========================================="
echo "✅ Done!"
echo "=========================================="
