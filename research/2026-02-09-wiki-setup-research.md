# Research Wiki Setup and Implementation

**Research Date:** 2026-02-09  
**Task Source:** Notion Ideas & Tasks Database  
**Status:** Complete  
**Research File:** `research/2026-02-09/wiki-setup-implementation-research.md`

---

## Executive Summary

Setting up a research wiki requires choosing between multiple platforms based on use case, technical comfort level, and desired features. For personal research organization and knowledge management, the optimal solution depends on whether you prioritize local-first storage, collaboration features, or ease of setup.

**Key Finding:** A hybrid approach using Obsidian for local knowledge capture with GitHub Wiki or MkDocs for published documentation offers the best balance of flexibility, control, and accessibility.

---

## Platform Comparison

### 1. GitHub Wiki
**Best For:** Technical projects, code documentation, version-controlled knowledge

**Pros:**
- Free with GitHub repositories
- Built-in version control via Git
- Markdown support with rich formatting
- Math expressions, diagrams, and 3D models
- Can edit directly on GitHub or locally
- Public or private (based on repo visibility)
- Soft limit: ~5,000 files

**Cons:**
- Less discoverable (only indexed by search engines with 500+ stars and restricted editing)
- No built-in search engine optimization
- Limited customization options
- Requires Git knowledge for advanced usage

**Setup Complexity:** Low-Medium  
**Cost:** Free (with GitHub account)

---

### 2. Notion Wiki
**Best For:** Teams, collaborative research, non-technical users

**Pros:**
- Intuitive drag-and-drop interface
- Powerful database and relation features
- Real-time collaboration
- Built-in AI assistance
- Templates and embeds
- Cross-platform (web, desktop, mobile)
- Granular permission controls

**Cons:**
- Requires internet connection
- Proprietary format (export options available but limited)
- Can become expensive for teams
- Performance issues with large workspaces
- Vendor lock-in concerns

**Setup Complexity:** Low  
**Cost:** Free tier available; Pro from $8/month

---

### 3. Obsidian
**Best For:** Personal knowledge management, Zettelkasten method, privacy-focused users

**Pros:**
- Local-first (files stored on your device)
- Plain text Markdown files
- Graph view for visualizing connections
- Thousands of community plugins
- Free for personal use
- Works offline
- Future-proof (open file formats)
- No vendor lock-in

**Cons:**
- Steeper learning curve
- Sync requires paid service or manual setup
- Publishing requires additional tools
- Mobile experience less polished

**Setup Complexity:** Low (personal), Medium (with sync/publish)  
**Cost:** Free for personal use; Sync/Publish from $4/month

---

### 4. MkDocs
**Best For:** Technical documentation, project wikis, static site generation

**Pros:**
- Fast static site generation
- Markdown-based
- Built-in dev server with auto-reload
- Multiple themes available (Material theme highly recommended)
- Can host anywhere (GitHub Pages, Netlify, Vercel, etc.)
- Full-text search
- Customizable with plugins

**Cons:**
- Requires technical knowledge (Python, YAML)
- Static content only (no dynamic features)
- No built-in editor
- Collaboration requires Git workflow

**Setup Complexity:** Medium  
**Cost:** Free (hosting costs may apply)

---

### 5. Docsify
**Best For:** Simple documentation, quick setup, client-side rendering

**Pros:**
- No build process required
- Runs entirely client-side
- Markdown support
- Easy to deploy (just HTML files)
- Full-text search plugin
- Customizable themes

**Cons:**
- Not SEO-friendly by default
- Can be slow with large wikis
- Limited to client-side capabilities
- Requires JavaScript enabled

**Setup Complexity:** Low  
**Cost:** Free

---

## Recommendation Matrix

| Use Case | Recommended Platform | Alternative |
|----------|---------------------|-------------|
| Personal Research Vault | **Obsidian** | Notion |
| Technical Documentation | **MkDocs + GitHub Pages** | GitHub Wiki |
| Team Collaboration | **Notion** | Obsidian + Git |
| Open Source Project | **GitHub Wiki** | MkDocs |
| Quick Documentation | **Docsify** | GitHub Wiki |
| Mixed Personal/Team | **Obsidian + GitHub Wiki** | Notion |

---

## Implementation Guide: Recommended Hybrid Setup

### Phase 1: Local Knowledge Capture (Obsidian)

**Setup Steps:**
1. Download Obsidian from https://obsidian.md
2. Create a new vault in your workspace
3. Install recommended plugins:
   - Daily Notes
   - Graph View
   - Templates
   - Dataview (for queries)
   - Git Integration (optional)

**Folder Structure:**
```
research-vault/
├── 00-Inbox/              # Fleeting notes, quick captures
├── 01-Projects/           # Active research projects
├── 02-Areas/             # Ongoing research areas
├── 03-Resources/         # Reference materials
├── 04-Archive/           # Completed research
├── 05-Templates/         # Note templates
└── 06-Daily/             # Daily notes
```

**Key Practices:**
- Use unique IDs for permanent notes (Zettelkasten method)
- Create MOCs (Maps of Content) for navigation
- Link notes liberally to build knowledge graph
- Use tags sparingly, prefer links

---

### Phase 2: Published Documentation (GitHub Wiki or MkDocs)

**Option A: GitHub Wiki (Easier)**

1. Create a repository: `sam-clawson-research`
2. Enable Wiki in repository settings
3. Clone wiki locally: `git clone https://github.com/username/sam-clawson-research.wiki.git`
4. Sync select notes from Obsidian to wiki
5. Use GitHub Actions for automation (optional)

**Option B: MkDocs (More Control)**

1. Install: `pip install mkdocs mkdocs-material`
2. Initialize: `mkdocs new research-wiki`
3. Configure `mkdocs.yml`:
   ```yaml
   site_name: Sam Clawson Research Wiki
   theme:
     name: material
     features:
       - navigation.tabs
       - search.suggest
   plugins:
     - search
   ```
4. Write content in `docs/` folder
5. Deploy to GitHub Pages: `mkdocs gh-deploy`

---

### Phase 3: Integration Workflow

**Daily Workflow:**
1. Capture thoughts in Obsidian Daily Notes
2. Process inbox notes into permanent notes
3. Weekly: Select notes for publication
4. Sync to GitHub Wiki/MkDocs via Git

**Automation Options:**
- Use Obsidian Git plugin for automatic commits
- GitHub Actions for MkDocs auto-deployment
- Pre-commit hooks for formatting

---

## Cost Analysis

| Component | Free Tier | Recommended Setup |
|-----------|-----------|-------------------|
| Obsidian | Free | Free |
| Obsidian Sync | N/A | $4/month (optional) |
| Obsidian Publish | N/A | $8/month (optional) |
| GitHub | Free | Free |
| GitHub Wiki | Free | Free |
| MkDocs Hosting | Free (GitHub Pages) | Free |
| **Total** | **$0/month** | **$0-4/month** |

---

## Key Insights

1. **Local-First is Best for Research:** Obsidian's local storage ensures your research is always accessible and private

2. **Version Control is Essential:** Git provides peace of mind and historical tracking

3. **Start Simple:** Begin with Obsidian, add publishing later when needed

4. **Avoid Vendor Lock-in:** Plain text Markdown ensures your knowledge remains accessible regardless of platform

5. **The Graph is Powerful:** Visualizing connections between ideas leads to new insights

6. **Consistency > Perfection:** Regular note-taking is more valuable than perfect organization

---

## Next Steps

1. **Immediate:** Install Obsidian and create research vault
2. **This Week:** Set up folder structure and import existing notes
3. **This Month:** Configure GitHub Wiki or MkDocs for publishing
4. **Ongoing:** Establish daily note-taking habit

---

## Resources

- **Obsidian:** https://obsidian.md
- **Obsidian Publish:** https://obsidian.md/publish
- **GitHub Wiki:** https://docs.github.com/en/communities/documenting-your-project-with-wikis
- **MkDocs:** https://www.mkdocs.org/
- **Material for MkDocs:** https://squidfunk.github.io/mkdocs-material/

---

*Research completed: 2026-02-09*  
*Findings saved to workspace research directory*
