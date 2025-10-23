# Phase 1 Testing Guide

This directory contains test scripts for validating Phase 1 implementations.

## Prerequisites

1. **Postman API Key** - Get from https://web.postman.co/settings/me/api-keys
2. **Workspace ID** (optional) - Get from Postman workspace settings

## Setup

```bash
# Set your API key (required)
export POSTMAN_API_KEY="PMAK-your-key-here"

# Set workspace ID (optional, will use default workspace if not set)
export POSTMAN_WORKSPACE_ID="your-workspace-id"

# Navigate to the skill directory
cd postman-skill
```

## Running Tests

### Manual Test Suite (Phase 1)

Run the comprehensive Phase 1 test suite:

```bash
python tests/test_phase1_manual.py
```

This will test:
- ✅ **Phase 1.1**: API version detection
- ✅ **Phase 1.2**: Enhanced error handling with custom exceptions
- ✅ **Phase 1.3**: Collections API (fork, PR, duplicate)
- ✅ **Phase 1.4**: Environments API (secrets, duplicate)

### Expected Output

```
======================================================================
  POSTMAN SKILL - PHASE 1 MANUAL TEST SUITE
  Testing v10+ Modernization - Core API Compatibility
======================================================================

Checking prerequisites...
✅ POSTMAN_API_KEY is set
✅ POSTMAN_WORKSPACE_ID is set

======================================================================
  Phase 1.1: API Version Detection
======================================================================

Making initial request to detect API version...
✅ API version detected: v10+
✅ PASS - API version detection

======================================================================
  Phase 1.2: Enhanced Error Handling
======================================================================

Test 1: ResourceNotFoundError (404)
✅ Caught ResourceNotFoundError: ...
✅ PASS - ResourceNotFoundError

...

======================================================================
  TEST SUMMARY
======================================================================

✅ PASS - Phase 1.1 - Version Detection
✅ PASS - Phase 1.2 - Error Handling
✅ PASS - Phase 1.3 - Collections API
✅ PASS - Phase 1.4 - Environments API

======================================================================
  RESULTS: 4/4 phases passed
======================================================================

🎉 All Phase 1 tests passed!
```

## Test Details

### Phase 1.1: API Version Detection
- Detects API version from response headers
- Warns users if using older API versions
- Validates v10+ structure detection

### Phase 1.2: Enhanced Error Handling
- Tests custom exception classes (ResourceNotFoundError, etc.)
- Validates helpful error messages
- Ensures resolution guidance is provided

### Phase 1.3: Collections API
- Creates test collection
- Tests fork functionality (v10+ feature)
- Tests duplicate functionality
- Tests pull request creation and listing (v10+ feature)
- Cleans up all created resources

### Phase 1.4: Environments API
- Creates environment with auto-secret detection
- Tests that api_key, bearer_token, etc. are marked as secrets
- Tests partial environment updates
- Validates secret type preservation
- Tests environment duplication with secret preservation
- Cleans up all created resources

## Notes

### v10+ Features

Some tests require Postman v10+ API:
- Collection forking
- Pull requests
- Enhanced secret handling

If these features fail, you may be using an older API version. The tests will show warnings instead of failures.

### Cleanup

All tests automatically clean up resources they create:
- Test collections are deleted after testing
- Test environments are deleted after testing

### Rate Limiting

If you hit rate limits during testing:
1. Wait a few minutes before retrying
2. The client has built-in retry logic with exponential backoff
3. Rate limit errors will show helpful messages with retry-after times

## Troubleshooting

### "Authentication failed"
- Check that your POSTMAN_API_KEY is set correctly
- Verify the key hasn't expired
- Ensure the key starts with "PMAK-"

### "Resource not found"
- Check that your POSTMAN_WORKSPACE_ID is valid
- Ensure you have access to the workspace
- Try without workspace ID to use default workspace

### "Rate limit exceeded"
- Wait for the retry-after period shown in the error
- Reduce test frequency
- Check your plan's rate limits

### Tests create but don't clean up resources
- This indicates an error during cleanup
- Manually delete test collections/environments from Postman
- Check the test output for specific cleanup errors

## Next Steps

After Phase 1 tests pass:
1. Review the test output for any warnings
2. Check Phase 1 implementation details
3. Proceed to Phase 2 development

## Manual Testing

You can also test features manually using the Python REPL:

```python
from scripts.config import get_config
from scripts.postman_client import PostmanClient

# Initialize client
config = get_config()
client = PostmanClient(config)

# Test version detection
print(f"API Version: {client.api_version}")

# Test collection operations
collections = client.list_collections()
print(f"Found {len(collections)} collections")

# Test environment with secrets
env = client.create_environment(
    name="Test Env",
    values={
        "api_key": "secret-123",  # Auto-detected as secret
        "base_url": "https://api.example.com"
    }
)
print(f"Created environment: {env['uid']}")

# Check secret detection
secrets = [v for v in env['values'] if v['type'] == 'secret']
print(f"Detected {len(secrets)} secret(s)")
```

## Feedback

If you encounter issues:
1. Check the error messages (they should be helpful!)
2. Review the test output
3. Check your API key and workspace permissions
4. Verify Postman API status: https://status.postman.com
