# SyncDB - Database Schema Synchronization Tool

SyncDB is a database schema synchronization tool designed to sync schema and data between different database systems.

**ALWAYS reference these instructions first and fallback to search or bash commands only when you encounter unexpected information that does not match the info here.**

## Current Repository State

**CRITICAL: This repository is currently in early development with minimal codebase.**

- Repository contains only: README.md, LICENSE, and git files
- No source code, build system, or dependencies implemented yet
- Active development is planned (see Issues #1 and #2)
- Project aims to be a "simple database schema synchronization tool"

## Working Effectively

### Repository Setup
- Clone the repository: `git clone https://github.com/ObjectOriented0/SyncDB.git`
- Navigate to directory: `cd SyncDB`
- Check current state: `ls -la` (will show only README.md, LICENSE, .git/)

### Current Limitations
- **NO BUILD SYSTEM**: There are no build scripts, package.json, requirements.txt, or Makefile
- **NO SOURCE CODE**: No application code has been implemented yet
- **NO TESTS**: No test infrastructure exists
- **NO DEPENDENCIES**: No external dependencies defined

### Expected Development Patterns
Based on the project description and similar tools, when implemented, this project will likely:

- **Language**: Most likely Python (common for database tools) or potentially Node.js
- **Dependencies**: Database connectors (sqlalchemy, psycopg2, mysql-connector, etc.)
- **Structure**: CLI tool with configuration files
- **Build**: Standard Python (`pip install -r requirements.txt`) or Node.js (`npm install`) setup

### When Code Gets Added
**Monitor these files for project evolution:**
- `requirements.txt` or `package.json` - indicates technology stack chosen
- `setup.py`, `pyproject.toml`, or `package.json` - build configuration
- `src/` or `lib/` directories - main source code
- `tests/` directory - test infrastructure
- `config/` or `examples/` - configuration and usage examples

### Validation Steps (Future)
**When actual code is implemented, always:**
1. Install dependencies according to the chosen stack
2. Run any available build commands
3. Execute test suites if they exist
4. Test CLI functionality with sample databases
5. Validate configuration file parsing
6. Check database connection capabilities

## Development Guidelines

### Making Changes
- **Always check current repository state first**: `git status && ls -la`
- **Look for new files**: Check if source code has been added since these instructions
- **Check for package files**: Look for `package.json`, `requirements.txt`, `Cargo.toml`, etc.
- **Validate your changes**: Run any available tests after modifications

### Technology Stack Considerations
**When implementing database sync functionality:**
- Support multiple database types (PostgreSQL, MySQL, SQLite, etc.)
- Handle schema differences gracefully
- Provide rollback capabilities
- Include detailed logging
- Support configuration files for connection settings

### Common Tasks
**Current state - these will NOT work yet:**
- `npm install` - NO package.json exists
- `pip install -r requirements.txt` - NO requirements.txt exists
- `make build` - NO Makefile exists
- `python setup.py install` - NO setup.py exists
- Any test commands - NO tests exist

**Working commands:**
- `git status` - check repository status
- `git log --oneline` - view commit history
- `ls -la` - list current files
- `cat README.md` - view project description
- `cat LICENSE` - view MIT license

## Repository Information

### Quick Reference
```
Repository root structure (current):
.
├── .git/           # Git repository data
├── LICENSE         # MIT license
└── README.md       # Basic project description (2 lines)
```

### README.md Content
```
# SyncDB
This project is a simple database schema synchronization tool.
```

### Related Issues
- Issue #1: "Add code to sync one db to another" 
- Issue #2: WIP implementation of database sync functionality
- Issue #3: Setup Copilot instructions (this file)

## Validation
- **Repository exploration**: `find . -type f -not -path "./.git/*" | head -10`
- **Check for new files**: Compare against known minimal state
- **Verify git status**: Ensure clean working directory for new changes

**ALWAYS validate that these instructions match the current repository state before making assumptions about available functionality.**