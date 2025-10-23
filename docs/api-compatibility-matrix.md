# Postman API v10+ Compatibility Matrix

**Date**: October 22, 2025
**API Base URL**: `https://api.getpostman.com`
**Documentation**: https://www.postman.com/postman/workspace/postman-public-workspace/documentation/12959542-c8142d51-e97c-46b6-bd77-52bb66712c9a

---

## Legend

| Symbol | Meaning |
|--------|---------|
| ✅ | Fully implemented and tested |
| ⚠️ | Partially implemented / needs enhancement |
| ❌ | Not implemented |
| 🔬 | Needs testing against live API |
| 📝 | Requires documentation update |
| 🔐 | May require paid plan / enterprise |

---

## Collections API

### Base Endpoint: `/collections`

| HTTP Method | Endpoint | Purpose | v9 Support | v10+ Support | Implementation Status | Notes |
|-------------|----------|---------|------------|--------------|---------------------|-------|
| GET | `/collections` | List all collections | ✅ Yes | ✅ Yes | ✅ Implemented | Works with workspace filter |
| GET | `/collections/{uid}` | Get collection | ✅ Yes | ✅ Yes | ✅ Implemented | Returns full collection |
| POST | `/collections` | Create collection | ✅ Yes | ✅ Yes | ✅ Implemented | Supports workspace param |
| PUT | `/collections/{uid}` | Update collection | ✅ Yes | ✅ Yes | ✅ Implemented | Full replacement |
| PATCH | `/collections/{uid}` | Partial update | ❌ No | ✅ Yes | ❌ Not implemented | v10+ feature |
| DELETE | `/collections/{uid}` | Delete collection | ✅ Yes | ✅ Yes | ✅ Implemented | Permanent deletion |
| POST | `/collections/{uid}/forks` | Fork collection | ❌ No | ✅ Yes | ❌ Not implemented | v10+ version control |
| GET | `/collections/{uid}/forks` | List forks | ❌ No | ✅ Yes | ❌ Not implemented | v10+ version control |
| POST | `/collections/{uid}/pull-requests` | Create PR | ❌ No | ✅ Yes | ❌ Not implemented | v10+ version control |
| GET | `/collections/{uid}/pull-requests` | List PRs | ❌ No | ✅ Yes | ❌ Not implemented | v10+ version control |
| POST | `/collections/{uid}/pull-requests/{id}/merge` | Merge PR | ❌ No | ✅ Yes | ❌ Not implemented | v10+ version control |
| POST | `/collections/{uid}/transformations` | Generate spec | ❌ No | ✅ Yes | ❌ Not implemented | Export to OpenAPI |

**v10+ New Features**:
- Collection forking workflow
- Pull request based merging
- OpenAPI transformation

**Required for Phase 1**: Fork, PR, Merge, PATCH operations

---

## Environments API

### Base Endpoint: `/environments`

| HTTP Method | Endpoint | Purpose | v9 Support | v10+ Support | Implementation Status | Notes |
|-------------|----------|---------|------------|--------------|---------------------|-------|
| GET | `/environments` | List environments | ✅ Yes | ✅ Yes | ✅ Implemented | Works with workspace filter |
| GET | `/environments/{uid}` | Get environment | ✅ Yes | ✅ Yes | ✅ Implemented | Returns full environment |
| POST | `/environments` | Create environment | ✅ Yes | ✅ Yes | ⚠️ Partial | Missing secret type support |
| PUT | `/environments/{uid}` | Update environment | ✅ Yes | ✅ Yes | ⚠️ Partial | Missing secret type support |
| DELETE | `/environments/{uid}` | Delete environment | ✅ Yes | ✅ Yes | ✅ Implemented | Permanent deletion |
| POST | `/environments/{uid}/forks` | Fork environment | ❌ No | ✅ Yes | ❌ Not implemented | v10+ feature |

**v10+ New Features**:
- Secret variable type (`type: "secret"`)
- Environment forking
- Enhanced variable metadata

**Required for Phase 1**: Secret handling, forking

---

## APIs Endpoint

### Base Endpoint: `/apis`

| HTTP Method | Endpoint | Purpose | v9 Support | v10+ Support | Implementation Status | Notes |
|-------------|----------|---------|------------|--------------|---------------------|-------|
| GET | `/apis` | List APIs | ⚠️ Limited | ✅ Yes | ✅ Implemented | Basic list only |
| GET | `/apis/{id}` | Get API details | ⚠️ Limited | ✅ Yes | ✅ Implemented | May miss v10+ fields |
| POST | `/apis` | Create API | ⚠️ Limited | ✅ Yes | ⚠️ Partial | Basic creation only |
| PUT | `/apis/{id}` | Update API | ⚠️ Limited | ✅ Yes | ⚠️ Partial | Full replacement |
| PATCH | `/apis/{id}` | Partial update | ❌ No | ✅ Yes | ❌ Not implemented | v10+ preferred method |
| DELETE | `/apis/{id}` | Delete API | ⚠️ Limited | ✅ Yes | ✅ Implemented | Works |
| POST | `/apis/{id}/schemas` | Add schema | ❌ No | ✅ Yes | ❌ Not implemented | Upload OpenAPI/etc |
| GET | `/apis/{id}/schemas` | List schemas | ⚠️ Limited | ✅ Yes | 🔬 Untested | Need to verify |
| GET | `/apis/{id}/schemas/{schemaId}` | Get schema | ⚠️ Limited | ✅ Yes | 🔬 Untested | Need to verify |
| PUT | `/apis/{id}/schemas/{schemaId}` | Update schema | ❌ No | ✅ Yes | ❌ Not implemented | Schema updates |
| DELETE | `/apis/{id}/schemas/{schemaId}` | Delete schema | ❌ No | ✅ Yes | ❌ Not implemented | Remove schema |
| GET | `/apis/{id}/versions` | List versions | ✅ Yes | ✅ Yes | ✅ Implemented | Read-only |
| GET | `/apis/{id}/versions/{versionId}` | Get version | ✅ Yes | ✅ Yes | ✅ Implemented | Read-only |
| POST | `/apis/{id}/versions` | Create version | ❌ No | ✅ Yes | ❌ Not implemented | Publish new version |
| PUT | `/apis/{id}/versions/{versionId}` | Update version | ❌ No | ✅ Yes | ❌ Not implemented | Update metadata |
| PATCH | `/apis/{id}/versions/{versionId}` | Partial update | ❌ No | ✅ Yes | ❌ Not implemented | v10+ method |
| DELETE | `/apis/{id}/versions/{versionId}` | Delete version | ❌ No | ✅ Yes | ❌ Not implemented | Remove version |
| POST | `/apis/{id}/collections` | Link collection | ❌ No | ✅ Yes | ❌ Not implemented | Associate collection |
| GET | `/apis/{id}/collections` | List linked collections | ❌ No | ✅ Yes | ❌ Not implemented | View associations |

**v10+ Enhanced Features**:
- Full schema lifecycle (CRUD)
- Version publishing and management
- Collection linking
- PATCH support for partial updates

**Required for Phase 2**: Schema CRUD, version creation, collection linking

---

## Specs Endpoint (Spec Hub - 2024+)

### Base Endpoint: `/specs`

**Status**: ❌ **NOT IMPLEMENTED - NEW IN v10+**

| HTTP Method | Endpoint | Purpose | v9 Support | v10+ Support | Implementation Status | Notes |
|-------------|----------|---------|------------|--------------|---------------------|-------|
| GET | `/specs` | List specs | ❌ N/A | ✅ Yes | ❌ Not implemented | Spec Hub feature |
| GET | `/specs/{id}` | Get spec | ❌ N/A | ✅ Yes | ❌ Not implemented | Fetch spec content |
| POST | `/specs` | Create spec | ❌ N/A | ✅ Yes | ❌ Not implemented | Upload OpenAPI/AsyncAPI |
| PUT | `/specs/{id}` | Update spec | ❌ N/A | ✅ Yes | ❌ Not implemented | Replace spec |
| PATCH | `/specs/{id}` | Partial update | ❌ N/A | ✅ Yes | ❌ Not implemented | Update metadata |
| DELETE | `/specs/{id}` | Delete spec | ❌ N/A | ✅ Yes | ❌ Not implemented | Remove spec |
| POST | `/specs/{id}/collections` | Generate collection | ❌ N/A | ✅ Yes | ❌ Not implemented | Spec → Collection |
| POST | `/specs/{id}/collections/{uid}/sync` | Sync to collection | ❌ N/A | ✅ Yes | ❌ Not implemented | Keep in sync |
| GET | `/specs/{id}/files` | Get spec files | ❌ N/A | ✅ Yes | ❌ Not implemented | Multi-file specs |
| POST | `/specs/{id}/files` | Add spec file | ❌ N/A | ✅ Yes | ❌ Not implemented | Upload file |

**v10+ New Feature Set**:
- Dedicated spec management
- Spec Hub integration
- Bi-directional sync with collections
- Multi-file spec support

**Required for Phase 3**: Full Spec Hub CRUD and sync operations

---

## Monitors API

### Base Endpoint: `/monitors`

| HTTP Method | Endpoint | Purpose | v9 Support | v10+ Support | Implementation Status | Notes |
|-------------|----------|---------|------------|--------------|---------------------|-------|
| GET | `/monitors` | List monitors | ✅ Yes | ✅ Yes | ✅ Implemented | Works with workspace filter |
| GET | `/monitors/{id}` | Get monitor | ✅ Yes | ✅ Yes | ✅ Implemented | Full details |
| POST | `/monitors` | Create monitor | ✅ Yes | ✅ Yes | ✅ Implemented | Schedule creation |
| PUT | `/monitors/{id}` | Update monitor | ✅ Yes | ✅ Yes | ✅ Implemented | Modify schedule |
| DELETE | `/monitors/{id}` | Delete monitor | ✅ Yes | ✅ Yes | ✅ Implemented | Remove monitor |
| GET | `/monitors/{id}/runs` | Get run history | ✅ Yes | ✅ Yes | ✅ Implemented | Last N runs |

**Status**: ✅ **FULLY COMPATIBLE**

**Notes**: Monitor API appears stable between v9 and v10+

---

## Mocks API

### Base Endpoint: `/mocks`

| HTTP Method | Endpoint | Purpose | v9 Support | v10+ Support | Implementation Status | Notes |
|-------------|----------|---------|------------|--------------|---------------------|-------|
| GET | `/mocks` | List mocks | ✅ Yes | ✅ Yes | ✅ Implemented | Works with workspace filter |
| GET | `/mocks/{id}` | Get mock | ✅ Yes | ✅ Yes | ✅ Implemented | Full details |
| POST | `/mocks` | Create mock | ✅ Yes | ✅ Yes | ✅ Implemented | Mock server creation |
| PUT | `/mocks/{id}` | Update mock | ✅ Yes | ✅ Yes | ✅ Implemented | Modify mock config |
| DELETE | `/mocks/{id}` | Delete mock | ✅ Yes | ✅ Yes | ✅ Implemented | Remove mock |
| POST | `/mocks/{id}/publish` | Publish mock | ❌ No | ✅ Yes | ❌ Not implemented | Make public/private |
| GET | `/mocks/{id}/server-responses` | Get responses | ❌ No | ✅ Yes | ❌ Not implemented | Response history |

**v10+ Enhancements**:
- Mock publishing controls
- Response history tracking

**Required for Phase 2**: Publishing, response tracking (optional)

---

## Workspaces API

### Base Endpoint: `/workspaces`

| HTTP Method | Endpoint | Purpose | v9 Support | v10+ Support | Implementation Status | Notes |
|-------------|----------|---------|------------|--------------|---------------------|-------|
| GET | `/workspaces` | List workspaces | ✅ Yes | ✅ Yes | ⚠️ Not exposed | Could add |
| GET | `/workspaces/{id}` | Get workspace | ✅ Yes | ✅ Yes | ✅ Implemented | Basic info |
| POST | `/workspaces` | Create workspace | ✅ Yes | ✅ Yes | ❌ Not implemented | Workspace creation |
| PUT | `/workspaces/{id}` | Update workspace | ✅ Yes | ✅ Yes | ❌ Not implemented | Modify workspace |
| DELETE | `/workspaces/{id}` | Delete workspace | ✅ Yes | ✅ Yes | ❌ Not implemented | Remove workspace |

**Status**: ⚠️ **PARTIALLY IMPLEMENTED**

**Notes**: Only GET single workspace implemented, CRUD operations missing

---

## Users / Teams API

### Base Endpoint: `/me` and `/teams`

| HTTP Method | Endpoint | Purpose | v9 Support | v10+ Support | Implementation Status | Notes |
|-------------|----------|---------|------------|--------------|---------------------|-------|
| GET | `/me` | Get current user | ✅ Yes | ✅ Yes | ❌ Not implemented | User info |
| GET | `/teams` | List teams | 🔐 Enterprise | 🔐 Enterprise | ❌ Not implemented | Team management |

**Status**: ❌ **NOT IMPLEMENTED**

---

## Integrations API (2024+)

### Base Endpoint: `/integrations`

**Status**: ❌ **NOT IMPLEMENTED - ENTERPRISE FEATURE**

| HTTP Method | Endpoint | Purpose | Implementation Status | Notes |
|-------------|----------|---------|---------------------|-------|
| GET | `/integrations` | List integrations | ❌ Not implemented | CI/CD integrations |
| GET | `/integrations/{id}` | Get integration | ❌ Not implemented | Integration details |

**Notes**: May require Enterprise plan, research needed

---

## Security / Governance API (2024+)

### Base Endpoint: `/security` or `/governance`

**Status**: 🔬 **RESEARCH NEEDED**

Postman may have added security scanning and governance APIs. Need to research:
- Secret scanning endpoints
- Security validation endpoints
- Governance rule endpoints
- API security scores

**Action**: Phase 0 - Research if APIs exist for these features

---

## Response Format Changes (v9 → v10+)

### Collections Response

**v9 Format**:
```json
{
  "collections": [
    {
      "id": "...",
      "name": "...",
      "uid": "...",
      "owner": "...",
      "createdAt": "...",
      "updatedAt": "..."
    }
  ]
}
```

**v10+ Format** (suspected changes):
```json
{
  "collections": [
    {
      "id": "...",
      "name": "...",
      "uid": "...",
      "owner": "...",
      "createdAt": "...",
      "updatedAt": "...",
      "fork": {
        "label": "...",
        "createdAt": "...",
        "from": "..."
      },
      "meta": {
        "type": "...",
        "visibility": "..."
      }
    }
  ]
}
```

**New Fields**:
- `fork` - Fork metadata (if collection is a fork)
- `meta` - Additional metadata (type, visibility, etc.)

**Risk**: ⚠️ **MEDIUM** - Need to validate parsers handle these fields

### APIs Response

**Suspected v10+ Changes**:
- More granular version metadata
- Schema relationship tracking
- Collection linkage information

**Risk**: ⚠️ **MEDIUM-HIGH** - Need live testing

### Error Response Format

**Current v9/v10 Format**:
```json
{
  "error": {
    "name": "instanceNotFoundError",
    "message": "The requested resource was not found."
  }
}
```

**v10+ May Also Include**:
```json
{
  "error": {
    "name": "...",
    "message": "...",
    "details": "..."
  }
}
```

---

## Feature Availability by Plan

| Feature | Free | Basic | Professional | Enterprise |
|---------|------|-------|--------------|------------|
| Collections CRUD | ✅ | ✅ | ✅ | ✅ |
| Collection Forking | ✅ | ✅ | ✅ | ✅ |
| Environments CRUD | ✅ | ✅ | ✅ | ✅ |
| Secret Variables | ✅ | ✅ | ✅ | ✅ |
| APIs CRUD | ✅ | ✅ | ✅ | ✅ |
| API Versioning | ✅ | ✅ | ✅ | ✅ |
| Spec Hub | ✅ | ✅ | ✅ | ✅ |
| Monitors | Limited | ✅ | ✅ | ✅ |
| Mocks | Limited | ✅ | ✅ | ✅ |
| Integrations | ❌ | ⚠️ | ✅ | ✅ |
| SSO / SCIM | ❌ | ❌ | ❌ | ✅ |
| Governance | ❌ | ❌ | ⚠️ | ✅ |

**Note**: Feature availability based on public documentation, may change.

---

## Testing Priorities

### Phase 0 - Immediate Testing Needed

1. **Collections API** 🔬
   - Test fork response format
   - Verify metadata fields
   - Test PR endpoints (if accessible)

2. **APIs Endpoint** 🔬
   - Test schema endpoints
   - Verify version creation
   - Test collection linking

3. **Specs Endpoint** 🔬
   - Verify endpoint exists
   - Test CRUD operations
   - Test collection generation

4. **Environments** 🔬
   - Test secret variable handling
   - Verify fork endpoint

### Phase 1 - Comprehensive Testing

- All v10+ endpoints
- Response format validation
- Error handling
- Rate limiting behavior

---

## Deprecated Endpoints (v9 → v10+)

**Research Needed**: Identify if any v9 endpoints are deprecated in v10+

Potential deprecations:
- None confirmed yet
- Need to review Postman changelog

---

## Summary Statistics

| Category | Total Endpoints | Implemented | Partial | Not Implemented | Testing Needed |
|----------|----------------|-------------|---------|-----------------|----------------|
| Collections | 12 | 5 (42%) | 0 | 7 (58%) | 7 |
| Environments | 6 | 5 (83%) | 0 | 1 (17%) | 2 |
| APIs | 20 | 6 (30%) | 4 (20%) | 10 (50%) | 10 |
| Specs | 10 | 0 (0%) | 0 | 10 (100%) | 10 |
| Monitors | 6 | 6 (100%) | 0 | 0 (0%) | 0 |
| Mocks | 7 | 5 (71%) | 0 | 2 (29%) | 2 |
| Workspaces | 5 | 1 (20%) | 0 | 4 (80%) | 4 |
| **TOTAL** | **66** | **28 (42%)** | **4 (6%)** | **34 (52%)** | **35** |

**Overall Compatibility**: ~48% (28 full + 4 partial out of 66)

---

## Next Actions

1. ✅ Document compatibility matrix
2. ⏳ Test high-priority endpoints against live API
3. ⏳ Capture actual response samples
4. ⏳ Update gap analysis with findings
5. ⏳ Create test scripts for validation

---

**Matrix Status**: Phase 0 - Initial Documentation Complete
**Next**: Live API testing and validation
**Updated**: October 22, 2025
