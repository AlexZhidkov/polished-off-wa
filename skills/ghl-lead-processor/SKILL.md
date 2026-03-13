---
name: ghl-lead-processor
description: Process GoHighLevel (GHL) webhook leads from Facebook Epoxy Forms. Extracts lead data, drafts professional email responses using the epoxy-enquiry-processor skill, and sends drafts to info@polishedoffwa.com for review.
metadata: {"clawdbot":{"emoji":"📥","os":["linux","darwin","win32"]}}
---

# GHL Lead Processor

## Overview

Process incoming GoHighLevel (GHL) webhook notifications for Facebook Epoxy Form submissions. Extracts lead contact information and project details, then drafts professional email responses for Val to review.

## When to Use This Skill

Use when receiving webhook notifications from GHL with:
- `PROCESS_GHL_LEAD` events
- Facebook Epoxy Form submissions
- New lead data from Facebook ads/forms

## Webhook Payload Structure

Expected GHL webhook payload format:

```json
{
  "type": "PROCESS_GHL_LEAD",
  "source": "facebook_epoxy_form",
  "lead": {
    "id": "string",
    "firstName": "string",
    "lastName": "string",
    "email": "string",
    "phone": "string",
    "address": "string",
    "city": "string",
    "state": "string",
    "postalCode": "string",
    "customFields": {
      "area_size": "string",
      "project_type": "string",
      "timeframe": "string",
      "finish_preference": "string",
      "additional_notes": "string"
    }
  },
  "timestamp": "ISO-8601 timestamp"
}
```

## Processing Steps

### 1. Extract Lead Data

Parse the webhook payload and extract:
- **Contact Info:** Name, email, phone
- **Location:** Address, suburb
- **Project Details:** Area size, type, timeframe, finish preference
- **Notes:** Any additional information

### 2. Validate Required Fields

Minimum required for processing:
- First name (or full name)
- Email OR phone (at least one contact method)

If missing critical fields, log error and skip.

### 3. Draft Email Response

Use the **epoxy-enquiry-processor** skill approach:

**Category:** Client Enquiry – Epoxy Flooring (GHL Lead)  
**Risk Level:** Low-Medium

### 4. Send Draft to info@polishedoffwa.com

Use the gog skill to send email:

**To:** info@polishedoffwa.com  
**Subject:** `DRAFT: Follow up Facebook Epoxy lead - [Lead Name]`  

**Email Format:**

```
**DRAFT RESPONSE**

[Category: Client Enquiry – Epoxy Flooring (GHL Lead)]
[Risk Level: Low-Medium]

Hi [First Name],

Thanks for your enquiry about epoxy flooring through our Facebook form.

To give you an accurate quote, could you let me know:

1. What type of finish interests you? (solid colour, flake system, or unsure)
2. Total area in m²?
3. Location/suburb?
4. When do you need the work done?

In the meantime, here's a quick overview of our epoxy options:

**Solid Colour Epoxy** – From $50 + GST per m²
Our most popular garage finish. Clean, seamless, durable.

**Flake System** – From $60 + GST per m²  
Modern architectural look, hides imperfections, easy to maintain.

**Outdoor Epoxy** – From $70 + GST per m²
UV-stable with slip-resistant texture.

If you have any photos of the area, that would help with accurate assessment.

Regards,
Val
Polished Off WA
0484 606 555

---

**NOTES**

- GHL Lead ID: [lead.id]
- Source: Facebook Epoxy Form
- Received: [timestamp]
- Contact: [email] | [phone]
- Address: [full address if available]
- Custom Fields: [project details from form]

---

**ORIGINAL LEAD DATA**

From: GHL Webhook
Date: [timestamp]
Lead ID: [lead.id]
Source: Facebook Epoxy Form

[Full JSON payload for reference]
```

## Error Handling

### Missing Payload
If webhook arrives with empty/missing payload:
- Log error with Job ID
- Do not attempt to draft response
- Note: "Payload missing — check GHL dashboard directly"

### Invalid Payload
If payload structure doesn't match expected format:
- Log error
- Attempt to extract any usable data
- Draft partial response if contact info available

### Email Send Failure
If gog send fails:
- Log error
- Retry once after 30 seconds
- If still failing, alert for manual processing

## Idempotency

Track processed leads by `lead.id` to prevent duplicate processing:
- Store processed IDs in `memory/ghl-processed-leads.json`
- Check against list before processing
- Retain IDs for 30 days

## Security

- Verify webhook authenticity if signature provided
- Log but do not store sensitive data long-term
- Redact full phone numbers in logs (show last 4 digits only)

## Integration with Other Skills

This skill leverages:
- **epoxy-enquiry-processor** – For response content and pricing
- **gog** – For sending draft emails via Gmail
- **email-templates** – For reusable template components

## File Locations

- Skill: `~/.openclaw/workspace/skills/ghl-lead-processor/`
- Processed leads log: `~/.openclaw/workspace/memory/ghl-processed-leads.json`
- Error log: `~/.openclaw/workspace/memory/ghl-lead-errors.log`
