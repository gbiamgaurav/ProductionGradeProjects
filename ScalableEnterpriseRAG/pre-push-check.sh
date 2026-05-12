#!/bin/bash

# ==============================================================================
# PRE-PUSH VERIFICATION SCRIPT
# ==============================================================================
# This script checks all documentation and code quality requirements
# before allowing a git push. Run with: ./pre-push-check.sh
#
# Checks performed:
# 1. ✅ Documentation completeness
# 2. ✅ Code formatting (black)
# 3. ✅ Import sorting (isort)
# 4. ✅ Code linting (pylint)
# 5. ✅ Type checking (mypy)
# 6. ✅ Unit tests (pytest)
# ==============================================================================

set -e  # Exit on first error

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Counters
CHECKS_PASSED=0
CHECKS_FAILED=0
CHECKS_WARNINGS=0

# Functions
print_header() {
    echo -e "${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
    echo -e "${BLUE}$1${NC}"
    echo -e "${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
}

print_success() {
    echo -e "${GREEN}✅ $1${NC}"
    ((CHECKS_PASSED++))
}

print_error() {
    echo -e "${RED}❌ $1${NC}"
    ((CHECKS_FAILED++))
}

print_warning() {
    echo -e "${YELLOW}⚠️  $1${NC}"
    ((CHECKS_WARNINGS++))
}

print_section() {
    echo ""
    echo -e "${BLUE}📋 $1${NC}"
}

# Main execution
main() {
    print_header "🚀 PRE-PUSH VERIFICATION SCRIPT"
    echo "Verifying all documentation and code quality standards..."
    echo ""
    
    # ========================================================================
    # 1. Documentation Checks
    # ========================================================================
    print_section "DOCUMENTATION CHECKS"
    
    # Check for TODO comments
    if git diff --cached | grep -E '^\+.*TODO'; then
        print_warning "TODO comments found in staged changes"
        ((CHECKS_WARNINGS++))
    else
        print_success "No TODO comments found"
    fi
    
    # Check for print statements (should use logging)
    if git diff --cached | grep -E '^\+.*print\('; then
        print_warning "print() statements found - consider using logging instead"
        ((CHECKS_WARNINGS++))
    else
        print_success "No print() statements found"
    fi
    
    # Check for docstrings in new files
    NEW_PY_FILES=$(git diff --cached --name-only --diff-filter=A | grep '\.py$' || true)
    if [ ! -z "$NEW_PY_FILES" ]; then
        print_section "CHECKING NEW PYTHON FILES FOR DOCSTRINGS"
        for file in $NEW_PY_FILES; do
            if [ -f "$file" ] && [ ! -z "$(head -1 "$file" | grep -v '#')" ]; then
                if ! head -20 "$file" | grep -q '"""'; then
                    print_warning "New file $file may be missing module docstring"
                else
                    print_success "Module docstring found in $file"
                fi
            fi
        done
    fi
    
    # ========================================================================
    # 2. Code Formatting Check
    # ========================================================================
    print_section "CODE FORMATTING CHECK"
    
    if command -v black &> /dev/null; then
        if black --check backend/ --quiet 2>/dev/null; then
            print_success "Code formatting compliant (black)"
        else
            print_error "Code formatting issues found"
            echo "  Run: black backend/"
        fi
    else
        print_warning "black not installed - skipping format check"
    fi
    
    # ========================================================================
    # 3. Import Sorting Check
    # ========================================================================
    print_section "IMPORT SORTING CHECK"
    
    if command -v isort &> /dev/null; then
        if isort --check-only backend/ --quiet 2>/dev/null; then
            print_success "Import sorting compliant (isort)"
        else
            print_warning "Import sorting issues found"
            echo "  Run: isort backend/"
        fi
    else
        print_warning "isort not installed - skipping import check"
    fi
    
    # ========================================================================
    # 4. Linting Check
    # ========================================================================
    print_section "CODE LINTING CHECK"
    
    if command -v pylint &> /dev/null; then
        print_section "Running pylint on backend (if installed)..."
        pylint backend/ --disable=all --enable=C0111,C0112 --fail-under=7 \
            --quiet 2>/dev/null && print_success "Linting passed" || \
            print_warning "Linting issues found (non-blocking)"
    else
        print_warning "pylint not installed - skipping linting"
    fi
    
    # ========================================================================
    # 5. Type Checking
    # ========================================================================
    print_section "TYPE CHECKING"
    
    if command -v mypy &> /dev/null; then
        if mypy backend/ --ignore-missing-imports --quiet 2>/dev/null; then
            print_success "Type checking passed (mypy)"
        else
            print_warning "Type checking issues found (non-blocking)"
        fi
    else
        print_warning "mypy not installed - skipping type check"
    fi
    
    # ========================================================================
    # 6. Unit Tests
    # ========================================================================
    print_section "UNIT TESTS"
    
    if command -v pytest &> /dev/null; then
        if [ -d "tests/" ]; then
            if pytest tests/ --tb=short --quiet 2>/dev/null; then
                print_success "All tests passed (pytest)"
            else
                print_error "Tests failed"
                echo "  Run: pytest tests/ --tb=short"
            fi
        else
            print_warning "tests/ directory not found - skipping tests"
        fi
    else
        print_warning "pytest not installed - skipping tests"
    fi
    
    # ========================================================================
    # 7. Git Status Check
    # ========================================================================
    print_section "GIT STATUS CHECK"
    
    # Check if .env is being committed
    if git diff --cached --name-only | grep -q '^\.env$'; then
        print_error ".env file being committed - it should not be versioned!"
        echo "  Add '.env' to .gitignore"
    else
        print_success ".env file not being committed"
    fi
    
    # Check for large files
    LARGE_FILES=$(git diff --cached --name-only | while read file; do
        if [ -f "$file" ]; then
            SIZE=$(stat -f%z "$file" 2>/dev/null || stat -c%s "$file" 2>/dev/null)
            if [ "$SIZE" -gt 5242880 ]; then  # 5MB
                echo "$file"
            fi
        fi
    done)
    
    if [ -z "$LARGE_FILES" ]; then
        print_success "No large files being committed"
    else
        print_warning "Large files detected: $LARGE_FILES"
    fi
    
    # ========================================================================
    # Summary
    # ========================================================================
    print_header "📊 VERIFICATION SUMMARY"
    
    echo -e "${GREEN}Passed: $CHECKS_PASSED${NC}"
    echo -e "${YELLOW}Warnings: $CHECKS_WARNINGS${NC}"
    echo -e "${RED}Failed: $CHECKS_FAILED${NC}"
    
    echo ""
    
    if [ $CHECKS_FAILED -gt 0 ]; then
        echo -e "${RED}❌ PRE-PUSH CHECK FAILED${NC}"
        echo "Please fix the errors above before pushing."
        return 1
    elif [ $CHECKS_WARNINGS -gt 0 ]; then
        echo -e "${YELLOW}⚠️  PRE-PUSH CHECK PASSED WITH WARNINGS${NC}"
        echo "Review warnings above. Continue? (y/n)"
        read -r response
        if [[ ! "$response" =~ ^[Yy]$ ]]; then
            return 1
        fi
    else
        echo -e "${GREEN}✅ PRE-PUSH CHECK PASSED - READY TO PUSH!${NC}"
    fi
    
    echo ""
    echo "Next steps:"
    echo "  1. Review commit message format (see CONTRIBUTING.md)"
    echo "  2. Verify all tests passing locally"
    echo "  3. Run: git push origin <branch-name>"
    echo ""
}

# Run main function
main
exit $?
