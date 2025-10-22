# Manage Mock Servers

## Metadata
- **Phase**: Deploy
- **Complexity**: Simple
- **Estimated Time**: 2-5 minutes
- **Prerequisites**: Collection exists for mock server

## When to Use

Use this workflow when:
- User asks to "create a mock server" or "set up mocking"
- User wants to test frontend without backend implementation
- User needs to demo API behavior
- Part of API prototyping process

## Prerequisites Check

Before starting, verify:
1. Collection exists to base mock on
2. (Optional) Environment for dynamic responses
3. API key has permissions to create mocks

## Instructions

### Step 1: List Existing Mocks

Check current mock servers:

```python
from scripts.postman_client import PostmanClient

client = PostmanClient()
mocks = client.list_mocks()

print(f"\nFound {len(mocks)} mock server(s):\n")
for i, mock in enumerate(mocks, 1):
    print(f"{i}. {mock.get('name', 'Unnamed')}")
    print(f"   UID: {mock.get('uid')}")
    print(f"   URL: {mock.get('mockUrl', 'N/A')}")
    print(f"   Collection: {mock.get('collection')}")
    print()
```

**Expected outcome**: Current mocks listed (may be empty)

### Step 2: Create New Mock Server

To create a mock, you need:
- Collection UID
- Mock server name
- (Optional) Environment UID
- (Optional) Private flag

```python
# Get collection ID
collections = client.list_collections()
# User selects collection...

mock_data = {
    "name": "Payment API Mock",
    "collection": "<collection-uid>",
    "environment": "<environment-uid>",  # Optional
    "private": False  # True for private mock
}

result = client.create_mock(mock_data)

print(f"\nMock server created successfully!")
print(f"Name: {result.get('name')}")
print(f"Mock URL: {result.get('mockUrl')}")
print(f"\nYou can now make requests to: {result.get('mockUrl')}")
```

**Expected outcome**: Mock server created and URL provided

### Step 3: Test Mock Server

Verify mock is working:

```bash
# Example test request
curl https://xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx.mock.pstmn.io/api/payments

# With specific example
curl https://xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx.mock.pstmn.io/api/payments \
  -H "x-mock-response-name: Success Response"
```

**Expected outcome**: Mock returns expected responses

### Step 4: Update Mock (If Needed)

Update mock server configuration:

```python
update_data = {
    "name": "Payment API Mock - Updated",
    "private": True  # Make it private
}

result = client.update_mock(mock_id="<mock-id>", mock_data=update_data)
print(f"Mock updated: {result.get('name')}")
```

**Expected outcome**: Mock configuration updated

### Step 5: Manage Mock Lifecycle

Present mock server details and options:

```
=== Mock Server Details ===
Name: Payment API Mock
URL: https://abc123.mock.pstmn.io
Collection: Payment Processing API
Environment: Development
Status: Active
Access: Public

Available Actions:
1. Update mock configuration
2. Make mock private/public
3. Delete mock server
4. View mock request logs (via Postman UI)

Next Steps:
- Share mock URL with frontend team
- Add example responses to collection
- Set up environment for dynamic data
```

## Success Criteria

This workflow succeeds when:
- [x] Mock server created successfully
- [x] Mock URL provided to user
- [x] Mock is accessible and returning responses
- [x] User understands how to use mock
- [x] Management options explained

## Error Handling

### Error: Collection Not Found

**Symptoms**: "Collection 'XXX' not found"

**Resolution**:
1. List collections to verify ID
2. Ensure collection exists in workspace
3. Check collection permissions

### Error: Mock Creation Failed

**Symptoms**: "Failed to create mock server"

**Resolution**:
1. Verify collection has example responses
2. Check API key permissions
3. Ensure collection has requests defined

### Error: Mock URL Not Accessible

**Symptoms**: 404 or connection errors to mock URL

**Resolution**:
1. Verify mock is not private (if accessing without auth)
2. Check URL is correct
3. Ensure collection has matching request paths
4. Add example responses to requests

## Common Operations

### List All Mocks

```python
mocks = client.list_mocks()
for mock in mocks:
    print(f"{mock['name']}: {mock['mockUrl']}")
```

### Get Mock Details

```python
mock = client.get_mock(mock_id="<mock-id>")
print(f"Name: {mock['name']}")
print(f"URL: {mock['mockUrl']}")
print(f"Collection: {mock['collection']}")
```

### Delete Mock

```python
client.delete_mock(mock_id="<mock-id>")
print("Mock server deleted successfully")
```

## Exit Conditions

- Mock server is running and accessible
- User has mock URL for integration
- User understands mock limitations
- User asks to work on different workflow

## Related Workflows

- **manage_collections.md**: Update collection with examples
- **manage_environments.md**: Create environment for mock
- **run_collection.md**: Test against mock server

## Tips

1. **Add Example Responses**: Mocks work best with saved example responses in your collection
2. **Use x-mock-response-name Header**: Specify which example to return
3. **Private Mocks**: Require API key authentication
4. **Dynamic Responses**: Use environments for variable data

## Examples

### Creating a Simple Mock

```python
mock_data = {
    "name": "Quick API Mock",
    "collection": "12345678-1234-1234-1234-123456789012"
}
client.create_mock(mock_data)
```

### Creating a Private Mock with Environment

```python
mock_data = {
    "name": "Production API Mock",
    "collection": "12345678-1234-1234-1234-123456789012",
    "environment": "87654321-4321-4321-4321-210987654321",
    "private": True
}
client.create_mock(mock_data)
```

## Implementation Details

**Location**: `/skills/postman-skill/scripts/` (uses PostmanClient)

**API Endpoints Used**:
- `GET /mocks` - List mock servers
- `GET /mocks/{id}` - Get mock details
- `POST /mocks` - Create mock server
- `PUT /mocks/{id}` - Update mock server
- `DELETE /mocks/{id}` - Delete mock server
