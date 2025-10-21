"""
Configuration management for Postman Agent Skill.
Handles environment variables and provides validated configuration.
"""

import os
import sys


class PostmanConfig:
    """
    Manages configuration from environment variables.
    Validates required settings and provides defaults.
    """

    def __init__(self):
        # Required
        self.api_key = os.getenv("POSTMAN_API_KEY")

        # Optional with defaults
        self.workspace_id = os.getenv("POSTMAN_WORKSPACE_ID")
        self.rate_limit_delay = int(os.getenv("POSTMAN_RATE_LIMIT_DELAY", "60"))
        self.max_retries = int(os.getenv("POSTMAN_MAX_RETRIES", "3"))
        self.timeout = int(os.getenv("POSTMAN_TIMEOUT", "30"))

        # Logging
        self.log_level = os.getenv("LOG_LEVEL", "INFO")

    def validate(self):
        """
        Validate that required configuration is present.
        Raises ValueError with helpful message if configuration is invalid.
        """
        if not self.api_key:
            raise ValueError(
                "POSTMAN_API_KEY not set.\n\n"
                "To get your API key:\n"
                "1. Go to https://web.postman.co/settings/me/api-keys\n"
                "2. Click 'Generate API Key'\n"
                "3. Copy the key (starts with 'PMAK-')\n"
                "4. Set it as environment variable:\n"
                "   export POSTMAN_API_KEY='your-key-here'\n"
            )

        if not self.api_key.startswith("PMAK-"):
            raise ValueError(
                "Invalid POSTMAN_API_KEY format.\n"
                "API keys should start with 'PMAK-'\n"
                "Please check your key from: https://web.postman.co/settings/me/api-keys"
            )

    @property
    def base_url(self):
        """Base URL for Postman API"""
        return "https://api.getpostman.com"

    @property
    def headers(self):
        """HTTP headers for API requests"""
        return {
            "X-API-Key": self.api_key,
            "Content-Type": "application/json"
        }


def get_config():
    """
    Get validated configuration instance.
    Exits with error message if configuration is invalid.
    """
    config = PostmanConfig()
    try:
        config.validate()
        return config
    except ValueError as e:
        print(f"Configuration Error: {e}", file=sys.stderr)
        sys.exit(1)
