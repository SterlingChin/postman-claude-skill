---
name: postman
description: API lifecycle management through Postman. Discover collections, run tests, monitor APIs, validate schemas, and publish documentation across the complete API development workflow.
version: 1.1.0
---

# Postman Agent Skill

**Version**: 1.1.0 (Phase 1 - Core API Compatibility)
**API Support**: Postman v10+ (with v9 graceful degradation)

## Overview

This skill gives Claude the ability to interact with the Postman API to manage the complete API lifecycle. It enables discovery of workspace resources, execution of test collections, monitoring analysis, and more.

### What's New in v1.1 (Phase 1)

✨ **Enhanced Error Handling**: Custom exception classes with helpful resolution guidance
🔀 **Git-like Workflows**: Fork collections, create pull requests, and merge changes
🔐 **Auto-Secret Detection**: Automatically protects sensitive environment variables
🔄 **Smart Duplication**: Copy collections and environments with full fidelity
📡 **API Version Detection**: Automatic detection with compatibility warnings
🎯 **Improved Developer Experience**: Simplified APIs and better error messages

## Capabilities

- **Discover**: List collections, APIs, environments, and monitors in your workspace
- **Design**: Validate API schemas, compare versions, and manage API definitions
- **Build**: Create, update, and delete collections and environments
  - 🆕 **Fork & Merge**: Git-like version control for collections (v10+)
  - 🆕 **Pull Requests**: Collaborative collection editing workflows (v10+)
  - 🆕 **Smart Duplication**: Copy collections and environments with full metadata
- **Test**: Run collection test suites with Newman and analyze results
- **Secure**: Check authentication configuration and security settings
  - 🆕 **Auto-Secret Detection**: Automatically mark sensitive variables as secrets
  - 🆕 **Secret Preservation**: Maintain secret types across operations
- **Deploy**: Create and manage mock servers for API prototyping
- **Observe**: Create, manage, and analyze monitors for continuous API monitoring
- **Distribute**: View and assess API documentation quality

## When to Use This Skill

Claude should use this skill when you:
- Mention Postman, collections, or API testing
- Want to validate API schemas or compare versions
- Want to create, update, or delete collections or environments
- Need to duplicate or organize collections and environments
- Ask to check authentication or security configuration
- Ask to create mock servers for prototyping
- Ask to run tests or check test results
- Want to see what APIs/collections are available
- Need to create, manage, or analyze monitors
- Ask about API uptime, monitoring, or observability
- Want to check monitor status or run history
- Ask about API documentation quality or access

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

### Validate API Schema
**File**: `workflows/design/validate_schema.md`

Validate API schemas against OpenAPI/Swagger standards. Check schema structure, retrieve API versions, and ensure API definitions are well-formed before deployment.

### Compare API Versions
**File**: `workflows/design/version_comparison.md`

Compare different versions of an API to identify changes, breaking updates, and migration requirements. Essential for API governance and version management.

### Manage Collections
**File**: `workflows/build/manage_collections.md`

Create, update, delete, and duplicate Postman collections. Build new test collections, organize existing ones, and manage collection lifecycle programmatically.

🆕 **v1.1 Enhanced Features**:
- Fork collections for independent development
- Create and manage pull requests
- Merge changes from forks
- Duplicate collections with full metadata preservation

### Manage Environments
**File**: `workflows/build/manage_environments.md`

Create, update, delete, and duplicate Postman environments. Set up environment variables for different stages (dev, staging, production) and manage environment configurations.

🆕 **v1.1 Enhanced Features**:
- Automatic secret detection for sensitive variables (api_key, token, password, etc.)
- Partial updates that preserve existing secrets
- Duplicate environments with secret preservation
- Simplified dict-based API for quick environment creation

### Run Collection Tests
**File**: `workflows/test/run_collection.md`

Execute a collection's test suite using Newman and get formatted results showing passes, failures, and detailed diagnostics. Requires Newman CLI to be installed.

### Check Authentication
**File**: `workflows/secure/check_auth.md`

Review authentication configuration in collections. Identify auth types, check security settings, and get recommendations for improving API security.

### Manage Mock Servers
**File**: `workflows/deploy/manage_mocks.md`

Create, update, and manage mock servers for API prototyping and frontend development. Enable testing without backend implementation.

### Manage Monitors
**File**: `workflows/observe/manage_monitors.md`

Create, update, delete, and analyze Postman monitors for continuous API monitoring. View monitor run history, success rates, and performance metrics to ensure API reliability.

### View Documentation
**File**: `workflows/distribute/view_documentation.md`

Access and assess API documentation quality. Check documentation completeness, review endpoint descriptions, and get recommendations for improving docs.

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
│   ├── design/
│   │   ├── validate_schema.md    # Schema validation workflow
│   │   └── version_comparison.md # API version comparison workflow
│   ├── build/
│   │   ├── manage_collections.md # Collection management workflow
│   │   └── manage_environments.md # Environment management workflow
│   ├── secure/
│   │   └── check_auth.md         # Authentication check workflow
│   ├── deploy/
│   │   └── manage_mocks.md       # Mock server management workflow
│   ├── observe/
│   │   └── manage_monitors.md    # Monitor management workflow
│   └── distribute/
│       └── view_documentation.md # Documentation access workflow
├── scripts/
│   ├── config.py                 # Configuration management
│   ├── postman_client.py         # API client with CRUD operations
│   ├── list_collections.py       # Collection discovery script
│   ├── manage_collections.py     # Collection management CLI
│   ├── manage_environments.py    # Environment management CLI
│   ├── run_collection.py         # Newman test execution wrapper
│   └── manage_monitors.py        # Monitor management CLI
├── utils/
│   ├── retry_handler.py          # Retry logic with backoff
│   ├── formatters.py             # Output formatting (collections, monitors, runs)
│   └── exceptions.py             # 🆕 Custom exception classes with helpful messages
├── tests/
│   ├── test_phase1_manual.py     # 🆕 Phase 1 test suite
│   └── README.md                 # 🆕 Testing guide
└── docs/
    ├── assessment-report.md      # 🆕 Current state analysis
    ├── api-compatibility-matrix.md # 🆕 API endpoint coverage
    ├── gap-analysis.md           # 🆕 Implementation roadmap
    └── compatibility-strategy.md # 🆕 v10+ compatibility approach
```

## Example Usage

### Basic Operations

**List all collections:**
```bash
python /skills/postman-skill/scripts/list_collections.py
```

**Create a new collection:**
```bash
python /skills/postman-skill/scripts/manage_collections.py --create --name "My API Tests"
```

**Create an environment with auto-secret detection (v1.1):**
```python
from scripts.postman_client import PostmanClient

client = PostmanClient()
env = client.create_environment(
    name="Production",
    values={
        "base_url": "https://api.example.com",
        "api_key": "secret-key-123",      # Auto-detected as secret! 🔐
        "bearer_token": "bearer-xyz-456"  # Auto-detected as secret! 🔐
    }
)
```

### Version Control Workflows (v1.1 - v10+ Required)

**Fork a collection:**
```python
# Create a fork for independent development
fork = client.fork_collection(
    collection_uid="12345-abcde",
    label="feature-new-tests"
)
print(f"Forked collection: {fork['uid']}")
```

**Create a pull request:**
```python
# Propose merging your changes
pr = client.create_pull_request(
    collection_uid="12345-abcde",      # Parent collection
    source_collection_uid=fork['uid'], # Your fork
    title="Add authentication tests",
    description="This PR adds comprehensive auth test coverage"
)
```

**Merge a pull request:**
```python
# Merge approved changes
client.merge_pull_request("12345-abcde", pr['id'])
```

**Duplicate a collection:**
```python
# Create a standalone copy (not a fork)
backup = client.duplicate_collection(
    collection_uid="12345-abcde",
    name="My Collection Backup"
)
```

**Validate API schema:**
```python
# See: workflows/design/validate_schema.md
from scripts.postman_client import PostmanClient
client = PostmanClient()
schemas = client.get_api_schema(api_id="<api-id>", version_id="<version-id>")
```

**Check authentication configuration:**
```python
# See: workflows/secure/check_auth.md
collection = client.get_collection(collection_uid="<collection-id>")
auth_type = collection.get('auth', {}).get('type', 'No auth')
```

**Create a mock server:**
```python
# See: workflows/deploy/manage_mocks.md
mock_data = {"name": "API Mock", "collection": "<collection-uid>"}
mock = client.create_mock(mock_data)
print(f"Mock URL: {mock['mockUrl']}")
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

## Error Handling (Enhanced in v1.1)

All scripts include:
- **Custom Exception Classes**: Specific exceptions for each error type
  - `AuthenticationError` (401) - Invalid API key with setup instructions
  - `PermissionError` (403) - Insufficient permissions with resolution steps
  - `ResourceNotFoundError` (404) - Missing resources with possible causes
  - `ValidationError` (400) - Request validation failures with details
  - `RateLimitError` (429) - Rate limit exceeded with retry-after info
  - `ServerError` (5xx) - Server errors with status page link
  - `NetworkError` - Connection issues with troubleshooting steps
  - `TimeoutError` - Request timeouts with configuration guidance
- **Automatic retry** with exponential backoff (3 attempts)
- **Helpful error messages** with resolution guidance
- **API version detection** with compatibility warnings
- **Rate limit handling** with automatic backoff

### Error Message Example

Before (v1.0):
```
Exception: API request failed with status 404: Resource not found
```

After (v1.1):
```
ResourceNotFoundError: Collection with ID '12345' was not found.

Possible reasons:
- The resource was deleted
- The ID is incorrect
- You don't have permission to access it
- The resource is in a different workspace
```

## Security (Enhanced in v1.1)

- API keys read from environment variables only
- All operations scoped to configured workspace
- Rate limiting with automatic backoff
- No sensitive data logged or cached
- 🆕 **Automatic secret detection** for environment variables
- 🆕 **Secret type preservation** across updates and duplication
- 🆕 **11 sensitive keywords** monitored (api_key, token, password, bearer, auth, etc.)
- 🆕 **No accidental exposure** of credentials in default-typed variables

## Limitations

- Runs in code execution container (no network access restrictions apply to API calls)
- Maximum 8MB skill size
- Uses pre-installed Python packages only
- Collection forking and pull requests require Postman v10+ API
- Some enterprise features may require paid Postman plans

## API Version Compatibility

This skill is optimized for **Postman v10+ APIs** but maintains graceful degradation:

| Feature | v9 API | v10+ API |
|---------|--------|----------|
| Collections CRUD | ✅ Best Effort | ✅ Full Support |
| Collection Forking | ❌ Not Available | ✅ Full Support |
| Pull Requests | ❌ Not Available | ✅ Full Support |
| Environments CRUD | ✅ Best Effort | ✅ Full Support |
| Secret Variables | ⚠️ Limited | ✅ Full Support |
| Custom Exceptions | ✅ Full Support | ✅ Full Support |
| Version Detection | ✅ Full Support | ✅ Full Support |

The client automatically detects your API version and will show warnings if v10+ features are unavailable.

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
