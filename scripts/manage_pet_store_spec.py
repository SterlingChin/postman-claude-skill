#!/usr/bin/env python3
"""
Create and manage Pet Store API using Postman's Spec Hub.

This demonstrates the new Spec Hub workflow which replaces the legacy API creation.
Spec Hub provides direct specification management with support for:
- OpenAPI 3.0 and AsyncAPI 2.0
- Single-file and multi-file specifications
- Bidirectional collection generation
- Better version control integration
"""

import sys
import os
import json

# Add parent directory to path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from scripts.postman_client import PostmanClient
from scripts.config import PostmanConfig


def create_petstore_openapi_spec():
    """Create OpenAPI 3.0 specification for Pet Store API."""
    return {
        "openapi": "3.0.0",
        "info": {
            "title": "Pet Store API",
            "description": "A simple Pet Store API with CRUD operations for managing pets",
            "version": "1.0.0",
            "contact": {
                "name": "API Support",
                "email": "support@petstore.example.com"
            },
            "license": {
                "name": "Apache 2.0",
                "url": "https://www.apache.org/licenses/LICENSE-2.0.html"
            }
        },
        "servers": [
            {
                "url": "https://api.petstore.example.com/v1",
                "description": "Production server"
            },
            {
                "url": "https://staging-api.petstore.example.com/v1",
                "description": "Staging server"
            }
        ],
        "paths": {
            "/pets": {
                "get": {
                    "summary": "List all pets",
                    "description": "Returns a list of all pets in the store",
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
                                "minimum": 1,
                                "maximum": 100,
                                "default": 20
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
                                    },
                                    "example": [
                                        {
                                            "id": "pet-001",
                                            "name": "Buddy",
                                            "species": "dog",
                                            "age": 3,
                                            "status": "available"
                                        }
                                    ]
                                }
                            }
                        },
                        "500": {
                            "description": "Internal server error",
                            "content": {
                                "application/json": {
                                    "schema": {
                                        "$ref": "#/components/schemas/Error"
                                    }
                                }
                            }
                        }
                    }
                },
                "post": {
                    "summary": "Create a pet",
                    "description": "Add a new pet to the store",
                    "operationId": "createPet",
                    "tags": ["pets"],
                    "requestBody": {
                        "required": True,
                        "description": "Pet object to be added",
                        "content": {
                            "application/json": {
                                "schema": {
                                    "$ref": "#/components/schemas/NewPet"
                                },
                                "example": {
                                    "name": "Fluffy",
                                    "species": "cat",
                                    "age": 2,
                                    "status": "available"
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
                        },
                        "400": {
                            "description": "Invalid input",
                            "content": {
                                "application/json": {
                                    "schema": {
                                        "$ref": "#/components/schemas/Error"
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
                    "description": "Returns detailed information about a specific pet",
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
                            "description": "Pet not found",
                            "content": {
                                "application/json": {
                                    "schema": {
                                        "$ref": "#/components/schemas/Error"
                                    }
                                }
                            }
                        }
                    }
                },
                "put": {
                    "summary": "Update a pet",
                    "description": "Update an existing pet's information",
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
                        },
                        "400": {
                            "description": "Invalid input"
                        }
                    }
                },
                "delete": {
                    "summary": "Delete a pet",
                    "description": "Remove a pet from the store",
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
                            "description": "Unique identifier for the pet",
                            "example": "pet-001"
                        },
                        "name": {
                            "type": "string",
                            "description": "Name of the pet",
                            "example": "Buddy"
                        },
                        "species": {
                            "type": "string",
                            "description": "Species of the pet",
                            "enum": ["dog", "cat", "bird", "fish", "other"],
                            "example": "dog"
                        },
                        "age": {
                            "type": "integer",
                            "description": "Age of the pet in years",
                            "minimum": 0,
                            "example": 3
                        },
                        "status": {
                            "type": "string",
                            "description": "Availability status",
                            "enum": ["available", "pending", "adopted"],
                            "example": "available"
                        }
                    }
                },
                "NewPet": {
                    "type": "object",
                    "required": ["name"],
                    "properties": {
                        "name": {
                            "type": "string",
                            "description": "Name of the pet",
                            "example": "Fluffy"
                        },
                        "species": {
                            "type": "string",
                            "description": "Species of the pet",
                            "enum": ["dog", "cat", "bird", "fish", "other"],
                            "example": "cat"
                        },
                        "age": {
                            "type": "integer",
                            "description": "Age of the pet in years",
                            "minimum": 0,
                            "example": 2
                        },
                        "status": {
                            "type": "string",
                            "description": "Availability status",
                            "enum": ["available", "pending", "adopted"],
                            "default": "available",
                            "example": "available"
                        }
                    }
                },
                "Error": {
                    "type": "object",
                    "required": ["code", "message"],
                    "properties": {
                        "code": {
                            "type": "integer",
                            "format": "int32",
                            "description": "Error code"
                        },
                        "message": {
                            "type": "string",
                            "description": "Error message"
                        }
                    }
                }
            }
        }
    }


def main():
    """Main workflow for Pet Store Spec Hub management."""

    print("=== Pet Store Spec Hub Management ===\n")
    print("This example demonstrates the NEW Spec Hub workflow")
    print("which replaces the legacy API creation approach.\n")

    # Initialize client
    client = PostmanClient()

    # Step 1: Create the specification in Spec Hub
    print("Step 1: Creating Pet Store specification in Spec Hub...")
    spec_content = create_petstore_openapi_spec()

    # Convert to JSON string
    spec_json = json.dumps(spec_content, indent=2)

    spec_data = {
        "name": "Pet Store API",
        "description": "A simple Pet Store API with CRUD operations",
        "files": [
            {
                "path": "openapi.json",
                "content": spec_json,
                "root": True
            }
        ]
    }

    try:
        spec = client.create_spec(spec_data)
        spec_id = spec.get('id')
        print(f"✓ Specification created successfully in Spec Hub!")
        print(f"  Spec ID: {spec_id}")
        print(f"  Name: {spec.get('name')}")
        print(f"  Files: {len(spec.get('files', []))}")
        print()
    except Exception as e:
        print(f"✗ Error creating specification: {e}")
        return

    # Step 2: Retrieve and validate the specification
    print("Step 2: Retrieving and validating specification...")
    try:
        retrieved_spec = client.get_spec(spec_id)
        files = retrieved_spec.get('files', [])

        print(f"✓ Specification retrieved successfully!")
        print(f"  Name: {retrieved_spec.get('name')}")
        print(f"  Description: {retrieved_spec.get('description')}")
        print(f"  Files: {len(files)}")

        # Show file details
        for file_obj in files:
            root_marker = "[ROOT] " if file_obj.get('root') else ""
            print(f"    - {root_marker}{file_obj.get('path')}")

        # Parse and show spec details
        if files:
            first_file = files[0]
            spec_parsed = json.loads(first_file.get('content', '{}'))
            print(f"\n  OpenAPI Version: {spec_parsed.get('openapi')}")
            print(f"  API Title: {spec_parsed.get('info', {}).get('title')}")
            print(f"  API Version: {spec_parsed.get('info', {}).get('version')}")
            print(f"  Endpoints: {len(spec_parsed.get('paths', {}))}")
            print(f"  Schemas: {len(spec_parsed.get('components', {}).get('schemas', {}))}")
        print()
    except Exception as e:
        print(f"✗ Error retrieving specification: {e}")
        return

    # Step 3: Generate a collection from the specification
    print("Step 3: Generating Postman collection from specification...")
    try:
        result = client.generate_collection_from_spec(
            spec_id,
            collection_name="Pet Store API Collection"
        )

        status = result.get('status', 'unknown')
        print(f"✓ Collection generation initiated!")
        print(f"  Status: {status}")

        if status == 'completed' or 'data' in result:
            data = result.get('data', {})
            collection_id = data.get('collectionId')
            if collection_id:
                print(f"  Collection ID: {collection_id}")
                print(f"  View in Postman: https://postman.postman.co/collections/{collection_id}")
        elif status == 'pending':
            print(f"  Generation is in progress...")
            print(f"  You can check the spec later to see generated collections")
        print()
    except Exception as e:
        print(f"✗ Error generating collection: {e}")
        print("  Note: Collection generation may be asynchronous")
        print()

    # Step 4: List all specs in workspace
    print("Step 4: Listing all specifications in workspace...")
    try:
        specs = client.list_specs(limit=5)
        print(f"✓ Found {len(specs)} specification(s) in workspace:")
        for i, s in enumerate(specs, 1):
            print(f"  {i}. {s.get('name')} (ID: {s.get('id')})")
        print()
    except Exception as e:
        print(f"✗ Error listing specifications: {e}")
        print()

    # Step 5: Show spec files
    print("Step 5: Listing files in specification...")
    try:
        files = client.get_spec_files(spec_id)
        print(f"✓ Specification contains {len(files)} file(s):")
        for file_obj in files:
            root_marker = "[ROOT] " if file_obj.get('root') else ""
            size = len(file_obj.get('content', ''))
            print(f"  - {root_marker}{file_obj.get('path')} ({size:,} bytes)")
        print()
    except Exception as e:
        print(f"✗ Error listing files: {e}")
        print()

    print("=== Workflow Complete ===\n")
    print("Summary:")
    print(f"  ✓ Created specification: {spec.get('name')}")
    print(f"  ✓ Spec ID: {spec_id}")
    print(f"  ✓ Generated collection from spec")
    print()
    print("Next Steps:")
    print("  • View your spec in Postman: https://postman.postman.co/workspace/specs")
    print("  • Update the spec using update_spec_file()")
    print("  • Generate more collections with different names")
    print("  • Create a spec from an existing collection using generate_spec_from_collection()")
    print()
    print("Note: This replaces the legacy create_api() workflow.")
    print("Spec Hub provides better version control and collection generation.")


if __name__ == '__main__':
    main()
