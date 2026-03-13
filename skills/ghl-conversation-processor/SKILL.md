---
name: ghl-conversation-processor
description: Process incoming GoHighLevel webhook payloads, draft concise follow-up replies, and post internal comments back to GHL.
---

# GHL Conversation Processor

Process customer updates from GHL webhooks and prepare a high-quality follow-up response.

## Workflow

### 1. Receive Webhook Payload

Expected flat webhook fields include:

```json
{
  "Message": "Customer message body or blank",
  "When required": "When possible",
  "Job Size": "Average",
  "contact_id": "abc123",
  "full_name": "Customer Name",
  "email": "customer@example.com",
  "tags": "",
  "date_created": "2026-01-03T07:28:43.806Z",
  "contact_source": "Epoxy",
  "full_address": ""
}
```

### 2. Extract Lead Information

Parse the payload to extract:

- `full_name`
- `email`
- `contact_id`
- `Message`
- `When required`
- `Job Size`
- `contact_source`
- `date_created`
- `full_address`

### 3. Draft Context-Aware Reply

Draft a concise response suitable for an internal handoff or operator review.

Reply structure:

- Greeting with customer name
- One-line summary of understood request
- 2 to 3 clarifying questions only when needed
- Clear next step and call to action

### 4. Prepare Internal Comment Payload

Use this GHL payload shape:

```json
{
  "contactId": "{contact_id}",
  "type": "InternalComment",
  "status": "delivered",
  "message": "INTERNAL NOTE\n\nDraft reply for {full_name} ({contact_id})\n\nCustomer message:\n{Message}\n\nDraft reply:\n{draft_reply}"
}
```

### 5. Missing Conversation ID Fallback

When `conversationId` is missing:

- First attempt contact-based conversation lookup in the hook transform.
- If lookup succeeds, use `conversationId` as matched-thread context only.
- Internal comment posting still uses `contact_id` as `contactId`.
- If the webhook does not contain a usable `contact_id`, do not post.

### 6. Error Handling

If API call fails:

- Capture status code and response body.
- Return the draft reply so work is not blocked.
- Include a one-line retry recommendation.

### 7. Required Postback Execution

After preparing `internalComment`, you MUST execute:

```text
/usr/bin/python3 /home/alex/.openclaw/workspace/skills/ghl-conversation-processor/scripts/post_ghl_comment.py --contact-id {contact_id} --message "{internalComment}"
```

Rules:

- Set `postResult=posted` only if command succeeds and API response is success.
- If command fails, set `postResult=failed` and include stderr or API response in `postError`.
- Do not claim missing token or config unless command output proves it.

## Output Contract

Always return:

1. `lead`
2. `draftReply`
3. `internalComment`
4. `postResult`: `posted`, `skipped_missing_contact_id`, or `failed`
5. `postError` when `postResult=failed`