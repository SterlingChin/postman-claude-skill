# View and Access API Documentation

## Metadata
- **Phase**: Distribute
- **Complexity**: Simple
- **Estimated Time**: 1-2 minutes
- **Prerequisites**: Collection exists

## When to Use

Use this workflow when:
- User asks to "view documentation" or "see API docs"
- User wants to share API documentation with team
- User needs documentation URL for external stakeholders
- Part of API distribution process

## Prerequisites Check

Before starting, verify:
1. Collection exists
2. Collection has documentation (descriptions, examples)
3. API key has permissions to access collections

## Instructions

### Step 1: Get Collection Documentation

Retrieve collection with documentation:

```python
from scripts.postman_client import PostmanClient

client = PostmanClient()
collection = client.get_collection(collection_uid="<collection-id>")

info = collection.get('info', {})
print(f"\n=== API Documentation ===")
print(f"Collection: {info.get('name', 'Unnamed')}")
print(f"Description: {info.get('description', 'No description available')}")
print(f"Schema: {info.get('schema', 'N/A')}")
```

**Expected outcome**: Collection metadata displayed

### Step 2: Extract Request Documentation

List all documented requests:

```python
items = collection.get('item', [])

print(f"\nAvailable Endpoints ({len(items)}):\n")
for i, item in enumerate(items, 1):
    request = item.get('request', {})
    method = request.get('method', 'N/A')
    url = request.get('url', {})

    if isinstance(url, dict):
        url_string = url.get('raw', 'N/A')
    else:
        url_string = url

    print(f"{i}. {method} {url_string}")

    # Show description if available
    description = item.get('request', {}).get('description', '')
    if description:
        print(f"   Description: {description[:100]}...")

    # Show if examples exist
    responses = item.get('response', [])
    if responses:
        print(f"   Examples: {len(responses)} response(s)")

    print()
```

**Expected outcome**: Documented endpoints listed

### Step 3: Check Documentation Completeness

Assess documentation quality:

```python
total_requests = len(items)
documented_requests = 0
requests_with_examples = 0

for item in items:
    # Check for description
    if item.get('request', {}).get('description'):
        documented_requests += 1

    # Check for examples
    if item.get('response', []):
        requests_with_examples += 1

doc_percentage = (documented_requests / total_requests * 100) if total_requests > 0 else 0
example_percentage = (requests_with_examples / total_requests * 100) if total_requests > 0 else 0

print(f"=== Documentation Quality ===")
print(f"Total Endpoints: {total_requests}")
print(f"With Descriptions: {documented_requests} ({doc_percentage:.0f}%)")
print(f"With Examples: {requests_with_examples} ({example_percentage:.0f}%)")

if doc_percentage >= 80:
    print("\n✓ Documentation coverage is excellent")
elif doc_percentage >= 50:
    print("\n⚠ Documentation coverage is moderate")
else:
    print("\n✗ Documentation coverage is low")
```

**Expected outcome**: Documentation quality assessment

### Step 4: Provide Documentation Access

Show how to access the documentation:

```
=== Access Documentation ===

1. Postman Web UI:
   https://www.postman.com/[workspace]/collection/[collection-id]

2. Public Documentation (if published):
   https://documenter.getpostman.com/view/[collection-id]

3. Export Documentation:
   - Export collection as JSON
   - Generate docs with postman-to-openapi
   - Use external documentation tools

Current Status:
- Collection: Payment Processing API
- Endpoints: 15
- Documentation: 90% complete
- Examples: 80% complete

Recommendations:
1. Add descriptions to 2 undocumented endpoints
2. Add examples to 3 endpoints without responses
3. Consider publishing public documentation
```

### Step 5: Suggest Next Steps

Based on documentation state:
- **Well documented**: "Documentation looks great! Would you like to publish it publicly?"
- **Partially documented**: "Add descriptions and examples to improve documentation."
- **Poorly documented**: "Consider documenting your API for better developer experience."

## Success Criteria

This workflow succeeds when:
- [x] Documentation accessed and reviewed
- [x] Quality assessment performed
- [x] Access methods provided
- [x] Recommendations given
- [x] User knows how to improve or share docs

## Error Handling

### Error: Collection Not Found

**Symptoms**: "Collection 'XXX' not found"

**Resolution**:
1. List collections to verify ID
2. Check workspace scope
3. Verify permissions

### Error: No Documentation Found

**Symptoms**: Empty descriptions or no examples

**Resolution**:
This is a finding, not an error:
1. Report documentation gaps
2. Recommend adding descriptions
3. Suggest adding example responses

## Documentation Best Practices

1. **Clear Descriptions**: Every endpoint should have a description
2. **Example Responses**: Include success and error examples
3. **Parameter Documentation**: Describe all parameters
4. **Authentication Info**: Document auth requirements
5. **Error Codes**: List possible error responses
6. **Rate Limits**: Document any rate limiting
7. **Versioning**: Clearly indicate API version

## Exit Conditions

- User has reviewed documentation
- User understands documentation gaps
- User asks to improve documentation
- User requests to publish documentation
- User moves to different workflow

## Related Workflows

- **publish_docs.md**: Publish public documentation (future)
- **manage_collections.md**: Update collection descriptions
- **export_collection.md**: Export for external tools (future)

## Tips

1. **Use Markdown**: Postman supports markdown in descriptions
2. **Add Examples**: Save real API responses as examples
3. **Organize Folders**: Use folders to group related endpoints
4. **Version Your Docs**: Keep docs in sync with API versions
5. **Test Examples**: Ensure examples are current and working

## Examples

### Quick Documentation Check

```python
collection = client.get_collection("<collection-id>")
items = collection.get('item', [])
undocumented = [item for item in items if not item.get('request', {}).get('description')]

if undocumented:
    print(f"⚠ {len(undocumented)} endpoints need documentation")
else:
    print("✓ All endpoints documented!")
```

### Generate Simple Documentation Report

```python
collection = client.get_collection("<collection-id>")
info = collection.get('info', {})

print(f"# {info.get('name')}")
print(f"\n{info.get('description', '')}\n")

for item in collection.get('item', []):
    request = item.get('request', {})
    print(f"## {request.get('method')} {item.get('name')}")
    print(f"{request.get('description', 'No description')}\n")
```

## Implementation Details

**Location**: `/skills/postman-skill/workflows/distribute/`

**API Endpoints Used**:
- `GET /collections/{uid}` - Get collection with documentation

**Note**: For publishing public documentation, additional Postman API endpoints may be required (not covered in this workflow).
