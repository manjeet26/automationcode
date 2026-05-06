#!/usr/bin/env python3
"""
Setup and Verification Script for Logging & Reporting System
Verifies all components are properly installed and configured
"""

import os
import sys
import subprocess
from pathlib import Path
from datetime import datetime


class Colors:
    """Terminal colors for output"""
    GREEN = '\033[92m'
    RED = '\033[91m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    RESET = '\033[0m'
    BOLD = '\033[1m'


def print_header(text):
    """Print header"""
    print(f"\n{Colors.BOLD}{Colors.BLUE}{'='*70}{Colors.RESET}")
    print(f"{Colors.BOLD}{Colors.BLUE}{text.center(70)}{Colors.RESET}")
    print(f"{Colors.BOLD}{Colors.BLUE}{'='*70}{Colors.RESET}\n")


def print_success(text):
    """Print success message"""
    print(f"{Colors.GREEN}✓ {text}{Colors.RESET}")


def print_error(text):
    """Print error message"""
    print(f"{Colors.RED}✗ {text}{Colors.RESET}")


def print_warning(text):
    """Print warning message"""
    print(f"{Colors.YELLOW}⚠ {text}{Colors.RESET}")


def print_info(text):
    """Print info message"""
    print(f"{Colors.BLUE}ℹ {text}{Colors.RESET}")


def check_python():
    """Check Python version"""
    print_info("Checking Python version...")
    version = sys.version_info
    if version.major >= 3 and version.minor >= 7:
        print_success(f"Python {version.major}.{version.minor}.{version.micro} found")
        return True
    else:
        print_error(f"Python 3.7+ required, found {version.major}.{version.minor}.{version.micro}")
        return False


def check_dependencies():
    """Check if required packages are installed"""
    print_info("Checking required dependencies...")
    
    required_packages = {
        'pytest': 'pytest',
        'pytest_html': 'pytest-html',
        'playwright': 'playwright',
        'pytest_playwright': 'pytest-playwright'
    }
    
    missing = []
    for package_name, display_name in required_packages.items():
        try:
            __import__(package_name)
            print_success(f"{display_name} is installed")
        except ImportError:
            print_error(f"{display_name} is NOT installed")
            missing.append(display_name)
    
    if missing:
        print_warning(f"Missing packages: {', '.join(missing)}")
        print_info("Installing missing packages...")
        subprocess.run([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"], check=False)
        return False
    
    return True


def check_directory_structure():
    """Check project directory structure"""
    print_info("Checking project structure...")
    
    required_files = {
        'utils/logger.py': 'Logger configuration',
        'tests/conftest.py': 'Pytest configuration',
        'pytest.ini': 'Pytest settings',
        'run-tests-with-report.py': 'Test runner',
        'generate-comprehensive-report.py': 'Report generator',
    }
    
    required_dirs = {
        'tests': 'Tests directory',
        'utils': 'Utils directory',
        'pages': 'Pages directory',
    }
    
    missing_files = []
    missing_dirs = []
    
    # Check files
    for file_path, description in required_files.items():
        if Path(file_path).exists():
            print_success(f"{description}: {file_path}")
        else:
            print_error(f"{description} NOT FOUND: {file_path}")
            missing_files.append(file_path)
    
    # Check directories
    for dir_path, description in required_dirs.items():
        if Path(dir_path).is_dir():
            print_success(f"{description}: {dir_path}/")
        else:
            print_error(f"{description} NOT FOUND: {dir_path}/")
            missing_dirs.append(dir_path)
    
    return len(missing_files) == 0 and len(missing_dirs) == 0


def check_logger_implementation():
    """Check logger implementation"""
    print_info("Checking logger implementation...")
    
    logger_file = Path('utils/logger.py')
    if not logger_file.exists():
        print_error("Logger file not found")
        return False
    
    with open(logger_file, 'r') as f:
        content = f.read()
    
    checks = {
        'LoggerConfig': 'LoggerConfig class',
        'setup_logging': 'setup_logging method',
        'get_logger': 'get_logger function',
        'Formatter': 'Log formatting',
    }
    
    all_found = True
    for check_str, description in checks.items():
        if check_str in content:
            print_success(f"{description} found")
        else:
            print_error(f"{description} NOT found")
            all_found = False
    
    return all_found


def check_conftest_configuration():
    """Check conftest.py configuration"""
    print_info("Checking conftest.py configuration...")
    
    conftest_file = Path('tests/conftest.py')
    if not conftest_file.exists():
        print_error("conftest.py not found")
        return False
    
    with open(conftest_file, 'r') as f:
        content = f.read()
    
    checks = {
        'pytest_configure': 'pytest_configure hook',
        'pytest_runtest_setup': 'pytest_runtest_setup hook',
        '@pytest.fixture': 'Pytest fixtures',
        'logger': 'Logger fixture',
        'LoggerConfig': 'LoggerConfig usage',
    }
    
    all_found = True
    for check_str, description in checks.items():
        if check_str in content:
            print_success(f"{description} found")
        else:
            print_error(f"{description} NOT found")
            all_found = False
    
    return all_found


def check_pytest_configuration():
    """Check pytest.ini configuration"""
    print_info("Checking pytest.ini configuration...")
    
    pytest_ini = Path('pytest.ini')
    if not pytest_ini.exists():
        print_error("pytest.ini not found")
        return False
    
    with open(pytest_ini, 'r') as f:
        content = f.read()
    
    checks = {
        '--log-cli': 'Console logging',
        '--log-file': 'File logging',
        '--log-file-level=DEBUG': 'File log level',
        '--html': 'HTML report',
        '--tb=short': 'Traceback format',
    }
    
    all_found = True
    for check_str, description in checks.items():
        if check_str in content:
            print_success(f"{description} configured")
        else:
            print_warning(f"{description} NOT configured")
            all_found = False
    
    return all_found


def verify_log_directory():
    """Verify/create log directory"""
    print_info("Verifying log directory...")
    
    log_dir = Path('test-results/logs')
    try:
        log_dir.mkdir(parents=True, exist_ok=True)
        print_success(f"Log directory ready: {log_dir}")
        return True
    except Exception as e:
        print_error(f"Failed to create log directory: {e}")
        return False


def test_logger_functionality():
    """Test logger functionality"""
    print_info("Testing logger functionality...")
    
    try:
        from utils.logger import LoggerConfig, get_logger
        
        # Test LoggerConfig.setup_logging()
        logger = LoggerConfig.setup_logging("verification_test")
        logger.info("✓ Logger successfully created and configured")
        print_success("Logger initialization works")
        
        # Test get_logger()
        logger2 = get_logger("test_logger")
        print_success("get_logger() works")
        
        # Check if log file was created
        log_files = list(Path('test-results/logs').glob('verification_test_*.log'))
        if log_files:
            print_success(f"Log file created: {log_files[0].name}")
            return True
        else:
            print_warning("Log file not found (may be expected)")
            return True
            
    except Exception as e:
        print_error(f"Logger test failed: {e}")
        return False


def test_pytest_execution():
    """Test pytest execution"""
    print_info("Testing pytest execution...")
    
    try:
        result = subprocess.run(
            [sys.executable, "-m", "pytest", "--version"],
            capture_output=True,
            text=True
        )
        
        if result.returncode == 0:
            print_success(f"Pytest working: {result.stdout.strip()}")
            return True
        else:
            print_error(f"Pytest error: {result.stderr}")
            return False
            
    except Exception as e:
        print_error(f"Pytest test failed: {e}")
        return False


def generate_summary(results):
    """Generate verification summary"""
    print_header("Verification Summary")
    
    total = len(results)
    passed = sum(1 for v in results.values() if v)
    failed = total - passed
    
    print(f"Total checks: {total}")
    print(f"{Colors.GREEN}Passed: {passed}{Colors.RESET}")
    
    if failed > 0:
        print(f"{Colors.RED}Failed: {failed}{Colors.RESET}")
    
    print(f"\nResult: {Colors.GREEN}{'PASS' if failed == 0 else 'FAIL'}{Colors.RESET}")
    
    if failed > 0:
        print("\nNext steps:")
        print("1. Review the errors above")
        print("2. Install missing packages: pip install -r requirements.txt")
        print("3. Ensure all files are in correct locations")
        print("4. Run this verification script again")
    else:
        print("\n✓ All checks passed!")
        print("\nYou're ready to run tests:")
        print("  • python run-tests-with-report.py")
        print("  • pytest tests/ -v --log-cli=true")
        print("  • ./run-tests.sh")


def main():
    """Main verification flow"""
    print_header("Logging & Reporting System Verification")
    print(f"Started at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
    
    results = {}
    
    # Run checks
    results['Python Version'] = check_python()
    results['Dependencies'] = check_dependencies()
    results['Directory Structure'] = check_directory_structure()
    results['Logger Implementation'] = check_logger_implementation()
    results['Conftest Configuration'] = check_conftest_configuration()
    results['Pytest Configuration'] = check_pytest_configuration()
    results['Log Directory'] = verify_log_directory()
    results['Logger Functionality'] = test_logger_functionality()
    results['Pytest Execution'] = test_pytest_execution()
    
    # Generate summary
    print("\n")
    generate_summary(results)
    
    print_info(f"\nCompleted at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    # Return exit code
    failed = sum(1 for v in results.values() if not v)
    return 0 if failed == 0 else 1


if __name__ == "__main__":
    exit_code = main()
    sys.exit(exit_code)
