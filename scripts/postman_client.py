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
