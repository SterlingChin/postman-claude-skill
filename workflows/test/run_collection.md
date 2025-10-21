# Run Postman Collection Tests

## Metadata
- **Phase**: Test
- **Complexity**: Medium
- **Estimated Time**: 1-5 minutes (depends on collection size)
- **Prerequisites**:
  - POSTMAN_API_KEY environment variable set
  - Newman installed (`npm install -g newman`)
  - Node.js installed

## When to Use

Use this workflow when:
- User asks to "run tests" or "execute collection"
- User wants to verify API functionality
- User needs to check if tests pass
- User mentions collection testing or validation
- Part of CI/CD workflow

## Prerequisites Check

### Step 1: Verify environment variables

```bash
echo $POSTMAN_API_KEY
```

If not set, guide user to set it up (see list_collections.md).

### Step 2: Check Newman installation

```bash
newman --version
```

**Expected output**: Version number (e.g., `5.3.2`)

**If Newman not installed**:
1. Verify Node.js is installed: `node --version`
2. Install Newman globally: `npm install -g newman`
3. Verify installation: `newman --version`

**If Node.js not installed**:
- Guide user to download from https://nodejs.org/
- After installation, install Newman
- Verify both are working

## Instructions

### Option A: Run by Collection Name

If user provides a collection name:

```bash
python /skills/postman-skill/scripts/run_collection.py --collection="My API Tests"
```

**What happens**:
1. Script searches for collection by name
2. Downloads collection from Postman
3. Executes with Newman
4. Formats and displays results

### Option B: Run by Collection UID

If you have the collection UID (more reliable):

```bash
python /skills/postman-skill/scripts/run_collection.py --collection-uid="12345-67890-abcdef"
```

### Option C: Run with Environment

To use a specific environment for variables:

```bash
python /skills/postman-skill/scripts/run_collection.py \
  --collection="My API Tests" \
  --environment="Production"
```

Or with UIDs:

```bash
python /skills/postman-skill/scripts/run_collection.py \
  --collection-uid="12345-67890" \
  --environment-uid="abc-def-123"
```

### Option D: Custom Timeout

For long-running collections:

```bash
python /skills/postman-skill/scripts/run_collection.py \
  --collection="Load Tests" \
  --timeout=600
```

Default timeout is 300 seconds (5 minutes).

## Reading the Results

### Success Output

```
✓ Newman 5.3.2 is installed

Collection UID: 12345-67890-abcdef
Downloading collection...
Running collection with Newman (timeout: 300s)...
============================================================

newman

My API Tests

→ Get Users
  GET https://api.example.com/users [200 OK, 1.2KB, 145ms]
  ✓  Status code is 200
  ✓  Response has users array

→ Create User
  POST https://api.example.com/users [201 Created, 450B, 203ms]
  ✓  Status code is 201
  ✓  User created successfully

============================================================
TEST RESULTS
============================================================

Summary:
  Total Requests: 2
  Requests Failed: 0
  Total Assertions: 4
  Assertions Failed: 0

  Total Duration: 350ms

✓ All tests passed!

============================================================
```

### Failure Output

```
============================================================
TEST RESULTS
============================================================

Summary:
  Total Requests: 2
  Requests Failed: 1
  Total Assertions: 4
  Assertions Failed: 2

  Total Duration: 250ms

2 Failure(s):

  1. AssertionError
     Test: Status code is 200
     Message: expected response to have status code 200 but got 404
     Request: Get Users

  2. JSONError
     Test: Response has users array
     Message: Cannot read property 'length' of undefined
     Request: Get Users

============================================================
```

## Interpreting Results

### Key Metrics

1. **Total Requests**: How many API calls were made
2. **Requests Failed**: HTTP-level failures (timeouts, connection errors)
3. **Total Assertions**: Number of test checks
4. **Assertions Failed**: Number of test failures

### Success Criteria

Tests are successful when:
- ✓ Requests Failed = 0
- ✓ Assertions Failed = 0
- ✓ No error output to stderr

### Common Failure Types

1. **Status Code Mismatch**
   - Expected: 200, Got: 404/500/etc.
   - Indicates API endpoint issues

2. **Assertion Errors**
   - Response doesn't match expected format
   - Data validation failed

3. **Timeout Errors**
   - Collection took too long to execute
   - Increase timeout parameter

4. **Connection Errors**
   - Cannot reach API
   - Check network/VPN/firewall

## Next Steps After Execution

### If Tests Pass
- Inform user all tests passed
- Offer to:
  - Run tests in different environment
  - Set up monitoring
  - Show test details

### If Tests Fail
- Show failure summary
- Suggest debugging steps:
  1. Check API status/health
  2. Verify environment variables
  3. Review failed request details
  4. Test individual endpoints
- Offer to:
  - Re-run with verbose logging
  - Check API documentation
  - Debug specific failures

## Error Handling

### Error: Newman not installed

**Symptoms**: "Newman is not installed" message

**Resolution**:
1. Install Node.js from https://nodejs.org/
2. Run: `npm install -g newman`
3. Verify: `newman --version`
4. Retry the collection run

### Error: Collection not found

**Symptoms**: "Collection 'XYZ' not found"

**Resolution**:
1. List available collections first:
   ```bash
   python /skills/postman-skill/scripts/list_collections.py
   ```
2. Use exact collection name (case-sensitive) or UID
3. Verify workspace is set correctly

### Error: Newman execution timeout

**Symptoms**: "Newman execution timed out after X seconds"

**Resolution**:
1. Increase timeout: `--timeout=600`
2. Check if API is responsive
3. Consider running smaller subset of tests
4. Check for infinite loops in pre-request scripts

### Error: Authentication failed (401/403)

**Symptoms**: Tests fail with 401 or 403 status codes

**Resolution**:
1. Verify environment has correct auth tokens/keys
2. Check if tokens are expired
3. Ensure collection is using correct auth method
4. Verify API key permissions

### Error: npm permissions

**Symptoms**: "Permission denied" when installing Newman

**Resolution**:
- Use sudo (not recommended): `sudo npm install -g newman`
- Or use nvm for user-level Node.js installation
- Or use `npx newman` instead of global install

## Advanced Usage

### Generate HTML Report

While Newman can generate HTML reports, this basic implementation uses CLI and JSON.
For HTML reports, consider extending the script or using Newman directly:

```bash
newman run collection.json --reporters cli,html --reporter-html-export report.html
```

### Run Specific Folder

Newman supports running specific folders within a collection:

```bash
newman run collection.json --folder="Smoke Tests"
```

(This would require extending the Python script)

### Parallel Execution

For running multiple collections in parallel, use separate script calls or extend
with Python's multiprocessing.

## Integration Notes

### CI/CD Integration

This workflow is designed to work in CI/CD pipelines:
- Returns exit code 0 on success, 1 on failure
- Outputs structured JSON for parsing
- Timeout configurable for different environments

### Monitoring Integration

Results can be sent to monitoring systems by:
- Parsing the JSON output
- Extracting success/failure metrics
- Posting to monitoring APIs

## Related Workflows

- **list_collections.md**: Discover collections to run
- **workspace_audit.md**: Comprehensive workspace health check (future)
- **monitor_analysis.md**: Analyze monitor runs (future)

## Examples

### Example 1: Quick smoke test

**User**: "Run the smoke tests"

**Claude**:
1. Lists collections to find "Smoke Tests"
2. Runs: `python ... --collection="Smoke Tests"`
3. Reports results
4. Suggests next action based on outcome

### Example 2: Environment-specific test

**User**: "Test the API in staging"

**Claude**:
1. Finds API test collection
2. Confirms staging environment exists
3. Runs: `python ... --collection="API Tests" --environment="Staging"`
4. Shows results with environment context

### Example 3: Debugging failed test

**User**: "The user creation test is failing"

**Claude**:
1. Runs collection to reproduce issue
2. Shows specific failure details
3. Suggests checking:
   - API endpoint availability
   - Request payload format
   - Authentication credentials
4. Offers to check API documentation

## Tips

1. **Use Collection UIDs** when possible - more reliable than names
2. **Start with short timeout** (60s) for quick tests, increase as needed
3. **Check Newman version** - ensure it's up to date
4. **Use environments** for different deployment stages
5. **Monitor execution time** - slow tests indicate API performance issues

## Security Notes

- API credentials should be in environments, not hardcoded
- Sensitive data in responses won't be logged
- Collection files are temporary and cleaned up after run
- Newman runs locally - no data sent to Postman cloud

## Limitations

- Requires Node.js and Newman installation
- Cannot run collections that require OAuth flows (yet)
- File upload tests may have path dependencies
- Some advanced Newman features not exposed in wrapper

## Future Enhancements

- Support for Newman reporters (HTML, JUnit, etc.)
- Collection folder/request filtering
- Parallel collection execution
- Integration with Postman monitors
- Result storage and trending
