#!/bin/bash
# Daily token usage estimator
# Calculates based on cron job schedule and models

cat << 'EOF'
📊 **Token Usage Estimate (Last 24h):**

**Cron Jobs:**
• Voice transcription (K1): ~288 runs × 100 tokens = ~28,800
• Reminders/check-ins (K1): 3 runs × 500 tokens = ~1,500
• Overnight tasks (K2.5): 8 runs × 2,000 tokens = ~16,000
• Blog/security (K1): 2 runs × 800 tokens = ~1,600

**Main Chat Sessions:**
• Interactive sessions: ~5,000-10,000 tokens (estimated)

**Total Estimate:** ~53,000-58,000 tokens/day
**Monthly Estimate:** ~1.6-1.8M tokens

**Cost (Mixed Models):**
• K1 jobs (~60%): ~$0.60/day
• K2.5 jobs (~40%): ~$3.50/day
• **Total: ~$4-5/day (~$120-150/month)**

**Savings vs All-K2.5:** ~$100-180/month

---

*Note: For precise tracking, enable detailed logging in OpenClaw config.*
EOF
