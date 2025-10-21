# Postman Agent Skill - POC

A proof-of-concept Agent Skill that enables Claude to interact with the Postman API for API lifecycle management.

## What is This?

This is an **Agent Skill** - a structured way to give Claude new capabilities through organized instructions and executable code. Agent Skills use progressive disclosure: Claude loads only what it needs when it needs it, keeping context usage efficient.

## Quick Start

### 1. Get Your Postman API Key

1. Go to https://web.postman.co/settings/me/api-keys
2. Click "Generate API Key"
3. Copy the key (it starts with `PMAK-`)

### 2. Set Environment Variable

```bash
export POSTMAN_API_KEY="PMAK-your-key-here"
```

Optional: Set your workspace ID to scope operations:
```bash
export POSTMAN_WORKSPACE_ID="your-workspace-id"
```

### 3. Test the Skill Locally

```bash
# Test configuration
python postman-skill/scripts/list_collections.py

# List all resources
python postman-skill/scripts/list_collections.py --all

# List specific resource types
python postman-skill/scripts/list_collections.py --environments
python postman-skill/scripts/list_collections.py --monitors
python postman-skill/scripts/list_collections.py --apis
```

### 4. Upload to Claude (Agent Skills API)

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

### 5. Use in Claude API

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

### Capabilities (POC)

✅ List collections
✅ List environments
✅ List monitors
✅ List APIs
✅ Get detailed collection info
✅ Get detailed environment info
✅ Get detailed monitor info
✅ Error handling with retry logic

### Not Yet Implemented

❌ Running collection tests (requires Newman integration)
❌ Creating/updating resources
❌ Schema validation
❌ Monitor analysis
❌ Documentation publishing

## File Structure

```
postman-skill/
├── SKILL.md                      # Entry point - skill metadata & overview
├── README.md                     # This file
├── workflows/
│   └── test/
│       └── list_collections.md   # Discovery workflow
├── scripts/
│   ├── config.py                 # Configuration management
│   ├── postman_client.py         # API client
│   └── list_collections.py       # Collection discovery script
├── utils/
│   ├── retry_handler.py          # Retry logic with backoff
│   └── formatters.py             # Output formatting
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

### Run Tests

```bash
# Test configuration validation
python postman-skill/scripts/config.py

# Test API connection
python postman-skill/scripts/list_collections.py

# Test with different options
python postman-skill/scripts/list_collections.py --all
python postman-skill/scripts/list_collections.py --environments
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

## Resources

- [Postman API Documentation](https://www.postman.com/postman/workspace/postman-public-workspace/documentation/12959542-c8142d51-e97c-46b6-bd77-52bb66712c9a)
- [Anthropic Agent Skills Documentation](https://docs.anthropic.com/en/docs/agents-and-tools/agent-skills)
- [Agent Skills Blog Post](https://www.anthropic.com/engineering/equipping-agents-for-the-real-world-with-agent-skills)

## License

This is a proof-of-concept demonstration. Customize as needed for your use case.
