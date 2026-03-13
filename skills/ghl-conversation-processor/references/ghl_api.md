# GHL Conversations API Reference

## Endpoint

`POST https://services.leadconnectorhq.com/conversations/messages`

## Headers

```text
Authorization: Bearer {GHL_API_TOKEN}
Content-Type: application/json
Version: 2021-04-15
```

## Internal Comment Payload

```json
{
  "contactId": "abc123",
  "type": "InternalComment",
  "status": "delivered",
  "message": "Internal note text"
}
```

## Notes

- `contactId` is required for internal comment creation.
- `conversationId` is useful for lookup and debugging context, but not sufficient on its own for this endpoint.
- The token must be a valid sub-account token with conversation write access.
