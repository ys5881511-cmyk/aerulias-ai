#!/bin/bash
# Quality Check Script - Run all code quality checks

set -e

echo "================================"
echo "Aerulias AI - Quality Check"
echo "================================"
echo ""

# Colors
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

total_checks=0
passed_checks=0

run_check() {
    local check_name=$1
    local command=$2
    
    echo -n "Running $check_name... "
    ((total_checks++))
    
    if eval "$command" 2>/dev/null; then
        echo -e "${GREEN}✓ PASSED${NC}"
        ((passed_checks++))
    else
        echo -e "${RED}✗ FAILED${NC}"
    fi
}

# 1. Check if Python files exist
echo -e "${YELLOW}Basic Checks${NC}"
run_check "File existence" "test -f agents/evaluator.py && test -f tests/test_evaluator.py"

# 2. Check syntax errors
echo ""
echo -e "${YELLOW}Python Syntax Checks${NC}"
run_check "Syntax (agents)" "python -m py_compile agents/*.py"
run_check "Syntax (tests)" "python -m py_compile tests/*.py"

# 3. Black formatting
echo ""
echo -e "${YELLOW}Code Formatting${NC}"
if command -v black &> /dev/null; then
    run_check "Black format" "black --check agents/ tests/ 2>/dev/null"
else
    echo -e "${YELLOW}! Black not installed, skipping${NC}"
fi

# 4. Flake8 linting
echo ""
echo -e "${YELLOW}Code Linting${NC}"
if command -v flake8 &> /dev/null; then
    run_check "Flake8 lint" "flake8 agents/ tests/ --max-line-length=100 --ignore=E203,W503 2>/dev/null"
else
    echo -e "${YELLOW}! Flake8 not installed, skipping${NC}"
fi

# 5. mypy type checking
echo ""
echo -e "${YELLOW}Type Checking${NC}"
if command -v mypy &> /dev/null; then
    run_check "mypy types" "mypy agents/ --ignore-missing-imports 2>/dev/null"
else
    echo -e "${YELLOW}! mypy not installed, skipping${NC}"
fi

# 6. Bandit security
echo ""
echo -e "${YELLOW}Security${NC}"
if command -v bandit &> /dev/null; then
    run_check "Bandit security" "bandit -r agents/ -q 2>/dev/null"
else
    echo -e "${YELLOW}! Bandit not installed, skipping${NC}"
fi

# 7. Tests
echo ""
echo -e "${YELLOW}Testing${NC}"
if command -v pytest &> /dev/null; then
    run_check "pytest tests" "pytest tests/ -q 2>/dev/null"
else
    echo -e "${YELLOW}! pytest not installed, skipping${NC}"
fi

# 8. Coverage
echo ""
echo -e "${YELLOW}Coverage${NC}"
if command -v pytest &> /dev/null; then
    run_check "Coverage (>80%)" "pytest tests/ --cov=agents --cov-fail-under=80 -q 2>/dev/null"
else
    echo -e "${YELLOW}! pytest not installed, skipping${NC}"
fi

# Summary
echo ""
echo "================================"
echo "Quality Check Summary"
echo "================================"
echo "Passed: $passed_checks / $total_checks checks"

if [ $passed_checks -eq $total_checks ]; then
    echo -e "${GREEN}✓ All checks passed!${NC}"
    exit 0
else
    echo -e "${RED}✗ Some checks failed${NC}"
    exit 1
fi
