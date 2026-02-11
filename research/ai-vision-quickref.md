# AI Vision Quick Reference
**One-page summary for implementation**

---

## Model Comparison Matrix

| Model | Cost/Image | Speed | Accuracy | Best For |
|-------|-----------|-------|----------|----------|
| GPT-4o-mini | $0.001-0.003 | ⚡ Fast | ⭐⭐⭐⭐ | Default choice, cost-effective |
| GPT-4o | $0.003-0.007 | ⚡ Fast | ⭐⭐⭐⭐⭐ | High accuracy needs |
| Claude 3.5 Sonnet | $0.004-0.010 | 🚀 Medium | ⭐⭐⭐⭐⭐ | Complex docs, reasoning |
| Gemini 1.5 Flash | $0.0005-0.002 | ⚡ Fastest | ⭐⭐⭐⭐ | High volume, budget |
| Llama 3.2 (local) | ~$0 | 🐢 Slower | ⭐⭐⭐ | Privacy-critical |

---

## Quick Implementation

```python
# 1. Encode image
import base64
with open("image.png", "rb") as f:
    b64 = base64.b64encode(f.read()).decode()

# 2. Send to API (OpenAI example)
response = await openai.chat.completions.create(
    model="gpt-4o-mini",
    messages=[{
        "role": "user",
        "content": [
            {"type": "text", "text": "Extract text from this image"},
            {"type": "image_url", "image_url": {"url": f"data:image/png;base64,{b64}"}}
        ]
    }]
)
```

---

## WHOOP Extraction Prompt

```
Extract from this WHOOP dashboard screenshot and return JSON:
{
    "hrv": <number or null>,
    "resting_hr": <number or null>,
    "sleep_score": <number or null>,
    "recovery_percent": <number or null>,
    "strain": <number or null>,
    "date": "YYYY-MM-DD" or null
}
```

---

## Cost Calculator

| Images/Month | GPT-4o-mini | Claude 3.5 | Gemini Flash |
|--------------|-------------|------------|--------------|
| 50 | $0.15 | $0.40 | $0.05 |
| 200 | $0.60 | $1.60 | $0.20 |
| 1000 | $3.00 | $8.00 | $1.00 |

---

## Privacy Checklist

- [ ] Enable API data opt-out (prevents training)
- [ ] Strip EXIF metadata from images
- [ ] Crop to relevant region only
- [ ] Delete raw images after extraction
- [ ] Use local model for sensitive data

---

## API Keys Needed

| Provider | Environment Variable | Get Key At |
|----------|---------------------|------------|
| OpenAI | `OPENAI_API_KEY` | platform.openai.com |
| Anthropic | `ANTHROPIC_API_KEY` | console.anthropic.com |
| Google | `GOOGLE_API_KEY` | aistudio.google.com |

---

## When to Use What

**Use GPT-4o-mini when:**
- Cost matters most
- Simple OCR/text extraction
- Quick prototyping

**Use Claude 3.5 when:**
- Complex documents
- Need reasoning about image
- Tables, forms, layouts

**Use Local Llama when:**
- Medical/health data
- Financial documents
- Privacy is paramount

---

## Common Pitfalls

❌ Sending full-resolution photos (expensive!)
✅ Resize to 1024px max before sending

❌ No error handling for API failures
✅ Implement retry with backoff

❌ Storing API responses with PII
✅ Sanitize and store only needed data

❌ Using wrong model for task
✅ Start cheap, upgrade if accuracy fails

---

## Testing Checklist

- [ ] Test with 10 real WHOOP screenshots
- [ ] Verify numeric accuracy (no hallucinations)
- [ ] Check date extraction format
- [ ] Measure response time
- [ ] Calculate actual cost per extraction
- [ ] Test edge cases (blurry, partial screenshots)

---

## Integration with OpenClaw

```
workspace/
├── skills/
│   └── vision/
│       ├── SKILL.md
│       ├── __init__.py
│       ├── extract.py      # Main extraction
│       ├── whoop.py        # WHOOP-specific
│       └── models.py       # Provider configs
```

---

**Full report:** `research/ai-vision-capabilities.md`
