#!/usr/bin/env python3
"""
Create and manage Pet Store API using v10 API model with collections.
Demonstrates Design phase workflow using collections as the primary artifact.
"""

import sys
import os
import json

# Add parent directory to path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from scripts.postman_client import PostmanClient
from scripts.config import PostmanConfig


def create_petstore_v1_collection():
    """Create a Postman collection for Pet Store v1.0 with CRUD operations."""
    return {
        "info": {
            "name": "Pet Store API v1.0",
            "description": "A simple Pet Store API with CRUD operations for managing pets",
            "schema": "https://schema.getpostman.com/json/collection/v2.1.0/collection.json"
        },
        "variable": [
            {
                "key": "baseUrl",
                "value": "https://api.petstore.example.com/v1",
                "type": "string"
            }
        ],
        "item": [
            {
                "name": "Pets",
                "item": [
                    {
                        "name": "List all pets",
                        "request": {
                            "method": "GET",
                            "header": [],
                            "url": {
                                "raw": "{{baseUrl}}/pets?limit=20",
                                "host": ["{{baseUrl}}"],
                                "path": ["pets"],
                                "query": [
                                    {
                                        "key": "limit",
                                        "value": "20",
                                        "description": "Maximum number of pets to return"
                                    }
                                ]
                            },
                            "description": "Retrieve a list of all pets in the store"
                        },
                        "response": []
                    },
                    {
                        "name": "Create a pet",
                        "request": {
                            "method": "POST",
                            "header": [
                                {
                                    "key": "Content-Type",
                                    "value": "application/json"
                                }
                            ],
                            "body": {
                                "mode": "raw",
                                "raw": json.dumps({
                                    "name": "Buddy",
                                    "species": "dog",
                                    "age": 3,
                                    "status": "available"
                                }, indent=2)
                            },
                            "url": {
                                "raw": "{{baseUrl}}/pets",
                                "host": ["{{baseUrl}}"],
                                "path": ["pets"]
                            },
                            "description": "Add a new pet to the store"
                        },
                        "response": []
                    },
                    {
                        "name": "Get pet by ID",
                        "request": {
                            "method": "GET",
                            "header": [],
                            "url": {
                                "raw": "{{baseUrl}}/pets/:petId",
                                "host": ["{{baseUrl}}"],
                                "path": ["pets", ":petId"],
                                "variable": [
                                    {
                                        "key": "petId",
                                        "value": "123",
                                        "description": "ID of the pet to retrieve"
                                    }
                                ]
                            },
                            "description": "Retrieve details of a specific pet by ID"
                        },
                        "response": []
                    },
                    {
                        "name": "Update a pet",
                        "request": {
                            "method": "PUT",
                            "header": [
                                {
                                    "key": "Content-Type",
                                    "value": "application/json"
                                }
                            ],
                            "body": {
                                "mode": "raw",
                                "raw": json.dumps({
                                    "name": "Buddy",
                                    "species": "dog",
                                    "age": 4,
                                    "status": "adopted"
                                }, indent=2)
                            },
                            "url": {
                                "raw": "{{baseUrl}}/pets/:petId",
                                "host": ["{{baseUrl}}"],
                                "path": ["pets", ":petId"],
                                "variable": [
                                    {
                                        "key": "petId",
                                        "value": "123",
                                        "description": "ID of the pet to update"
                                    }
                                ]
                            },
                            "description": "Update an existing pet's information"
                        },
                        "response": []
                    },
                    {
                        "name": "Delete a pet",
                        "request": {
                            "method": "DELETE",
                            "header": [],
                            "url": {
                                "raw": "{{baseUrl}}/pets/:petId",
                                "host": ["{{baseUrl}}"],
                                "path": ["pets", ":petId"],
                                "variable": [
                                    {
                                        "key": "petId",
                                        "value": "123",
                                        "description": "ID of the pet to delete"
                                    }
                                ]
                            },
                            "description": "Remove a pet from the store"
                        },
                        "response": []
                    }
                ]
            }
        ]
    }


def create_petstore_v1_1_collection():
    """Create a Postman collection for Pet Store v1.1 with search endpoint."""
    collection = create_petstore_v1_collection()

    # Update metadata
    collection["info"]["name"] = "Pet Store API v1.1"
    collection["info"]["description"] = "Pet Store API v1.1 - Added search functionality"

    # Add search endpoint
    search_request = {
        "name": "Search pets",
        "request": {
            "method": "GET",
            "header": [],
            "url": {
                "raw": "{{baseUrl}}/pets/search?species=dog&status=available&minAge=1&maxAge=5",
                "host": ["{{baseUrl}}"],
                "path": ["pets", "search"],
                "query": [
                    {
                        "key": "species",
                        "value": "dog",
                        "description": "Filter by species (dog, cat, bird, fish, other)"
                    },
                    {
                        "key": "status",
                        "value": "available",
                        "description": "Filter by status (available, pending, adopted)"
                    },
                    {
                        "key": "minAge",
                        "value": "1",
                        "description": "Minimum age in years"
                    },
                    {
                        "key": "maxAge",
                        "value": "5",
                        "description": "Maximum age in years"
                    }
                ]
            },
            "description": "Search for pets using multiple criteria"
        },
        "response": []
    }

    # Insert search request after "List all pets"
    collection["item"][0]["item"].insert(1, search_request)

    return collection


def compare_collections(collection1, collection2):
    """Compare two collections and identify differences."""

    def get_requests(collection):
        """Extract all request names from a collection."""
        requests = []
        for folder in collection.get("item", []):
            for item in folder.get("item", []):
                requests.append(item.get("name"))
        return requests

    requests_v1 = get_requests(collection1)
    requests_v1_1 = get_requests(collection2)

    added = [r for r in requests_v1_1 if r not in requests_v1]
    removed = [r for r in requests_v1 if r not in requests_v1_1]
    unchanged = [r for r in requests_v1 if r in requests_v1_1]

    return {
        "added": added,
        "removed": removed,
        "unchanged": unchanged
    }


def main():
    """Main workflow for Pet Store API management using collections."""

    print("=== Pet Store API Management (v10 Collections Approach) ===\n")

    # Initialize client
    client = PostmanClient()

    # Step 1: Create v1.0 collection
    print("Step 1: Creating Pet Store API v1.0 collection...")
    collection_v1 = create_petstore_v1_collection()

    try:
        created_v1 = client.create_collection(collection_v1)
        collection_v1_id = created_v1.get('uid')
        print(f"✓ Collection v1.0 created successfully!")
        print(f"  ID: {collection_v1_id}")
        print(f"  Name: {created_v1.get('name')}")
        print(f"  Endpoints: 5 (CRUD operations)")
        print("    - GET /pets (List all pets)")
        print("    - POST /pets (Create a pet)")
        print("    - GET /pets/:petId (Get pet by ID)")
        print("    - PUT /pets/:petId (Update a pet)")
        print("    - DELETE /pets/:petId (Delete a pet)")
        print()
    except Exception as e:
        print(f"✗ Error creating v1.0 collection: {e}")
        return

    # Step 2: Validate the collection structure
    print("Step 2: Validating v1.0 collection structure...")
    try:
        retrieved_v1 = client.get_collection(collection_v1_id)

        total_requests = sum(len(folder.get('item', [])) for folder in retrieved_v1.get('item', []))

        print("✓ Collection validation successful!")
        print(f"  Schema: {retrieved_v1.get('info', {}).get('schema')}")
        print(f"  Folders: {len(retrieved_v1.get('item', []))}")
        print(f"  Total Requests: {total_requests}")
        print(f"  Variables: {len(retrieved_v1.get('variable', []))}")
        print()
    except Exception as e:
        print(f"✗ Error validating collection: {e}")
        return

    # Step 3: Create v1.1 collection with search endpoint
    print("Step 3: Creating Pet Store API v1.1 with search endpoint...")
    collection_v1_1 = create_petstore_v1_1_collection()

    try:
        created_v1_1 = client.create_collection(collection_v1_1)
        collection_v1_1_id = created_v1_1.get('uid')
        print(f"✓ Collection v1.1 created successfully!")
        print(f"  ID: {collection_v1_1_id}")
        print(f"  Name: {created_v1_1.get('name')}")
        print(f"  Endpoints: 6 (added search)")
        print("    - GET /pets (List all pets)")
        print("    - GET /pets/search (Search pets) [NEW]")
        print("    - POST /pets (Create a pet)")
        print("    - GET /pets/:petId (Get pet by ID)")
        print("    - PUT /pets/:petId (Update a pet)")
        print("    - DELETE /pets/:petId (Delete a pet)")
        print()
    except Exception as e:
        print(f"✗ Error creating v1.1 collection: {e}")
        return

    # Step 4: Compare versions
    print("Step 4: Comparing v1.0 and v1.1...")

    try:
        diff = compare_collections(collection_v1, collection_v1_1)

        print("=== Version Comparison ===")
        print()
        print(f"Version 1.0:")
        print(f"  Collection ID: {collection_v1_id}")
        print(f"  Total Endpoints: 5")
        print()

        print(f"Version 1.1:")
        print(f"  Collection ID: {collection_v1_1_id}")
        print(f"  Total Endpoints: 6")
        print()

        print("Key Differences:")
        if diff["added"]:
            print(f"✓ Added {len(diff['added'])} new endpoint(s):")
            for endpoint in diff["added"]:
                print(f"  - {endpoint}")

        if diff["removed"]:
            print(f"⚠ Removed {len(diff['removed'])} endpoint(s):")
            for endpoint in diff["removed"]:
                print(f"  - {endpoint}")

        print()
        print(f"Unchanged: {len(diff['unchanged'])} endpoints remain the same")
        print()

        print("Breaking Changes Analysis:")
        if not diff["removed"]:
            print("✓ No breaking changes - all v1.0 endpoints preserved")
            print("✓ Backward compatible with existing clients")
        else:
            print("⚠ Breaking changes detected - removed endpoints may affect clients")
        print()

        print("Recommendations:")
        print("- v1.1 adds search capabilities without breaking existing functionality")
        print("- Safe to migrate existing clients from v1.0 to v1.1")
        print("- New search endpoint enhances pet discovery")
        print("- Consider deprecating v1.0 after client migration period")
        print()

    except Exception as e:
        print(f"✗ Error comparing collections: {e}")
        return

    # Step 5: Generate OpenAPI schema from collection (validation)
    print("Step 5: Schema representation of v1.1...")
    print("The collection contains the following schema elements:")
    print("  - Base URL: {{baseUrl}} = https://api.petstore.example.com/v1")
    print("  - Request/Response formats: JSON")
    print("  - Query parameters: Documented in each request")
    print("  - Path parameters: Documented with examples")
    print()

    print("=== Workflow Complete ===")
    print(f"\nCollection IDs:")
    print(f"  v1.0: {collection_v1_id}")
    print(f"  v1.1: {collection_v1_1_id}")
    print(f"\nView in Postman workspace: https://postman.postman.co/workspace/4ed66bb6-3d06-4a48-a84b-9424dd65fa0c")
    print()
    print("Next Steps:")
    print("  - Run collections with Newman: python scripts/run_collection.py --collection='Pet Store API v1.1'")
    print("  - Create mock server: python scripts/manage_mocks.py")
    print("  - Set up monitoring: python scripts/manage_monitors.py")


if __name__ == '__main__':
    main()
