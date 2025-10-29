# Contributing to Postman Agent Skill

Thank you for your interest in contributing to the Postman Agent Skill! This document provides guidelines and instructions for contributing.

## Table of Contents

- [Code of Conduct](#code-of-conduct)
- [Getting Started](#getting-started)
- [How to Contribute](#how-to-contribute)
- [Development Setup](#development-setup)
- [Submitting Changes](#submitting-changes)
- [Coding Standards](#coding-standards)
- [Testing](#testing)

## Code of Conduct

This project aims to foster an open and welcoming environment. Please be respectful and constructive in all interactions.

## Getting Started

1. Fork the repository on GitHub
2. Clone your fork locally
3. Set up your development environment (see [Development Setup](#development-setup))
4. Create a branch for your changes
5. Make your changes and test them
6. Submit a pull request

## How to Contribute

### Reporting Bugs

If you find a bug, please create an issue with:
- A clear, descriptive title
- Steps to reproduce the issue
- Expected behavior vs. actual behavior
- Your environment (Python version, OS, etc.)
- Any relevant error messages or logs

### Suggesting Enhancements

We welcome feature requests! Please create an issue with:
- A clear description of the proposed feature
- Use cases and benefits
- Any implementation ideas you have

### Pull Requests

1. **Small, focused changes**: Each PR should address a single concern
2. **Update documentation**: If you change functionality, update the relevant docs
3. **Add tests**: Include tests for new functionality
4. **Follow coding standards**: See [Coding Standards](#coding-standards)
5. **Update CHANGELOG**: Add a note about your changes (if applicable)

## Development Setup

### Prerequisites

- Python 3.7+
- Node.js and npm (for Newman/test execution features)
- A Postman account with API key

### Setup Steps

1. Clone your fork:
   ```bash
   git clone https://github.com/YOUR-USERNAME/postman-claude-skill.git
   cd postman-claude-skill
   ```

2. Set up environment variables:
   ```bash
   cp .env.example .env
   # Edit .env and add your POSTMAN_API_KEY
   ```

3. Install Newman (for test execution):
   ```bash
   npm install -g newman
   ```

4. Test your setup:
   ```bash
   python scripts/list_collections.py
   ```

## Submitting Changes

1. **Create a branch** from `main`:
   ```bash
   git checkout -b feature/your-feature-name
   ```

2. **Make your changes** with clear, descriptive commit messages:
   ```bash
   git commit -m "Add support for collection variables"
   ```

3. **Push to your fork**:
   ```bash
   git push origin feature/your-feature-name
   ```

4. **Open a Pull Request** on GitHub with:
   - Clear description of the changes
   - Reference to any related issues
   - Screenshots/examples if applicable

## Coding Standards

### Python Style

- Follow [PEP 8](https://pep8.org/) style guide
- Use meaningful variable and function names
- Add docstrings to functions and classes
- Keep functions focused and single-purpose

### File Organization

- **Scripts** (`scripts/`): Executable Python scripts that interact with Postman API
- **Workflows** (`workflows/`): Markdown files with step-by-step instructions for Claude
- **Utils** (`utils/`): Reusable utility modules (formatters, retry logic, etc.)
- **Examples** (`examples/`): Sample responses and test data

### Documentation

- Update `README.md` if you add new features or change setup steps
- Update `SKILL.md` if you add new capabilities or workflows
- Create/update workflow `.md` files for new operations
- Add inline comments for complex logic

### Error Handling

- Include clear, actionable error messages
- Suggest resolution steps in error output
- Use the retry handler for API calls
- Validate inputs early and provide helpful feedback

## Testing

### Manual Testing

Before submitting a PR, test your changes:

1. **Discovery operations**:
   ```bash
   python scripts/list_collections.py --all
   ```

2. **Test execution** (if you have collections):
   ```bash
   python scripts/run_collection.py --collection="Test Collection"
   ```

3. **Monitor operations**:
   ```bash
   python scripts/manage_monitors.py --list
   ```

4. **Error cases**: Test with invalid API keys, missing env vars, etc.

### Test Checklist

- [ ] Code runs without errors
- [ ] New features work as expected
- [ ] Error handling works correctly
- [ ] Documentation is updated
- [ ] No sensitive data (API keys, etc.) in commits
- [ ] `.gitignore` properly excludes sensitive files
- [ ] Skill can be packaged correctly (see [Packaging](#packaging))

## Packaging

### Important: Claude Desktop's 10-Folder Depth Limit

Claude Desktop has a **hard limit of 10 folder depth** for zip files. Directories like `venv/`, `node_modules/`, and `.git/` often exceed this limit and **must be excluded** from packages.

### Using the Packaging Script

Always use the provided packaging script to create distribution-ready zip files:

```bash
cd postman-skill
./package_skill.sh
```

This script:
- Excludes deep directories (`venv/`, `.git/`, etc.)
- Removes unnecessary files (`.DS_Store`, `__pycache__/`, etc.)
- Excludes secrets (`.env` files)
- Creates a clean zip in the parent directory

### What Gets Excluded

The `.skillignore` file documents all exclusion patterns:

```
venv/              # Python virtual environment (10+ folders deep)
.git/              # Git repository metadata
.env               # Environment variables (contains secrets)
__pycache__/       # Python cache files
.claude/           # Claude Desktop metadata
*.pyc              # Compiled Python files
.DS_Store          # macOS metadata
.vscode/           # IDE settings
.idea/             # IDE settings
dist/, build/      # Build artifacts
```

### Why This Matters

**Before packaging script:**
- `postman-skill.zip` = 6.3 MB
- Contains `venv/lib/python3.13/site-packages/...` (10+ levels deep)
- **Fails to install in Claude Desktop** with "path too deep" error

**After packaging script:**
- `postman-skill.zip` = 106 KB
- Only includes source code and workflows
- **Installs successfully** in Claude Desktop

### Testing Your Package

Before submitting a PR that adds files or directories:

1. Run the packaging script:
   ```bash
   ./package_skill.sh
   ```

2. Verify the package is small (< 500 KB for this skill):
   ```bash
   ls -lh ../postman-skill.zip
   ```

3. Check for deep paths:
   ```bash
   unzip -l ../postman-skill.zip | awk -F/ '{print NF-1, $0}' | sort -rn | head -10
   ```
   All paths should be ≤ 9 folders deep.

### Adding New Dependencies

If you add Python dependencies:

1. **DO NOT** commit `venv/` or virtual environment files
2. **Update** `.gitignore` to exclude them
3. **Update** `.skillignore` to document why they're excluded
4. **Test** that `package_skill.sh` excludes them correctly

### Manual Packaging (Not Recommended)

If you must package manually, use the exact command from `package_skill.sh`:

```bash
zip -r ../postman-skill.zip . \
  -x "venv/*" \
  -x ".git/*" \
  -x "*.DS_Store" \
  -x "*.pyc" \
  -x "*__pycache__/*" \
  -x ".env" \
  -x ".env.*" \
  -x ".claude/*" \
  # ... (see package_skill.sh for complete list)
```

## Project Structure

```
postman-skill/
├── SKILL.md                      # Entry point - skill metadata
├── README.md                     # User-facing documentation
├── CONTRIBUTING.md               # This file
├── LICENSE                       # MIT License
├── .env.example                  # Environment variable template
├── .gitignore                    # Git ignore rules
├── workflows/                    # Step-by-step instructions
│   ├── test/
│   │   ├── list_collections.md
│   │   └── run_collection.md
│   └── observe/
│       └── manage_monitors.md
├── scripts/                      # Executable Python scripts
│   ├── config.py
│   ├── postman_client.py
│   ├── list_collections.py
│   ├── run_collection.py
│   └── manage_monitors.py
└── utils/                        # Reusable utilities
    ├── retry_handler.py
    └── formatters.py
```

## Development Workflow Phases

This project follows a phased approach:

- **Phases 1-4**: Discovery (List collections, environments, monitors, APIs)
- **Phase 5**: Test execution with Newman
- **Phase 6**: Monitor management and analytics
- **Future**: Schema validation, documentation publishing, resource creation

When adding features, consider which phase they belong to and follow existing patterns.

## Questions?

If you have questions about contributing, feel free to:
- Open an issue for discussion
- Check existing issues and PRs for context
- Review the code to see examples of similar features

## Recognition

Contributors will be recognized in the project. Thank you for helping make this skill better!

## License

By contributing, you agree that your contributions will be licensed under the MIT License.
