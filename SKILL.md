---
name: postman
description: API lifecycle management through Postman. Discover collections, run tests, monitor APIs, validate schemas, and publish documentation across the complete API development workflow.
---

# Postman Agent Skill

## Overview

This skill gives Claude the ability to interact with the Postman API to manage the complete API lifecycle. It enables discovery of workspace resources, execution of test collections, monitoring analysis, and more.

## Capabilities

- **Discover**: List collections, APIs, environments, and monitors in your workspace
- **Test**: Run collection test suites with Newman and analyze results
- **Observe**: Create, manage, and analyze monitors for continuous API monitoring
- **Validate**: Review API schemas and security configurations (future)

## When to Use This Skill

Claude should use this skill when you:
- Mention Postman, collections, or API testing
- Ask to run tests or check test results
- Want to see what APIs/collections are available
- Need to create, manage, or analyze monitors
- Ask about API uptime, monitoring, or observability
- Want to check monitor status or run history
- Ask about API validation or documentation

## Prerequisites

Before using this skill, ensure:
1. `POSTMAN_API_KEY` environment variable is set (get yours from [Postman API Keys](https://web.postman.co/settings/me/api-keys))
2. `POSTMAN_WORKSPACE_ID` is configured (recommended for users with many workspaces)
3. Python 3 with `requests` module (pre-installed in Claude Code)
4. For test execution: Node.js and Newman (`npm install -g newman`)

## Getting Your Postman API Key

1. Go to https://web.postman.co/settings/me/api-keys
2. Click "Generate API Key"
3. Copy the key (starts with `PMAK-`)
4. Set it as an environment variable: `export POSTMAN_API_KEY="your-key-here"`

## Available Workflows

### Discover Resources
**File**: `workflows/test/list_collections.md`

List all collections, environments, and monitors in your workspace to understand what resources are available.

### Run Collection Tests
**File**: `workflows/test/run_collection.md`

Execute a collection's test suite using Newman and get formatted results showing passes, failures, and detailed diagnostics. Requires Newman CLI to be installed.

### Manage Monitors
**File**: `workflows/observe/manage_monitors.md`

Create, update, delete, and analyze Postman monitors for continuous API monitoring. View monitor run history, success rates, and performance metrics to ensure API reliability.

## Architecture

This skill uses progressive disclosure:

1. **Metadata** (always loaded): Skill name and description from YAML frontmatter
2. **SKILL.md** (loaded when triggered): This overview document
3. **Workflow files** (loaded as needed): Specific step-by-step instructions
4. **Python scripts** (executed, not loaded): Actual API interaction code

## File Structure

```
postman-skill/
├── SKILL.md                      # This file - skill overview
├── workflows/
│   ├── test/
│   │   ├── list_collections.md   # Discovery workflow
│   │   └── run_collection.md     # Test execution workflow
│   └── observe/
│       └── manage_monitors.md    # Monitor management workflow
├── scripts/
│   ├── config.py                 # Configuration management
│   ├── postman_client.py         # API client with CRUD operations
│   ├── list_collections.py       # Collection discovery script
│   ├── run_collection.py         # Newman test execution wrapper
│   └── manage_monitors.py        # Monitor management CLI
└── utils/
    ├── retry_handler.py          # Retry logic with backoff
    └── formatters.py             # Output formatting (collections, monitors, runs)
```

## Example Usage

**List all collections:**
```bash
python /skills/postman-skill/scripts/list_collections.py
```

**Run a specific collection:**
```bash
python /skills/postman-skill/scripts/run_collection.py --collection="My API Tests"
```

**List all monitors:**
```bash
python /skills/postman-skill/scripts/manage_monitors.py --list
```

**Analyze monitor run history:**
```bash
python /skills/postman-skill/scripts/manage_monitors.py --analyze <monitor-id> --limit 20
```

## Error Handling

All scripts include:
- Automatic retry with exponential backoff (3 attempts)
- Clear error messages with resolution guidance
- Validation of required environment variables
- Rate limit handling

## Security

- API keys read from environment variables only
- All operations scoped to configured workspace
- Rate limiting with automatic backoff
- No sensitive data logged or cached

## Limitations

- Runs in code execution container (no network access restrictions apply to API calls)
- Maximum 8MB skill size
- Uses pre-installed Python packages only

## Next Steps

After loading this skill:
1. Check if `POSTMAN_API_KEY` is set
2. If not, guide user to get their key from Postman
3. Use `list_collections.py` to discover available resources
4. Execute specific workflows based on user requests

## Related Resources

- [Postman API Documentation](https://www.postman.com/postman/workspace/postman-public-workspace/documentation/12959542-c8142d51-e97c-46b6-bd77-52bb66712c9a)
- [Workflow Files](workflows/)
- [Example Responses](examples/api_responses/)
