# Product Requirements Document (PRD)
## Health & Nutrition App - MVP

**Version:** 1.0  
**Date:** February 16, 2026  
**Author:** Sam + Clawson (OpenClaw)  
**Status:** Draft - Ready for Review

---

## 1. Executive Summary

### 1.1 Product Vision
A simple, fast nutrition tracking web app for individuals and families. Core value: make meal logging so easy that people actually do it consistently.

### 1.2 MVP Scope
Ultra-minimal version to validate core behavior (meal logging) before building full platform.

**In Scope:**
- Google OAuth authentication
- Single-page nutrition dashboard
- Meal logging (text input only)
- Daily macro visualization
- Multi-user support (3-5 family members)

**Out of Scope (v2):**
- AI chat/natural language
- Photo logging
- Exercise tracking
- Habits
- Mobile app
- Social features

### 1.3 Success Criteria
- 3-5 Beta users log meals for 7 consecutive days
- Average 3+ meals logged per user per day
- Zero critical bugs preventing logging
- Users request "more features" (indicates engagement)

---

## 2. User Personas

### 2.1 Primary: Health-Conscious Individual
**Name:** Sarah, 34, working professional  
**Goal:** Track nutrition to maintain energy and manage weight  
**Pain Point:** Existing apps (MyFitnessPal) are too complex, takes 5+ minutes to log a meal  
**Need:** 30-second meal logging, no calorie counting expertise required

### 2.2 Secondary: Family Organizer
**Name:** Mike, 42, father of 2  
**Goal:** Track family nutrition, ensure kids eat balanced meals  
**Pain Point:** Can't see what spouse/kids are eating, no family overview  
**Need:** Multi-user support, simple overview of family eating patterns

---

## 3. User Stories

### 3.1 Authentication
- As a user, I want to sign in with Google so I don't need to remember another password
- As a user, I want my data isolated from other users so my nutrition info stays private

### 3.2 Meal Logging
- As a user, I want to quickly add a meal so I can log without interrupting my day
- As a user, I want to see today's meals so I know what I've eaten
- As a user, I want to see macro breakdown so I understand my nutrition balance
- As a user, I want to edit a logged meal so I can fix mistakes

### 3.3 Historical View
- As a user, I want to see past days so I can track patterns over time
- As a user, I want a simple weekly summary so I can see trends

### 3.4 Family (Stretch)
- As a family organizer, I want to invite family members so we can track together
- As a family member, I want to see my own data only so I maintain privacy

---

## 4. Functional Requirements

### 4.1 Authentication (FR-001 to FR-003)

| ID | Requirement | Priority | Acceptance Criteria |
|----|-------------|----------|---------------------|
| FR-001 | Google OAuth sign-in | Must Have | User clicks "Sign in with Google", authenticates, sees dashboard |
| FR-002 | User session management | Must Have | Session persists 24 hours, auto-refresh token |
| FR-003 | Data isolation | Must Have | User A cannot access User B's data via API or UI |

### 4.2 Meal Management (FR-004 to FR-010)

| ID | Requirement | Priority | Acceptance Criteria |
|----|-------------|----------|---------------------|
| FR-004 | Add meal | Must Have | Form with: meal type (dropdown), food name (text), optional calories, timestamp auto-set |
| FR-005 | View today's meals | Must Have | List shows all meals for current date, sorted by time |
| FR-006 | Edit meal | Should Have | Click meal → edit form → save updates database |
| FR-007 | Delete meal | Should Have | Swipe/click delete → confirmation → removes from DB |
| FR-008 | View past dates | Should Have | Date picker or calendar to navigate to any date |
| FR-009 | Macro calculation | Should Have | Pie chart showing carb/protein/fat ratio for selected day |
| FR-010 | Quick-add templates | Nice to Have | Save frequent meals for one-click logging |

### 4.3 Dashboard (FR-011 to FR-014)

| ID | Requirement | Priority | Acceptance Criteria |
|----|-------------|----------|---------------------|
| FR-011 | Today's summary | Must Have | Total calories, meal count, water (if tracked) prominently displayed |
| FR-012 | Macro visualization | Should Have | Pie chart or bar chart of macros for selected day |
| FR-013 | Weekly trend | Nice to Have | Simple line graph of calories over past 7 days |
| FR-014 | Mobile responsive | Must Have | All features work on iPhone/Android browsers |

### 4.4 Multi-User (Stretch - FR-015 to FR-017)

| ID | Requirement | Priority | Acceptance Criteria |
|----|-------------|----------|---------------------|
| FR-015 | Invite system | Should Have | Generate invite link, send to email/phone, recipient can sign up |
| FR-016 | Admin view | Nice to Have | Admin sees list of users, not their private data |
| FR-017 | User management | Nice to Have | Admin can disable/delete user accounts |

---

## 5. Non-Functional Requirements

### 5.1 Performance
- Page load: < 2 seconds on 4G
- Meal log submission: < 1 second
- Supports 10 concurrent users (Beta scope)

### 5.2 Security
- All data encrypted in transit (HTTPS)
- Database encrypted at rest
- No sensitive data in logs
- OAuth tokens never exposed client-side

### 5.3 Reliability
- 99.9% uptime (Cloudflare SLA)
- Daily database backups
- Graceful error handling with user-friendly messages

### 5.4 Scalability (Future)
- Architecture supports 1000+ users (even if Beta is 5)
- Database queries use user_id indexing
- API rate limiting built-in

---

## 6. Technical Architecture

### 6.1 Stack
| Layer | Technology | Rationale |
|-------|------------|-----------|
| Frontend | Vanilla HTML/JS + Tailwind | Fast, simple, no build step needed for MVP |
| Backend | Cloudflare Workers | Edge deployment, free tier, serverless |
| Database | Cloudflare D1 (SQLite) | Free tier, integrated with Workers, SQL familiar |
| Auth | Google OAuth 2.0 | Users already have accounts, secure, free |
| Hosting | Cloudflare Pages | Free, fast CDN, integrated with Workers |

### 6.2 Data Model

```sql
-- Users table
CREATE TABLE users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    google_id TEXT UNIQUE NOT NULL,
    email TEXT UNIQUE NOT NULL,
    name TEXT,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
);

-- Meals table
CREATE TABLE meals (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    date DATE NOT NULL,
    meal_type TEXT NOT NULL, -- breakfast, lunch, dinner, snack
    food_name TEXT NOT NULL,
    calories INTEGER,
    carbs REAL,
    protein REAL,
    fat REAL,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id)
);

-- Indexes for performance
CREATE INDEX idx_meals_user_date ON meals(user_id, date);
```

### 6.3 API Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/api/auth/google` | POST | Handle Google OAuth callback |
| `/api/meals` | GET | Get meals for date (query: date) |
| `/api/meals` | POST | Create new meal |
| `/api/meals/:id` | PUT | Update meal |
| `/api/meals/:id` | DELETE | Delete meal |
| `/api/summary` | GET | Get daily summary stats |

---

## 7. User Interface

### 7.1 Dashboard Layout (Mobile-First)

```
┌─────────────────────────────┐
│ [Logo] Health & Nutrition   │
│ Hello, [Name]      [Menu]   │
├─────────────────────────────┤
│ Today's Summary             │
│ ┌───────────────────────┐   │
│ │ 1,450 / 2,000 cal     │   │
│ │ ████████░░░░░░░░░░░   │   │
│ │ 3 meals logged        │   │
│ └───────────────────────┘   │
├─────────────────────────────┤
│ + Log Meal (Big Button)     │
├─────────────────────────────┤
│ Today's Meals               │
│ • Breakfast: Eggs & toast   │
│   8:30 AM · 450 cal         │
│ • Lunch: Chicken salad      │
│   1:00 PM · 650 cal         │
│ [+ Add another]             │
├─────────────────────────────┤
│ Macros                      │
│ [Pie chart: C/P/F]          │
│ Carbs: 45% · 163g           │
│ Protein: 30% · 109g         │
│ Fat: 25% · 40g              │
├─────────────────────────────┤
│ [Date picker: < Feb 16 >]   │
└─────────────────────────────┘
```

### 7.2 Key UI Principles
- One primary action per screen
- Minimal text - icons where possible
- Immediate feedback (no "save" button, auto-save)
- Large touch targets (min 44px)
- High contrast for readability

---

## 8. Success Metrics & Analytics

### 8.1 Primary Metrics
| Metric | Target | Measurement |
|--------|--------|-------------|
| Daily Active Users (DAU) | 3-5 | Users logging in per day |
| Meals Logged per User | 3+ / day | Average across Beta period |
| Retention (Day 7) | 80%+ | Users still logging after 7 days |
| Log Completion Time | < 60 seconds | Time from open to logged meal |

### 8.2 Secondary Metrics
- Error rate: < 1%
- Page load time: < 2 seconds
- Support requests: < 2 per user

---

## 9. Risks & Mitigations

| Risk | Impact | Likelihood | Mitigation |
|------|--------|------------|------------|
| Users don't log meals consistently | High | Medium | Daily push notification (later); simple reminder email |
| Complex foods hard to log | Medium | High | Allow free-text description; skip exact calories if unknown |
| Family members don't adopt | Medium | Medium | Make invite super easy; start with most motivated family member |
| Database performance issues | Low | Low | Proper indexing; query optimization; can migrate to PostgreSQL |
| Google OAuth issues | Medium | Low | Test thoroughly; have fallback error message |

---

## 10. Timeline & Phases

### Phase 1: Foundation (3-4 days)
- [ ] Cloudflare setup (Pages, D1, Workers)
- [ ] Google OAuth configuration
- [ ] Database schema + migrations
- [ ] Basic login flow

### Phase 2: Core Features (4-5 days)
- [ ] Dashboard UI (HTML/CSS)
- [ ] Add meal form + API
- [ ] View meals list
- [ ] Macro calculation + chart
- [ ] Edit/delete meals

### Phase 3: Multi-User (3-4 days)
- [ ] Invite system
- [ ] User isolation verification
- [ ] Admin basics
- [ ] Onboard 2-3 family members

### Phase 4: Beta Testing (7 days)
- [ ] Daily check-ins with users
- [ ] Bug fixes
- [ ] Collect feedback
- [ ] Decision: Build v2 or pivot

**Total MVP Timeline:** 17-20 days

---

## 11. Open Questions for Review

1. **Nutrition Data:** Skip API integration for MVP and use manual estimates + user correction?
2. **Offline Support:** Is basic offline support needed, or online-only acceptable for Beta?
3. **Notifications:** Email reminders for Beta, or rely on users checking app?
4. **Data Export:** Should users be able to export their data (CSV/JSON)?
5. **Monetization Path:** If Beta succeeds, what's the freemium split (what's free vs paid)?

---

## 12. Appendices

### Appendix A: Competitor Analysis
- **MyFitnessPal:** Too complex, cluttered UI, takes too long
- **Cronometer:** Too detailed, overwhelming for casual users
- **Noom:** Behavioral focus, expensive, not family-oriented
- **Apple Health:** Platform-locked, limited nutrition features

**Our Differentiator:** Family-first, ultra-simple, web-based (cross-platform)

### Appendix B: Budget Estimate
| Item | Monthly Cost |
|------|--------------|
| Cloudflare (free tier) | $0 |
| D1 Database (free tier) | $0 |
| Google OAuth | $0 |
| AI/Development assistance | $20-30 |
| **Total** | **$20-30/mo** |

---

## Document Control

| Version | Date | Author | Changes |
|---------|------|--------|---------|
| 1.0 | Feb 16, 2026 | Sam + Clawson | Initial draft |

**Next Review:** After Phase 1 completion  
**Reviewers:** Sam, [Claude/Technical Advisor], [Potential Beta User]
