#!/usr/bin/env python3
"""
Project Cleanup and Optimization Script
Removes duplicate files, optimizes code, and prepares for git push
"""

import os
import sys
from pathlib import Path

# Files to remove (duplicates and unnecessary files)
EXTRA_FILES = [
    "generate-sample-report.py",
    "run-sample-report.sh",
    "generate-html-report.js",
    "generate-excel-report.js",
    "inspect-logged-in.js",
    "inspect-page.js",
    "test-logout-popup.js",
    "admin-panel-tests.spec.js",
    "logged-in-page.html",
    "page-structure.html",
    "report.html",
    ".stakpak/",  # Junk directory
]

# Keep these documentation files (essential ones)
KEEP_DOCS = [
    "README.md",  # Main readme
    "START_HERE.md",  # Quick start
    "QUICK_REFERENCE.md",  # Quick reference
    "LOGGING_AND_REPORTING.md",  # Complete guide
]

# Remove these documentation files (consolidated into main docs)
REMOVE_DOCS = [
    "ARCHITECTURE.md",  # Included in main docs
    "COMPLETION_REPORT.md",  # Archived info
    "DELIVERY_SUMMARY.md",  # Archived info
    "FILES_DELIVERED.md",  # Archived info
    "IMPLEMENTATION_SUMMARY.md",  # Archived info
    "INDEX.md",  # Consolidated
    "SETUP_CHECKLIST.md",  # Archived info
    "VISUAL_GUIDE.md",  # Consolidated
    "README_LOGGING_REPORTING.md",  # Deprecated
]


def print_header(text):
    """Print section header"""
    print(f"\n{'='*60}")
    print(f"🚀 {text}")
    print(f"{'='*60}\n")


def remove_files():
    """Remove extra and duplicate files"""
    print_header("Removing Extra Files")
    
    removed = []
    failed = []
    
    for file_path in EXTRA_FILES + REMOVE_DOCS:
        path = Path(file_path)
        try:
            if path.exists():
                if path.is_dir():
                    import shutil
                    shutil.rmtree(path)
                else:
                    path.unlink()
                print(f"✅ Removed: {file_path}")
                removed.append(file_path)
            else:
                print(f"⏭️  Skipped (not found): {file_path}")
        except Exception as e:
            print(f"❌ Failed to remove {file_path}: {e}")
            failed.append(file_path)
    
    return removed, failed


def optimize_code():
    """Optimize Python code files"""
    print_header("Optimizing Code")
    
    python_files = [
        "utils/logger.py",
        "tests/conftest.py",
        "run-tests-with-report.py",
        "verify-setup.py",
        "generate-comprehensive-report.py",
    ]
    
    for file_path in python_files:
        path = Path(file_path)
        if path.exists():
            try:
                # Read file
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                # Remove trailing whitespace
                lines = [line.rstrip() for line in content.split('\n')]
                content = '\n'.join(lines)
                
                # Write back
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(content)
                
                print(f"✅ Optimized: {file_path}")
            except Exception as e:
                print(f"❌ Failed to optimize {file_path}: {e}")
        else:
            print(f"⏭️  Skipped (not found): {file_path}")


def verify_structure():
    """Verify project structure"""
    print_header("Verifying Project Structure")
    
    required_dirs = [
        "tests",
        "pages",
        "utils",
        "data",
        "test-results",
    ]
    
    required_files = [
        "pytest.ini",
        "requirements.txt",
        "README.md",
        "tests/conftest.py",
        "tests/test_smoke.py",
        "utils/logger.py",
    ]
    
    # Check directories
    print("📁 Checking directories:")
    for dir_name in required_dirs:
        if Path(dir_name).exists():
            print(f"  ✅ {dir_name}/")
        else:
            print(f"  ❌ {dir_name}/ (MISSING)")
    
    # Check files
    print("\n📄 Checking files:")
    for file_name in required_files:
        if Path(file_name).exists():
            print(f"  ✅ {file_name}")
        else:
            print(f"  ❌ {file_name} (MISSING)")
    
    # Check documentation
    print("\n📚 Keeping documentation:")
    for doc in KEEP_DOCS:
        if Path(doc).exists():
            print(f"  ✅ {doc}")


def print_summary(removed, failed):
    """Print cleanup summary"""
    print_header("Cleanup Summary")
    
    print(f"📊 Files Removed: {len(removed)}")
    for file in removed:
        print(f"   - {file}")
    
    if failed:
        print(f"\n⚠️  Failed Operations: {len(failed)}")
        for file in failed:
            print(f"   - {file}")
    
    print(f"\n✅ Project cleanup and optimization complete!")
    print(f"\n📝 Next steps:")
    print(f"   1. Review the project structure")
    print(f"   2. Run: python verify-setup.py")
    print(f"   3. Run: bash setup-git.sh")
    print(f"   4. Add remote: git remote add origin <url>")
    print(f"   5. Push: git push -u origin main")


def main():
    """Main execution"""
    try:
        print(f"\n{'='*60}")
        print("🧹 PROJECT CLEANUP AND OPTIMIZATION")
        print(f"{'='*60}")
        
        # Remove extra files
        removed, failed = remove_files()
        
        # Optimize code
        optimize_code()
        
        # Verify structure
        verify_structure()
        
        # Print summary
        print_summary(removed, failed)
        
        return 0
        
    except Exception as e:
        print(f"\n❌ Error during cleanup: {e}")
        return 1


if __name__ == "__main__":
    sys.exit(main())
