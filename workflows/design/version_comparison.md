# Compare API Versions

## Metadata
- **Phase**: Design
- **Complexity**: Moderate
- **Estimated Time**: 2-4 minutes
- **Prerequisites**: API with multiple versions

## When to Use

Use this workflow when:
- User asks to "compare API versions" or "show version differences"
- User wants to understand changes between releases
- Part of API governance review
- Before deprecating old versions

## Prerequisites Check

Before starting, verify:
1. API has at least 2 versions
2. API ID or name is known
3. Version identifiers are known (or can be listed)

## Instructions

### Step 1: List API Versions

Get all versions for comparison:

```python
from scripts.postman_client import PostmanClient

client = PostmanClient()
versions = client.get_api_versions(api_id="<api-id>")

print(f"\nAvailable versions:")
for i, version in enumerate(versions, 1):
    print(f"{i}. {version.get('name', 'Unnamed')}")
    print(f"   ID: {version.get('id')}")
    print(f"   Created: {version.get('createdAt', 'N/A')}")
    print()
```

**Expected outcome**: List of all versions displayed

### Step 2: Select Versions to Compare

User should specify which versions to compare:
- Latest vs. previous
- Specific versions (e.g., v2.0 vs v1.5)
- All sequential versions

### Step 3: Retrieve Version Details

Get detailed information for each version:

```python
version1 = client.get_api_version(api_id="<api-id>", version_id="<version1-id>")
version2 = client.get_api_version(api_id="<api-id>", version_id="<version2-id>")

# Get schemas if available
schemas1 = client.get_api_schema(api_id="<api-id>", version_id="<version1-id>")
schemas2 = client.get_api_schema(api_id="<api-id>", version_id="<version2-id>")
```

**Expected outcome**: Version details retrieved

### Step 4: Compare and Format Results

Present comparison:

```
=== API Version Comparison ===
API: Orders API

Version 1: v1.5.0
- Created: 2024-06-15
- Schema Type: OpenAPI 3.0
- Endpoints: 12
- Last Modified: 2024-07-20

Version 2: v2.0.0
- Created: 2024-09-01
- Schema Type: OpenAPI 3.0
- Endpoints: 15
- Last Modified: 2024-10-15

Key Differences:
✓ Added 3 new endpoints
  - POST /orders/bulk
  - GET /orders/analytics
  - PUT /orders/{id}/status

⚠ Breaking Changes:
  - Removed deprecated endpoint: DELETE /orders/cancel
  - Changed response format for GET /orders (added pagination)

Recommendations:
- Update clients to use v2.0.0 pagination
- Migrate away from deprecated endpoints
- Consider deprecation timeline for v1.5.0
```

### Step 5: Provide Recommendations

Based on comparison:
- Highlight breaking changes
- Suggest migration path
- Recommend version deprecation strategy
- Offer to update collections or tests

## Success Criteria

This workflow succeeds when:
- [x] Versions identified and retrieved
- [x] Comparison performed
- [x] Differences clearly presented
- [x] Breaking changes highlighted
- [x] Migration guidance provided

## Error Handling

### Error: Version Not Found

**Symptoms**: "Version 'XXX' not found"

**Resolution**:
1. List all versions to verify ID
2. Check version was not deleted
3. Verify API ID is correct

### Error: Schema Differences Too Complex

**Symptoms**: Cannot determine specific differences

**Resolution**:
1. Present high-level summary
2. Suggest using external diff tools
3. Recommend manual schema review

## Exit Conditions

- User understands version differences
- User requests migration plan
- User asks to deprecate old version
- User moves to update workflow

## Related Workflows

- **validate_schema.md**: Validate individual schemas
- **manage_apis.md**: Update or create new versions (future)
- **deprecate_version.md**: Sunset old versions (future)

## Examples

Common scenarios:
- Comparing v1.0 to v2.0 for major release
- Checking v2.1 vs v2.2 for minor changes
- Reviewing all versions for governance audit

## Implementation Details

**Location**: `/skills/postman-skill/workflows/design/`

**API Endpoints Used**:
- `GET /apis/{id}/versions` - List versions
- `GET /apis/{id}/versions/{versionId}` - Get version details
- `GET /apis/{id}/versions/{versionId}/schemas` - Get schemas

**Note**: Detailed schema diff requires comparing schema structures programmatically or using external tools.
