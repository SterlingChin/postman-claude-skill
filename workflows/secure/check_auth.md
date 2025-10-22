# Check Authentication Configuration

## Metadata
- **Phase**: Secure
- **Complexity**: Simple
- **Estimated Time**: 2-3 minutes
- **Prerequisites**: Collection or API exists

## When to Use

Use this workflow when:
- User asks to "check authentication" or "verify security setup"
- User wants to audit API security configuration
- Part of security review process
- Before deploying to production

## Prerequisites Check

Before starting, verify:
1. Collection or API exists
2. Collection has authentication configured
3. API key has read permissions

## Instructions

### Step 1: Get Collection Details

Retrieve collection with auth configuration:

```python
from scripts.postman_client import PostmanClient

client = PostmanClient()
collection = client.get_collection(collection_uid="<collection-id>")

# Check collection-level auth
auth = collection.get('auth', {})
auth_type = auth.get('type', 'No auth configured')

print(f"\n=== Authentication Configuration ===")
print(f"Collection: {collection.get('info', {}).get('name')}")
print(f"Auth Type: {auth_type}")
```

**Expected outcome**: Collection auth type identified

### Step 2: Analyze Authentication Type

Check what type of authentication is configured:

```python
if auth_type == 'apikey':
    print("\n✓ API Key Authentication")
    print(f"  Key: {auth.get('apikey', [{}])[0].get('key', 'N/A')}")
    print(f"  Location: {auth.get('apikey', [{}])[0].get('in', 'N/A')}")

elif auth_type == 'bearer':
    print("\n✓ Bearer Token Authentication")
    print("  Token: [CONFIGURED]")

elif auth_type == 'oauth2':
    print("\n✓ OAuth 2.0 Authentication")
    oauth_config = auth.get('oauth2', [])
    print(f"  Grant Type: {oauth_config[0].get('grant_type', 'N/A') if oauth_config else 'N/A'}")

elif auth_type == 'basic':
    print("\n✓ Basic Authentication")
    print("  Username: [CONFIGURED]")
    print("  Password: [HIDDEN]")

elif auth_type == 'hawk' or auth_type == 'awsv4':
    print(f"\n✓ {auth_type.upper()} Authentication")
    print("  Advanced auth configured")

else:
    print("\n⚠ No authentication configured")
```

**Expected outcome**: Auth configuration details displayed

### Step 3: Check Request-Level Auth

Scan individual requests for auth overrides:

```python
items = collection.get('item', [])
requests_with_auth = 0
requests_without_auth = 0

for item in items:
    if 'auth' in item:
        requests_with_auth += 1
    else:
        requests_without_auth += 1

print(f"\nRequest-Level Authentication:")
print(f"  Requests with custom auth: {requests_with_auth}")
print(f"  Requests using collection auth: {requests_without_auth}")
```

**Expected outcome**: Request auth overview

### Step 4: Security Assessment

Provide security recommendations:

```
=== Security Assessment ===

Authentication: CONFIGURED ✓
Type: Bearer Token

Findings:
✓ Collection-level auth configured
✓ All requests inherit authentication
✓ Secure auth method (Bearer token)

Recommendations:
1. Ensure bearer token is stored in environment variables
2. Rotate tokens regularly (recommended: every 90 days)
3. Use different tokens for dev/staging/production
4. Consider OAuth 2.0 for enhanced security

Security Score: 8/10

Next Steps:
- Review token expiration policy
- Audit environment variable security
- Consider adding rate limiting
```

### Step 5: Provide Recommendations

Based on auth configuration:
- **No Auth**: "Warning: No authentication configured. This is insecure for production APIs."
- **API Key**: "Consider rotating API keys regularly and using environment variables."
- **Bearer**: "Good choice. Ensure tokens are stored securely and expire appropriately."
- **OAuth 2.0**: "Excellent! Most secure option. Verify grant type is appropriate for use case."
- **Basic**: "Warning: Basic auth transmits credentials with each request. Consider upgrading to token-based auth."

## Success Criteria

This workflow succeeds when:
- [x] Authentication configuration identified
- [x] Security assessment performed
- [x] Vulnerabilities or gaps highlighted
- [x] Recommendations provided
- [x] User understands next steps

## Error Handling

### Error: Collection Not Found

**Symptoms**: "Collection 'XXX' not found"

**Resolution**:
1. List collections to verify ID
2. Check workspace scope
3. Verify permissions

### Error: No Auth Configuration

**Symptoms**: Auth field is null or empty

**Resolution**:
This is actually a finding, not an error:
1. Report: "No authentication configured"
2. Recommend adding authentication
3. Suggest appropriate auth type for use case

## Common Auth Types

| Type | Use Case | Security Level |
|------|----------|----------------|
| **No Auth** | Public APIs only | Low |
| **API Key** | Simple authentication | Medium |
| **Bearer Token** | Modern APIs, JWT | High |
| **OAuth 2.0** | Third-party integrations | Very High |
| **Basic Auth** | Legacy systems | Low-Medium |
| **AWS Signature** | AWS services | High |
| **Hawk** | Message authentication | High |

## Exit Conditions

- User understands current auth setup
- Security gaps identified
- User requests to update auth configuration
- User moves to different security workflow

## Related Workflows

- **audit_security.md**: Comprehensive security audit (future)
- **manage_environments.md**: Store auth credentials securely
- **update_collection.md**: Update auth configuration (future)

## Tips

1. **Use Environment Variables**: Never hardcode credentials in collections
2. **Different Creds Per Environment**: Use separate credentials for dev/staging/prod
3. **Regular Rotation**: Rotate API keys and tokens periodically
4. **Least Privilege**: Use minimum required permissions
5. **Monitor Usage**: Track auth failures and suspicious patterns

## Examples

### Checking Multiple Collections

```python
collections = client.list_collections()
for coll in collections:
    full_coll = client.get_collection(coll['uid'])
    auth_type = full_coll.get('auth', {}).get('type', 'none')
    print(f"{coll['name']}: {auth_type}")
```

### Identifying Unsecured Collections

```python
collections = client.list_collections()
unsecured = []

for coll in collections:
    full_coll = client.get_collection(coll['uid'])
    if not full_coll.get('auth'):
        unsecured.append(coll['name'])

if unsecured:
    print(f"⚠ Warning: {len(unsecured)} collections without authentication:")
    for name in unsecured:
        print(f"  - {name}")
```

## Implementation Details

**Location**: `/skills/postman-skill/workflows/secure/`

**API Endpoints Used**:
- `GET /collections/{uid}` - Get collection with auth config

**Note**: This workflow analyzes configuration only. It does not test if credentials are valid or perform penetration testing.
