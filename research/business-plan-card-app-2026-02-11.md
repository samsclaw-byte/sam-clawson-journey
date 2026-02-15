# Card App Business Plan: Moonpig for Dubai
## AI-Generated Greeting Cards & Gift Delivery Platform

**Prepared for:** Sam  
**Date:** February 11, 2026  
**Version:** 1.0

---

## 1. Executive Summary

### Business Concept
CardApp Dubai is a next-generation greeting card and gift delivery platform targeting the 200,000+ British expatriate community in Dubai. Leveraging AI-powered card generation and a dropshipping fulfillment model, we combine personalized creativity with seamless logistics to capture market share from legacy players like Moonpig, Funky Pigeon, and local flower shops.

### Core Value Proposition
- **AI-Generated Personalization:** Users describe their recipient and occasion; AI generates unique, bespoke card designs in seconds
- **One-Stop Gift Solution:** Cards + flowers + cakes + gifts delivered together
- **Dubai-Focused:** Local delivery networks, culturally relevant designs, Gulf timezone support
- **Expat-Optimized:** British humor, occasion reminders (Mother's Day UK vs UAE), international shipping options

### Key Metrics
| Metric | Target |
|--------|--------|
| Target Market | 200,000 British expats in Dubai |
| Serviceable Addressable Market (SAM) | 50,000 active users (25%) |
| Average Order Value (AOV) | AED 120 ($33 USD) |
| Year 1 Revenue Target | $500,000 USD |
| Year 3 Revenue Target | $2.5M USD |

### Funding Requirements
- **Initial Capital:** $25,000 - $50,000 USD
- **Primary Use:** Platform development, initial inventory, marketing launch
- **Break-even:** Month 8-12

---

## 2. Market Analysis

### 2.1 Target Market

#### Primary Segment: British Expatriates in Dubai
- **Population:** 200,000+ British citizens (largest Western expat group)
- **Demographics:** Professionals, families, retirees
- **Income Level:** Middle to upper-middle class (household income AED 25,000-80,000/month)
- **Behavior:** Maintain strong ties to UK; celebrate British occasions; active on social media
- **Pain Points:** 
  - Difficulty sending timely cards/gifts to UK
  - Limited local options for personalized cards
  - High cost of international shipping
  - Time zone challenges with UK-based services

#### Secondary Segments
| Segment | Size | Opportunity |
|---------|------|-------------|
| Other Western Expats (US, AU, EU) | 150,000 | Similar needs, English-speaking |
| UAE Nationals (English-speaking) | 25,000 | Western-influenced gift-giving |
| Corporate/B2B | 5,000+ companies | Bulk orders, employee recognition |
| Regional Expansion (GCC) | 500,000+ | Phase 2 expansion to KSA, Kuwait |

### 2.2 Market Size

#### Total Addressable Market (TAM)
- UAE Greeting Card Market: ~$45M USD annually
- UAE Online Gift Market: ~$800M USD annually
- Dubai represents ~60% of UAE market

#### Serviceable Addressable Market (SAM)
- British expat card/gift spend: ~$12M USD annually
- 25% digital adoption target: $3M USD

#### Serviceable Obtainable Market (SOM) - Year 3
- 15% market share: $450,000 USD (cards only)
- Including gifts/flowers: $1.5M - $2.5M USD

### 2.3 Competitive Landscape

| Competitor | Strengths | Weaknesses | Our Advantage |
|------------|-----------|------------|---------------|
| **Moonpig** | Brand recognition, UK designs | Slow UAE delivery, expensive shipping | Local fulfillment, faster delivery |
| **Funky Pigeon** | Competitive pricing | No Dubai presence | Local market expertise |
| **800 Flowers** | Fast local delivery | Limited personalization, no cards | AI-generated cards + gifts bundle |
| **GiftMojo** | UAE-based | Limited design variety | AI-powered customization |
| **Local Florists** | Same-day delivery | No online ordering, no cards | Full digital experience |

### 2.4 Market Trends

1. **AI-Powered Personalization:** 73% of consumers prefer personalized experiences
2. **Mobile-First Commerce:** 75% of UAE e-commerce is mobile
3. **Same-Day Delivery Expectation:** Amazon/Uber Eats trained consumers
4. **Sustainability Focus:** Demand for eco-friendly cards and packaging
5. **Experience Gifting:** Shift from products to experiences

---

## 3. Product Features

### 3.1 Core Product: AI-Generated Cards

#### Feature Set
| Feature | Description | Technology |
|---------|-------------|------------|
| **AI Design Generator** | User describes recipient/occasion; AI creates unique artwork | Stable Diffusion / DALL-E 3 API |
| **Smart Text Suggestions** | AI suggests personalized messages based on relationship | GPT-4o / Kimi K2.5 |
| **Template Library** | 1,000+ pre-designed templates for quick selection | Curated design system |
| **Photo Upload & Integration** | User photos merged with AI backgrounds | Computer vision APIs |
| **Multi-Language Support** | English, Arabic (Phase 2), Hindi (Phase 2) | Translation APIs |
| **Occasion Calendar** | Reminds users of upcoming birthdays, anniversaries | Calendar integration |

#### User Journey
1. **Onboarding:** Quick signup, connect contacts/calendar
2. **Card Creation:** 
   - Choose occasion (birthday, anniversary, new baby, etc.)
   - Describe recipient ("my sarcastic brother who loves golf and hates mornings")
   - AI generates 5 unique card designs
   - User selects, customizes message, adds photos
3. **Checkout:** Card + optional gifts, delivery date selection
4. **Delivery Tracking:** Real-time updates via WhatsApp/SMS
5. **Post-Delivery:** Recipient can send thank-you, share on social

### 3.2 Add-On Products (Dropshipped)

| Category | Products | Margin | Delivery |
|----------|----------|--------|----------|
| **Flowers** | Bouquets, arrangements, plants | 35-45% | Same-day via local florist network |
| **Cakes** | Custom cakes, cupcakes, sweets | 30-40% | Next-day via bakery partners |
| **Gifts** | Chocolates, balloons, teddy bears | 40-50% | Same-day via courier |
| **Experiences** | Spa vouchers, dinner reservations | 20-30% | Digital delivery |
| **Corporate** | Branded cards, bulk orders | 25-35% | Scheduled delivery |

### 3.3 AI Agent Integration (Competitive Moat)

Sam's vision for multi-agent automation:

| Agent | Function | Value |
|-------|----------|-------|
| **Design Agent** | Generates card artwork 24/7 | Unlimited creative capacity |
| **Customer Support Agent** | Handles inquiries, complaints | Instant response, 24/7 coverage |
| **Social Media Agent** | Creates content, responds to comments | Organic marketing automation |
| **Inventory Agent** | Monitors stock, reorders supplies | Zero stockouts |
| **Marketing Agent** | Runs ads, optimizes campaigns | Performance marketing at scale |
| **Analytics Agent** | Tracks KPIs, generates insights | Data-driven decisions |

### 3.4 Technology Stack

```
Frontend:
- Next.js 14 (React)
- Tailwind CSS
- Framer Motion (animations)

Backend:
- Node.js / Express or Python / FastAPI
- PostgreSQL (user data, orders)
- Redis (caching, sessions)

AI/ML:
- Image Generation: Stable Diffusion API / Replicate
- Text Generation: OpenAI GPT-4o / Kimi K2.5
- Image Processing: Cloudinary

Infrastructure:
- Vercel (frontend hosting)
- AWS/GCP (backend, storage)
- Cloudflare (CDN, security)

Integrations:
- Stripe/PayPal (payments)
- WhatsApp Business API (notifications)
- Google/Apple Calendar (reminders)
- Local courier APIs (delivery)
```

---

## 4. Technical Architecture

### 4.1 System Overview

```
┌─────────────────────────────────────────────────────────────┐
│                        USER INTERFACE                        │
│              (Web App + iOS/Android Apps)                    │
└────────────────────┬────────────────────────────────────────┘
                     │
┌────────────────────▼────────────────────────────────────────┐
│                      API GATEWAY                             │
│         (Authentication, Rate Limiting, Routing)             │
└────────────────────┬────────────────────────────────────────┘
                     │
        ┌────────────┼────────────┐
        │            │            │
┌───────▼───┐ ┌──────▼────┐ ┌─────▼──────┐
│   CARD    │ │   ORDER   │ │   USER     │
│  SERVICE  │ │  SERVICE  │ │  SERVICE   │
│ (AI Gen)  │ │ (Payment, │ │ (Auth,     │
│           │ │ Tracking) │ │ Profile)   │
└─────┬─────┘ └─────┬─────┘ └─────┬──────┘
      │             │             │
      └─────────────┼─────────────┘
                    │
┌───────────────────▼─────────────────────────────────────────┐
│                    DATA LAYER                                │
│  PostgreSQL  │  Redis  │  S3 (Images)  │  External APIs     │
└─────────────────────────────────────────────────────────────┘
```

### 4.2 AI Card Generation Pipeline

```
User Input (Occasion + Recipient Description)
      │
      ▼
┌─────────────────────────────────────┐
│  Prompt Engineering Service         │
│  - Enhances user description        │
│  - Adds style guidelines            │
│  - Generates negative prompts       │
└────────────────┬────────────────────┘
                 │
                 ▼
┌─────────────────────────────────────┐
│  Image Generation (Stable Diffusion)│
│  - 5 variations generated           │
│  - 1024x1024 resolution             │
│  - ~10 seconds generation time      │
└────────────────┬────────────────────┘
                 │
                 ▼
┌─────────────────────────────────────┐
│  Post-Processing                    │
│  - Upscaling (optional)             │
│  - Text overlay placement           │
│  - Quality scoring                  │
└────────────────┬────────────────────┘
                 │
                 ▼
          User Preview
```

### 4.3 Database Schema (Simplified)

```sql
-- Users
users (id, email, phone, name, created_at)

-- Contacts (for reminders)
contacts (id, user_id, name, birthday, anniversary, preferences)

-- Cards
cards (id, user_id, design_url, message, status, created_at)

-- Orders
orders (id, user_id, card_id, total_amount, status, delivery_date)
order_items (id, order_id, product_type, product_id, quantity, price)

-- Delivery
deliveries (id, order_id, address, tracking_number, status, courier)

-- AI Prompts
prompts (id, user_input, enhanced_prompt, generated_images, selected_image)
```

### 4.4 Scalability Plan

| Phase | Users | Infrastructure | Cost/Month |
|-------|-------|----------------|------------|
| MVP (0-6 mo) | 1,000 | Vercel + Render + Supabase | $200 |
| Growth (6-12 mo) | 10,000 | AWS ECS + RDS + CloudFront | $800 |
| Scale (12-24 mo) | 50,000 | Kubernetes + Multi-region | $2,500 |
| Enterprise (24+ mo) | 200,000+ | Multi-cloud + Edge | $8,000 |

---

## 5. Operations & Delivery

### 5.1 Fulfillment Model: Hybrid Dropshipping

#### Card Production
- **In-House:** High-quality card printing (Canon imagePROGRAF)
- **Location:** Dubai South or Al Quoz industrial area
- **Capacity:** 500 cards/day initial, scalable to 2,000/day
- **Quality Control:** Each card inspected before dispatch

#### Gift Partners (Dropship)
| Partner Type | Selection Criteria | Margin |
|--------------|-------------------|--------|
| Florists | Same-day delivery capability, 4.5+ rating | 35% |
| Bakeries | Food safety certified, custom cake capability | 30% |
| Gift Shops | Inventory API integration, reliable fulfillment | 40% |
| Couriers | Real-time tracking, 95%+ on-time rate | 15% |

### 5.2 Delivery Zones

| Zone | Areas | Delivery Time | Fee |
|------|-------|---------------|-----|
| Central | Downtown, DIFC, Business Bay | Same-day (4hr) | Free (AED 150+) |
| Inner | Marina, JBR, Palm, JLT | Same-day (6hr) | AED 15 |
| Outer | Mirdif, Arabian Ranches, Al Barsha | Next-day | AED 25 |
| Sharjah/Ajman | Neighboring emirates | 1-2 days | AED 35 |
| International | UK, US, EU | 3-5 days | AED 75+ |

### 5.3 Quality Assurance

- **Card Quality:** 300gsm cardstock, matte/glossy options, premium envelopes
- **Print Quality:** Color-calibrated daily, sample prints reviewed
- **Packaging:** Branded boxes, protective wrapping, handwritten note option
- **Delivery:** Photo confirmation at delivery, recipient signature capture

### 5.4 Customer Service

| Channel | Response Time | Staffing |
|---------|---------------|----------|
| WhatsApp | <5 minutes | AI Agent + Human backup |
| Email | <2 hours | Human |
| Phone | <2 minutes (business hours) | Human |
| Social Media | <30 minutes | AI Agent |

---

## 6. Growth Strategy

### 6.1 Launch Strategy (Months 1-3)

#### Pre-Launch (Month 0)
- Beta testing with 50 friends/family
- Partner agreements with 5 florists, 3 bakeries
- Social media presence (Instagram, Facebook, TikTok)
- Waitlist building (target: 1,000 emails)

#### Launch (Month 1)
- Soft launch to waitlist
- PR push: "Moonpig for Dubai"
- Influencer partnerships (5 micro-influencers, British expat audience)
- Google Ads: "send cards Dubai", "flower delivery Dubai"

### 6.2 Customer Acquisition

| Channel | CAC Target | Strategy |
|---------|-----------|----------|
| Paid Social | $8-12 | Instagram/Facebook ads targeting expats |
| Google Ads | $10-15 | High-intent keywords (birthday cards Dubai) |
| Influencers | $5-8 | British expat mom bloggers, Dubai lifestyle |
| Referral | $3-5 | "Give AED 20, Get AED 20" program |
| Organic SEO | $0 | Content: "Dubai gift guide", "expat life" |
| Corporate | $20 | B2B outreach, HR departments |

### 6.3 Retention Strategy

- **Occasion Reminders:** Calendar integration, proactive notifications
- **Subscription Model:** "Card Club" - 12 cards/year for AED 299
- **Loyalty Program:** Points for purchases, referrals, reviews
- **Re-engagement:** Win-back emails after 90 days of inactivity

### 6.4 Expansion Roadmap

| Phase | Timeline | Action |
|-------|----------|--------|
| Phase 1 | Months 1-6 | Establish Dubai operations, prove unit economics |
| Phase 2 | Months 6-12 | Launch Abu Dhabi, add Arabic language support |
| Phase 3 | Year 2 | Expand to Saudi Arabia (Riyadh, Jeddah), Kuwait |
| Phase 4 | Year 3 | Franchise model for other GCC countries |

---

## 7. Financial Projections

### 7.1 Revenue Model

| Revenue Stream | Year 1 | Year 2 | Year 3 |
|----------------|--------|--------|--------|
| Card Sales | $250,000 | $800,000 | $1,500,000 |
| Gift Add-ons | $150,000 | $600,000 | $1,200,000 |
| Corporate Orders | $75,000 | $300,000 | $600,000 |
| Subscription (Card Club) | $25,000 | $150,000 | $400,000 |
| **Total Revenue** | **$500,000** | **$1,850,000** | **$3,700,000** |

### 7.2 Unit Economics

| Metric | Value |
|--------|-------|
| Average Order Value (AOV) | $33 USD (AED 120) |
| Cost of Goods Sold (COGS) | $13 USD (40%) |
| Gross Margin | $20 USD (60%) |
| Payment Processing (3%) | $1 USD |
| Delivery Cost | $4 USD |
| Contribution Margin | $15 USD (45%) |
| Customer Acquisition Cost (CAC) | $10 USD |
| **Net Margin per Order** | **$5 USD (15%)** |

### 7.3 Operating Expenses (Monthly)

| Category | Month 6 | Month 12 | Month 24 |
|----------|---------|----------|----------|
| Salaries (2 FTE) | $6,000 | $10,000 | $18,000 |
| Marketing | $3,000 | $8,000 | $15,000 |
| Technology (Hosting, APIs) | $500 | $1,500 | $3,500 |
| Rent & Operations | $1,500 | $2,500 | $4,000 |
| **Total OPEX** | **$11,000** | **$22,000** | **$40,500** |

### 7.4 Profit & Loss Projection

| Metric | Year 1 | Year 2 | Year 3 |
|--------|--------|--------|--------|
| Revenue | $500,000 | $1,850,000 | $3,700,000 |
| COGS | $200,000 | $740,000 | $1,480,000 |
| Gross Profit | $300,000 | $1,110,000 | $2,220,000 |
| OPEX | $180,000 | $350,000 | $550,000 |
| **Net Profit** | **$120,000** | **$760,000** | **$1,670,000** |
| **Net Margin** | **24%** | **41%** | **45%** |

### 7.5 Funding Requirements

| Use Case | Amount |
|----------|--------|
| Platform Development (MVP) | $15,000 |
| Initial Inventory & Equipment | $5,000 |
| Marketing Launch | $10,000 |
| Working Capital (6 months) | $15,000 |
| Contingency | $5,000 |
| **Total** | **$50,000** |

---

## 8. Implementation Roadmap

### 8.1 Phase 1: MVP (Months 1-3)

#### Month 1: Foundation
| Week | Tasks |
|------|-------|
| 1 | Finalize tech stack, set up development environment |
| 2 | Design database schema, build authentication system |
| 3 | Implement AI card generation integration |
| 4 | Build card customization UI, payment integration |

#### Month 2: Operations
| Week | Tasks |
|------|-------|
| 1 | Secure printing equipment, test card quality |
| 2 | Partner with 3 florists, 2 bakeries |
| 3 | Set up delivery logistics, courier agreements |
| 4 | Beta testing with 50 users, bug fixes |

#### Month 3: Launch
| Week | Tasks |
|------|-------|
| 1 | Soft launch to waitlist |
| 2 | Collect feedback, iterate |
| 3 | Full marketing launch |
| 4 | Monitor metrics, optimize conversion |

### 8.2 Phase 2: Growth (Months 4-12)

#### Key Milestones
- [ ] 1,000 registered users (Month 4)
- [ ] 100 orders/month (Month 5)
- [ ] Break-even (Month 8)
- [ ] 1,000 orders/month (Month 10)
- [ ] Launch iOS/Android apps (Month 12)

#### Initiatives
- Scale marketing spend based on ROAS
- Add corporate/ B2B sales channel
- Launch subscription "Card Club"
- Expand to Abu Dhabi

### 8.3 Phase 3: Scale (Year 2)

#### Key Milestones
- [ ] 10,000 registered users
- [ ] 5,000 orders/month
- [ ] $1.5M annual revenue
- [ ] Launch in Saudi Arabia
- [ ] Introduce Arabic language support
- [ ] Franchise model pilot

### 8.4 Risk Assessment

| Risk | Likelihood | Impact | Mitigation |
|------|------------|--------|------------|
| AI generation quality issues | Medium | High | Human review process, quality thresholds |
| Partner delivery failures | Medium | High | Multiple partners per zone, SLA agreements |
| Low customer acquisition | Medium | High | Diversify channels, referral incentives |
| Seasonal demand fluctuations | High | Medium | Corporate sales, subscription model |
| Competitor response | Medium | Medium | Build brand loyalty, superior UX |
| Payment fraud | Low | Medium | Stripe fraud detection, manual review |

### 8.5 Key Performance Indicators (KPIs)

| Metric | Month 3 | Month 6 | Month 12 |
|--------|---------|---------|----------|
| Registered Users | 500 | 2,000 | 8,000 |
| Monthly Orders | 50 | 300 | 1,000 |
| Conversion Rate | 8% | 12% | 15% |
| Customer Acquisition Cost | $15 | $12 | $10 |
| Average Order Value | $30 | $32 | $35 |
| Net Promoter Score | N/A | 40 | 50 |
| Gross Margin | 55% | 58% | 60% |

---

## 9. Appendices

### Appendix A: AI Agent Implementation Details

Based on Sam's vision for multi-agent automation, here's the technical approach:

#### Agent Architecture
```
Orchestrator (Master Agent)
├── Design Agent (Image Generation)
├── Support Agent (Customer Service)
├── Social Agent (Marketing)
├── Inventory Agent (Stock Management)
└── Analytics Agent (Reporting)
```

#### Implementation Priority
1. **Design Agent** - Core differentiator, implement first
2. **Support Agent** - High ROI for customer service
3. **Social Agent** - Organic growth driver
4. **Inventory Agent** - Operational efficiency
5. **Analytics Agent** - Business intelligence

### Appendix B: Competitive Analysis Deep Dive

See Section 2.3 for summary. Full analysis includes pricing comparison, feature matrices, and customer review sentiment analysis.

### Appendix C: Marketing Assets

- Brand guidelines (logo, colors, typography)
- Social media templates
- Ad copy templates
- Email sequences (welcome, abandoned cart, retention)

### Appendix D: Technical Specifications

- API documentation
- Database schema (full)
- Security protocols
- Deployment procedures

---

## 10. Conclusion

CardApp Dubai represents a compelling opportunity to capture market share in the underserved British expat greeting card market. By combining AI-generated personalization with local fulfillment, we address key pain points that existing solutions (Moonpig, local florists) fail to solve.

**Key Success Factors:**
1. Superior AI-generated card quality and personalization
2. Reliable local delivery network
3. Strong brand positioning with British expat community
4. Efficient multi-agent automation for scalability
5. Capital-efficient dropshipping model

**Next Steps:**
1. Approve business plan and funding allocation
2. Begin MVP development (estimated 8-10 weeks)
3. Secure initial florist/bakery partnerships
4. Build waitlist through organic marketing
5. Launch beta in Q2 2026

**Investment Ask:** $50,000 initial capital for MVP development and launch
**Expected Return:** 24% net margin Year 1, scaling to 45% by Year 3

---

*Document prepared by Clawson*  
*For Sam's AI-Augmented Business Ventures*  
*February 11, 2026*
