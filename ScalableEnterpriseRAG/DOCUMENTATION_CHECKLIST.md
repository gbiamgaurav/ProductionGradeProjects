# 📋 Documentation Checklist for Code Pushes

Use this checklist before **every** `git push` to ensure complete documentation.

---

## ✅ Quick Checklist (Before Each Push)

```
[ ] All new functions have docstrings
[ ] All new classes have docstrings  
[ ] Module has docstring at top
[ ] Type hints added to function signatures
[ ] Examples provided for complex functions
[ ] .env.example updated (if env vars changed)
[ ] README.md updated (if API/feature changed)
[ ] CHANGELOG.md entry added
[ ] No TODO comments left behind
[ ] Code is formatted and linted
[ ] All tests passing
[ ] Commit message is descriptive
```

---

## 📝 Detailed Documentation Requirements by File Type

### Python Files (.py)

#### File Start (Module Docstring)
```python
"""
module_name.py

Single-line summary of module purpose.

Longer description explaining what this module does, its main
components, and how it fits into the system.

Classes:
    ClassName: Brief description
    
Functions:
    function_name(): Brief description

Example:
    >>> from module_name import ClassName
    >>> obj = ClassName()
"""
```

#### Functions
```python
def my_function(param1: str, param2: int = 10) -> dict:
    """One-line summary ending with period.
    
    Longer description of what the function does, how it processes
    the input, and what it returns. Include any important behavior.
    
    Args:
        param1: Description of first parameter and its type
        param2: Description of second parameter, defaults to 10
        
    Returns:
        Dictionary with keys:
            - 'status' (str): Success or error status
            - 'data' (dict): Result data
            
    Raises:
        ValueError: If param1 is empty
        TypeError: If param2 is not an integer
        
    Example:
        >>> result = my_function("test", 20)
        >>> print(result['status'])
        'success'
    """
    pass
```

#### Classes
```python
class MyProcessor:
    """Brief description of class purpose and responsibility.
    
    Longer description explaining what this class does, when to use it,
    and how it interacts with other components in the system.
    
    Attributes:
        config (dict): Configuration dictionary
        logger (logging.Logger): Logger instance
        
    Example:
        >>> processor = MyProcessor(config={"timeout": 30})
        >>> result = processor.process(data)
    """
    
    def __init__(self, config: dict) -> None:
        """Initialize processor with configuration.
        
        Args:
            config: Configuration dictionary with keys:
                - 'timeout' (int): Operation timeout in seconds
                - 'retries' (int): Number of retries
                
        Raises:
            ValueError: If config is invalid
        """
        pass
```

---

### Configuration Files

#### .env.example
```
# Include descriptive comments for each variable
# Format: VARIABLE_NAME=placeholder_value

# External API Keys
GROQ_API_KEY=your_key_here           # Get from https://console.groq.com
LANGSMITH_API_KEY=lsv2_pt_...        # Get from https://smith.langchain.com

# Database Configuration
DATABASE_URL=postgresql://user:pass@host:5432/dbname
REDIS_URL=redis://localhost:6379/0

# Application Settings
DEBUG=false                            # Set to true for development
LOG_LEVEL=INFO                         # DEBUG, INFO, WARNING, ERROR
```

#### Setup/Configuration Changes
If you add new environment variables, configuration files, or change setup:
1. [ ] Update `.env.example` with new variables
2. [ ] Add comments explaining each variable
3. [ ] Update `README.md` Environment Setup section
4. [ ] Add to `CHANGELOG.md`

---

### README Updates

When updating README for code changes:

#### New Feature
Add to the Features section:
```markdown
- ✅ Feature name: Brief description of what it does
```

#### New API Endpoint
Update the API table:
```markdown
| `/endpoint` | METHOD | Description |
|-------------|--------|-------------|
| `/new-api` | POST | What this endpoint does |
```

#### New Configuration
Add to Environment Setup:
```markdown
#### **Component Name**
\`\`\`
NEW_VAR=description_here
\`\`\`
What this does and where to get it.
```

---

### CHANGELOG Updates

Create/update `CHANGELOG.md`:

```markdown
## [Unreleased]

### Added
- Feature description with context
- New API endpoint `/documents/search`

### Changed
- Modified behavior of existing function
- Updated configuration requirement

### Fixed
- Bug fix description
- How it was resolved

### Deprecated
- Old API endpoint (use `/new-endpoint` instead)

### Removed
- Removed obsolete function

### Security
- Security issue and how it was fixed
```

---

## 🔍 Documentation Verification Checklist

### For Each New Function
- [ ] Function name is clear and descriptive (no `func`, `process_data` should be `parse_customer_data`)
- [ ] Docstring explains purpose clearly
- [ ] All parameters documented with types
- [ ] Return value documented with type
- [ ] Exceptions documented
- [ ] At least one usage example for complex functions
- [ ] Type hints on all parameters and return
- [ ] No bare `pass` statements without explanation

### For Each New Class
- [ ] Class name follows PascalCase
- [ ] Class docstring explains purpose and use cases
- [ ] All public methods have docstrings
- [ ] Attributes documented
- [ ] `__init__` documents parameters thoroughly
- [ ] Usage example provided
- [ ] Relationships to other classes explained

### For Each New Module
- [ ] Module docstring at top explains purpose
- [ ] Key classes and functions listed in module docstring
- [ ] `__init__.py` imports and exports documented
- [ ] `__all__` defined to control public API
- [ ] At least one usage example
- [ ] Private functions start with `_` and have docstrings

### For Configuration Changes
- [ ] `.env.example` updated with new variables
- [ ] `.env` is in `.gitignore` (not committed)
- [ ] Default values provided where applicable
- [ ] Comments explain each variable's purpose
- [ ] README.md updated with setup instructions

### For API Changes
- [ ] Endpoint documented in README API table
- [ ] Request/response schemas documented
- [ ] Error codes documented
- [ ] Example requests/responses provided
- [ ] Authentication requirements noted

---

## 📊 Documentation Metrics

Aim for these standards in each commit:

| Metric | Standard |
|--------|----------|
| Functions with docstrings | 100% |
| Classes with docstrings | 100% |
| Functions with type hints | 100% |
| Code with examples | Complex functions |
| Test coverage | 80%+ |
| Commit message length | 50-72 characters |

---

## 🔧 Tools to Verify Documentation

```bash
# Check docstring coverage
pydocstyle backend/

# Generate documentation
pydoc -w backend.module_name

# Type checking
mypy backend/

# Code formatting
black backend/ --check

# Import sorting
isort backend/ --check-only

# Linting
pylint backend/ --disable=all --enable=C0103,C0111,C0112
```

---

## 📋 Pre-Push Git Hooks (Optional Setup)

Create `.git/hooks/pre-push` to automatically check:

```bash
#!/bin/bash

# Check for TODO comments (documentation left incomplete)
if git diff --cached | grep -E '^\+.*TODO'; then
    echo "❌ TODO comments found - complete documentation before pushing"
    exit 1
fi

# Check for print() statements (use logging instead)
if git diff --cached | grep -E '^\+.*print\('; then
    echo "⚠️  print() found - use logging instead"
fi

# Verify tests pass
pytest tests/ --tb=short
if [ $? -ne 0 ]; then
    echo "❌ Tests failed - fix before pushing"
    exit 1
fi

echo "✅ Pre-push checks passed!"
exit 0
```

---

## 🚀 When Ready to Push

```bash
# 1. Review this checklist
# 2. Verify documentation is complete
# 3. Run: ./pre-push-check.sh (if configured)
# 4. Run: git push origin feature/branch-name

# The push will fail if documentation standards aren't met
```

---

## 💡 Documentation Tips

### ✅ Do's
- ✅ Use clear, professional language
- ✅ Provide examples for complex functionality
- ✅ Document edge cases and error conditions
- ✅ Link to external resources when relevant
- ✅ Keep documentation near the code it describes
- ✅ Update docs when behavior changes
- ✅ Use consistent formatting

### ❌ Don'ts
- ❌ Write obvious docstrings (`"""Get value."""`)
- ❌ Leave TODO comments in code
- ❌ Document what code does (that's obvious), document why
- ❌ Commit incomplete documentation
- ❌ Update code without updating docs
- ❌ Use vague parameter names that need excessive documentation
- ❌ Write documentation in comments instead of docstrings

---

## 📞 Questions Answered

**Q: Do I need to document helper/private functions?**  
A: Yes, even private functions (`_function_name`) need docstrings, but they can be shorter.

**Q: How detailed should examples be?**  
A: Provide enough detail to understand the most common use case and expected output.

**Q: What if I'm refactoring existing code?**  
A: Update docstrings to match the new behavior. If the signature changed, update completely.

**Q: Can I push without CHANGELOG entry?**  
A: No - CHANGELOG.md must be updated for every push that changes functionality.

---

## ✨ Final Reminder

**Every commit should be self-documenting.**

Someone reading your code 6 months from now (or your future self) should understand:
- ✅ What the code does (function/class names + docstrings)
- ✅ Why it exists (module docstring + comments)
- ✅ How to use it (examples in docstrings)
- ✅ When it might fail (Raises section + tests)

**Happy documenting! 📚**
