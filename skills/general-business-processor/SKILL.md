---
name: general-business-processor
description: Process general business emails for Polished Off WA - supplier communications, staff issues, payment disputes, complaints, and legal matters. Use when receiving supplier emails, internal staff communications, payment issues, complaints, or any sensitive business correspondence requiring careful risk assessment.
---

# General Business Processor

Process supplier, staff, payment, complaint, and legal emails with appropriate risk assessment.

## Email Categories

| Category | Description | Risk Level |
|----------|-------------|------------|
| `supplier` | Materials, pricing, delivery | Low |
| `staff` | Internal team communication | Medium |
| `complaint` | Quality/issue complaint | **CRITICAL** |
| `payment` | Invoicing, payment disputes | **CRITICAL** |
| `legal` | Threats, legal language | **CRITICAL** |

## Workflow

### Step 1: Analyze

Read the email and identify:
- Category (from table above)
- Tone (friendly, neutral, aggressive, threatening)
- Risk indicators (see Risk Triggers below)
- Missing information needed to respond

### Step 2: Risk Assessment

**⚠️ HIGH-RISK TRIGGERS** — If ANY present, apply **Draft-Only Protocol**:

- Legal language or threats
- Demand for compensation
- Quality/damage disputes
- Payment disputes
- Aggressive or threatening tone
- Staff/supervisor conflicts

**Draft-Only Protocol:**
1. Label output: `⚠️ Review Carefully – Sensitive Matter`
2. Do NOT suggest auto-sending
3. Flag specific risks
4. Provide options, not recommendations

### Step 3: Draft Response

**Standard Structure:**
1. **Acknowledge** — Show you received and understood
2. **Core Response** — Answer the question/request
3. **Next Step** — Clear action item
4. **Professional Closing**

**Tone Guidelines:**
- Professional, direct, calm
- No emotional language
- No over-apologising
- No admitting liability

### Step 4: Output

Format:
```
**DRAFT RESPONSE**

[Category: <category>]
[Risk Level: <low|medium|high>]

---

[Draft email]

---

**Notes:** [Any warnings, missing info, or options to consider]
```

## Templates

See [references/business-templates.md](references/business-templates.md) for:
- Template 1: Supplier Communication
- Template 2: Timeline Update
- Template 3: Payment Follow-up
- Template 4: Complaint Response (High Risk)
- Template 5: Staff Communication

## Red Lines

**NEVER:**
- Admit liability
- Confirm compensation
- Agree to discounts without instruction
- Confirm variations without instruction
- Overpromise timelines
- Use emotional or defensive language

**ALWAYS:**
- Protect margin
- Protect reputation
- Protect optionality
- Provide clear next steps
- Flag high-risk items for review
