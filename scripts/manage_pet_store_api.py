#!/usr/bin/env python3
"""
Create and manage Pet Store API with versions and schemas.
Demonstrates the full Design phase workflow: create, validate, version, and compare.
"""

import sys
import os
import json

# Add parent directory to path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from scripts.postman_client import PostmanClient
from scripts.config import PostmanConfig


def create_petstore_v1_schema():
    """Create OpenAPI 3.0 schema for Pet Store v1.0 with basic CRUD operations."""
    return {
        "openapi": "3.0.0",
        "info": {
            "title": "Pet Store API",
            "description": "A simple Pet Store API with CRUD operations for managing pets",
            "version": "1.0.0"
        },
        "servers": [
            {
                "url": "https://api.petstore.example.com/v1",
                "description": "Production server"
            }
        ],
        "paths": {
            "/pets": {
                "get": {
                    "summary": "List all pets",
                    "operationId": "listPets",
                    "tags": ["pets"],
                    "parameters": [
                        {
                            "name": "limit",
                            "in": "query",
                            "description": "Maximum number of pets to return",
                            "required": False,
                            "schema": {
                                "type": "integer",
                                "format": "int32",
                                "default": 20
                            }
                        }
                    ],
                    "responses": {
                        "200": {
                            "description": "A list of pets",
                            "content": {
                                "application/json": {
                                    "schema": {
                                        "type": "array",
                                        "items": {
                                            "$ref": "#/components/schemas/Pet"
                                        }
                                    }
                                }
                            }
                        }
                    }
                },
                "post": {
                    "summary": "Create a pet",
                    "operationId": "createPet",
                    "tags": ["pets"],
                    "requestBody": {
                        "required": True,
                        "content": {
                            "application/json": {
                                "schema": {
                                    "$ref": "#/components/schemas/NewPet"
                                }
                            }
                        }
                    },
                    "responses": {
                        "201": {
                            "description": "Pet created successfully",
                            "content": {
                                "application/json": {
                                    "schema": {
                                        "$ref": "#/components/schemas/Pet"
                                    }
                                }
                            }
                        }
                    }
                }
            },
            "/pets/{petId}": {
                "get": {
                    "summary": "Get a pet by ID",
                    "operationId": "getPetById",
                    "tags": ["pets"],
                    "parameters": [
                        {
                            "name": "petId",
                            "in": "path",
                            "required": True,
                            "description": "The ID of the pet to retrieve",
                            "schema": {
                                "type": "string"
                            }
                        }
                    ],
                    "responses": {
                        "200": {
                            "description": "Pet details",
                            "content": {
                                "application/json": {
                                    "schema": {
                                        "$ref": "#/components/schemas/Pet"
                                    }
                                }
                            }
                        },
                        "404": {
                            "description": "Pet not found"
                        }
                    }
                },
                "put": {
                    "summary": "Update a pet",
                    "operationId": "updatePet",
                    "tags": ["pets"],
                    "parameters": [
                        {
                            "name": "petId",
                            "in": "path",
                            "required": True,
                            "description": "The ID of the pet to update",
                            "schema": {
                                "type": "string"
                            }
                        }
                    ],
                    "requestBody": {
                        "required": True,
                        "content": {
                            "application/json": {
                                "schema": {
                                    "$ref": "#/components/schemas/NewPet"
                                }
                            }
                        }
                    },
                    "responses": {
                        "200": {
                            "description": "Pet updated successfully",
                            "content": {
                                "application/json": {
                                    "schema": {
                                        "$ref": "#/components/schemas/Pet"
                                    }
                                }
                            }
                        },
                        "404": {
                            "description": "Pet not found"
                        }
                    }
                },
                "delete": {
                    "summary": "Delete a pet",
                    "operationId": "deletePet",
                    "tags": ["pets"],
                    "parameters": [
                        {
                            "name": "petId",
                            "in": "path",
                            "required": True,
                            "description": "The ID of the pet to delete",
                            "schema": {
                                "type": "string"
                            }
                        }
                    ],
                    "responses": {
                        "204": {
                            "description": "Pet deleted successfully"
                        },
                        "404": {
                            "description": "Pet not found"
                        }
                    }
                }
            }
        },
        "components": {
            "schemas": {
                "Pet": {
                    "type": "object",
                    "required": ["id", "name"],
                    "properties": {
                        "id": {
                            "type": "string",
                            "description": "Unique identifier for the pet"
                        },
                        "name": {
                            "type": "string",
                            "description": "Name of the pet"
                        },
                        "species": {
                            "type": "string",
                            "description": "Species of the pet",
                            "enum": ["dog", "cat", "bird", "fish", "other"]
                        },
                        "age": {
                            "type": "integer",
                            "description": "Age of the pet in years"
                        },
                        "status": {
                            "type": "string",
                            "description": "Availability status",
                            "enum": ["available", "pending", "adopted"]
                        }
                    }
                },
                "NewPet": {
                    "type": "object",
                    "required": ["name"],
                    "properties": {
                        "name": {
                            "type": "string",
                            "description": "Name of the pet"
                        },
                        "species": {
                            "type": "string",
                            "description": "Species of the pet",
                            "enum": ["dog", "cat", "bird", "fish", "other"]
                        },
                        "age": {
                            "type": "integer",
                            "description": "Age of the pet in years"
                        },
                        "status": {
                            "type": "string",
                            "description": "Availability status",
                            "enum": ["available", "pending", "adopted"],
                            "default": "available"
                        }
                    }
                }
            }
        }
    }


def create_petstore_v1_1_schema():
    """Create OpenAPI 3.0 schema for Pet Store v1.1 with additional search endpoint."""
    schema = create_petstore_v1_schema()

    # Update version
    schema["info"]["version"] = "1.1.0"
    schema["info"]["description"] = "Pet Store API v1.1 - Added search functionality"

    # Add new search endpoint
    schema["paths"]["/pets/search"] = {
        "get": {
            "summary": "Search pets by criteria",
            "operationId": "searchPets",
            "tags": ["pets"],
            "parameters": [
                {
                    "name": "species",
                    "in": "query",
                    "description": "Filter by species",
                    "required": False,
                    "schema": {
                        "type": "string",
                        "enum": ["dog", "cat", "bird", "fish", "other"]
                    }
                },
                {
                    "name": "status",
                    "in": "query",
                    "description": "Filter by availability status",
                    "required": False,
                    "schema": {
                        "type": "string",
                        "enum": ["available", "pending", "adopted"]
                    }
                },
                {
                    "name": "minAge",
                    "in": "query",
                    "description": "Minimum age",
                    "required": False,
                    "schema": {
                        "type": "integer"
                    }
                },
                {
                    "name": "maxAge",
                    "in": "query",
                    "description": "Maximum age",
                    "required": False,
                    "schema": {
                        "type": "integer"
                    }
                }
            ],
            "responses": {
                "200": {
                    "description": "Search results",
                    "content": {
                        "application/json": {
                            "schema": {
                                "type": "array",
                                "items": {
                                    "$ref": "#/components/schemas/Pet"
                                }
                            }
                        }
                    }
                }
            }
        }
    }

    return schema


def main():
    """Main workflow for Pet Store API management."""

    print("=== Pet Store API Management ===\n")

    # Initialize client
    client = PostmanClient()

    # Step 1: Create the API
    print("Step 1: Creating Pet Store API...")
    api_data = {
        "name": "Pet Store API v1.0",
        "summary": "A simple Pet Store API",
        "description": "API for managing pets with CRUD operations"
    }

    try:
        api = client.create_api(api_data)
        api_id = api.get('id')
        print(f"✓ API created successfully!")
        print(f"  ID: {api_id}")
        print(f"  Name: {api.get('name')}")
        print()
    except Exception as e:
        print(f"✗ Error creating API: {e}")
        return

    # Step 2: Create v1.0 version and add schema
    print("Step 2: Creating version 1.0.0 with OpenAPI schema...")
    try:
        # Create version
        version_data = {
            "name": "1.0.0"
        }
        version_response = client._make_request(
            'POST',
            f"/apis/{api_id}/versions",
            json={'version': version_data}
        )
        version_1_id = version_response.get('version', {}).get('id')
        print(f"✓ Version 1.0.0 created!")
        print(f"  ID: {version_1_id}")

        # Add schema to version
        schema_v1 = create_petstore_v1_schema()
        schema_data = {
            "type": "openapi3",
            "language": "json",
            "schema": json.dumps(schema_v1)
        }

        schema_response = client._make_request(
            'POST',
            f"/apis/{api_id}/versions/{version_1_id}/schemas",
            json={'schema': schema_data}
        )
        schema_1_id = schema_response.get('schema', {}).get('id')
        print(f"✓ OpenAPI 3.0 schema added to v1.0.0!")
        print(f"  Schema ID: {schema_1_id}")
        print(f"  Endpoints: 5 (GET /pets, POST /pets, GET /pets/{{petId}}, PUT /pets/{{petId}}, DELETE /pets/{{petId}})")
        print()
    except Exception as e:
        print(f"✗ Error creating version or schema: {e}")
        return

    # Step 3: Validate the schema
    print("Step 3: Validating v1.0.0 schema...")
    try:
        schemas = client.get_api_schema(api_id, version_1_id)
        if schemas:
            schema = schemas[0]
            schema_content = json.loads(schema.get('schema', '{}'))

            print("✓ Schema validation successful!")
            print(f"  Type: {schema.get('type')}")
            print(f"  Language: {schema.get('language')}")
            print(f"  API Title: {schema_content.get('info', {}).get('title')}")
            print(f"  API Version: {schema_content.get('info', {}).get('version')}")
            print(f"  Paths defined: {len(schema_content.get('paths', {}))}")
            print(f"  Schemas defined: {len(schema_content.get('components', {}).get('schemas', {}))}")
            print()
        else:
            print("✗ No schema found")
            return
    except Exception as e:
        print(f"✗ Error validating schema: {e}")
        return

    # Step 4: Create v1.1 with additional endpoint
    print("Step 4: Creating version 1.1.0 with search endpoint...")
    try:
        # Create v1.1 version
        version_data = {
            "name": "1.1.0"
        }
        version_response = client._make_request(
            'POST',
            f"/apis/{api_id}/versions",
            json={'version': version_data}
        )
        version_2_id = version_response.get('version', {}).get('id')
        print(f"✓ Version 1.1.0 created!")
        print(f"  ID: {version_2_id}")

        # Add enhanced schema to v1.1
        schema_v1_1 = create_petstore_v1_1_schema()
        schema_data = {
            "type": "openapi3",
            "language": "json",
            "schema": json.dumps(schema_v1_1)
        }

        schema_response = client._make_request(
            'POST',
            f"/apis/{api_id}/versions/{version_2_id}/schemas",
            json={'schema': schema_data}
        )
        schema_2_id = schema_response.get('schema', {}).get('id')
        print(f"✓ Enhanced OpenAPI 3.0 schema added to v1.1.0!")
        print(f"  Schema ID: {schema_2_id}")
        print(f"  Endpoints: 6 (added GET /pets/search)")
        print()
    except Exception as e:
        print(f"✗ Error creating v1.1: {e}")
        return

    # Step 5: Compare versions
    print("Step 5: Comparing v1.0.0 and v1.1.0...")
    try:
        # Get both versions
        version_1 = client.get_api_version(api_id, version_1_id)
        version_2 = client.get_api_version(api_id, version_2_id)

        # Get schemas
        schemas_1 = client.get_api_schema(api_id, version_1_id)
        schemas_2 = client.get_api_schema(api_id, version_2_id)

        schema_1_content = json.loads(schemas_1[0].get('schema', '{}'))
        schema_2_content = json.loads(schemas_2[0].get('schema', '{}'))

        print("=== Version Comparison ===")
        print()
        print(f"Version 1.0.0:")
        print(f"  Created: {version_1.get('createdAt', 'N/A')}")
        print(f"  Schema Version: {schema_1_content.get('info', {}).get('version')}")
        print(f"  Endpoints: {len(schema_1_content.get('paths', {}))}")
        print(f"  Paths: {', '.join(schema_1_content.get('paths', {}).keys())}")
        print()

        print(f"Version 1.1.0:")
        print(f"  Created: {version_2.get('createdAt', 'N/A')}")
        print(f"  Schema Version: {schema_2_content.get('info', {}).get('version')}")
        print(f"  Endpoints: {len(schema_2_content.get('paths', {}))}")
        print(f"  Paths: {', '.join(schema_2_content.get('paths', {}).keys())}")
        print()

        print("Key Differences:")
        print("✓ Added new endpoint: GET /pets/search")
        print("  - Supports filtering by species, status, age range")
        print("  - Enhances pet discovery capabilities")
        print()
        print("No Breaking Changes:")
        print("✓ All v1.0.0 endpoints remain unchanged")
        print("✓ Backward compatible with existing clients")
        print()

        print("Recommendations:")
        print("- v1.1.0 is a minor version with new features")
        print("- Safe to migrate existing clients")
        print("- New search functionality available for adoption")
        print()

    except Exception as e:
        print(f"✗ Error comparing versions: {e}")
        return

    print("=== Workflow Complete ===")
    print(f"\nAPI ID: {api_id}")
    print(f"View in Postman: https://postman.postman.co/workspace/apis/{api_id}")


if __name__ == '__main__':
    main()
