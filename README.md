# Polished Off WA OpenClaw Automation

This repository contains the Polished Off WA OpenClaw automation files.

Included:

- GHL webhook transform for conversation lookup
- GHL conversation processing skill
- Internal-comment postback script
- Sanitized OpenClaw hook config example
- Sanitized example webhook payload
- VM deployment notes
- Automated Gitleaks secret scanning via GitHub Actions

## Environment

Required environment variables:

- `GHL_API_TOKEN`
- `GHL_LOCATION_ID`

## Layout

- `hooks/transforms/ghl-conversation-update.mjs`
- `skills/ghl-conversation-processor/SKILL.md`
- `skills/ghl-conversation-processor/scripts/post_ghl_comment.py`
- `skills/ghl-conversation-processor/references/ghl_api.md`
- `config/openclaw.ghl.example.json`
- `examples/ghl-conversation-update.payload.json`
- `docs/deploy-vm.md`

## Notes

- The GHL message creation endpoint for internal notes uses `contactId`, `type: "InternalComment"`, `status: "delivered"`, and `message`.
- `conversationId` is still useful for lookup and debugging, but it is not the required key for the internal comment POST.
- There are currently no GHL-specific cron jobs included in this repository.

## Secret Scanning

This repository runs an automated Gitleaks scan on:

- Pull requests
- Pushes to `master`

The workflow is defined in `.github/workflows/gitleaks.yml` and uses the repo-level configuration in `.gitleaks.toml`.

To scan on every local commit as well, this repository includes `.pre-commit-config.yaml` with a Gitleaks hook.

Install it once per clone:

```bash
python3 -m pip install pre-commit
pre-commit install
```

Run it manually at any time with:

```bash
pre-commit run --all-files
```

If Gitleaks ever flags an intentional test value, prefer adding a narrow `gitleaks:allow` comment on that line or a specific ignore entry rather than weakening the global rules.
