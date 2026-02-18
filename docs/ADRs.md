# Architecture Decision Records (ADRs)

## What is an ADR?
An Architecture Decision Record (ADR) captures an important architectural decision made along with its context and consequences. Each ADR has a unique ID and describes:
- **Context** — What is the issue we're deciding?
- **Decision** — What did we decide?
- **Consequences** — What are the trade-offs?

---

## ADR-001: AI Meal Logging Engine

**Status:** ✅ Accepted  
**Date:** Feb 18, 2026  
**Deciders:** Sam + Clawson

### Context
Trak app needs a way for users to log meals without manual calorie counting. Options:
1. Manual form entry (user types everything)
2. Edamam API (nutrition database)
3. Cloudflare Workers AI (edge LLM)
4. Kimi API (cloud LLM)
5. Local LLM (self-hosted)

### Decision
Use **Kimi K2.5 API** for AI-powered meal logging.

### Rationale
- Sam already uses and trusts Kimi
- Reliable and fast (1-2 seconds)
- Cost-effective (~$0.02 per meal vs Claude at $0.60)
- Better accuracy than edge LLMs for food specifics
- Easier setup than local LLM

### Consequences
**Positive:**
- 30-second meal logging achieved
- Natural language input ("lunch: spaghetti bolognese")
- Automatic macro breakdown (protein, carbs, fat)
- No calorie expertise required from users

**Negative:**
- Ongoing API costs (~$9-15/month for Beta, scales with users)
- Requires internet connection
- API key management needed

**Trade-offs Accepted:**
- Cost vs accuracy: Chose Kimi over free alternatives for reliability
- Cloud vs local: Chose cloud for easier setup and maintenance

---

## ADR-002: Technology Stack

**Status:** ✅ Accepted  
**Date:** Feb 16, 2026  
**Deciders:** Sam + Clawson

### Context
Need to choose tech stack for Trak Beta MVP. Requirements:
- Free/low cost
- Easy to deploy
- Scales to 100+ users eventually
- Mobile-friendly

### Decision
**Frontend:** Vanilla HTML/JS + Tailwind  
**Backend:** Cloudflare Workers  
**Database:** Cloudflare D1 (SQLite)  
**Auth:** Google OAuth 2.0  
**Hosting:** Cloudflare Pages  
**AI:** Kimi K2.5 API

### Rationale
- All free tiers sufficient for Beta (5 users)
- No build step needed (vanilla JS)
- Edge deployment = fast global
- Familiar SQL with D1
- Google OAuth = no password management

### Consequences
**Positive:**
- Zero infrastructure cost for Beta
- Fast deployment via git push
- Automatic HTTPS + CDN
- Easy to scale later

**Negative:**
- Vendor lock-in to Cloudflare
- D1 has limitations vs PostgreSQL
- No ORM (raw SQL queries)

---

## ADR-003: MVP Scope Definition

**Status:** ✅ Accepted  
**Date:** Feb 16, 2026  
**Deciders:** Sam + Clawson

### Context
Full Mission Control platform has many features. Need to define minimal scope for Beta to test core hypothesis: "Will people consistently log meals?"

### Decision
**In Scope:**
- Google OAuth only
- Nutrition page ONLY (meal logging + macros)
- Text input with AI estimation
- Single user (stretch: invite 2-3 family)
- PostgreSQL database
- 2-3 week timeline

**Out of Scope:**
- Exercise tracking
- Habits
- Work/productivity
- AI chat interface
- Photo logging
- Mobile app

### Rationale
- Test meal logging behavior before building more
- If Beta fails → pivot/kill with minimal sunk cost
- If Beta succeeds → expand with validated demand

### Consequences
**Positive:**
- Focused development
- Clear success metrics
- Fast time to Beta

**Negative:**
- Limited user value (only nutrition)
- May need to rebuild for full platform

---

## How to Add a New ADR

1. Copy the template below
2. Fill in Context, Decision, Rationale, Consequences
3. Add to this file with next ADR number
4. Update any relevant PRD sections
5. Commit to git with message: `docs(adr): Add ADR-XXX description`

### ADR Template

```markdown
## ADR-XXX: [Title]

**Status:** [Proposed / Accepted / Deprecated / Superseded by ADR-YYY]  
**Date:** [YYYY-MM-DD]  
**Deciders:** [Names]

### Context
[What is the issue we're deciding? What are the options?]

### Decision
[What did we decide?]

### Rationale
[Why this option? What criteria?]

### Consequences
**Positive:**
- [Benefit 1]
- [Benefit 2]

**Negative:**
- [Trade-off 1]
- [Trade-off 2]
```

---

## Decision Log Summary

| Date | Decision | ADR | Impact |
|------|----------|-----|--------|
| Feb 16, 2026 | Cloudflare stack chosen | ADR-002 | Architecture |
| Feb 16, 2026 | MVP scope defined | ADR-003 | Scope |
| Feb 18, 2026 | Kimi AI for meal logging | ADR-001 | Feature |

---

*Last Updated: Feb 18, 2026*
