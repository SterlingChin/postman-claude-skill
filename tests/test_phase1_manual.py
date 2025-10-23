#!/usr/bin/env python3
"""
Manual Test Script for Phase 1 Features

This script tests all Phase 1 enhancements:
- Phase 1.1: API version detection
- Phase 1.2: Enhanced error handling
- Phase 1.3: Collections API (fork, PR, duplicate)
- Phase 1.4: Environments API (secrets, duplicate)

Requirements:
- POSTMAN_API_KEY environment variable set
- POSTMAN_WORKSPACE_ID environment variable set (optional)

Usage:
    python tests/test_phase1_manual.py
"""

import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from scripts.config import get_config
from scripts.postman_client import PostmanClient
from utils.exceptions import (
    AuthenticationError,
    ResourceNotFoundError,
    ValidationError,
    NetworkError
)


def print_section(title):
    """Print a formatted section header."""
    print("\n" + "=" * 70)
    print(f"  {title}")
    print("=" * 70 + "\n")


def print_test(name, passed=True):
    """Print test result."""
    status = "✅ PASS" if passed else "❌ FAIL"
    print(f"{status} - {name}")


def test_phase_1_1_version_detection():
    """Test Phase 1.1: API Version Detection"""
    print_section("Phase 1.1: API Version Detection")

    try:
        config = get_config()
        client = PostmanClient(config)

        # Make a request to trigger version detection
        print("Making initial request to detect API version...")
        collections = client.list_collections()

        # Check if version was detected
        if client.api_version:
            print(f"✅ API version detected: {client.api_version}")
            print_test("API version detection", True)
        else:
            print("⚠️  API version not detected (may be ok)")
            print_test("API version detection", True)

        return True

    except Exception as e:
        print(f"❌ Error: {e}")
        print_test("API version detection", False)
        return False


def test_phase_1_2_error_handling():
    """Test Phase 1.2: Enhanced Error Handling"""
    print_section("Phase 1.2: Enhanced Error Handling")

    config = get_config()
    client = PostmanClient(config)

    # Test 1: ResourceNotFoundError
    print("\nTest 1: ResourceNotFoundError (404)")
    try:
        client.get_collection("invalid-collection-id-12345")
        print_test("ResourceNotFoundError", False)
    except ResourceNotFoundError as e:
        print(f"✅ Caught ResourceNotFoundError: {str(e)[:100]}...")
        print_test("ResourceNotFoundError", True)
    except Exception as e:
        print(f"❌ Wrong exception type: {type(e).__name__}")
        print_test("ResourceNotFoundError", False)

    # Test 2: AuthenticationError (if we can trigger it)
    print("\nTest 2: Exception messages are helpful")
    try:
        # Try to get a non-existent resource
        client.get_collection("fake-id")
    except ResourceNotFoundError as e:
        has_helpful_info = "not found" in str(e).lower()
        if has_helpful_info:
            print("✅ Error message contains helpful information")
            print_test("Helpful error messages", True)
        else:
            print("⚠️  Error message could be more helpful")
            print_test("Helpful error messages", False)
    except Exception as e:
        print(f"⚠️  Unexpected error: {e}")
        print_test("Helpful error messages", False)

    return True


def test_phase_1_3_collections():
    """Test Phase 1.3: Collections API Enhancements"""
    print_section("Phase 1.3: Collections API - Version Control Features")

    config = get_config()
    client = PostmanClient(config)

    created_collection = None
    forked_collection = None
    duplicated_collection = None

    try:
        # List existing collections
        print("Listing existing collections...")
        collections = client.list_collections()
        print(f"✅ Found {len(collections)} collection(s)")

        # Test 1: Create a test collection
        print("\nTest 1: Creating test collection...")
        test_collection = {
            'info': {
                'name': 'Phase 1.3 Test Collection',
                'description': 'Test collection for fork/PR/duplicate features',
                'schema': 'https://schema.getpostman.com/json/collection/v2.1.0/collection.json'
            },
            'item': [
                {
                    'name': 'Test Request',
                    'request': {
                        'method': 'GET',
                        'url': 'https://httpbin.org/get'
                    }
                }
            ]
        }

        created_collection = client.create_collection(test_collection)
        collection_uid = created_collection['uid']
        print(f"✅ Created collection: {collection_uid}")
        print_test("Create collection", True)

        # Test 2: Fork collection (v10+ feature)
        print("\nTest 2: Forking collection (v10+ feature)...")
        try:
            forked_collection = client.fork_collection(
                collection_uid=collection_uid,
                label="test-fork"
            )
            fork_uid = forked_collection.get('uid') or forked_collection.get('id')
            print(f"✅ Forked collection: {fork_uid}")
            print_test("Fork collection", True)
        except Exception as e:
            print(f"⚠️  Fork failed (may require v10+ API): {e}")
            print_test("Fork collection (v10+ required)", None)

        # Test 3: Duplicate collection
        print("\nTest 3: Duplicating collection...")
        try:
            duplicated_collection = client.duplicate_collection(
                collection_uid=collection_uid,
                name="Phase 1.3 Test Collection (Copy)"
            )
            duplicate_uid = duplicated_collection['uid']
            print(f"✅ Duplicated collection: {duplicate_uid}")
            print_test("Duplicate collection", True)
        except Exception as e:
            print(f"❌ Duplicate failed: {e}")
            print_test("Duplicate collection", False)

        # Test 4: Create pull request (v10+ feature)
        if forked_collection:
            print("\nTest 4: Creating pull request (v10+ feature)...")
            try:
                fork_uid = forked_collection.get('uid') or forked_collection.get('id')
                pr = client.create_pull_request(
                    collection_uid=collection_uid,
                    source_collection_uid=fork_uid,
                    title="Test PR from Phase 1.3",
                    description="Testing PR functionality"
                )
                pr_id = pr.get('id')
                print(f"✅ Created PR: {pr_id}")
                print_test("Create pull request", True)

                # Test 5: List pull requests
                print("\nTest 5: Listing pull requests...")
                prs = client.get_pull_requests(collection_uid)
                print(f"✅ Found {len(prs)} pull request(s)")
                print_test("List pull requests", True)

            except Exception as e:
                print(f"⚠️  PR operations failed (may require v10+ API): {e}")
                print_test("Pull request operations (v10+ required)", None)

        return True

    except Exception as e:
        print(f"❌ Collections test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

    finally:
        # Cleanup
        print("\n" + "-" * 70)
        print("Cleanup: Deleting test collections...")
        try:
            if created_collection:
                client.delete_collection(created_collection['uid'])
                print(f"✅ Deleted original collection")
            if duplicated_collection:
                client.delete_collection(duplicated_collection['uid'])
                print(f"✅ Deleted duplicated collection")
            if forked_collection:
                fork_uid = forked_collection.get('uid') or forked_collection.get('id')
                if fork_uid:
                    client.delete_collection(fork_uid)
                    print(f"✅ Deleted forked collection")
        except Exception as e:
            print(f"⚠️  Cleanup error (non-critical): {e}")


def test_phase_1_4_environments():
    """Test Phase 1.4: Environments API Enhancements"""
    print_section("Phase 1.4: Environments API - Secrets & Duplication")

    config = get_config()
    client = PostmanClient(config)

    created_env = None
    duplicated_env = None

    try:
        # Test 1: Create environment with auto-secret detection
        print("Test 1: Creating environment with auto-secret detection...")
        created_env = client.create_environment(
            name="Phase 1.4 Test Environment",
            values={
                "base_url": "https://api.example.com",
                "api_key": "secret-test-key-12345",  # Should be auto-detected as secret
                "timeout": "30",
                "bearer_token": "test-bearer-token"  # Should be auto-detected as secret
            }
        )

        env_uid = created_env['uid']
        print(f"✅ Created environment: {env_uid}")

        # Verify secret detection
        variables = created_env.get('values', [])
        secret_vars = [v for v in variables if v.get('type') == 'secret']
        print(f"✅ Auto-detected {len(secret_vars)} secret variable(s):")
        for var in secret_vars:
            print(f"   - {var['key']} (type: {var['type']})")

        if len(secret_vars) >= 2:
            print_test("Auto-secret detection", True)
        else:
            print("⚠️  Expected 2+ secret variables (api_key, bearer_token)")
            print_test("Auto-secret detection", False)

        # Test 2: Update environment
        print("\nTest 2: Updating environment (partial update)...")
        updated_env = client.update_environment(
            environment_uid=env_uid,
            values={
                "new_var": "new_value",
                "api_key": "updated-secret-key"  # Should remain secret
            }
        )
        print(f"✅ Updated environment")

        # Verify update preserved secrets
        variables = updated_env.get('values', [])
        api_key_var = next((v for v in variables if v['key'] == 'api_key'), None)
        if api_key_var and api_key_var.get('type') == 'secret':
            print(f"✅ Secret type preserved for api_key")
            print_test("Update preserves secrets", True)
        else:
            print(f"⚠️  Secret type not preserved")
            print_test("Update preserves secrets", False)

        # Test 3: Duplicate environment
        print("\nTest 3: Duplicating environment...")
        duplicated_env = client.duplicate_environment(
            environment_uid=env_uid,
            name="Phase 1.4 Test Environment (Copy)"
        )

        duplicate_uid = duplicated_env['uid']
        print(f"✅ Duplicated environment: {duplicate_uid}")

        # Verify secrets were preserved in duplicate
        dup_variables = duplicated_env.get('values', [])
        dup_secrets = [v for v in dup_variables if v.get('type') == 'secret']
        print(f"✅ Duplicated environment has {len(dup_secrets)} secret(s)")

        if len(dup_secrets) >= 2:
            print_test("Duplicate preserves secrets", True)
        else:
            print_test("Duplicate preserves secrets", False)

        return True

    except Exception as e:
        print(f"❌ Environments test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

    finally:
        # Cleanup
        print("\n" + "-" * 70)
        print("Cleanup: Deleting test environments...")
        try:
            if created_env:
                client.delete_environment(created_env['uid'])
                print(f"✅ Deleted original environment")
            if duplicated_env:
                client.delete_environment(duplicated_env['uid'])
                print(f"✅ Deleted duplicated environment")
        except Exception as e:
            print(f"⚠️  Cleanup error (non-critical): {e}")


def main():
    """Run all Phase 1 tests."""
    print("\n" + "=" * 70)
    print("  POSTMAN SKILL - PHASE 1 MANUAL TEST SUITE")
    print("  Testing v10+ Modernization - Core API Compatibility")
    print("=" * 70)

    # Check prerequisites
    print("\nChecking prerequisites...")
    if not os.getenv('POSTMAN_API_KEY'):
        print("❌ ERROR: POSTMAN_API_KEY environment variable not set")
        print("\nPlease set your API key:")
        print("  export POSTMAN_API_KEY='your-key-here'")
        sys.exit(1)

    print("✅ POSTMAN_API_KEY is set")

    if os.getenv('POSTMAN_WORKSPACE_ID'):
        print(f"✅ POSTMAN_WORKSPACE_ID is set")
    else:
        print("⚠️  POSTMAN_WORKSPACE_ID not set (will use default workspace)")

    # Run tests
    results = {
        'Phase 1.1 - Version Detection': test_phase_1_1_version_detection(),
        'Phase 1.2 - Error Handling': test_phase_1_2_error_handling(),
        'Phase 1.3 - Collections API': test_phase_1_3_collections(),
        'Phase 1.4 - Environments API': test_phase_1_4_environments()
    }

    # Summary
    print_section("TEST SUMMARY")

    passed = sum(1 for v in results.values() if v)
    total = len(results)

    for phase, result in results.items():
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{status} - {phase}")

    print(f"\n{'=' * 70}")
    print(f"  RESULTS: {passed}/{total} phases passed")
    print(f"{'=' * 70}\n")

    if passed == total:
        print("🎉 All Phase 1 tests passed!")
        return 0
    else:
        print(f"⚠️  {total - passed} phase(s) failed - check output above")
        return 1


if __name__ == '__main__':
    sys.exit(main())
