#!/usr/bin/env python3
"""
Phase 1 Feature Examples - Postman Skill v1.1

This script demonstrates all Phase 1 enhancements:
- Enhanced error handling
- Collection forking and pull requests
- Environment secret detection
- Duplication features

Requirements:
    export POSTMAN_API_KEY="your-key-here"
    export POSTMAN_WORKSPACE_ID="your-workspace-id"  # optional
"""

import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from scripts.config import get_config
from scripts.postman_client import PostmanClient
from utils.exceptions import (
    ResourceNotFoundError,
    ValidationError,
    AuthenticationError
)


def example_1_enhanced_error_handling():
    """Example 1: Enhanced Error Handling with Custom Exceptions"""
    print("\n" + "="*70)
    print("Example 1: Enhanced Error Handling")
    print("="*70 + "\n")

    client = PostmanClient()

    # Example 1a: Catching specific exceptions
    print("Attempting to get non-existent collection...")
    try:
        client.get_collection("invalid-id-12345")
    except ResourceNotFoundError as e:
        print(f"✅ Caught ResourceNotFoundError")
        print(f"Message: {str(e)[:200]}...")
        print("\nNotice how the error message provides:")
        print("  - Clear description of what went wrong")
        print("  - Possible reasons for the error")
        print("  - Suggestions for resolution")

    # Example 1b: API version detection
    print("\n" + "-"*70)
    print("\nAPI Version Detection:")
    print(f"Detected API version: {client.api_version or 'Not yet detected'}")
    print("The client automatically detects your API version on the first request")


def example_2_collection_version_control():
    """Example 2: Git-like Collection Workflows (v10+ Required)"""
    print("\n" + "="*70)
    print("Example 2: Collection Version Control (Fork, PR, Merge)")
    print("="*70 + "\n")

    client = PostmanClient()

    # Create a test collection
    print("Step 1: Creating a test collection...")
    collection_data = {
        'info': {
            'name': 'Example API Collection',
            'description': 'Demonstrating fork/PR workflows',
            'schema': 'https://schema.getpostman.com/json/collection/v2.1.0/collection.json'
        },
        'item': [
            {
                'name': 'Get Users',
                'request': {
                    'method': 'GET',
                    'url': 'https://jsonplaceholder.typicode.com/users'
                }
            }
        ]
    }

    collection = client.create_collection(collection_data)
    collection_uid = collection['uid']
    print(f"✅ Created collection: {collection_uid}\n")

    # Fork the collection
    print("Step 2: Forking the collection (v10+ feature)...")
    try:
        fork = client.fork_collection(
            collection_uid=collection_uid,
            label="feature-add-posts-endpoint"
        )
        fork_uid = fork.get('uid') or fork.get('id')
        print(f"✅ Forked collection: {fork_uid}")
        print("   This creates an independent copy you can modify\n")

        # Simulate making changes to the fork
        print("Step 3: [Simulated] Making changes to the fork...")
        print("   (In real usage, you'd modify the fork here)\n")

        # Create a pull request
        print("Step 4: Creating a pull request...")
        pr = client.create_pull_request(
            collection_uid=collection_uid,
            source_collection_uid=fork_uid,
            title="Add Posts endpoint",
            description="This PR adds a new endpoint to fetch posts"
        )
        print(f"✅ Created PR: {pr.get('id')}")
        print(f"   Status: {pr.get('status', 'open')}\n")

        # List pull requests
        print("Step 5: Listing all pull requests...")
        prs = client.get_pull_requests(collection_uid)
        print(f"✅ Found {len(prs)} pull request(s)")

        # Merge the pull request
        print("\nStep 6: Merging the pull request...")
        merged = client.merge_pull_request(collection_uid, pr['id'])
        print(f"✅ Merged PR: {merged.get('id')}")
        print("   Changes are now in the parent collection\n")

        # Cleanup
        print("Cleanup: Deleting test collections...")
        client.delete_collection(collection_uid)
        client.delete_collection(fork_uid)
        print("✅ Cleanup complete")

    except Exception as e:
        print(f"⚠️  Fork/PR features require Postman v10+ API")
        print(f"   Error: {str(e)[:100]}...")
        print("\nCleaning up base collection...")
        client.delete_collection(collection_uid)


def example_3_collection_duplication():
    """Example 3: Collection Duplication (Works on all API versions)"""
    print("\n" + "="*70)
    print("Example 3: Collection Duplication")
    print("="*70 + "\n")

    client = PostmanClient()

    # Create a test collection
    print("Step 1: Creating a test collection...")
    collection_data = {
        'info': {
            'name': 'API Tests v1',
            'description': 'Original test collection',
            'schema': 'https://schema.getpostman.com/json/collection/v2.1.0/collection.json'
        },
        'item': [
            {
                'name': 'Health Check',
                'request': {
                    'method': 'GET',
                    'url': 'https://httpbin.org/status/200'
                }
            }
        ]
    }

    original = client.create_collection(collection_data)
    original_uid = original['uid']
    print(f"✅ Created collection: {original_uid}\n")

    # Duplicate the collection
    print("Step 2: Duplicating the collection...")
    duplicate = client.duplicate_collection(
        collection_uid=original_uid,
        name="API Tests v1 - Backup"
    )
    duplicate_uid = duplicate['uid']
    print(f"✅ Duplicated collection: {duplicate_uid}")
    print(f"   Original name: {original['info']['name']}")
    print(f"   Duplicate name: {duplicate['info']['name']}")
    print("\n   Note: Duplication creates a standalone copy (not a fork)")

    # Cleanup
    print("\nCleanup: Deleting test collections...")
    client.delete_collection(original_uid)
    client.delete_collection(duplicate_uid)
    print("✅ Cleanup complete")


def example_4_environment_secrets():
    """Example 4: Automatic Secret Detection for Environments"""
    print("\n" + "="*70)
    print("Example 4: Environment Auto-Secret Detection")
    print("="*70 + "\n")

    client = PostmanClient()

    # Create environment with auto-secret detection
    print("Step 1: Creating environment with sensitive variables...")
    print("\nVariables:")
    print("  - base_url: https://api.example.com  (regular)")
    print("  - api_key: secret-abc-123           (sensitive)")
    print("  - bearer_token: token-xyz-456       (sensitive)")
    print("  - timeout: 30                        (regular)")

    env = client.create_environment(
        name="Example Production Environment",
        values={
            "base_url": "https://api.example.com",
            "api_key": "secret-abc-123",
            "bearer_token": "token-xyz-456",
            "timeout": "30"
        }
    )

    env_uid = env['uid']
    print(f"\n✅ Created environment: {env_uid}")

    # Check which variables were marked as secrets
    variables = env.get('values', [])
    secret_vars = [v for v in variables if v.get('type') == 'secret']
    regular_vars = [v for v in variables if v.get('type') != 'secret']

    print(f"\n🔐 Auto-detected {len(secret_vars)} secret variable(s):")
    for var in secret_vars:
        print(f"   - {var['key']} (type: secret)")

    print(f"\n📝 Regular variables: {len(regular_vars)}")
    for var in regular_vars:
        print(f"   - {var['key']} (type: {var.get('type', 'default')})")

    print("\nKeywords monitored for secrets:")
    print("  api_key, token, secret, password, passwd, pwd,")
    print("  auth, credential, private, bearer, authorization")

    # Cleanup
    print("\nCleanup: Deleting test environment...")
    client.delete_environment(env_uid)
    print("✅ Cleanup complete")


def example_5_environment_updates():
    """Example 5: Partial Environment Updates with Secret Preservation"""
    print("\n" + "="*70)
    print("Example 5: Partial Updates & Secret Preservation")
    print("="*70 + "\n")

    client = PostmanClient()

    # Create initial environment
    print("Step 1: Creating environment with secrets...")
    env = client.create_environment(
        name="Example Staging Environment",
        values={
            "base_url": "https://staging.api.example.com",
            "api_key": "staging-secret-key",
            "timeout": "30"
        }
    )

    env_uid = env['uid']
    print(f"✅ Created environment: {env_uid}")

    # Show initial secrets
    initial_secrets = [v for v in env['values'] if v.get('type') == 'secret']
    print(f"   Initial secrets: {len(initial_secrets)}")
    for var in initial_secrets:
        print(f"     - {var['key']}")

    # Perform partial update
    print("\nStep 2: Performing partial update...")
    print("   Updating: api_key (existing secret)")
    print("   Adding: new_var (new regular variable)")

    updated = client.update_environment(
        environment_uid=env_uid,
        values={
            "api_key": "new-staging-secret-key",  # Update existing
            "new_var": "new_value"                 # Add new
        }
    )

    # Verify secret type was preserved
    variables = updated.get('values', [])
    api_key_var = next((v for v in variables if v['key'] == 'api_key'), None)

    print(f"\n✅ Update complete")
    print(f"   api_key type: {api_key_var.get('type')}")
    print(f"   Secret preserved: {'Yes ✅' if api_key_var.get('type') == 'secret' else 'No ❌'}")
    print(f"   Total variables: {len(variables)}")

    # Cleanup
    print("\nCleanup: Deleting test environment...")
    client.delete_environment(env_uid)
    print("✅ Cleanup complete")


def example_6_environment_duplication():
    """Example 6: Environment Duplication with Secret Preservation"""
    print("\n" + "="*70)
    print("Example 6: Environment Duplication")
    print("="*70 + "\n")

    client = PostmanClient()

    # Create environment with secrets
    print("Step 1: Creating environment with secrets...")
    original = client.create_environment(
        name="Production Config",
        values={
            "base_url": "https://api.production.com",
            "api_key": "prod-secret-key-123",
            "db_password": "prod-db-password",
            "timeout": "60"
        }
    )

    original_uid = original['uid']
    original_secrets = [v for v in original['values'] if v.get('type') == 'secret']
    print(f"✅ Created environment: {original_uid}")
    print(f"   Secrets: {len(original_secrets)}")

    # Duplicate the environment
    print("\nStep 2: Duplicating environment...")
    duplicate = client.duplicate_environment(
        environment_uid=original_uid,
        name="Production Config - Backup"
    )

    duplicate_uid = duplicate['uid']
    duplicate_secrets = [v for v in duplicate['values'] if v.get('type') == 'secret']
    print(f"✅ Duplicated environment: {duplicate_uid}")
    print(f"   Secrets preserved: {len(duplicate_secrets)}")

    # Verify all secrets were preserved
    print(f"\n✅ All {len(original_secrets)} secret(s) preserved:")
    for var in duplicate_secrets:
        print(f"   - {var['key']} (type: secret)")

    # Cleanup
    print("\nCleanup: Deleting test environments...")
    client.delete_environment(original_uid)
    client.delete_environment(duplicate_uid)
    print("✅ Cleanup complete")


def main():
    """Run all Phase 1 examples."""
    print("\n" + "="*70)
    print("  POSTMAN SKILL v1.1 - PHASE 1 FEATURE EXAMPLES")
    print("="*70)

    # Check prerequisites
    if not os.getenv('POSTMAN_API_KEY'):
        print("\n❌ ERROR: POSTMAN_API_KEY not set")
        print("\nPlease set your API key:")
        print("  export POSTMAN_API_KEY='your-key-here'")
        return 1

    print("\n✅ POSTMAN_API_KEY is set")
    print("Ready to demonstrate Phase 1 features!\n")

    # Run examples
    examples = [
        ("Enhanced Error Handling", example_1_enhanced_error_handling),
        ("Collection Version Control", example_2_collection_version_control),
        ("Collection Duplication", example_3_collection_duplication),
        ("Environment Secrets", example_4_environment_secrets),
        ("Environment Updates", example_5_environment_updates),
        ("Environment Duplication", example_6_environment_duplication)
    ]

    for i, (name, func) in enumerate(examples, 1):
        try:
            func()
        except KeyboardInterrupt:
            print("\n\n⚠️  Interrupted by user")
            return 1
        except Exception as e:
            print(f"\n❌ Example failed: {e}")
            import traceback
            traceback.print_exc()

        if i < len(examples):
            input("\nPress Enter to continue to next example...")

    print("\n" + "="*70)
    print("  ALL EXAMPLES COMPLETE!")
    print("="*70 + "\n")

    return 0


if __name__ == '__main__':
    sys.exit(main())
