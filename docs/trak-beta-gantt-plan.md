# Trak Beta Launch GANTT & Clawson Integration Plan

## Overview
Build a GANTT chart for Trak Health & Nutrition app beta launch with 10 delivery tasks. Include local storage for editing and research Clawson AI integration.

---

## Trak Beta Launch - 10 Tasks

### Phase 1: Infrastructure (Days 1-3)
**Task 1: Cloudflare Setup**
- Duration: 1 day
- Start: Day 1
- Setup: Pages, D1 database, Workers
- Owner: Sam
- Status: Not Started

**Task 2: D1 Database Schema**
- Duration: 1 day
- Start: Day 2
- Tables: Users, Food Log, Daily Habits, Goals
- Owner: Sam
- Status: Not Started

**Task 3: Authentication (Google OAuth)**
- Duration: 1 day
- Start: Day 2
- Setup: Google Cloud, OAuth flow
- Owner: Sam
- Status: Not Started

### Phase 2: Core Features (Days 4-7)
**Task 4: Food Logging UI**
- Duration: 2 days
- Start: Day 4
- Screens: Quick add, history, edit
- Owner: Sam
- Status: Not Started

**Task 5: Daily Habits Tracker**
- Duration: 1 day
- Start: Day 5
- Features: Water, vitamins, exercise, fruit
- Owner: Sam
- Status: Not Started

**Task 6: Macro Estimation Engine**
- Duration: 1 day
- Start: Day 6
- Fallback: Keyword-based (no Edamam API)
- Owner: Sam
- Status: Not Started

### Phase 3: Polish & Launch (Days 8-10)
**Task 7: Dashboard & Analytics**
- Duration: 1 day
- Start: Day 8
- Charts: Weekly trends, goal progress
- Owner: Sam
- Status: Not Started

**Task 8: Settings & Profile**
- Duration: 1 day
- Start: Day 8
- Features: Units, goals, notifications
- Owner: Sam
- Status: Not Started

**Task 9: Testing & QA**
- Duration: 1 day
- Start: Day 9
- Test: Food logging, habits, UI
- Owner: Sam
- Status: Not Started

**Task 10: Beta Launch**
- Duration: 1 day
- Start: Day 10
- Deploy: Production, invite beta users
- Owner: Sam
- Status: Not Started

---

## Clawson AI Integration Research

### Permission Model
**What Clawson CAN do:**
1. **Add entries**: Food logs, habits, notes
2. **Edit entries**: Modify existing data (user confirms)
3. **Delete entries**: Remove items (requires confirmation)
4. **Query data**: Read-only access to user's own data
5. **Suggest**: Recommendations based on patterns

**What Clawson CANNOT do:**
1. **Access other users' data**
2. **Modify app settings**
3. **Delete account**
4. **Access payment info**
5. **Export bulk data**

### Implementation Options

**Option 1: Scoped API Keys**
```javascript
// User-specific token with limited scopes
const clawsonToken = {
  userId: "user_123",
  scopes: ["food:write", "habits:write", "data:read"],
  expires: "2026-03-01"
}
```

**Option 2: Proxy Server (Recommended)**
```javascript
// Cloudflare Worker validates permissions
async function handleClawsonRequest(request, env) {
  const { userId, action, data } = await request.json();
  
  // Validate user owns the data
  if (!await validateOwnership(userId, data.id)) {
    return new Response("Unauthorized", { status: 403 });
  }
  
  // Check action is allowed
  const allowedActions = ["addFood", "editHabit", "deleteEntry"];
  if (!allowedActions.includes(action)) {
    return new Response("Action not allowed", { status: 403 });
  }
  
  // Execute via OpenClaw Gateway
  return await forwardToClawson(userId, action, data);
}
```

**Option 3: Webhook Integration**
```javascript
// Trak app sends webhook to OpenClaw Gateway
// Gateway responds with actions
app.post('/webhook/clawson', async (req, res) => {
  const { message, userId } = req.body;
  
  // Parse intent
  const intent = await parseIntent(message);
  
  // Execute if allowed
  if (isAllowed(intent.action)) {
    const result = await executeAction(userId, intent);
    res.json({ success: true, result });
  }
});
```

### Security Model

**Authentication Flow:**
1. User authenticates with Trak (Google OAuth)
2. Trak generates scoped token for Clawson
3. Token stored securely (D1 encrypted)
4. All Clawson requests include token + user signature
5. Worker validates token + action permission

**Rate Limiting:**
- 100 requests/hour per user
- 10 write operations/hour (prevent spam)

**Audit Log:**
- All Clawson actions logged
- User can review in settings
- Can revoke Clawson access anytime

### UI Integration

**Chat Interface in Trak:**
```
┌─────────────────────────┐
│ 🦞 Ask Clawson          │
├─────────────────────────┤
│ [User message]          │
│ [Clawson response]      │
│                         │
│ "Log: Chicken salad"    │
│ [Preview] [Confirm]     │
└─────────────────────────┘
```

**Permission Settings:**
```
☑️ Allow Clawson to add food logs
☑️ Allow Clawson to edit entries (with confirmation)
☑️ Allow Clawson to delete entries (with confirmation)
☑️ Allow Clawson to view my data
☐ Allow Clawson to suggest goals
[Revoke Access]
```

---

## Next Steps

1. **Build GANTT chart** in Mission Control Projects section
2. **Implement local storage** for task editing
3. **Set up proxy server** for Clawson integration
4. **Test permission model** with scoped tokens
5. **Build chat UI** in Trak app

---

*Created: Feb 18, 2026*
