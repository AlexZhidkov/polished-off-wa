# VM Deployment

This repository intentionally excludes secrets. Set these on the VM separately:

- `GHL_API_TOKEN`
- `GHL_LOCATION_ID`
- webhook token for `hooks.token`

## Files to deploy

- `hooks/transforms/ghl-conversation-update.mjs`
- `skills/ghl-conversation-processor/SKILL.md`
- `skills/ghl-conversation-processor/scripts/post_ghl_comment.py`
- `skills/ghl-conversation-processor/references/ghl_api.md`

## Python dependency

Use `/usr/bin/python3` on Ubuntu and ensure `requests` is available.

```bash
sudo apt-get install -y python3-requests
```

## Post-deploy smoke test

```bash
/usr/bin/python3 /home/alex/.openclaw/workspace/skills/ghl-conversation-processor/scripts/post_ghl_comment.py \
  --api-token "$GHL_API_TOKEN" \
  --contact-id CONTACT_ID \
  --message "OpenClaw deploy smoke test"
```

## Runtime verification

After a real webhook, confirm the session shows an exec call for the post script:

```bash
find ~/.openclaw/agents -path '*/sessions/*.jsonl' -mmin -10 -type f -print0 | \
xargs -0 rg -n 'post_ghl_comment.py|toolName":"exec"|postResult|postError|failed|error'
```
