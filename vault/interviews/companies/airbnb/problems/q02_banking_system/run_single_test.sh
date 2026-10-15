#!/bin/sh
# Mirrors CodeSignal's locked runner. Usage: bash run_single_test.sh "case_05"   (IMPL=starter to test your file)
cd "$(dirname "$0")" && python3 -m unittest discover -s tests -p "test_*.py" -k "$1" 2>&1
