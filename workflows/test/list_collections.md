# List Postman Collections

## Metadata
- **Phase**: Define
- **Complexity**: Simple
- **Estimated Time**: 30 seconds
- **Prerequisites**: `.env` file with POSTMAN_API_KEY (automatically loaded)

## ⚠️ IMPORTANT: API Call Method

**All Postman API interactions MUST use the Python scripts provided.**

- ✅ **CORRECT**: Run `python /skills/postman-skill/scripts/list_collections.py`
- ❌ **WRONG**: Direct HTTP calls to `api.getpostman.com` (will fail with CORS errors)

The Python scripts automatically load your API key from the `.env` file in the skill package. Direct browser-based API calls will be blocked by CORS.

## When to Use

Use this workflow when:
- User asks "what collections do I have?"
- User wants to discover available resources in their workspace
- Starting any workflow that needs a collection UID
- User mentions Postman but doesn't specify what they want to do

## Prerequisites Check

The script automatically loads configuration from the `.env` file in the skill package. If the API key is not found, the script will provide clear instructions on how to add it to the `.env` file.

**No manual environment variable setup is required** - just ensure the skill was packaged with a properly configured `.env` file.

## Instructions

### Step 1: Run the discovery script

Execute the list collections script:

```bash
python /skills/postman-skill/scripts/list_collections.py
```

**Expected outcome**:
- Script connects to Postman API
- Returns list of collections with names and UIDs
- Output is formatted and readable

### Step 2: Parse and present results

The script will output collections in this format:
```
Found X collection(s):

1. Collection Name
   UID: abc123-def456-ghi789
   Owner: user@example.com

2. Another Collection
   UID: xyz789-uvw456-rst123
```

Present this information to the user in a clear, conversational way.

### Step 3: Offer next steps

Based on the results, suggest relevant actions:
- If collections found: "Would you like to run tests from any of these collections?"
- If no collections: "No collections found. Would you like help creating one?"
- If many collections: "I found several collections. Which one would you like to work with?"

## Additional Options

**List all resource types:**
```bash
python /skills/postman-skill/scripts/list_collections.py --all
```

**List only environments:**
```bash
python /skills/postman-skill/scripts/list_collections.py --environments
```

**List only monitors:**
```bash
python /skills/postman-skill/scripts/list_collections.py --monitors
```

**List only APIs:**
```bash
python /skills/postman-skill/scripts/list_collections.py --apis
```

## Success Criteria

This workflow succeeds when:
- [x] Script executes without errors
- [x] Collections are displayed in readable format
- [x] User understands what collections are available
- [x] Next steps are offered

## Error Handling

### Error: POSTMAN_API_KEY not set

**Symptoms**: Script exits with "Configuration Error: POSTMAN_API_KEY not set"

**Resolution**:
1. Guide user to get their API key from Postman
2. Help them set the environment variable
3. Retry the script

### Error: Authentication failed

**Symptoms**: "API request failed with status 401"

**Resolution**:
1. Verify the API key is correct and hasn't expired
2. Check that it starts with `PMAK-`
3. Generate a new key if needed

### Error: No collections found

**Symptoms**: "No collections found in this workspace"

**Resolution**:
1. This is not an error - workspace might be empty
2. Ask user if they want to:
   - Check a different workspace
   - Create a new collection
   - Use a different Postman account

### Error: Rate limited

**Symptoms**: "Rate limited or server error"

**Resolution**:
- Script automatically retries with backoff
- Wait for retry to complete
- If persistent, suggest waiting a few minutes

## Exit Conditions

- User acknowledges the list
- User asks to perform an action on a specific collection
- User asks for a different workflow

## Related Workflows

- **run_collection.md**: Execute tests from a collection (coming soon)
- **workspace_audit.md**: Complete workspace health check (coming soon)

## Examples

### Example 1: User asks about collections

**User**: "What collections do I have in Postman?"

**Claude**:
1. Runs `list_collections.py`
2. Presents formatted list
3. Asks if user wants to do anything with them

### Example 2: User wants to run tests but doesn't specify which

**User**: "Run my API tests"

**Claude**:
1. First runs `list_collections.py` to discover collections
2. If multiple found, asks which one to run
3. Proceeds with test execution workflow

## Notes

- This workflow uses the Postman API directly (not Newman)
- Collections are listed but not downloaded/cached
- UIDs are required for most other operations - always capture them
- Workspace scoping is optional but recommended for teams
