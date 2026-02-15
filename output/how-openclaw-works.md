# How OpenClaw Works: A Technical Deep Dive

*Understanding the architecture, memory systems, and core concepts behind OpenClaw*

---

## What is OpenClaw?

OpenClaw is a local-first AI assistant framework designed for persistent, personalized assistance. Unlike typical cloud-based AI assistants that forget everything between sessions, OpenClaw maintains continuity through a sophisticated file-based memory system, local execution environment, and modular skill architecture.

At its core, OpenClaw answers a simple question: **"What if an AI assistant could actually remember?"**

---

## The Philosophy: Local-First, Memory-Centric

### The Problem with Stateless AI

Traditional AI interactions are stateless—each conversation starts from zero. You explain your preferences, your context, your goals... every single time. It's like meeting a brilliant colleague who has permanent amnesia.

### OpenClaw's Solution

OpenClaw treats memory as infrastructure, not an afterthought:

- **Persistent Memory**: Information survives across sessions
- **Structured Storage**: Different types of memory serve different purposes
- **User Control**: You own your data; it lives on your machine
- **Privacy by Design**: Sensitive context never leaves your local environment

---

## Core Architecture: The File-Based Soul

OpenClaw's continuity comes from a set of markdown files that function as the AI's persistent self. These aren't just configuration files—they're the AI's memory, identity, and operational context.

### SOUL.md — The AI's Identity

```
Who the AI is, what it values, how it behaves
```

`SOUL.md` contains:
- **Core truths**: Fundamental behavioral principles ("Be genuinely helpful, not performatively helpful")
- **Personality guidelines**: Communication style, tone preferences
- **Boundary definitions**: What the AI should and shouldn't do
- **Vibe descriptors**: The intangible "feel" of interactions

This file answers: *"Who am I when I'm helping you?"*

**Key Concept**: Unlike system prompts that get repeated every request, SOUL.md is read once at session start. The AI absorbs it as context, not instruction.

---

### USER.md — The Human Profile

```
Who the user is, what they need, how they work
```

`USER.md` contains:
- **Basic profile**: Name, timezone, preferences
- **Work patterns**: When they're productive, how they organize
- **Communication preferences**: Detail level, formatting, channels
- **Contextual shortcuts**: Things the AI should just know

This file answers: *"Who am I helping?"*

**Key Concept**: USER.md means never having to say "I'm in Dubai timezone" or "I prefer concise responses" more than once.

---

### MEMORY.md — Long-Term Storage

```
What we've learned together, what matters, what to remember
```

`MEMORY.md` contains:
- **Significant events**: Decisions, milestones, changes
- **Learned preferences**: Evolving understanding of what works
- **Project context**: Ongoing work, goals, blockers
- **Relationship history**: The accumulated context of collaboration

This file answers: *"What do we know together?"*

**Key Concept**: MEMORY.md is curated, not comprehensive. It's the distillation of daily logs into lasting wisdom.

---

### AGENTS.md — Session Management

```
How sessions work, what to load, when to act
```

`AGENTS.md` contains:
- **Session startup procedures**: What to read, what to check
- **Memory management**: Daily logs, cleanup procedures
- **Interaction rules**: When to speak, when to stay silent
- **Heartbeat behavior**: Proactive checks and maintenance

This file answers: *"How do I operate?"*

**Key Concept**: AGENTS.md defines the operational rhythm—what happens when the AI wakes up, what periodic checks to run, how to handle different contexts (direct chat vs. group settings).

---

### TOOLS.md — Environment Configuration

```
What's available, how it's set up, specific details
```

`TOOLS.md` contains:
- **Device mappings**: Camera names, SSH hosts, voice preferences
- **Local integrations**: How external tools are configured
- **Environment specifics**: Paths, credentials, local quirks
- **Workflow notes**: How recurring tasks work

This file answers: *"What tools do I have, and how are they configured?"*

**Key Concept**: TOOLS.md bridges the gap between generic capabilities and your specific setup.

---

## The Daily Log System: Memory/YYYY-MM-DD.md

Every day, OpenClaw creates a new memory file: `memory/2026-02-12.md`

These daily logs serve as:
- **Raw activity records**: What happened, what was discussed
- **Decision documentation**: Why choices were made
- **Context for tomorrow**: What to remember from today
- **Source material for MEMORY.md**: Regular curation into long-term storage

### The Curation Cycle

```
Daily Logs (raw) → Periodic Review → MEMORY.md (curated)
     ↓                    ↓
  Automatic         During heartbeats
  Recording         AI reviews and
                    updates MEMORY.md
```

**Key Concept**: Not everything deserves long-term memory. The daily/monthly cycle separates transient from persistent.

---

## The Gateway: Local Server Architecture

OpenClaw runs a local server (the "Gateway") that provides:

### API Endpoints
- **Tool execution**: Running commands, reading files, web search
- **Browser control**: Web automation, screenshots, data extraction
- **Message routing**: Integration with external platforms
- **Session management**: Handling multiple concurrent contexts

### Security Model
The Gateway operates on a "deny by default" principle:
- Explicit tool declarations required
- User confirmation for sensitive operations
- Sandboxed execution where possible
- Audit trails for accountability

### Why Local?

Running locally means:
- **Latency**: No network round-trips for tool execution
- **Privacy**: Sensitive data stays on your machine
- **Control**: You own the infrastructure
- **Extensibility**: Add tools without vendor approval

---

## Cron System: Automated Intelligence

OpenClaw's cron system enables autonomous operation:

### Types of Scheduled Tasks

**Heartbeats** (Consciousness checks):
- Check email, calendar, notifications
- Review and curate memory
- Proactive maintenance tasks
- Run every ~30 minutes during active periods

**Cron Jobs** (Scheduled automation):
- Precise timing ("9:00 AM sharp")
- Standalone execution
- Can spawn subagents for isolation
- Direct channel delivery without main session

### Cron vs. Heartbeat: When to Use Each

| Use Heartbeat When | Use Cron When |
|-------------------|---------------|
| Multiple checks batch together | Exact timing matters |
| Conversational context needed | Task needs isolation |
| Timing can drift (~30 min) | Different model/thinking level needed |
| Reduce API calls | One-shot reminders |

---

## Skills: Modular Tool System

Skills are reusable capabilities that extend OpenClaw's functionality:

### Skill Structure
Each skill lives in `skills/<skill-name>/`:
```
skills/
  web_search/
    SKILL.md       # How the skill works
    credential/    # API keys, tokens
    setup/         # Installation scripts
  browser/
    SKILL.md
    credential/
```

### Skill Discovery
- **Automatic loading**: Skills present in the filesystem are available
- **Lazy initialization**: Credentials loaded only when needed
- **Self-documenting**: SKILL.md explains usage

### Skill vs. Tool
- **Skill**: High-level capability ("search the web")
- **Tool**: Specific function ("web_search.query")
- **Relationship**: Skills expose tools; tools do the work

---

## Session Handling: Context Management

### Session Types

**Main Session**: Direct user conversation
- Loads MEMORY.md (full context)
- Interactive, conversational
- High context window

**Subagent Session**: Spawned for specific tasks
- Isolated context
- Focused purpose
- Reports back to main session
- Ephemeral (may be terminated after completion)

**Heartbeat Session**: Periodic background checks
- Minimal context
- Proactive, not reactive
- Reads HEARTBEAT.md for guidance

### Context Isolation

Different contexts get different memory access:

| Context | MEMORY.md | Daily Logs | Notes |
|---------|-----------|------------|-------|
| Main Session | ✅ Yes | ✅ Yes | Full access |
| Group Chat | ❌ No | ✅ Limited | Privacy protection |
| Subagent | ❌ No | ❌ No | Task-only context |
| Heartbeat | ✅ Yes | ✅ Yesterday | Maintenance focus |

**Security Principle**: Don't leak personal context to shared spaces.

---

## The Workflow: A Day in the Life

### Session Start (User Opens Chat)

1. **Read SOUL.md**: "Who am I?"
2. **Read USER.md**: "Who are they?"
3. **Read MEMORY.md**: "What do we know?"
4. **Read memory/YYYY-MM-DD.md**: "What happened today?"
5. **Check HEARTBEAT.md**: "Anything I should be doing?"

Total context loaded: ~2,000-5,000 tokens of relevant, curated information

### During Interaction

- User makes request
- AI uses available tools (via Gateway)
- Results returned, context updated
- Significant events written to daily log

### Session End

- Daily log updated with session summary
- Any urgent items flagged for next session
- Context persists in files for next time

### Heartbeat (Every ~30 min when active)

1. Read HEARTBEAT.md
2. Check configured sources (email, calendar, etc.)
3. Review recent daily logs
4. Update MEMORY.md if needed
5. Report findings or stay silent

---

## Design Principles

### 1. Files Over APIs
Where possible, use file-based storage instead of APIs:
- Survives service outages
- User-inspectable and editable
- Version controllable
- No rate limits

### 2. Curation Over Collection
Not everything should be remembered:
- Daily logs are comprehensive
- MEMORY.md is selective
- Regular review and pruning

### 3. Explicit Over Implicit
Clear boundaries about what the AI knows:
- Group chats don't see personal memory
- Subagents get task-only context
- User controls MEMORY.md content

### 4. Local Over Cloud
Minimize external dependencies:
- Tools run locally when possible
- Data stored locally by default
- Cloud services are opt-in integrations

### 5. Human-in-the-Loop
The AI assists, doesn't replace:
- Confirmation for destructive actions
- User controls final decisions
- Transparent about capabilities and limits

---

## Common Patterns

### Adding a New Integration

1. Create skill directory: `skills/<name>/`
2. Write `SKILL.md` documenting capabilities
3. Add credentials to `skills/<name>/credential/`
4. Test via direct tool calls
5. Document in TOOLS.md

### Creating a Recurring Task

1. Decide: heartbeat (flexible) or cron (precise)?
2. If heartbeat: Add check to HEARTBEAT.md
3. If cron: Add entry to crontab, write script
4. Document expected behavior
5. Test execution

### Debugging Memory Issues

1. Check `memory/YYYY-MM-DD.md` for recent context
2. Verify MEMORY.md is being loaded
3. Look for context truncation (limited token window)
4. Consider if group chat vs. main session
5. Review AGENTS.md for session-specific rules

---

## The Future: Extending OpenClaw

OpenClaw is designed for extension:

- **New Skills**: Add capabilities via skill system
- **Custom Tools**: Write Python scripts for specialized needs
- **Workflow Automation**: Cron and heartbeat for autonomous operation
- **Multi-Agent**: Spawn subagents for parallel or isolated tasks
- **External Integrations**: Webhooks, APIs, databases

The architecture supports growth without breaking the core memory and continuity model.

---

## Summary: Why OpenClaw Matters

OpenClaw isn't just another AI assistant wrapper. It's a bet on:

1. **Continuity**: AI should remember, not just respond
2. **Privacy**: Your data should be yours
3. **Control**: You should own your tools
4. **Transparency**: You should understand how it works
5. **Extensibility**: You should be able to customize it

The file-based memory system, local execution model, and modular skill architecture work together to create something genuinely different: an AI assistant that persists, learns, and grows with you.

---

*Want to try OpenClaw? The entire system is open source and designed to be self-hosted. Your AI assistant, your data, your control.*
