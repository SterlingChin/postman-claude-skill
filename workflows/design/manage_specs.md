# Manage API Specifications in Spec Hub

**Workflow Category**: Design
**Complexity**: Medium
**Prerequisites**: Postman API key, Workspace ID

## Overview

This workflow demonstrates how to manage API specifications using Postman's **Spec Hub**. Spec Hub is the modern, recommended way to manage API specifications, replacing the legacy API creation workflow.

**Key Benefits of Spec Hub:**
- Direct specification management (OpenAPI 3.0, AsyncAPI 2.0)
- Support for both single-file and multi-file specifications
- Bidirectional collection generation (spec → collection, collection → spec)
- Better version control and collaboration
- Simplified workflow without intermediate API/version entities

**What's Deprecated:**
- The old `create_api()` method is deprecated in favor of `create_spec()`
- Legacy workflow: Create API → Create Version → Add Schema
- New workflow: Create Spec directly with files

## Supported Specification Formats

- **OpenAPI 3.0** (JSON or YAML)
- **AsyncAPI 2.0** (JSON or YAML)

## Use Cases

1. **Create a new API specification** from scratch
2. **Upload existing OpenAPI/AsyncAPI specs** to Postman
3. **Generate collections** automatically from specifications
4. **Generate specifications** from existing collections
5. **Manage multi-file specifications** with separate schema files
6. **Update and version** API specifications over time

---

## Workflow 1: Create a Single-File Specification

### Step 1: Prepare Your Specification

Create or prepare your OpenAPI 3.0 or AsyncAPI 2.0 specification as a JSON or YAML string.

```python
import json

# OpenAPI 3.0 specification
openapi_spec = {
    "openapi": "3.0.0",
    "info": {
        "title": "My API",
        "version": "1.0.0",
        "description": "A sample API"
    },
    "servers": [
        {"url": "https://api.example.com"}
    ],
    "paths": {
        "/users": {
            "get": {
                "summary": "List users",
                "responses": {
                    "200": {
                        "description": "Success",
                        "content": {
                            "application/json": {
                                "schema": {
                                    "type": "array",
                                    "items": {"$ref": "#/components/schemas/User"}
                                }
                            }
                        }
                    }
                }
            }
        }
    },
    "components": {
        "schemas": {
            "User": {
                "type": "object",
                "properties": {
                    "id": {"type": "string"},
                    "name": {"type": "string"}
                }
            }
        }
    }
}

# Convert to JSON string
spec_json = json.dumps(openapi_spec, indent=2)
```

### Step 2: Create Specification in Spec Hub

```python
from scripts.postman_client import PostmanClient

client = PostmanClient()

# Create spec with single file
spec_data = {
    "name": "My API",
    "description": "A sample API specification",
    "files": [
        {
            "path": "openapi.json",  # or "openapi.yaml" for YAML
            "content": spec_json,
            "root": True
        }
    ]
}

spec = client.create_spec(spec_data)
print(f"Created spec: {spec['id']}")
```

### Step 3: Retrieve and Validate

```python
# Get spec details
spec = client.get_spec(spec_id)
print(f"Name: {spec['name']}")
print(f"Files: {len(spec.get('files', []))}")

# List all files
files = client.get_spec_files(spec_id)
for file_obj in files:
    root_marker = "[ROOT] " if file_obj.get('root') else ""
    print(f"  {root_marker}{file_obj['path']}")
```

---

## Workflow 2: Create a Multi-File Specification

Multi-file specifications are useful for complex APIs with modular schemas.

### Example: Separate Schema Files

```python
import json

# Main OpenAPI spec with $refs to external files
main_spec = {
    "openapi": "3.0.0",
    "info": {"title": "E-commerce API", "version": "1.0.0"},
    "paths": {
        "/products": {
            "get": {
                "responses": {
                    "200": {
                        "content": {
                            "application/json": {
                                "schema": {
                                    "type": "array",
                                    "items": {"$ref": "schemas/product.json"}
                                }
                            }
                        }
                    }
                }
            }
        }
    }
}

# Separate schema file
product_schema = {
    "type": "object",
    "properties": {
        "id": {"type": "string"},
        "name": {"type": "string"},
        "price": {"type": "number"}
    }
}

# Create multi-file spec
spec_data = {
    "name": "E-commerce API",
    "description": "Multi-file API specification",
    "files": [
        {
            "path": "openapi.json",
            "content": json.dumps(main_spec),
            "root": True  # This is the root file
        },
        {
            "path": "schemas/product.json",
            "content": json.dumps(product_schema),
            "root": False  # Supporting file
        }
    ]
}

spec = client.create_spec(spec_data)
```

### Add Files to Existing Spec

```python
# Add a new schema file later
order_schema = {
    "type": "object",
    "properties": {
        "id": {"type": "string"},
        "items": {"type": "array"}
    }
}

client.create_spec_file(
    spec_id=spec['id'],
    file_path="schemas/order.json",
    content=json.dumps(order_schema)
)
```

---

## Workflow 3: Generate Collection from Specification

Once you have a spec, automatically generate a Postman collection with requests, folders, and examples.

```python
# Generate collection from spec
result = client.generate_collection_from_spec(
    spec_id,
    collection_name="My API Collection"
)

# Check status
status = result.get('status')
if status == 'completed':
    collection_id = result['data']['collectionId']
    print(f"Collection created: {collection_id}")
elif status == 'pending':
    print("Generation in progress...")

# List all collections generated from this spec
collections = client.list_collections_from_spec(spec_id)
for col in collections:
    print(f"- {col['name']} (ID: {col['id']})")
```

**What Gets Generated:**
- Folders for each tag/path
- Requests for each operation
- Example responses from the spec
- Request parameters and bodies
- Authentication configuration

---

## Workflow 4: Generate Specification from Collection

Reverse-engineer a specification from an existing Postman collection.

```python
# Generate spec from collection
result = client.generate_spec_from_collection(
    collection_id="your-collection-uid",
    spec_name="Generated API Spec"
)

# Check result
if result.get('status') == 'completed':
    spec_id = result['data']['specId']
    print(f"Spec created: {spec_id}")

    # Retrieve the generated spec
    spec = client.get_spec(spec_id)
    print(f"Generated spec: {spec['name']}")
```

**Use Cases:**
- Document existing APIs that only have collections
- Migrate from collection-first to spec-first workflow
- Generate OpenAPI specs for API gateways

---

## Workflow 5: Update Specifications

### Update Spec Metadata

```python
# Update name and description
client.update_spec(spec_id, {
    "name": "My API v2",
    "description": "Updated API description"
})
```

### Update File Content

```python
# Update the spec file content
updated_spec_json = json.dumps(updated_openapi_spec)

client.update_spec_file(
    spec_id=spec_id,
    file_path="openapi.json",
    content=updated_spec_json
)
```

### Change Root File

```python
# Make a different file the root
client.update_spec_file(
    spec_id=spec_id,
    file_path="openapi-v2.json",
    root=True
)
```

---

## Workflow 6: List and Manage Specifications

### List All Specs in Workspace

```python
# List specs with pagination
specs = client.list_specs(limit=20, offset=0)

for spec in specs:
    print(f"{spec['name']}")
    print(f"  ID: {spec['id']}")
    print(f"  Files: {len(spec.get('files', []))}")
    print()
```

### Delete a Specification

```python
# Delete spec (warning: this is permanent!)
client.delete_spec(spec_id)
print("Specification deleted")
```

---

## YAML Support

Both JSON and YAML formats are supported. Simply provide YAML content as a string:

```python
import yaml

# Define spec in YAML (more human-readable)
openapi_yaml = """
openapi: 3.0.0
info:
  title: My API
  version: 1.0.0
paths:
  /users:
    get:
      summary: List users
      responses:
        '200':
          description: Success
"""

spec_data = {
    "name": "My API",
    "files": [
        {
            "path": "openapi.yaml",
            "content": openapi_yaml,
            "root": True
        }
    ]
}

spec = client.create_spec(spec_data)
```

---

## Complete Example Script

See `scripts/manage_pet_store_spec.py` for a complete working example demonstrating:
- Creating a single-file OpenAPI 3.0 spec
- Retrieving and validating the spec
- Generating a collection from the spec
- Listing all specs
- Listing spec files

**Run the example:**
```bash
python scripts/manage_pet_store_spec.py
```

---

## Migration from Legacy API Creation

If you're currently using the old `create_api()` approach:

### Old Workflow (Deprecated)
```python
# ❌ Old way - deprecated
api = client.create_api({"name": "My API"})
version = client._make_request('POST', f"/apis/{api['id']}/versions", ...)
schema = client._make_request('POST', f"/apis/{api['id']}/versions/{version['id']}/schemas", ...)
```

### New Workflow (Recommended)
```python
# ✅ New way - Spec Hub
spec = client.create_spec({
    "name": "My API",
    "files": [
        {
            "path": "openapi.json",
            "content": spec_json,
            "root": True
        }
    ]
})
```

**Benefits:**
- Single operation instead of three
- Direct file management
- Better collection generation
- More intuitive workflow

---

## Best Practices

1. **Use Spec Hub for all new APIs** - Don't use the legacy `create_api()` method
2. **Start with single-file specs** - Only use multi-file when needed
3. **Validate specs locally first** - Use tools like Swagger Editor before uploading
4. **Use meaningful file paths** - e.g., `schemas/user.json`, not `file1.json`
5. **Generate collections early** - Test your spec by generating a collection
6. **Version in file names** - e.g., `openapi-v1.json`, `openapi-v2.json`
7. **Use YAML for readability** - YAML is often easier to read and edit than JSON

---

## Error Handling

Common errors and solutions:

**Invalid spec format:**
```
ValidationError: Invalid OpenAPI specification
```
- Validate your spec with Swagger Editor or OpenAPI validator first
- Check that all $refs are valid
- Ensure required fields are present

**Missing root file:**
```
ValueError: At least one file must be marked as root
```
- Ensure one file has `"root": True`
- Or let the first file be root by default

**File path conflicts:**
```
ValidationError: File path already exists
```
- Use unique file paths within the spec
- Delete old file before creating new one with same path

---

## Advanced Use Cases

### Importing External Specs

```python
# Import from file
with open('my-api.json', 'r') as f:
    spec_content = f.read()

spec = client.create_spec({
    "name": "Imported API",
    "files": [{"path": "openapi.json", "content": spec_content, "root": True}]
})
```

### Syncing with GitHub

```python
import requests

# Fetch spec from GitHub
response = requests.get('https://raw.githubusercontent.com/user/repo/main/openapi.yaml')
spec_content = response.text

# Create spec in Postman
spec = client.create_spec({
    "name": "GitHub Synced API",
    "files": [{"path": "openapi.yaml", "content": spec_content, "root": True}]
})
```

### Spec Comparison

```python
# Get two versions of a spec
spec_v1 = client.get_spec(spec_id_v1)
spec_v2 = client.get_spec(spec_id_v2)

# Compare (you would implement comparison logic)
# This is where you could detect breaking changes, new endpoints, etc.
```

---

## Related Operations

- **Collections**: See `workflows/build/manage_collections.md`
- **Schema Validation**: See `workflows/design/validate_schema.md`
- **Mock Servers**: See `workflows/deploy/manage_mocks.md`

---

## API Reference

### PostmanClient Methods

- `create_spec(spec_data, workspace_id=None)` - Create new spec
- `list_specs(workspace_id=None, limit=10, offset=0)` - List all specs
- `get_spec(spec_id)` - Get spec details
- `update_spec(spec_id, spec_data)` - Update spec metadata
- `delete_spec(spec_id)` - Delete spec
- `create_spec_file(spec_id, file_path, content, root=False)` - Add file
- `update_spec_file(spec_id, file_path, content=None, root=None)` - Update file
- `delete_spec_file(spec_id, file_path)` - Delete file
- `get_spec_files(spec_id)` - List all files
- `generate_collection_from_spec(spec_id, collection_name=None)` - Generate collection
- `list_collections_from_spec(spec_id)` - List generated collections
- `generate_spec_from_collection(collection_id, spec_name=None, workspace_id=None)` - Generate spec

---

## Learn More

- [Postman Spec Hub Documentation](https://learning.postman.com/docs/design-apis/specifications/overview/)
- [OpenAPI 3.0 Specification](https://swagger.io/specification/)
- [AsyncAPI 2.0 Specification](https://www.asyncapi.com/docs/specifications/v2.0.0)
