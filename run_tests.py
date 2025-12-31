#!/usr/bin/env python3
"""
Test runner script for the Living Architecture Resume project.
"""
import subprocess
import sys
import os
from pathlib import Path


def run_command(command, description):
    """Run a command and handle errors."""
    print(f"\n🧪 {description}")
    print(f"Running: {' '.join(command)}")
    
    try:
        result = subprocess.run(command, check=True, capture_output=True, text=True)
        print(f"✅ {description} - PASSED")
        if result.stdout:
            print(result.stdout)
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ {description} - FAILED")
        if e.stdout:
            print("STDOUT:", e.stdout)
        if e.stderr:
            print("STDERR:", e.stderr)
        return False


def main():
    """Main test runner."""
    print("🚀 Living Architecture Resume - Test Suite")
    print("=" * 50)
    
    # Change to project root
    project_root = Path(__file__).parent
    os.chdir(project_root)
    
    # Check if pytest is installed
    try:
        subprocess.run(["pytest", "--version"], check=True, capture_output=True)
    except (subprocess.CalledProcessError, FileNotFoundError):
        print("❌ pytest not found. Please install test dependencies:")
        print("pip install -r tests/requirements.txt")
        sys.exit(1)
    
    success_count = 0
    total_tests = 0
    
    # Test categories to run
    test_categories = [
        (["pytest", "tests/test_api_*.py", "-v"], "API Tests"),
        (["pytest", "tests/test_scripts_*.py", "-v"], "Script Tests"),
        (["pytest", "tests/test_*_properties*.py", "-v"], "Property-Based Tests"),
        (["pytest", "tests/", "--cov=api", "--cov=scripts", "--cov-report=term-missing"], "Full Test Suite with Coverage"),
    ]
    
    for command, description in test_categories:
        total_tests += 1
        if run_command(command, description):
            success_count += 1
    
    # Frontend tests (if Node.js is available)
    if os.path.exists("frontend/package.json"):
        print("\n🧪 Frontend Tests")
        frontend_commands = [
            (["npm", "test", "--prefix", "frontend"], "Frontend Unit Tests"),
            (["npx", "tsc", "--noEmit", "--project", "frontend"], "TypeScript Type Checking"),
        ]
        
        for command, description in frontend_commands:
            total_tests += 1
            if run_command(command, description):
                success_count += 1
    
    # Summary
    print("\n" + "=" * 50)
    print(f"📊 Test Summary: {success_count}/{total_tests} test categories passed")
    
    if success_count == total_tests:
        print("🎉 All tests passed!")
        sys.exit(0)
    else:
        print("💥 Some tests failed!")
        sys.exit(1)


if __name__ == "__main__":
    main()