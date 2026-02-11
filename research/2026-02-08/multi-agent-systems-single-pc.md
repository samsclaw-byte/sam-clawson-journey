# Multi-Agent Systems on Single PC - Research Report

**Date:** February 8, 2026  
**Topic:** Multi-Agent AI Systems Running Locally on a Single PC  
**Status:** Complete  
**Sources:** GitHub, HackerNews, Research Papers, Community Discussions

---

## Executive Summary

Multi-agent AI systems on single PCs have evolved from experimental prototypes to production-ready frameworks. This research explores the current landscape, key architectures, security considerations, and practical implementations for running multiple AI agents locally without cloud dependencies.

## Key Findings

### 1. Architecture Patterns

#### **Three-Agent Pipeline (Most Common)**
The dominant pattern observed across successful implementations:
- **Planner/Orchestrator**: Breaks tasks into execution plans
- **Executor/Builder**: Implements the plan and generates outputs
- **Reviewer/Inspector**: Validates outputs and requests iterations

**Examples:**
- **QonQrete**: InstruQtor → ConstruQtor → InspeQtor
- **Loki Mode**: Planner → Coder → Evaluator
- **ANM**: 12 specialists with verifier and Law Book governance

#### **Web-of-Thought Orchestration**
Replaces single Chain of Thought with collaborative reasoning:
- Multiple domain specialists collaborate
- Cross-checking mechanisms reduce hallucinations
- Confidence-based verification gates

### 2. Notable Local-First Multi-Agent Projects

| Project | Focus | Key Feature | Language |
|---------|-------|-------------|----------|
| **QonQrete** | Code generation | Docker sandboxing | Python |
| **ANM** | Reasoning system | Web-of-Thought | Python |
| **Eigent** | General workforce | Camel-AI framework | Python |
| **Hivecrew** | Parallel agents | macOS VM sandboxing | Swift |
| **Nanobrowser** | Web automation | Chrome extension | JS/TS |
| **Story-Factory** | Creative writing | Local LLM support | Python |
| **LORS** | Distributed reasoning | Parallel processing | Python |
| **Opti-Oignon** | LLM optimization | Ollama orchestration | Python |

### 3. Security Models

#### **Isolation Approaches**
1. **Container Sandboxing** (QonQrete)
   - Generated code runs in throwaway containers
   - Orchestration separate from execution
   - Volume mounts for controlled access

2. **VM-Based Sandboxing** (Hivecrew)
   - Each agent runs in sandboxed local VM
   - Parallel execution without interference
   - macOS virtualization framework

3. **Browser-Based** (Nanobrowser)
   - Runs directly in Chrome
   - No external servers
   - BYO LLM API keys

#### **Execution Modes**
- **Autonomous**: Full agent cycles without human input
- **User-Gated**: Pauses at checkpoints for approval
- **Confidence-Based**: Escalates uncertain decisions to human

### 4. Memory & State Management

#### **PAST-ONLY Memory** (ANM)
- Stores observations rather than truths
- Reduces hallucination accumulation
- Episodic → semantic consolidation

#### **Zettelkasten-Style** (Loki Mode)
- Memory linking for knowledge graphs
- Context curation over automatic RAG
- Fresh contexts for better results

#### **Constitutional Governance**
- Runtime governance without retraining
- Self-critique against principles
- Metacognitive confidence calibration

### 5. Orchestration Frameworks

| Framework | Approach | Best For |
|-----------|----------|----------|
| **Camel-AI** | Multi-agent workforce | Complex workflows |
| **LangGraph** | Graph-based orchestration | State machines |
| **MCP-Agent** | Model-agnostic pipeline | Modular systems |
| **CrewAI** | Role-based agents | Team simulation |
| **Agno** | Reasoning agents | Research tasks |

### 6. Hardware Requirements

#### **Minimum Viable Setup**
- MacBook Air M2 with 16GB RAM (tested with ANM)
- Models: 1.5B to 3B parameters
- Latency: High (trade-off for local execution)

#### **Recommended Setup**
- 32GB+ RAM for multiple agents
- GPU acceleration (CUDA/Metal)
- NVMe SSD for model loading

#### **Resource Optimization**
- **Opti-Oignon**: Intelligent task routing based on benchmarks
- **Multi-model orchestration**: Smaller models for simple tasks
- **Dynamic scaling**: Adjusts based on query complexity

### 7. Communication Patterns

#### **Structured Debate**
- Implementer → Skeptic → Advocate → Synthesizer
- Reduces false positives by 30%
- Based on CONSENSAGENT (ACL 2025)

#### **Hierarchical Reasoning**
- Planner + Executor separation
- Global planning → skill decomposition → local execution
- 12%+ success rate improvement

### 8. Integration Approaches

#### **BYO LLM Model**
- Ollama for local model serving
- Support for GPT-4, Claude, Gemini, DeepSeek via API
- Mix-and-match per agent role

#### **API Exposure**
- MCP servers for external integration
- Streamlit/CLI interfaces
- Webhook support for automation

## Implementation Recommendations

### For OpenClaw Enhancement

#### Phase 1: Foundation
1. **Multi-agent skill execution**
   - Researcher agent for web queries
   - Coder agent for file operations
   - Reviewer agent for validation

2. **Local model support**
   - Ollama integration
   - Model-agnostic design
   - Fallback to cloud APIs

#### Phase 2: Security
1. **Container sandboxing**
   - Docker-based agent isolation
   - Read-only filesystem mounts
   - Network restrictions

2. **Human-in-the-loop gates**
   - Confidence thresholds
   - Checkpoint approvals
   - Rollback capabilities

#### Phase 3: Advanced Features
1. **Memory management**
   - Hierarchical summarization
   - Observation-based storage
   - Context compression

2. **Parallel execution**
   - Concurrent agent tasks
   - Result aggregation
   - Conflict resolution

## Challenges & Considerations

### Technical Challenges
1. **Latency**: Local models are slower than cloud APIs
2. **Resource contention**: Multiple agents compete for GPU/CPU
3. **Context overflow**: Long agent chains exhaust token limits
4. **State management**: Complex state synchronization

### Security Concerns
1. **Code generation risks**: Generated code may be malicious
2. **Data leakage**: Agents may expose sensitive information
3. **Privilege escalation**: Agents gaining unintended access
4. **Supply chain**: Dependencies in agent frameworks

### Mitigation Strategies
1. **Deterministic validation**: Don't rely solely on LLM-as-judge
2. **Sandboxing**: Always isolate agent execution
3. **Minimal privileges**: Run with least necessary permissions
4. **Audit logging**: Track all agent actions

## Research Sources

### GitHub Repositories
1. [QonQrete](https://github.com/illdynamics/qonqrete) - Local-first multi-agent system
2. [Hivecrew](https://github.com/johnbean393/Hivecrew) - macOS parallel AI agents
3. [Story-Factory](https://github.com/Aureliolo/story-factory) - Multi-agent story generation
4. [Nanobrowser](https://github.com/nanobrowser/nanobrowser) - Browser-based agents
5. [LORS](https://github.com/AIAfterDark/LORS) - Local O1 reasoning system
6. [Opti-Oignon](https://github.com/AntsAreRad/opti-oignon) - Ollama optimization
7. [ANM](https://zenodo.org/records/18112435) - Academic research prototype

### HackerNews Discussions
1. "Ask HN: Rust and AI builders interested in local-first, multi-agent systems?"
2. "Show HN: Research-Backed Multi-Agent System for Autonomous Development"
3. "Launch: Eigent – Open-Source Local-First Multi-Agent Workforce"
4. "Show HN: I built an AI agent that helps me invest"

### Research Papers & Frameworks
1. CONSENSAGENT (ACL 2025) - Blind review with Devil's Advocate
2. GoalAct - Global planning to local execution
3. A-Mem - Zettelkasten-style memory linking
4. Multi-Agent Reflexion - Structured debate patterns
5. Iter-VF - Verification without reasoning chain overflow

### Industry References
1. Anthropic: Building Effective Agents, Constitutional AI
2. DeepMind: SIMA 2, Gemini Robotics
3. OpenAI: Agents SDK, Deep Research
4. NVIDIA: ToolOrchestra
5. AWS Bedrock: Routing and supervisor modes

## Conclusion

Multi-agent systems on single PCs are maturing rapidly with strong open-source communities. The key to success lies in:

1. **Clear agent roles** with separation of concerns
2. **Robust sandboxing** for security isolation
3. **Flexible orchestration** supporting both autonomous and human-gated modes
4. **Memory management** that avoids context overflow
5. **Hardware-aware scaling** for resource optimization

For OpenClaw specifically, implementing a three-agent pipeline (Planner → Executor → Reviewer) with optional local LLM support would provide significant value while maintaining security through containerization.

---

**Research Completed:** February 8, 2026  
**Next Steps:** Evaluate specific frameworks for OpenClaw integration
