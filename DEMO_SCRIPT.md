# Postman Agent Skill - Demo Script

This is a sample conversation showing how developers interact with Claude using the Postman Agent Skill. Use this to demonstrate the skill's capabilities in videos, screenshots, or social posts.

---

## Demo 1: API-First Development Workflow

**Perfect for:** LinkedIn post, tutorial videos

```
👤 User:
I need to create a REST API for a task management app.
It should handle tasks, users, and projects.

🤖 Claude:
I'll help you create an API specification for your task management app.
Let me create an OpenAPI 3.0 spec with those resources.

[Claude creates the specification]

✅ I've created "Task Management API" with:
   • 12 endpoints (CRUD for tasks, users, projects)
   • 6 data models with relationships
   • Authentication with Bearer tokens
   • Full OpenAPI 3.0 specification

Spec ID: spec-a1b2c3d4
View in Postman: https://postman.postman.co/workspace/specs

Would you like me to generate a Postman collection from this spec
so you can start testing?

👤 User:
Yes! Generate the collection.

🤖 Claude:
✅ Collection generated: "Task Management API Collection"
   • 12 ready-to-use requests
   • Organized in folders (Tasks, Users, Projects)
   • Example responses included
   • Environment variables configured

Collection ID: col-e5f6g7h8
View: https://postman.postman.co/collections/col-e5f6g7h8

Next steps:
   1. Configure your base_url in the environment
   2. Add your API key
   3. Start sending requests!

Want me to create a dev environment for testing?
```

---

## Demo 2: Taking Over an Existing API

**Perfect for:** Reddit post, showing practical use

```
👤 User:
How many Postman collections do I have?

🤖 Claude:
Let me check your workspace...

✅ Found 8 collections:
   1. Customer API v2 (47 requests)
   2. Payment Gateway (23 requests)
   3. User Authentication (12 requests)
   4. Analytics Dashboard API (31 requests)
   5. Internal Tools (8 requests)
   6. Legacy API (deprecated) (15 requests)
   7. Mobile App Backend (38 requests)
   8. Webhook Handlers (9 requests)

Total: 183 requests across 8 collections

👤 User:
Run the tests for "Customer API v2"

🤖 Claude:
Running tests for Customer API v2...

✅ Test Results:
   ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
   Passed:  41 / 47  (87.2%)
   Failed:   6 / 47  (12.8%)
   Skipped:  0
   ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

❌ Failed Tests:
   1. GET /customers/{id} - Status code is 500 (expected 200)
   2. POST /customers - Schema validation failed
   3. PUT /customers/{id} - Authentication failed
   4. DELETE /customers/{id} - 404 Not Found
   5. GET /customers?status=active - Response time > 2000ms
   6. POST /customers/bulk - Request timeout

👤 User:
Create a monitor to run these tests every hour and alert me
if success rate drops below 90%

🤖 Claude:
✅ Monitor created: "Customer API v2 Health Check"
   • Schedule: Every hour
   • Alerts: Enabled (success rate < 90%)
   • Environment: Production
   • Notification: Email

Monitor ID: mon-i9j0k1l2
Status: Active

I'll send you alerts if your API health degrades.
```

---

## Demo 3: Team Collaboration

**Perfect for:** Showing advanced features

```
👤 User:
I want to add authentication tests to the shared "Mobile App Backend"
collection, but I don't want to break it for the team.

🤖 Claude:
Smart approach! I'll create a fork so you can work independently,
then we can merge your changes via a pull request.

✅ Forked collection: "Mobile App Backend"
   Fork label: "add-auth-tests"
   Fork ID: col-m3n4o5p6

Your fork is a complete copy. Any changes you make won't affect
the original until merged.

👤 User:
Add tests for OAuth2 flow and token refresh

🤖 Claude:
✅ Added to your fork:
   • OAuth2 Authorization Test (validates token grant)
   • Token Refresh Test (validates refresh flow)
   • Invalid Token Test (validates 401 handling)
   • Expired Token Test (validates refresh trigger)

   All tests include assertions and example responses.

Ready to create a pull request?

👤 User:
Yes, create the PR

🤖 Claude:
✅ Pull Request created: "Add OAuth2 authentication tests"

   Description:
   • Adds comprehensive OAuth2 testing
   • Covers token grant and refresh flows
   • Includes negative test cases
   • All tests passing ✓

   PR ID: pr-q7r8s9t0
   Status: Open - awaiting review

   Share this with your team to review and merge!
```

---

## Demo 4: Documentation & API Governance

**Perfect for:** Enterprise/governance angle

```
👤 User:
Check the security configuration of all my collections

🤖 Claude:
Running security audit across 8 collections...

⚠️ Security Issues Found:

🔴 Critical (3):
   • "Legacy API" - No authentication configured
   • "Webhook Handlers" - Using hardcoded API keys in requests
   • "Internal Tools" - Basic auth with plaintext password

🟡 Warning (2):
   • "Payment Gateway" - API key in URL parameters (should be in header)
   • "Mobile App Backend" - Using deprecated OAuth 1.0

✅ Secure (3):
   • "Customer API v2" - Bearer token auth ✓
   • "User Authentication" - OAuth 2.0 ✓
   • "Analytics Dashboard API" - API key in header ✓

Recommendations:
   1. Add authentication to "Legacy API" immediately
   2. Move hardcoded credentials to environment variables
   3. Migrate OAuth 1.0 to OAuth 2.0
   4. Use header-based API keys instead of URL parameters

Want me to help fix these issues?

👤 User:
Yes, start with the hardcoded API keys

🤖 Claude:
✅ Fixed "Webhook Handlers" collection:
   • Removed 3 hardcoded API keys from requests
   • Created environment variables: webhook_api_key, signing_secret, auth_token
   • All 3 variables marked as SECRET (won't be exposed in logs)
   • Updated requests to use {{webhook_api_key}}

⚠️ Action Required:
   You need to set the actual values in your environment:

   1. Go to Environments in Postman
   2. Select "Webhook Handlers Environment"
   3. Set values for webhook_api_key, signing_secret, auth_token

Your credentials are now secure!
```

---

## Demo 5: Quick API Validation

**Perfect for:** Twitter/short-form content

```
👤 User:
Generate an OpenAPI spec from my "Payment Gateway" collection

🤖 Claude:
✅ Specification generated: "Payment Gateway API"
   • Format: OpenAPI 3.0
   • Endpoints: 23
   • Models: 8
   • Security: API Key defined

Spec ID: spec-u1v2w3x4

The spec includes all your endpoints, request/response schemas,
and authentication configuration. Perfect for API gateways,
documentation, or client SDK generation!

👤 User:
Validate the spec for errors

🤖 Claude:
Running OpenAPI validation...

✅ Spec is valid!
   • All endpoints properly defined
   • Request/response schemas complete
   • Security schemes configured
   • No breaking changes detected

Your API is well-documented and standards-compliant!
```

---

## One-Liner Examples

**Perfect for:** Quick feature demos in tweets or bullets

```
📊 "Show me monitor analytics for the last 30 days"
   → Response times, success rates, failure patterns

🔄 "Duplicate this collection for staging environment"
   → Full copy with all requests and tests

🧪 "Run all my test collections and summarize results"
   → Aggregate pass/fail across entire workspace

🔍 "Which endpoints in my API are missing documentation?"
   → Quality audit with specific gaps identified

⚡ "Create a mock server for rapid frontend development"
   → Instant mock API from collection examples

🌐 "List all my workspaces and switch to 'Production'"
   → Multi-workspace management

📝 "Export this spec and show me the YAML"
   → Direct access to spec content
```

---

## Key Talking Points for Demos

### What Makes This Special?

1. **Natural Language → Working API**
   - "Create a task API" → Full OpenAPI spec + collection in seconds

2. **Bidirectional Workflows**
   - Collection → Spec OR Spec → Collection

3. **Git-Like Collaboration**
   - Fork → Edit → Pull Request → Merge

4. **Security by Default**
   - Auto-detects secrets, prevents exposure

5. **Complete Lifecycle**
   - Design → Build → Test → Deploy → Monitor → Distribute

### Use Cases to Highlight

- **Junior Devs**: Learn API best practices while Claude guides them
- **Senior Devs**: Accelerate routine tasks (spec creation, testing)
- **QA Engineers**: Automated test execution and monitoring
- **DevOps**: API health monitoring and observability
- **API Product Managers**: Documentation quality and governance

---

## Recording Tips

### For Video Demos:

1. **Start clean** - Empty workspace or new collection
2. **Show the problem** - "I need to build an API but starting from scratch is tedious"
3. **Demo the solution** - Natural conversation with Claude
4. **Show the result** - Switch to Postman UI to show what was created
5. **Highlight the speed** - "This would have taken hours manually"

### For Screenshots:

1. **Before/After** - Show empty workspace, then populated
2. **Test Results** - Green checkmarks are visually compelling
3. **Spec Preview** - Show generated OpenAPI in Postman
4. **Monitor Dashboard** - Analytics and graphs look professional

### For GIFs:

1. **Type the request** (sped up 2x)
2. **Claude responds** (normal speed)
3. **Show result in Postman** (normal speed)
4. **Loop** - Keep it under 10 seconds

---

## Sample Screenshots to Create

### Screenshot 1: "The Ask"
```
💬 User message: "Create a REST API spec for a blog platform with
posts, comments, users, and tags. Use OpenAPI 3.0"
```

### Screenshot 2: "The Result"
```
✅ Claude's response showing:
   - Spec created with ID
   - Number of endpoints
   - Data models
   - Link to view in Postman
```

### Screenshot 3: "Postman UI"
```
📸 Postman interface showing the generated spec with:
   - API definition visible
   - Multiple endpoints listed
   - Schemas in components
```

### Screenshot 4: "Test Results"
```
✅ Test execution results:
   - Green checkmarks
   - Pass/fail ratio
   - Response times
   - Assertions validated
```

---

## Customization for Your Audience

### For Reddit (r/ClaudeAI):
- Focus on "what Claude can now do"
- Show natural language → technical output
- Emphasize developer productivity

### For LinkedIn:
- Focus on business value (time saved, quality improved)
- Mention enterprise features (security, governance)
- Professional tone, real-world scenarios

### For Twitter:
- One compelling feature per tweet
- GIF or screenshot essential
- Catchy one-liner

### For Dev.to / Hashnode:
- Full tutorial format
- Code examples
- Step-by-step walkthrough
- Tips and best practices

---

## Call to Action Ideas

```
🔗 "Get started: [GitHub URL]"
⭐ "Star the repo if you find this useful!"
💬 "What API workflow would you want Claude to handle?"
📖 "Full documentation: [Link]"
🎯 "Try it: Install the skill in Claude Desktop"
🤝 "Contributions welcome!"
```

---

**Pro Tip**: The most effective demos show a **real problem** being solved in **under 60 seconds** with **visible results**. Keep it focused on one workflow per demo.
