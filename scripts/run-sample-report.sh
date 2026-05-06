#!/bin/bash
cd /home/user/PycharmProjects/adminPanelWebAutomation
python3 generate-sample-report.py
echo ""
echo "📖 Full report with logs available at:"
echo "   test-results/sample-test-results.html"
echo ""
echo "✨ Open in browser to view:"
ls -lh test-results/sample-test-results.html 2>/dev/null && echo "   ✅ File ready to open!"
