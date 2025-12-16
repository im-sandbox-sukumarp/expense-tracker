#!/usr/bin/env python3
"""
Test Runner Script for Expense Tracker Application.

This module provides a command-line interface to run all tests for the
Expense Tracker application with coverage reporting capabilities.

The script supports various coverage report formats including terminal
output, HTML reports, and XML reports suitable for CI/CD pipelines.

Example:
    Run tests with default settings::

        $ python run_tests.py

    Run tests with verbose output and HTML coverage report::

        $ python run_tests.py --verbose --html

    Generate XML coverage report for CI/CD::

        $ python run_tests.py --xml

Attributes:
    None

Functions:
    main: The main entry point for the test runner.
"""

import argparse
import os
import sys

import pytest


def main() -> int:
    """
    Run the test suite with coverage reporting.

    Parses command-line arguments to determine which coverage reports
    to generate and runs pytest with the appropriate configuration.

    Returns:
        int: The exit code from pytest. Returns 0 if all tests pass,
            non-zero otherwise.

    Command-line Arguments:
        --html: Generate an HTML coverage report in the htmlcov/ directory.
        --xml: Generate an XML coverage report as coverage.xml.
        --verbose, -v: Enable verbose output during test execution.

    Example:
        >>> exit_code = main()
        >>> print(f"Tests completed with exit code: {exit_code}")
    """
    parser = argparse.ArgumentParser(
        description="Run tests for Expense Tracker with coverage."
    )
    parser.add_argument(
        "--html",
        action="store_true",
        help="Generate HTML coverage report"
    )
    parser.add_argument(
        "--xml",
        action="store_true",
        help="Generate XML coverage report for CI/CD"
    )
    parser.add_argument(
        "--verbose", "-v",
        action="store_true",
        help="Verbose output"
    )
    args: argparse.Namespace = parser.parse_args()

    # Add the parent directory to sys.path
    sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

    # Build pytest arguments
    pytest_args: list[str] = []

    if args.verbose:
        pytest_args.append("-v")

    # Always run with coverage
    pytest_args.append("--cov=app")
    pytest_args.append("--cov-report=term")

    # Add HTML coverage report if requested
    if args.html:
        pytest_args.append("--cov-report=html")
        print("HTML coverage report will be generated in htmlcov/ directory")

    # Add XML coverage report if requested (useful for CI/CD)
    if args.xml:
        pytest_args.append("--cov-report=xml")
        print("XML coverage report will be generated as coverage.xml")

    # Add the tests directory
    pytest_args.append("tests/")

    # Run pytest with constructed arguments
    exit_code: pytest.ExitCode = pytest.main(pytest_args)

    # Display coverage information
    if exit_code == 0:
        print("\n✅ All tests passed!")

    # Exit with pytest's exit code
    return int(exit_code)


if __name__ == "__main__":
    sys.exit(main())
