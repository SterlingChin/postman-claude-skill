# Validate API Schema

## Metadata
- **Phase**: Design
- **Complexity**: Moderate
- **Estimated Time**: 3-5 minutes
- **Prerequisites**: API exists with schema defined

## When to Use

Use this workflow when:
- User asks to "validate schema" or "check API definition"
- User wants to ensure API conforms to OpenAPI/Swagger standards
- Part of API design review process
- Before publishing or deploying an API

## Prerequisites Check

Before starting, verify:
1. API name or ID is known
2. API has at least one version defined
3. Schema is attached to the API version
4. API key has permissions to access APIs

## Instructions

### Step 1: Identify API

If user provides an API name, find its ID:

```bash
python /skills/postman-skill/scripts/list_collections.py --apis
```

If user provides an ID directly, skip to Step 2.

**Expected outcome**: API ID identified

### Step 2: Get API Versions

List all versions of the API:

```python
from scripts.postman_client import PostmanClient

client = PostmanClient()
versions = client.get_api_versions(api_id="<api-id>")

print(f"Found {len(versions)} version(s):")
for version in versions:
    print(f"  - {version.get('name', 'Unnamed')}: {version.get('id')}")
```

**Expected outcome**: Available versions listed

### Step 3: Get Schema

Retrieve the schema for a specific version:

```python
schemas = client.get_api_schema(api_id="<api-id>", version_id="<version-id>")

if schemas:
    schema = schemas[0]
    print(f"Schema type: {schema.get('type', 'N/A')}")
    print(f"Language: {schema.get('language', 'N/A')}")
else:
    print("No schema found for this version")
```

**Expected outcome**: Schema retrieved and displayed

### Step 4: Validate Schema

The schema validation happens automatically when you retrieve it. Check for:

1. **Schema Type**: Should be "openapi3", "openapi2", "graphql", etc.
2. **Valid Structure**: Schema should have required fields
3. **No Errors**: Postman API will return errors if schema is malformed

Present findings:

```
=== Schema Validation Results ===
API: Payment Processing API
Version: v2.1.0
Schema Type: OpenAPI 3.0

Status: VALID ✓

Schema Details:
- Endpoints: 15
- Models: 8
- Security: OAuth 2.0

Recommendations:
- Schema is well-formed
- Ready for collection generation
- Consider adding example responses
```

### Step 5: Provide Recommendations

Based on the schema:
- If valid: "Schema looks good! Would you like to generate a collection from it?"
- If has warnings: "Schema is valid but consider these improvements..."
- If invalid: "Schema has errors that need to be fixed before use"

## Success Criteria

This workflow succeeds when:
- [x] API and version identified
- [x] Schema retrieved successfully
- [x] Validation status determined
- [x] Results presented clearly
- [x] Next steps suggested

## Error Handling

### Error: API Not Found

**Symptoms**: "API with ID 'XXX' not found"

**Resolution**:
1. List all APIs: `python scripts/list_collections.py --apis`
2. Verify API name spelling
3. Check workspace scope

### Error: No Schema Found

**Symptoms**: "No schema attached to this version"

**Resolution**:
1. Verify the version has a schema uploaded
2. Check if schema is in a different version
3. Consider importing a schema file

### Error: Invalid Schema

**Symptoms**: "Schema validation failed" or "Malformed schema"

**Resolution**:
1. Check schema follows OpenAPI/Swagger spec
2. Use online validators to find specific errors
3. Re-upload corrected schema

## Exit Conditions

- User acknowledges validation results
- User requests schema corrections
- User asks to generate collection from schema
- User moves to different workflow

## Related Workflows

- **version_comparison.md**: Compare schemas across versions
- **generate_collection.md**: Create collection from schema (future)
- **publish_docs.md**: Publish API documentation

## Examples

Common use cases:
- Validating OpenAPI 3.0 spec before deployment
- Checking GraphQL schema for errors
- Verifying Swagger 2.0 compliance

## Implementation Details

**Location**: `/skills/postman-skill/scripts/` (uses PostmanClient directly)

**API Endpoints Used**:
- `GET /apis` - List APIs
- `GET /apis/{id}/versions` - Get versions
- `GET /apis/{id}/versions/{versionId}/schemas` - Get schema
