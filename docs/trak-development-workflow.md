# Trak Beta - Development Workflow & Stack

## Overview
Modern, serverless stack for rapid MVP development with AI-assisted design and coding.

---

## Tech Stack

| Layer | Technology | Purpose |
|-------|------------|---------|
| **Frontend** | React + Vite | Fast, modern UI with hot reload |
| **Backend** | Cloudflare Workers | Serverless edge functions |
| **Database** | Cloudflare D1 | SQLite at the edge, zero latency |
| **Hosting** | Cloudflare Pages | Global CDN, instant deploys |
| **Auth** | Google OAuth | Secure, familiar login |
| **AI** | Kimi K2.5 | Meal logging, natural language |

---

## Design Workflow

### 1. Google Stitch → Wireframes
**Input:** Natural language prompts  
**Output:** High-fidelity wireframes  
**Example prompts:**
```
Mobile app login screen for "Trak" nutrition app.
Clean white background, centered green gradient app icon,
"Continue with Google" button, minimalist design.
```

### 2. Stitch → Figma Export
- Export Stitch designs as PNG/SVG
- Import into Figma for refinement
- Create component library
- Define design system (colors, typography, spacing)

### 3. Rive → Animated Logo
**Tool:** [Rive.app](https://rive.app)  
**Use case:** Animated Trak logo for:
- Splash screen
- Loading states
- Success animations (meal logged)

**Process:**
1. Design logo in Figma/Illustrator
2. Import to Rive
3. Add animations (morph, bounce, pulse)
4. Export as lightweight .riv file
5. Embed in React with `@rive-app/react-canvas`

---

## Development Workflow

### Cursor + Claude Combo

**Cursor** (AI-powered IDE):
- Code generation from comments
- Auto-complete based on context
- Refactoring suggestions
- Debug assistance

**Claude** (via OpenClaw):
- Architecture decisions
- Complex problem solving
- Code review
- Documentation

**Workflow:**
```
1. Write prompt in Cursor:
   "Create React component for meal logging form
    with natural language input and AI estimation"

2. Cursor generates code

3. Ask Claude for review:
   "Review this component for best practices,
    error handling, and Kimi API integration"

4. Iterate based on feedback
```

---

## Project Structure

```
trak-beta/
├── frontend/                 # React + Vite
│   ├── src/
│   │   ├── components/      # Reusable UI
│   │   ├── pages/           # Route components
│   │   ├── hooks/           # Custom React hooks
│   │   ├── lib/             # Utils, API clients
│   │   └── assets/          # Images, .riv files
│   ├── public/              # Static assets
│   └── index.html
├── worker/                   # Cloudflare Worker
│   ├── src/
│   │   ├── index.ts         # Main entry
│   │   ├── auth.ts          # Google OAuth
│   │   ├── meals.ts         # Meal CRUD
│   │   └── kimai.ts         # Kimi AI integration
│   └── wrangler.toml
├── database/
│   └── schema.sql           # D1 schema
└── docs/
    ├── wireframes/          # Stitch exports
    ├── figma/              # Figma links
    └── adr/                # Architecture decisions
```

---

## Database Schema (D1)

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
    protein REAL,
    carbs REAL,
    fat REAL,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id)
);

-- Indexes for performance
CREATE INDEX idx_meals_user_date ON meals(user_id, date);
```

---

## API Endpoints (Cloudflare Workers)

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/api/auth/google` | POST | OAuth callback |
| `/api/meals` | GET | Get meals for date |
| `/api/meals` | POST | Create meal |
| `/api/meals/:id` | PUT | Update meal |
| `/api/meals/:id` | DELETE | Delete meal |
| `/api/estimate` | POST | Kimi AI macro estimation |

---

## Deployment Flow

### Local Development
```bash
# Frontend
cd frontend
npm run dev          # Vite dev server

# Worker (local simulation)
cd worker
wrangler dev         # Local Worker

# D1 (local)
wrangler d1 execute trak-db --local --file=./schema.sql
```

### Production Deploy
```bash
# Deploy frontend to Cloudflare Pages
cd frontend
wrangler pages deploy dist

# Deploy worker
cd worker
wrangler deploy

# D1 migrations
wrangler d1 migrations apply trak-db
```

---

## Key Decisions

### Why Cloudflare?
- **Free tier generous** (100k requests/day)
- **Edge deployment** = fast global
- **D1 SQLite** = familiar, zero config
- **Workers** = no server management

### Why React + Vite?
- **Fast HMR** (Hot Module Replacement)
- **Modern DX** (ES modules, TypeScript)
- **Small bundle** (tree shaking)
- **Easy deploy** (static export)

### Why Rive?
- **Lightweight** (vs Lottie)
- **Interactive** (state machines)
- **Cross-platform** (web, mobile)
- **Designer-friendly**

---

## Timeline

| Phase | Duration | Deliverable |
|-------|----------|-------------|
| **1. Design** | 2 days | Stitch wireframes → Figma → Rive logo |
| **2. Setup** | 1 day | Cloudflare project, D1, auth |
| **3. Core Features** | 3 days | Auth, meal logging, dashboard |
| **4. AI Integration** | 2 days | Kimi API, macro estimation |
| **5. Polish** | 2 days | Animations, testing, bug fixes |
| **6. Beta Launch** | 1 day | Deploy, invite family |

**Total: 11 days**

---

## Resources

- **Stitch:** https://stitch.withgoogle.com
- **Rive:** https://rive.app
- **Cloudflare:** https://cloudflare.com
- **Cursor:** https://cursor.sh
- **Claude:** https://claude.ai

---

*Last Updated: Feb 19, 2026*
