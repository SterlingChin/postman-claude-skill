# Changelog

All notable changes to the Postman Agent Skill for Claude will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.1.0] - 2024-11-05

### 🎉 Major Features

#### Spec Hub Integration (NEW!)
- **Create API Specifications**: Direct creation of OpenAPI 3.0 and AsyncAPI 2.0 specifications
- **Multi-File Support**: Organize complex APIs with separate schema files
- **Bidirectional Generation**:
  - Generate collections from specifications
  - Generate specifications from existing collections
- **YAML & JSON Support**: Use either format for maximum flexibility
- **Replaces Legacy Workflow**: Modern alternative to deprecated `create_api()` method

#### Git-like Workflows (v10+ APIs)
- **Fork Collections**: Create independent development branches
- **Pull Requests**: Propose and manage collection changes
- **Merge Operations**: Integrate approved changes
- **Smart Duplication**: Copy collections with full metadata preservation

#### Enhanced Security
- **Auto-Secret Detection**: Automatically identifies and protects 11 types of sensitive variables
  - `api_key`, `token`, `password`, `bearer`, `auth`, `secret`, `client_secret`, `private_key`, `access_token`, `refresh_token`, `jwt`
- **Secret Preservation**: Maintains secret types across updates and duplication
- **No Accidental Exposure**: Prevents credential leaks in environment variables

### ✨ Enhancements

#### Developer Experience
- **Custom Exception Classes**: Specific exceptions with helpful resolution guidance
  - `AuthenticationError` (401) - Invalid API key setup instructions
  - `PermissionError` (403) - Resolution steps for access issues
  - `ResourceNotFoundError` (404) - Detailed causes and troubleshooting
  - `ValidationError` (400) - Request validation failure details
  - `RateLimitError` (429) - Retry-after information
  - `ServerError` (5xx) - Status page links
  - `NetworkError` - Connection troubleshooting
  - `TimeoutError` - Configuration guidance

#### API Version Detection
- **Automatic Detection**: Identifies Postman API version (v9 vs v10+)
- **Compatibility Warnings**: Alerts when v10+ features are unavailable
- **Graceful Degradation**: Maintains functionality on older API versions

#### Environment Management
- **Simplified Dict API**: Create environments quickly with key-value dictionaries
- **Partial Updates**: Modify only specific variables without full replacement
- **Secret Preservation**: Maintains secret status during updates

### 📚 Documentation

#### New Workflows
- **`workflows/design/manage_specs.md`**: Comprehensive Spec Hub guide
- **`TESTING.md`**: Live testing instructions with step-by-step setup
- **Example Script**: `scripts/manage_pet_store_spec.py` demonstrating complete workflow

#### Enhanced Documentation
- **Setup Validation**: `scripts/validate_setup.py` for comprehensive diagnostics
- **Workspace Discovery**: `scripts/list_workspaces.py` for navigation
- **Improved README**: Clearer error state handling and setup instructions

### 🔧 Infrastructure

#### Network Compatibility
- **Proxy Support**: Enhanced handling for corporate networks
- **Claude Web Interface**: Full support with configured proxy
- **DNS Resolution**: Switched from `requests` to `curl` for better DNS handling
- **Debug Mode**: `POSTMAN_DEBUG=1` environment variable for troubleshooting

#### Packaging
- **Package Script**: `package_skill.sh` ensures proper zip structure
- **Depth Limit Compliance**: Automatically excludes deep directories (venv, .git)
- **Size Optimization**: Reduced package from 6.3 MB to ~106 KB
- **`.env` Inclusion**: Properly includes credentials while excluding examples

### 🐛 Bug Fixes

- Fixed proxy handling to enable Claude web interface support
- Resolved DNS issues by switching to curl-based requests
- Fixed packaging to exclude venv folders exceeding Claude Desktop's 10-folder depth limit
- Improved error states with clearer user guidance

### 📊 Testing

#### New Test Suite
- **`tests/test_phase1_manual.py`**: Phase 1 compatibility testing
- **`tests/README.md`**: Testing guidelines and procedures
- Live testing validation for Spec Hub workflows

### 🗂️ Project Documentation

#### Strategy Documents
- **`docs/assessment-report.md`**: Current state analysis
- **`docs/api-compatibility-matrix.md`**: Endpoint coverage mapping
- **`docs/gap-analysis.md`**: Implementation roadmap
- **`docs/compatibility-strategy.md`**: v10+ compatibility approach

---

## [1.0.0] - 2024-10-XX

### Initial Release

#### ✅ Core Features

**Discover Phase**
- List collections, environments, monitors, and APIs
- Detailed resource information retrieval
- Workspace resource discovery
- Error handling with retry logic

**Design Phase**
- Validate API schemas (OpenAPI, Swagger, GraphQL)
- Get API versions and compare changes
- Manage API definitions and versions
- Create, update, and delete APIs (legacy method)

**Build Phase**
- Create new collections and environments
- Update existing collections and environments
- Delete collections and environments
- Add requests to collections
- Manage environment variables

**Test Phase**
- Run collection tests with Newman integration
- Execute test suites with environment variables
- Parse and format test results
- Detailed pass/fail reporting with assertions

**Secure Phase**
- Check authentication configuration
- Review security settings in collections
- Identify unsecured endpoints
- Get security recommendations

**Deploy Phase**
- Create and manage mock servers
- List all mocks in workspace
- Update mock server configuration
- Delete mock servers

**Observe Phase**
- Create, update, and delete monitors
- List all monitors with status
- View monitor run history and analytics
- Analyze success rates and response times
- Get detailed run diagnostics

**Distribute Phase**
- View API documentation
- Assess documentation quality and completeness
- Check for missing descriptions or examples
- Get recommendations for improving docs

#### 🏗️ Architecture

**Progressive Disclosure**
- Skill metadata always visible
- SKILL.md loaded when triggered
- Workflow files loaded as needed
- Python scripts executed on demand

**File Structure**
- Organized workflows by API lifecycle phase
- Reusable utility modules
- Clear separation of concerns

#### 📖 Documentation

**Workflows Created**
- `workflows/test/list_collections.md`
- `workflows/test/run_collection.md`
- `workflows/design/validate_schema.md`
- `workflows/design/version_comparison.md`
- `workflows/build/manage_collections.md`
- `workflows/build/manage_environments.md`
- `workflows/secure/check_auth.md`
- `workflows/deploy/manage_mocks.md`
- `workflows/observe/manage_monitors.md`
- `workflows/distribute/view_documentation.md`

**Core Scripts**
- `scripts/config.py` - Configuration management
- `scripts/postman_client.py` - API client
- `scripts/list_collections.py` - Discovery
- `scripts/manage_collections.py` - Collection CRUD
- `scripts/manage_environments.py` - Environment CRUD
- `scripts/run_collection.py` - Test execution
- `scripts/manage_monitors.py` - Monitor management

**Utilities**
- `utils/retry_handler.py` - Exponential backoff
- `utils/formatters.py` - Human-readable output

#### ⚙️ Configuration

**Environment Variables**
- `POSTMAN_API_KEY` - Required API authentication
- `POSTMAN_WORKSPACE_ID` - Optional workspace scoping
- `POSTMAN_RATE_LIMIT_DELAY` - Rate limit handling (default: 60s)
- `POSTMAN_MAX_RETRIES` - Retry attempts (default: 3)
- `POSTMAN_TIMEOUT` - Request timeout (default: 30s)

---

## [Unreleased]

### Planned Features

- Advanced schema validation (breaking change detection)
- Public documentation publishing
- CI/CD integration workflows
- Advanced security auditing
- Collection import/export
- Bulk operations support
- Performance analytics

---

## Release Notes

### Version 1.1.0 Highlights

This release represents a major leap forward in API-first development workflows:

1. **Spec Hub replaces legacy API workflows** - Much simpler and more powerful
2. **Git-like collaboration** - Fork, PR, and merge for teams
3. **Security by default** - Auto-detection prevents credential exposure
4. **Better error handling** - Get actionable help when things go wrong
5. **Production ready** - Enhanced testing, compatibility detection, and reliability

### Migration from 1.0.0

**No breaking changes!** Version 1.1.0 is fully backward compatible.

**New features to adopt:**
- Use `create_spec()` instead of `create_api()` for new specifications
- Enable auto-secret detection for environment variables (automatic)
- Try fork/PR workflows if on Postman v10+ APIs
- Run `python scripts/validate_setup.py` for diagnostics

### Compatibility

| Environment | v1.0.0 | v1.1.0 |
|------------|--------|--------|
| Claude Web Interface | ⚠️ Limited | ✅ Full Support |
| Claude API | ✅ Supported | ✅ Supported |
| Claude Desktop | ⚠️ Manual | ✅ Improved |
| Local Scripts | ✅ Supported | ✅ Supported |

| Postman API | v1.0.0 | v1.1.0 |
|-------------|--------|--------|
| v9 APIs | ✅ Best Effort | ✅ Best Effort |
| v10+ APIs | ⚠️ Partial | ✅ Full Support |

---

## Support

For issues, feature requests, or questions:
- GitHub Issues: [Your Repo URL]
- Documentation: See README.md and workflow files
- Examples: See `scripts/manage_pet_store_spec.py`

---

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
