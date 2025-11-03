# Spec Hub Live Testing Instructions

## Quick Start

To test the Spec Hub implementation with live Postman API:

### 1. Get Your Workspace ID

1. Go to [Postman Web](https://web.postman.co/home)
2. Open any workspace (or create a new one)
3. Copy the workspace ID from the URL

Example URL:
```
https://web.postman.co/workspace/12345678-abcd-1234-efgh-123456789abc
                                  ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
                                  This is your workspace ID
```

### 2. Set Workspace ID in .env

Edit the `.env` file:
```bash
POSTMAN_API_KEY=PMAK-your-key-here
POSTMAN_WORKSPACE_ID=12345678-abcd-1234-efgh-123456789abc
```

### 3. Run the Example Script

```bash
cd /Users/sterling.chin@postman.com/work/agent-skill-v1/postman-skill
python scripts/manage_pet_store_spec.py
```

## Expected Output

If successful, you should see:

```
=== Pet Store Spec Hub Management ===

This example demonstrates the NEW Spec Hub workflow
which replaces the legacy API creation approach.

Step 1: Creating Pet Store specification in Spec Hub...
✓ Specification created successfully in Spec Hub!
  Spec ID: spec-12345-abcde
  Name: Pet Store API
  Files: 1

Step 2: Retrieving and validating specification...
✓ Specification retrieved successfully!
  Name: Pet Store API
  Description: A simple Pet Store API with CRUD operations
  Files: 1
    - [ROOT] openapi.json

  OpenAPI Version: 3.0.0
  API Title: Pet Store API
  API Version: 1.0.0
  Endpoints: 2
  Schemas: 3

Step 3: Generating Postman collection from specification...
✓ Collection generation initiated!
  Status: completed (or pending)
  Collection ID: col-12345-abcde
  View in Postman: https://postman.postman.co/collections/col-12345-abcde

Step 4: Listing all specifications in workspace...
✓ Found 1 specification(s) in workspace:
  1. Pet Store API (ID: spec-12345-abcde)

Step 5: Listing files in specification...
✓ Specification contains 1 file(s):
  - [ROOT] openapi.json (9,380 bytes)

=== Workflow Complete ===

Summary:
  ✓ Created specification: Pet Store API
  ✓ Spec ID: spec-12345-abcde
  ✓ Generated collection from spec

Next Steps:
  • View your spec in Postman: https://postman.postman.co/workspace/specs
  • Update the spec using update_spec_file()
  • Generate more collections with different names
  • Create a spec from an existing collection using generate_spec_from_collection()

Note: This replaces the legacy create_api() workflow.
Spec Hub provides better version control and collection generation.
```

## Verify in Postman Web

1. Go to your workspace in Postman Web
2. Click on "APIs" in the left sidebar
3. You should see "Pet Store API" listed
4. Click on it to view the spec details
5. You should see the generated collection in your workspace

## What Gets Created

The example script creates:

1. **API Specification**
   - Name: "Pet Store API"
   - Type: OpenAPI 3.0
   - File: openapi.json with full CRUD operations

2. **Endpoints** (5 operations)
   - GET /pets - List all pets
   - POST /pets - Create a pet
   - GET /pets/{petId} - Get pet by ID
   - PUT /pets/{petId} - Update a pet
   - DELETE /pets/{petId} - Delete a pet

3. **Schemas** (3 models)
   - Pet - Full pet object with ID
   - NewPet - Pet creation payload
   - Error - Error response format

4. **Generated Collection**
   - Automatically created from the spec
   - Includes all endpoints as requests
   - Has example responses
   - Ready to test immediately

## Troubleshooting

### Error: "workspace_id is required"
- Ensure `POSTMAN_WORKSPACE_ID` is set in `.env`
- Value should be a valid workspace ID from your Postman account

### Error: "API request failed"
- Check that `POSTMAN_API_KEY` is valid
- Ensure your API key has permissions for the workspace
- Verify you have internet connectivity

### Error: "Resource not found"
- Confirm the workspace ID is correct
- Make sure you have access to that workspace

### Collection Generation Status: "pending"
- Collection generation can be asynchronous
- Wait a few seconds and check your workspace
- The collection will appear even if status is "pending"

## Clean Up

To remove the test spec after testing:

```python
from scripts.postman_client import PostmanClient

client = PostmanClient()

# Get the spec ID from the output
spec_id = "spec-12345-abcde"

# Delete the spec
client.delete_spec(spec_id)
print(f"Deleted spec: {spec_id}")
```

## Additional Tests

### Test List Specs

```python
from scripts.postman_client import PostmanClient

client = PostmanClient()
specs = client.list_specs(limit=10)

print(f"Found {len(specs)} specs:")
for spec in specs:
    print(f"  - {spec['name']} ({spec['id']})")
```

### Test Update Spec

```python
client = PostmanClient()

# Update spec name
client.update_spec("spec-12345", {
    "name": "Pet Store API v2",
    "description": "Updated description"
})
```

### Test Generate Spec from Collection

```python
client = PostmanClient()

# Generate spec from existing collection
result = client.generate_spec_from_collection(
    collection_id="col-12345-abcde",
    spec_name="Generated from Collection"
)
print(f"Generated spec: {result}")
```

## Success Criteria

The implementation is working correctly if:

- ✅ Spec is created without errors
- ✅ Spec appears in Postman Web UI
- ✅ Spec details match the input (name, description, files)
- ✅ Collection is generated (immediately or asynchronously)
- ✅ Generated collection has all expected endpoints
- ✅ List specs shows the created spec
- ✅ Get spec returns full details including file content

## Support

If you encounter issues:

1. Run setup validation: `python scripts/validate_setup.py`
2. Check Postman API status: https://status.postman.com
3. Review error messages for specific guidance
4. Consult the workflow documentation: `workflows/design/manage_specs.md`
