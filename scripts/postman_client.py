"""
Postman API client with retry logic and error handling.
"""

import sys
import os

# Add parent directory to path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

import requests
from scripts.config import PostmanConfig
from utils.retry_handler import RetryHandler


class PostmanClient:
    """
    Client for interacting with the Postman API.
    Handles authentication, retries, and response parsing.
    """

    def __init__(self, config=None):
        self.config = config or PostmanConfig()
        self.config.validate()
        self.retry_handler = RetryHandler(max_retries=self.config.max_retries)

    def _make_request(self, method, endpoint, **kwargs):
        """
        Make an API request with retry logic.

        Args:
            method: HTTP method (get, post, etc.)
            endpoint: API endpoint path (without base URL)
            **kwargs: Additional arguments for requests

        Returns:
            Parsed JSON response

        Raises:
            Exception: If request fails after retries
        """
        url = f"{self.config.base_url}{endpoint}"
        kwargs['headers'] = self.config.headers
        kwargs['timeout'] = self.config.timeout

        # Use retry handler
        response = self.retry_handler.execute(
            lambda: requests.request(method, url, **kwargs)
        )

        # Handle response
        if response.status_code >= 400:
            error_msg = f"API request failed with status {response.status_code}"
            try:
                error_data = response.json()
                if 'error' in error_data:
                    error_msg += f": {error_data['error'].get('message', 'Unknown error')}"
            except:
                error_msg += f": {response.text}"
            raise Exception(error_msg)

        return response.json()

    def list_collections(self, workspace_id=None):
        """
        List all collections in a workspace.

        Args:
            workspace_id: Workspace ID (uses config default if not provided)

        Returns:
            List of collection objects
        """
        workspace_id = workspace_id or self.config.workspace_id

        if workspace_id:
            endpoint = f"/collections?workspace={workspace_id}"
        else:
            endpoint = "/collections"

        response = self._make_request('GET', endpoint)
        return response.get('collections', [])

    def get_collection(self, collection_uid):
        """
        Get detailed information about a specific collection.

        Args:
            collection_uid: Unique identifier for the collection

        Returns:
            Collection object with full details
        """
        endpoint = f"/collections/{collection_uid}"
        response = self._make_request('GET', endpoint)
        return response.get('collection', {})

    def create_collection(self, collection_data, workspace_id=None):
        """
        Create a new collection.

        Args:
            collection_data: Dictionary containing collection configuration:
                - info: Collection metadata (name, description, schema)
                - item: List of requests/folders (optional)
                - variable: List of collection variables (optional)
            workspace_id: Workspace ID to create collection in (uses config default if not provided)

        Returns:
            Created collection object
        """
        workspace_id = workspace_id or self.config.workspace_id

        if workspace_id:
            endpoint = f"/collections?workspace={workspace_id}"
        else:
            endpoint = "/collections"

        response = self._make_request('POST', endpoint, json={'collection': collection_data})
        return response.get('collection', {})

    def update_collection(self, collection_uid, collection_data):
        """
        Update an existing collection.

        Args:
            collection_uid: Unique identifier for the collection
            collection_data: Dictionary containing fields to update

        Returns:
            Updated collection object
        """
        endpoint = f"/collections/{collection_uid}"
        response = self._make_request('PUT', endpoint, json={'collection': collection_data})
        return response.get('collection', {})

    def delete_collection(self, collection_uid):
        """
        Delete a collection.

        Args:
            collection_uid: Unique identifier for the collection

        Returns:
            Deletion confirmation
        """
        endpoint = f"/collections/{collection_uid}"
        response = self._make_request('DELETE', endpoint)
        return response

    def list_environments(self, workspace_id=None):
        """
        List all environments in a workspace.

        Args:
            workspace_id: Workspace ID (uses config default if not provided)

        Returns:
            List of environment objects
        """
        workspace_id = workspace_id or self.config.workspace_id

        if workspace_id:
            endpoint = f"/environments?workspace={workspace_id}"
        else:
            endpoint = "/environments"

        response = self._make_request('GET', endpoint)
        return response.get('environments', [])

    def get_environment(self, environment_uid):
        """
        Get detailed information about a specific environment.

        Args:
            environment_uid: Unique identifier for the environment

        Returns:
            Environment object with full details
        """
        endpoint = f"/environments/{environment_uid}"
        response = self._make_request('GET', endpoint)
        return response.get('environment', {})

    def create_environment(self, environment_data, workspace_id=None):
        """
        Create a new environment.

        Args:
            environment_data: Dictionary containing environment configuration:
                - name: Environment name
                - values: List of environment variables (key, value, type, enabled)
            workspace_id: Workspace ID to create environment in (uses config default if not provided)

        Returns:
            Created environment object
        """
        workspace_id = workspace_id or self.config.workspace_id

        if workspace_id:
            endpoint = f"/environments?workspace={workspace_id}"
        else:
            endpoint = "/environments"

        response = self._make_request('POST', endpoint, json={'environment': environment_data})
        return response.get('environment', {})

    def update_environment(self, environment_uid, environment_data):
        """
        Update an existing environment.

        Args:
            environment_uid: Unique identifier for the environment
            environment_data: Dictionary containing fields to update

        Returns:
            Updated environment object
        """
        endpoint = f"/environments/{environment_uid}"
        response = self._make_request('PUT', endpoint, json={'environment': environment_data})
        return response.get('environment', {})

    def delete_environment(self, environment_uid):
        """
        Delete an environment.

        Args:
            environment_uid: Unique identifier for the environment

        Returns:
            Deletion confirmation
        """
        endpoint = f"/environments/{environment_uid}"
        response = self._make_request('DELETE', endpoint)
        return response

    def run_collection(self, collection_uid, environment_uid=None):
        """
        Run a collection's tests.

        Note: This requires additional Postman features like Newman or Collection Runner.
        For the POC, this is a placeholder showing the intended structure.

        Args:
            collection_uid: Unique identifier for the collection
            environment_uid: Optional environment to use

        Returns:
            Test run results
        """
        # Note: The actual test running would typically use Newman or the Collection Runner API
        # This is a simplified version for the POC
        raise NotImplementedError(
            "Collection test execution requires Postman Collection Runner or Newman integration. "
            "This POC demonstrates the API client structure. "
            "For now, use 'list_collections' to discover available collections."
        )

    def list_monitors(self, workspace_id=None):
        """
        List all monitors in a workspace.

        Args:
            workspace_id: Workspace ID (uses config default if not provided)

        Returns:
            List of monitor objects
        """
        workspace_id = workspace_id or self.config.workspace_id

        if workspace_id:
            endpoint = f"/monitors?workspace={workspace_id}"
        else:
            endpoint = "/monitors"

        response = self._make_request('GET', endpoint)
        return response.get('monitors', [])

    def get_monitor(self, monitor_id):
        """
        Get detailed information about a specific monitor.

        Args:
            monitor_id: Unique identifier for the monitor

        Returns:
            Monitor object with full details
        """
        endpoint = f"/monitors/{monitor_id}"
        response = self._make_request('GET', endpoint)
        return response.get('monitor', {})

    def create_monitor(self, monitor_data):
        """
        Create a new monitor.

        Args:
            monitor_data: Dictionary containing monitor configuration:
                - name: Monitor name
                - collection: Collection UID
                - environment: Environment UID (optional)
                - schedule: Schedule configuration (optional)

        Returns:
            Created monitor object
        """
        endpoint = "/monitors"
        response = self._make_request('POST', endpoint, json={'monitor': monitor_data})
        return response.get('monitor', {})

    def update_monitor(self, monitor_id, monitor_data):
        """
        Update an existing monitor.

        Args:
            monitor_id: Unique identifier for the monitor
            monitor_data: Dictionary containing fields to update

        Returns:
            Updated monitor object
        """
        endpoint = f"/monitors/{monitor_id}"
        response = self._make_request('PUT', endpoint, json={'monitor': monitor_data})
        return response.get('monitor', {})

    def delete_monitor(self, monitor_id):
        """
        Delete a monitor.

        Args:
            monitor_id: Unique identifier for the monitor

        Returns:
            Deletion confirmation
        """
        endpoint = f"/monitors/{monitor_id}"
        response = self._make_request('DELETE', endpoint)
        return response

    def get_monitor_runs(self, monitor_id, limit=10):
        """
        Get run history for a monitor.

        Args:
            monitor_id: Unique identifier for the monitor
            limit: Number of runs to retrieve (default: 10)

        Returns:
            List of monitor run objects
        """
        endpoint = f"/monitors/{monitor_id}/runs?limit={limit}"
        response = self._make_request('GET', endpoint)
        return response.get('runs', [])

    def list_apis(self, workspace_id=None):
        """
        List all APIs in a workspace.

        Args:
            workspace_id: Workspace ID (uses config default if not provided)

        Returns:
            List of API objects
        """
        workspace_id = workspace_id or self.config.workspace_id

        if workspace_id:
            endpoint = f"/apis?workspace={workspace_id}"
        else:
            endpoint = "/apis"

        response = self._make_request('GET', endpoint)
        return response.get('apis', [])

    def get_workspace(self, workspace_id=None):
        """
        Get information about a workspace.

        Args:
            workspace_id: Workspace ID (uses config default if not provided)

        Returns:
            Workspace object with details
        """
        workspace_id = workspace_id or self.config.workspace_id

        if not workspace_id:
            raise ValueError("Workspace ID must be provided or set in configuration")

        endpoint = f"/workspaces/{workspace_id}"
        response = self._make_request('GET', endpoint)
        return response.get('workspace', {})

    # Design Phase: Schema and API Operations

    def get_api(self, api_id):
        """
        Get detailed information about a specific API.

        Args:
            api_id: Unique identifier for the API

        Returns:
            API object with full details
        """
        endpoint = f"/apis/{api_id}"
        response = self._make_request('GET', endpoint)
        return response.get('api', {})

    def get_api_versions(self, api_id):
        """
        Get all versions of an API.

        Args:
            api_id: Unique identifier for the API

        Returns:
            List of API version objects
        """
        endpoint = f"/apis/{api_id}/versions"
        response = self._make_request('GET', endpoint)
        return response.get('versions', [])

    def get_api_version(self, api_id, version_id):
        """
        Get a specific version of an API.

        Args:
            api_id: Unique identifier for the API
            version_id: Unique identifier for the version

        Returns:
            API version object with details
        """
        endpoint = f"/apis/{api_id}/versions/{version_id}"
        response = self._make_request('GET', endpoint)
        return response.get('version', {})

    def get_api_schema(self, api_id, version_id):
        """
        Get the schema for a specific API version.

        Args:
            api_id: Unique identifier for the API
            version_id: Unique identifier for the version

        Returns:
            Schema object
        """
        endpoint = f"/apis/{api_id}/versions/{version_id}/schemas"
        response = self._make_request('GET', endpoint)
        return response.get('schemas', [])

    def create_api(self, api_data, workspace_id=None):
        """
        Create a new API.

        Args:
            api_data: Dictionary containing API configuration:
                - name: API name
                - summary: API summary (optional)
                - description: API description (optional)
            workspace_id: Workspace ID (uses config default if not provided)

        Returns:
            Created API object
        """
        workspace_id = workspace_id or self.config.workspace_id

        if workspace_id:
            endpoint = f"/apis?workspace={workspace_id}"
        else:
            endpoint = "/apis"

        response = self._make_request('POST', endpoint, json={'api': api_data})
        return response.get('api', {})

    def update_api(self, api_id, api_data):
        """
        Update an existing API.

        Args:
            api_id: Unique identifier for the API
            api_data: Dictionary containing fields to update

        Returns:
            Updated API object
        """
        endpoint = f"/apis/{api_id}"
        response = self._make_request('PUT', endpoint, json={'api': api_data})
        return response.get('api', {})

    def delete_api(self, api_id):
        """
        Delete an API.

        Args:
            api_id: Unique identifier for the API

        Returns:
            Deletion confirmation
        """
        endpoint = f"/apis/{api_id}"
        response = self._make_request('DELETE', endpoint)
        return response

    # Deploy Phase: Mock Server Operations

    def list_mocks(self, workspace_id=None):
        """
        List all mock servers in a workspace.

        Args:
            workspace_id: Workspace ID (uses config default if not provided)

        Returns:
            List of mock server objects
        """
        workspace_id = workspace_id or self.config.workspace_id

        if workspace_id:
            endpoint = f"/mocks?workspace={workspace_id}"
        else:
            endpoint = "/mocks"

        response = self._make_request('GET', endpoint)
        return response.get('mocks', [])

    def get_mock(self, mock_id):
        """
        Get detailed information about a specific mock server.

        Args:
            mock_id: Unique identifier for the mock server

        Returns:
            Mock server object with full details
        """
        endpoint = f"/mocks/{mock_id}"
        response = self._make_request('GET', endpoint)
        return response.get('mock', {})

    def create_mock(self, mock_data):
        """
        Create a new mock server.

        Args:
            mock_data: Dictionary containing mock server configuration:
                - name: Mock server name
                - collection: Collection UID
                - environment: Environment UID (optional)
                - private: Boolean, whether mock is private (optional)

        Returns:
            Created mock server object
        """
        endpoint = "/mocks"
        response = self._make_request('POST', endpoint, json={'mock': mock_data})
        return response.get('mock', {})

    def update_mock(self, mock_id, mock_data):
        """
        Update an existing mock server.

        Args:
            mock_id: Unique identifier for the mock server
            mock_data: Dictionary containing fields to update

        Returns:
            Updated mock server object
        """
        endpoint = f"/mocks/{mock_id}"
        response = self._make_request('PUT', endpoint, json={'mock': mock_data})
        return response.get('mock', {})

    def delete_mock(self, mock_id):
        """
        Delete a mock server.

        Args:
            mock_id: Unique identifier for the mock server

        Returns:
            Deletion confirmation
        """
        endpoint = f"/mocks/{mock_id}"
        response = self._make_request('DELETE', endpoint)
        return response
