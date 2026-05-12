# 🤝 Contributing Guidelines

## Overview
This document outlines the contribution workflow for the Enterprise Agentic RAG project. Every code push must follow these guidelines to maintain code quality, documentation standards, and project organization.

---

## 📋 Pre-Commit Checklist

Before pushing any code to a branch, ensure you've completed ALL items in this checklist:

### ✅ Code Quality
- [ ] Code follows PEP 8 style guide
- [ ] All functions have docstrings (Google/NumPy style)
- [ ] Type hints are added to function signatures
- [ ] No unused imports or variables
- [ ] Tests are written and passing

### ✅ Documentation Requirements
- [ ] **Module Docstring**: Every `.py` file starts with module-level documentation
- [ ] **Function Documentation**: Every function has a docstring explaining:
  - Purpose/description
  - Args with types
  - Returns with types
  - Raises (if applicable)
  - Example usage (for complex functions)
- [ ] **Class Documentation**: Every class documents:
  - Purpose and use cases
  - Key attributes
  - Key methods with brief descriptions
- [ ] **Configuration Changes**: Update `.env.example` if new env vars added
- [ ] **API Changes**: Update `README.md` API endpoints table if modified

### ✅ File Organization
- [ ] New files placed in appropriate modular directories
- [ ] `__init__.py` properly exports public APIs
- [ ] No circular imports
- [ ] Single responsibility per module

### ✅ Commit Quality
- [ ] Descriptive commit message (see format below)
- [ ] Commit message references related issue (if applicable)
- [ ] One logical change per commit (avoid mixing features/fixes)

### ✅ Testing
- [ ] Unit tests written for new functions
- [ ] All tests pass locally: `pytest tests/`
- [ ] Code coverage maintained/improved

### ✅ Git Workflow
- [ ] Working on a feature/fix branch (not main/master)
- [ ] Branch name follows convention: `feature/feature-name` or `fix/bug-name`
- [ ] Latest changes pulled before pushing: `git pull origin main`

---

## 📝 Commit Message Format

Follow this format for clear commit history:

```
<type>(<scope>): <subject>

<body>

<footer>
```

### Types
- `feat`: A new feature
- `fix`: A bug fix
- `docs`: Documentation changes
- `refactor`: Code refactoring (no feature changes)
- `perf`: Performance improvements
- `test`: Adding/updating tests
- `chore`: Build process, dependencies, tooling

### Scope
Module or component affected (e.g., `data_ingestion`, `rag`, `api`)

### Subject
- Use imperative mood ("add" not "added")
- Don't capitalize first letter
- No period (.) at the end
- Limit to 50 characters

### Body (optional but recommended)
- Explain what and why, not how
- Wrap at 72 characters
- Separate from subject with blank line

### Footer (optional)
- Reference issues: `Fixes #123`
- Breaking changes: `BREAKING CHANGE: description`

### Examples

**Good:**
```
feat(data_ingestion): add document ai processor

Implement GCP Document AI integration for OCR processing.
Supports PDF parsing with automatic text extraction.

Fixes #45
```

**Good:**
```
fix(rag): handle empty context in retriever

Added null check before semantic search to prevent
errors when context is empty.
```

---

## 🗂️ Project Structure Standards

### Backend Module Organization
```
backend/module_name/
├── __init__.py              # Public API exports
├── core.py                  # Main implementation
├── models.py               # Data models (if applicable)
├── schemas.py              # Pydantic schemas (if applicable)
└── utils.py                # Helper functions (if applicable)
```

### Documentation in Code
```python
"""
module_name.py

Brief description of module purpose and main functionality.

This module handles [specific responsibility]. It provides classes
and functions for [use cases].

Key Classes:
    ClassName: Description of what this class does
    
Key Functions:
    function_name(): Description of what it does

Example:
    Basic usage example showing the most common use case
"""

from typing import Optional, List
import logging

logger = logging.getLogger(__name__)


class MyClass:
    """Brief description of class purpose.
    
    Longer description explaining the class, its responsibilities,
    and how it fits into the larger system.
    
    Attributes:
        attr1 (str): Description of first attribute
        attr2 (int): Description of second attribute
        
    Example:
        >>> obj = MyClass("example")
        >>> result = obj.process()
    """
    
    def __init__(self, name: str) -> None:
        """Initialize the class.
        
        Args:
            name: The name identifier for this instance
            
        Raises:
            ValueError: If name is empty string
        """
        if not name:
            raise ValueError("Name cannot be empty")
        self.attr1 = name
        self.attr2 = 0


def process_data(data: List[str], debug: bool = False) -> dict:
    """Process input data and return results.
    
    This function takes a list of strings, performs validation,
    and returns structured results.
    
    Args:
        data: List of strings to process
        debug: Enable debug logging if True
        
    Returns:
        Dictionary with keys:
            - 'success' (bool): Whether processing succeeded
            - 'result' (list): Processed items
            - 'errors' (list): Any errors encountered
            
    Raises:
        TypeError: If data is not a list
        ValueError: If data contains non-string items
        
    Example:
        >>> result = process_data(["item1", "item2"])
        >>> print(result['success'])
        True
    """
    pass
```

---

## 🔄 Branch Workflow

### Creating a Feature Branch
```bash
# Update main
git checkout main
git pull origin main

# Create feature branch
git checkout -b feature/your-feature-name

# Make changes and commit
git add .
git commit -m "feat(scope): description"

# Push to remote
git push origin feature/your-feature-name
```

### Before Pushing
1. Run tests: `pytest tests/`
2. Check documentation: `python -m pydoc module_name`
3. Verify `.env.example` updated if needed
4. Review `.gitignore` compliance
5. Check git status: `git status`

### Push Command
```bash
# Ensure all documentation is complete
git push origin feature/your-feature-name
```

---

## 📚 Documentation Files to Update

### When Adding New Feature
- [ ] Update `README.md` with usage examples
- [ ] Add docstrings to all new functions/classes
- [ ] Create `CHANGE_LOG.md` entry
- [ ] Update `.env.example` if new configuration needed
- [ ] Update API documentation if API endpoint changed

### When Fixing Bug
- [ ] Add test case that reproduces the bug
- [ ] Document fix in function docstring
- [ ] Update `CHANGE_LOG.md` with fix details
- [ ] Reference issue number in commit message

### When Refactoring
- [ ] Preserve all docstrings
- [ ] Update docstrings if behavior changed
- [ ] Add docstrings to any new functions
- [ ] Document breaking changes in commit footer

---

## 🧪 Testing Requirements

### Unit Tests
```bash
# Run all tests
pytest tests/

# Run specific test file
pytest tests/test_module.py

# Run with coverage
pytest --cov=backend tests/
```

### Test Documentation
- [ ] Test file has docstring explaining what's tested
- [ ] Each test function is clearly named (e.g., `test_feature_success_case`)
- [ ] Test docstring explains the test scenario

### Example Test
```python
"""Tests for data_ingestion module."""

import pytest
from backend.data_ingestion import processor


class TestProcessor:
    """Test suite for document processor."""
    
    def test_processor_initialization(self):
        """Verify processor initializes with default config."""
        proc = processor.DocumentProcessor()
        assert proc is not None
        assert proc.config is not None
```

---

## 📖 Inline Code Comments

Use comments for **why**, not **what**. Code should be self-documenting.

**❌ Bad:**
```python
# Loop through items
for item in items:
    # Add to total
    total += item
```

**✅ Good:**
```python
# Use iterative sum instead of built-in to support custom types
for item in items:
    total += item
```

---

## 🚀 Pre-Push Verification Script

Run this script before pushing to ensure everything is ready:

```bash
#!/bin/bash
# save as: pre-push-check.sh

echo "🔍 Running pre-push checks..."

# 1. Run tests
echo "✓ Running tests..."
pytest tests/ --tb=short || { echo "❌ Tests failed"; exit 1; }

# 2. Check code style
echo "✓ Checking code style..."
black --check backend/ || { echo "⚠️  Run 'black backend/' to fix"; exit 1; }

# 3. Check imports
echo "✓ Checking imports..."
isort --check-only backend/ || { echo "⚠️  Run 'isort backend/' to fix"; exit 1; }

# 4. Type checking
echo "✓ Running type checks..."
mypy backend/ --ignore-missing-imports || { echo "⚠️  Type hints missing"; exit 1; }

echo "✅ All checks passed! Ready to push."
```

**Usage:**
```bash
chmod +x pre-push-check.sh
./pre-push-check.sh
```

---

## 📋 Review Process

Before code is merged to main:

1. **Self-Review**: Run through this checklist yourself
2. **Peer Review**: Code is reviewed by another team member
3. **Documentation Review**: Ensure all docs are clear and complete
4. **Test Review**: Verify test coverage
5. **Integration**: Merge after approval

---

## ⚠️ Common Mistakes to Avoid

| ❌ Mistake | ✅ Fix |
|-----------|--------|
| Pushing without tests | Write tests first, then code |
| Missing module docstring | Add at top of every `.py` file |
| No docstrings on functions | Document every public function |
| Committing `.env` file | Use `.env.example` instead |
| Large commits with multiple changes | Split into logical commits |
| Pushing to main directly | Use feature branches |
| No description in commit | Use detailed commit messages |
| Forgetting to update README | Update docs with each feature |

---

## 📞 Questions?

If you have questions about:
- **Documentation style**: Check existing modules for examples
- **Project structure**: See `README.md` project structure section
- **Git workflow**: Run `git flow --help` or ask team lead
- **Testing**: Check `tests/` directory for examples

---

## 📝 Sign-Off

By contributing to this project, you agree to:
- Follow this contribution guide
- Write clear, documented code
- Include appropriate tests
- Provide detailed commit messages
- Update relevant documentation

Thank you for contributing! 🚀
