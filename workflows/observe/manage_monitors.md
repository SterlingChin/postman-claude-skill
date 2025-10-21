# Manage Postman Monitors

## Metadata
- **Phase**: Observe
- **Complexity**: Medium
- **Estimated Time**: 2-10 minutes (depends on operation)
- **Prerequisites**:
  - POSTMAN_API_KEY environment variable set
  - POSTMAN_WORKSPACE_ID configured (optional but recommended)

## When to Use

Use this workflow when:
- User asks to "list monitors" or "show monitors"
- User wants to create/update/delete a monitor
- User needs to check monitor performance or health
- User asks about uptime or API monitoring
- Part of observability/monitoring strategy

## Instructions

### List All Monitors

```bash
python /skills/postman-skill/scripts/manage_monitors.py --list
```

**With verbose output:**
```bash
python /skills/postman-skill/scripts/manage_monitors.py --list --verbose
```

**Expected Output:**
```
Found 5 monitor(s)
================================================================================

✓ Active API Health Check
   ID: 1eeb6da8-fbd0-47c0-b78a-b7ea8424a0e5
   UID: 13144781-1eeb6da8-fbd0-47c0-b78a-b7ea8424a0e5

✗ Inactive Load Test Monitor
   ID: 2ff7eb9-gce1-58d1-c89b-c8fb9535b1f6
   UID: 13144781-2ff7eb9-gce1-58d1-c89b-c8fb9535b1f6
```

### Get Monitor Details

```bash
python /skills/postman-skill/scripts/manage_monitors.py --details <monitor-id>
```

**Example:**
```bash
python /skills/postman-skill/scripts/manage_monitors.py --details 1eeb6da8-fbd0-47c0-b78a-b7ea8424a0e5
```

**Expected Output:**
```
Monitor Details
================================================================================

Name: API Health Check
ID: 1eeb6da8-fbd0-47c0-b78a-b7ea8424a0e5
UID: 13144781-1eeb6da8-fbd0-47c0-b78a-b7ea8424a0e5
Status: Active

Configuration:
  Collection: 12345-abcd-ef67-8901
  Environment: 98765-zyxw-vut-4321
  Schedule: 0 */6 * * * (Every 6 hours)
  Timezone: UTC

Last Run:
  Status: success
  Started: 2025-01-20T10:00:00.000Z
  Finished: 2025-01-20T10:00:15.230Z
  Assertions: 25 total, 0 failed
```

### Create a New Monitor

```bash
python /skills/postman-skill/scripts/manage_monitors.py \
  --create \
  --name "Monitor Name" \
  --collection <collection-uid>
```

**With environment and schedule:**
```bash
python /skills/postman-skill/scripts/manage_monitors.py \
  --create \
  --name "API Health Check" \
  --collection "12345-abcd-ef67-8901" \
  --environment "98765-zyxw-vut-4321" \
  --schedule "0 */6 * * *"
```

**Schedule Cron Formats:**
- `0 * * * *` - Every hour
- `0 */6 * * *` - Every 6 hours
- `0 0 * * *` - Daily at midnight
- `0 0 * * 1` - Weekly on Monday
- `*/15 * * * *` - Every 15 minutes

**Expected Output:**
```
Creating monitor 'API Health Check'...
✓ Monitor created successfully!
  Name: API Health Check
  ID: 1eeb6da8-fbd0-47c0-b78a-b7ea8424a0e5
  UID: 13144781-1eeb6da8-fbd0-47c0-b78a-b7ea8424a0e5
```

### Update a Monitor

**Rename:**
```bash
python /skills/postman-skill/scripts/manage_monitors.py \
  --update <monitor-id> \
  --name "New Monitor Name"
```

**Activate/Deactivate:**
```bash
python /skills/postman-skill/scripts/manage_monitors.py \
  --update <monitor-id> \
  --activate
```

```bash
python /skills/postman-skill/scripts/manage_monitors.py \
  --update <monitor-id> \
  --deactivate
```

**Change Schedule:**
```bash
python /skills/postman-skill/scripts/manage_monitors.py \
  --update <monitor-id> \
  --schedule "0 0 * * *"
```

### Delete a Monitor

```bash
python /skills/postman-skill/scripts/manage_monitors.py \
  --delete <monitor-id> \
  --confirm
```

**Note:** The `--confirm` flag is required to prevent accidental deletions.

### Analyze Monitor Run History

```bash
python /skills/postman-skill/scripts/manage_monitors.py \
  --analyze <monitor-id>
```

**With custom limit:**
```bash
python /skills/postman-skill/scripts/manage_monitors.py \
  --analyze <monitor-id> \
  --limit 20
```

**Expected Output:**
```
Monitor Run History (Last 10 runs)
================================================================================

Summary:
  Total Runs: 10
  Successful: 9 (90.0%)
  Failed: 1 (10.0%)

Recent Runs:
--------------------------------------------------------------------------------
1. ✓ SUCCESS
   Started: 2025-01-20T10:00:00.000Z
   Duration: 15.2s
   Requests: 5 total, 0 failed
   Assertions: 25 total, 0 failed

2. ✗ FAILURE
   Started: 2025-01-20T04:00:00.000Z
   Duration: 8.5s
   Requests: 5 total, 1 failed
   Assertions: 25 total, 3 failed
```

## Interpreting Results

### Monitor Status
- **✓ Active** - Monitor is running on schedule
- **✗ Inactive** - Monitor is paused/disabled

### Run Status
- **SUCCESS** - All requests and assertions passed
- **FAILURE** - One or more requests or assertions failed

### Key Metrics
- **Success Rate** - Percentage of successful runs
- **Request Failures** - API requests that failed (timeouts, connection errors)
- **Assertion Failures** - Test assertions that failed

### Success Criteria
A monitor is healthy when:
- ✓ Success rate > 95%
- ✓ Request failures = 0
- ✓ Assertion failures = 0
- ✓ Average duration < expected threshold

## Next Steps After Operations

### After Listing Monitors
- Offer to show details for specific monitors
- Suggest analyzing run history for failing monitors
- Offer to create new monitors if none exist

### After Creating Monitor
- Confirm creation with monitor ID
- Suggest testing the monitor immediately
- Offer to adjust schedule if needed

### After Analyzing Runs
- If failures detected, suggest investigating failed requests
- Recommend checking API health
- Offer to adjust monitor frequency or timeout settings

## Error Handling

### Error: Monitor not found
**Symptoms:** "Monitor {id} not found"

**Resolution:**
1. List all monitors to verify ID
2. Check if monitor was deleted
3. Verify workspace access

### Error: Invalid collection UID
**Symptoms:** "Collection not found" when creating monitor

**Resolution:**
1. List collections to get valid UID
2. Ensure collection is in the same workspace
3. Verify collection exists

### Error: Invalid cron schedule
**Symptoms:** "Invalid schedule format"

**Resolution:**
1. Use standard cron format: `minute hour day month dayofweek`
2. Validate cron expression
3. Examples:
   - `0 * * * *` (every hour)
   - `*/30 * * * *` (every 30 minutes)
   - `0 0 * * 1` (weekly on Monday)

### Error: Permission denied
**Symptoms:** 403 Forbidden errors

**Resolution:**
1. Verify API key has monitor permissions
2. Check workspace access rights
3. Ensure you're the monitor owner (for update/delete)

## Advanced Usage

### Monitoring Strategy

**High-Priority APIs:**
- Schedule: Every 15-30 minutes
- Purpose: Quick detection of issues
- Collections: Critical endpoints

**Standard APIs:**
- Schedule: Every 1-6 hours
- Purpose: Regular health checks
- Collections: All endpoints

**Low-Priority APIs:**
- Schedule: Daily
- Purpose: Basic availability checks
- Collections: Non-critical endpoints

### Combining with Other Workflows

**With Collection Testing:**
1. Test collection locally first
2. Verify all tests pass
3. Create monitor with that collection
4. Analyze monitor runs regularly

**With Environment Management:**
1. Create environment for monitoring
2. Configure production credentials
3. Link environment to monitor
4. Monitor uses production environment

## Tips

1. **Use descriptive names** - "Production API Health" vs "Monitor 1"
2. **Start inactive** - Test monitor manually before activating
3. **Monitor the monitors** - Check run history weekly
4. **Set appropriate schedules** - Don't over-monitor (API rate limits)
5. **Use environments** - Separate staging/production monitors

## Limitations

- Monitors run from Postman's infrastructure (not local)
- Schedule minimum is typically 5 minutes
- Monitor runs consume API usage limits
- Maximum number of monitors depends on plan
- Some advanced Newman features may not be available

## Related Workflows

- **list_collections.md** - Discover collections to monitor
- **run_collection.md** - Test collections before creating monitors
- **workspace_audit.md** - Comprehensive workspace health check (future)

## Security Notes

- API keys in environments are encrypted
- Monitor runs are logged
- Sensitive data in responses is not logged
- Only workspace members can view monitors
- Monitor deletion requires confirmation

