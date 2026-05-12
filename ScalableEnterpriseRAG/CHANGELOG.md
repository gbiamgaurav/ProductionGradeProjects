# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added
- Created comprehensive README.md with project overview, setup instructions, and architecture documentation
- Created .env.example for secure configuration management
- Created CONTRIBUTING.md with contribution guidelines and commit message standards
- Created DOCUMENTATION_CHECKLIST.md for documentation requirements on each push
- Created CHANGELOG.md to track all notable changes
- Initial project structure with modularized backend and data ingestion directories

### Changed
- N/A

### Fixed
- N/A

### Deprecated
- N/A

### Removed
- N/A

### Security
- N/A

---

## Versioning Guide

### Format: [MAJOR.MINOR.PATCH]

- **MAJOR**: Breaking changes to API or core functionality
- **MINOR**: New features added, backward compatible
- **PATCH**: Bug fixes, backward compatible

---

## Release Template

Use this template for each new release:

```markdown
## [VERSION] - YYYY-MM-DD

### Added
- New features added

### Changed
- Changes in existing functionality

### Deprecated
- Soon-to-be removed features

### Removed
- Removed features

### Fixed
- Bug fixes

### Security
- Security vulnerability fixes
```

---

## How to Contribute to Changelog

1. For each commit/PR, add an entry to the "Unreleased" section
2. Use appropriate categories: Added, Changed, Fixed, etc.
3. Be descriptive but concise
4. Reference issue numbers when applicable: `Fixes #123`

### Example Entry:
```
### Added
- Implemented semantic search with Qdrant vector database (#45)
- Added API endpoint `/search` for document retrieval
- Created document processor with GCP Document AI integration

### Fixed
- Fixed null pointer exception in retriever (#52)
```

---

## Release Process

When releasing a new version:

1. Update version in code (if versioning file exists)
2. Move "Unreleased" section to new version section
3. Add release date in format: YYYY-MM-DD
4. Create git tag: `git tag v1.0.0`
5. Push tag: `git push origin v1.0.0`

---

## Previous Versions

### [0.0.1] - 2026-05-12

Initial project setup with documentation framework.

**Status**: Project initialized with foundational documentation and contribution guidelines.
