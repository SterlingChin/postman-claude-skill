# Postman Agent Skill

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.7+](https://img.shields.io/badge/python-3.7+-blue.svg)](https://www.python.org/downloads/)

A Claude Agent Skill that enables AI-powered interaction with the Postman API for complete API lifecycle management.

## ⚠️ Important: Environment Compatibility

| Environment | Status | Notes |
|------------|--------|-------|
| **Claude Desktop** | ✅ Fully Supported | **Primary target** - requires network egress configuration |
| **Claude API** (Code Execution) | ✅ Fully Supported | No network restrictions |
| **Local Python Scripts** | ✅ Fully Supported | Run scripts directly on your machine |

**This skill is designed for Claude Desktop** with proper network egress configuration to access `api.getpostman.com`.

## What is This?

This is an **Agent Skill** - a structured way to give Claude new capabilities through organized instructions and executable code. Agent Skills use progressive disclosure: Claude loads only what it needs when it needs it, keeping context usage efficient.

## 🔧 Required: Network Egress Configuration

**Before using this skill in Claude Desktop**, you must enable network egress to allow access to Postman API endpoints.

### Step 1: Enable Network Egress

In Claude Desktop settings, enable **"Allow network egress"**:

![Enable Network Egress](docs/Screenshot%202025-11-03%20at%208.35.41%20AM.png)

### Step 2: Configure Domain Allowlist

You have two options for domain access:

**Option 1: Allow All Domains (Easiest)**
- Set Domain allowlist to **"All domains"**
- Claude can access all domains on the internet
- This is the simplest configuration

**Option 2: Allow Specific Postman Domains (More Restrictive)**
- Set Domain allowlist to **"None"**
- Add the following domains individually:
  - `*.getpostman.com`
  - `*.postman.com`
  - `api.getpostman.com`
  - `api.postman.com`

![Configure Domain Allowlist](docs/Screenshot%202025-11-03%20at%208.36.51%20AM.png)

**Recommendation**: Use "All domains" for the best experience, as it allows Claude to access any APIs you need.

## Quick Start

### For Claude Desktop (Recommended)

#### 1. Configure Network Egress

See the [Network Egress Configuration](#-required-network-egress-configuration) section above to enable network access.

#### 2. Get Your Postman API Key

1. Go to https://web.postman.co/settings/me/api-keys
2. Click "Generate API Key"
3. Copy the key (it starts with `PMAK-`)

#### 3. Configure the Skill

```bash
cd postman-skill
cp .env.example .env
# Edit .env and add your POSTMAN_API_KEY
```

#### 4. Package and Install in Claude Desktop

```bash
# Package the skill
./package_skill.sh

# Install in Claude Desktop:
# - Open Claude Desktop
# - Go to Settings > Skills
# - Click "Install Skill"
# - Select postman-skill.zip from the parent directory
```

#### 5. Test the Skill

Ask Claude in Claude Desktop:
```
"List my Postman collections"
"Show me my workspace resources"
"Run validation on my setup"
```

### For Local Testing (Alternative)

You can also test the scripts locally before installing in Claude Desktop:

#### Test Commands

```bash
# Test configuration and discover resources
python postman-skill/scripts/list_collections.py

# List all resources
python postman-skill/scripts/list_collections.py --all

# List specific resource types
python postman-skill/scripts/list_collections.py --environments
python postman-skill/scripts/list_collections.py --monitors
python postman-skill/scripts/list_collections.py --apis

# Run collection tests (requires Newman: npm install -g newman)
python postman-skill/scripts/run_collection.py --collection="My Collection"

# Manage collections
python postman-skill/scripts/manage_collections.py --list
python postman-skill/scripts/manage_collections.py --create --name="New Collection"
python postman-skill/scripts/manage_collections.py --duplicate <collection-id> --name="Copy"

# Manage environments
python postman-skill/scripts/manage_environments.py --list
python postman-skill/scripts/manage_environments.py --create --name="Development"

# Manage monitors
python postman-skill/scripts/manage_monitors.py --list
python postman-skill/scripts/manage_monitors.py --analyze <monitor-id>
```

### For Claude API Use (Alternative)

This section is for using the skill with the Claude API instead of Claude Desktop.

#### Upload to Claude API (Agent Skills API)

**Note**: The Claude API with code execution has no network restrictions and supports this skill without additional configuration.

Once you have an Anthropic API key with Skills beta access:

```python
import anthropic
from anthropic.lib import files_from_dir

client = anthropic.Anthropic()

# Upload the skill
skill = client.beta.skills.create(
    display_title="Postman API Management",
    files=files_from_dir("postman-skill"),
    betas=["skills-2025-10-02"]
)

print(f"Created skill: {skill.id}")
print(f"Latest version: {skill.latest_version}")
```

#### Use in Claude API

```python
import anthropic

client = anthropic.Anthropic()

response = client.messages.create(
    model="claude-sonnet-4-5-20250929",
    max_tokens=4096,
    betas=["code-execution-2025-08-25", "skills-2025-10-02"],
    container={
        "skills": [
            {
                "type": "custom",
                "skill_id": "skill_01AbCdEfGhIjKlMnOpQrStUv",  # Your skill ID
                "version": "latest"
            }
        ]
    },
    messages=[{
        "role": "user",
        "content": "List my Postman collections"
    }],
    tools=[{
        "type": "code_execution_20250825",
        "name": "code_execution"
    }]
)

print(response.content)
```

## Packaging for Claude Desktop

### ✅ Claude Desktop Fully Supported

This skill is designed for Claude Desktop and works great with proper network egress configuration.

### Packaging Workflow

1. **Clone the repository**
   ```bash
   git clone <repo-url>
   cd postman-skill
   ```

2. **Set up your API key**
   ```bash
   cp .env.example .env
   # Edit .env and add your POSTMAN_API_KEY
   ```

3. **Package the skill**
   ```bash
   ./package_skill.sh
   ```

4. **Install in Claude Desktop**
   - Open Claude Desktop
   - Go to Settings > Skills
   - Click "Install Skill"
   - Select `postman-skill.zip` from the parent directory

### Why Packaging is Required

Claude Desktop has a **10-folder depth limit** for zip files. Directories like `venv/` (Python virtual environment) can be 10+ folders deep and must be excluded.

The packaging script:
- ✅ **Includes** your `.env` file with API keys (needed at runtime)
- ❌ **Excludes** deep directories (`venv/`, `.git/`)
- ❌ **Excludes** unnecessary files (`.DS_Store`, `__pycache__/`)

### What Gets Included vs Excluded

**INCLUDED in the package:**
- ✅ **.env** - Your API keys (required for the skill to work)
- ✅ All Python scripts and workflows
- ✅ Documentation and examples

**EXCLUDED from the package:**
- ❌ **venv/** - Python virtual environment (10+ folders deep)
- ❌ **.git/** - Git repository metadata
- ❌ **.env.example** - Template file (not needed at runtime)
- ❌ **__pycache__/** - Python cache files
- ❌ **IDE files** - .vscode/, .idea/, etc.

### Important: .env File Handling

The `.env` file has different rules for git vs packaging:

| Context | .env Status | Why |
|---------|-------------|-----|
| **Git repository** | ❌ Excluded (in `.gitignore`) | Security: Never commit API keys |
| **Skill package** | ✅ Included (in zip) | Required: Claude needs your API keys at runtime |

### Manual Packaging (Not Recommended)

If you need to package manually:

```bash
cd postman-skill
zip -r ../postman-skill.zip . \
  -x "venv/*" \
  -x ".git/*" \
  -x "*.DS_Store" \
  -x "*.pyc" \
  -x "*__pycache__/*" \
  -x ".env.example" \
  -x ".claude/*"
```

Note: `.env` is **not** in the exclusion list - it must be included!

## What's Included in This POC

### Core Components

- **SKILL.md**: Entry point with metadata, overview, and capability descriptions
- **config.py**: Environment variable management and validation
- **postman_client.py**: API client with retry logic and error handling
- **retry_handler.py**: Exponential backoff for rate limits and errors
- **formatters.py**: Human-readable output formatting
- **list_collections.py**: Executable script to discover workspace resources

### Workflows

- **list_collections.md**: Step-by-step guide for discovering workspace resources
- **validate_schema.md**: Validate API schemas against OpenAPI/Swagger standards
- **version_comparison.md**: Compare API versions and identify changes
- **manage_collections.md**: Create, update, delete, and duplicate collections
- **manage_environments.md**: Create, update, delete, and duplicate environments
- **check_auth.md**: Review authentication configuration and security
- **manage_mocks.md**: Create and manage mock servers for prototyping
- **run_collection.md**: Execute collection tests with Newman and analyze results
- **manage_monitors.md**: Create, manage, and analyze monitors for continuous API monitoring
- **view_documentation.md**: Access and assess API documentation quality

### Capabilities

#### ✅ Discover Phase
- List collections, environments, monitors, and APIs
- Get detailed resource information
- Workspace resource discovery
- Error handling with retry logic

#### ✅ Design Phase
- Validate API schemas (OpenAPI, Swagger, GraphQL)
- Get API versions and compare changes
- Manage API definitions and versions
- Create, update, and delete APIs

#### ✅ Build Phase
- Create new collections and environments
- Update existing collections and environments
- Delete collections and environments
- Duplicate collections and environments
- Add requests to collections
- Manage environment variables (including secrets)

#### ✅ Test Phase
- Run collection tests with Newman integration
- Execute test suites with environment variables
- Parse and format test results
- Detailed pass/fail reporting with assertions

#### ✅ Secure Phase
- Check authentication configuration
- Review security settings in collections
- Identify unsecured endpoints
- Get security recommendations

#### ✅ Deploy Phase
- Create and manage mock servers
- List all mocks in workspace
- Update mock server configuration
- Delete mock servers

#### ✅ Observe Phase
- Create, update, and delete monitors
- List all monitors with status
- View monitor run history and analytics
- Analyze success rates and response times
- Get detailed run diagnostics

#### ✅ Distribute Phase
- View API documentation
- Assess documentation quality and completeness
- Check for missing descriptions or examples
- Get recommendations for improving docs

### Not Yet Implemented

❌ Advanced schema validation (breaking change detection)
❌ Documentation publishing (public docs)
❌ CI/CD integration workflows
❌ Advanced security auditing

## File Structure

```
postman-skill/
├── SKILL.md                      # Entry point - skill metadata & overview
├── README.md                     # This file
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
│   └── formatters.py             # Output formatting (collections, monitors, runs)
└── examples/
    └── api_responses/            # Sample responses (for future reference)
```

## How It Works

### Progressive Disclosure Architecture

1. **System Prompt**: Claude always sees skill metadata (name + description from SKILL.md YAML)
2. **Skill Triggered**: When relevant, Claude reads SKILL.md for overview
3. **Workflow Loaded**: For specific tasks, Claude reads workflow .md files
4. **Code Executed**: Scripts run to interact with Postman API
5. **Results Formatted**: Output is made human-readable

### Example Flow

```
User: "What Postman collections do I have?"
  ↓
Claude sees "postman" skill metadata
  ↓
Claude reads SKILL.md
  ↓
Claude identifies list_collections.md workflow
  ↓
Claude reads workflow instructions
  ↓
Claude executes: python /skills/postman-skill/scripts/list_collections.py
  ↓
Script calls Postman API
  ↓
Results formatted and returned to user
```

## Environment Variables

| Variable | Required | Default | Description |
|----------|----------|---------|-------------|
| `POSTMAN_API_KEY` | ✅ Yes | - | Your Postman API key (get from https://web.postman.co/settings/me/api-keys) |
| `POSTMAN_WORKSPACE_ID` | ❌ No | None | Workspace ID to scope operations |
| `POSTMAN_RATE_LIMIT_DELAY` | ❌ No | 60 | Seconds to wait on rate limit |
| `POSTMAN_MAX_RETRIES` | ❌ No | 3 | Maximum retry attempts |
| `POSTMAN_TIMEOUT` | ❌ No | 30 | Request timeout in seconds |

## Testing Locally

### Requirements

- Python 3.7+
- `requests` library (usually pre-installed)
- Node.js and Newman (for test execution): `npm install -g newman`

### Run Tests

```bash
# Test configuration validation
python postman-skill/scripts/config.py

# Test API connection and discovery
python postman-skill/scripts/list_collections.py

# Test with different options
python postman-skill/scripts/list_collections.py --all
python postman-skill/scripts/list_collections.py --environments

# Test collection execution
python postman-skill/scripts/run_collection.py --collection="Your Collection Name"

# Test monitor operations
python postman-skill/scripts/manage_monitors.py --list
python postman-skill/scripts/manage_monitors.py --get <monitor-id>
python postman-skill/scripts/manage_monitors.py --analyze <monitor-id> --limit 10
```

### Expected Output

```
Fetching collections...
Found 3 collection(s):

1. Payment API Tests
   UID: 12345678-1234-1234-1234-123456789012
   Owner: user@example.com

2. User Management API
   UID: 87654321-4321-4321-4321-210987654321

3. Integration Tests
   UID: abcdef12-3456-7890-abcd-ef1234567890
```

## Troubleshooting

### "Configuration Error: POSTMAN_API_KEY not set"

**Solution**: Set your API key as an environment variable:
```bash
export POSTMAN_API_KEY="PMAK-your-key-here"
```

### "Invalid POSTMAN_API_KEY format"

**Solution**: Ensure your key starts with `PMAK-`. Generate a new one if needed.

### "API request failed with status 401"

**Solution**: Your API key might be invalid or expired. Generate a new one from Postman settings.

### "No collections found"

**Solution**: This is normal if your workspace is empty. The skill is working correctly.

## Next Steps

### To Expand This POC

1. **Add test execution**: Integrate Newman or Collection Runner API
2. **Add more workflows**: Schema validation, monitor analysis, etc.
3. **Add creation operations**: Create collections, environments, etc.
4. **Add examples**: Sample API responses for testing
5. **Add tests**: Unit and integration tests

### To Deploy

1. Get Anthropic API key with Skills beta access
2. Upload skill using the Python SDK
3. Use in your Claude API applications
4. Iterate based on usage and feedback

## Architecture Notes

This POC follows the design principles from the project plan:

- ✅ Progressive disclosure (metadata → instructions → code)
- ✅ Proactive, not prescriptive (suggests next steps)
- ✅ Respects existing work (read-only operations in POC)
- ✅ Clear error messages with resolution guidance
- ✅ Retry logic with exponential backoff
- ✅ Configuration validation

## Contributing

Contributions are welcome! Please see [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

### How to Contribute

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Make your changes and test them
4. Commit your changes (`git commit -m 'Add amazing feature'`)
5. Push to the branch (`git push origin feature/amazing-feature`)
6. Open a Pull Request

## Resources

- [Postman API Documentation](https://www.postman.com/postman/workspace/postman-public-workspace/documentation/12959542-c8142d51-e97c-46b6-bd77-52bb66712c9a)
- [Anthropic Agent Skills Documentation](https://docs.anthropic.com/en/docs/agents-and-tools/agent-skills)
- [Agent Skills Blog Post](https://www.anthropic.com/engineering/equipping-agents-for-the-real-world-with-agent-skills)

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

Built with [Claude](https://claude.ai) and designed for the [Anthropic Agent Skills](https://docs.anthropic.com/en/docs/agents-and-tools/agent-skills) framework.
