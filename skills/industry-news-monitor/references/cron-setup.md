# Cron Job Setup Guide

## Automated Weekly News Monitoring

### Create Cron Job

```bash
cron add \
  --name "weekly-concrete-industry-news" \
  --schedule "cron:0 6 * * SAT" \
  --tz "Australia/Perth" \
  --payload "agentTurn:Run industry-news-monitor skill to check for weekly news" \
  --session-target isolated \
  --delivery none
```

### Parameters

| Parameter | Value |
|-----------|-------|
| Name | `weekly-concrete-industry-news` |
| Schedule | `0 6 * * SAT` (6 AM Saturday) |
| Timezone | `Australia/Perth` |
| Session | `isolated` (runs in background) |

### What Happens

1. Every Saturday 6 AM AWST, cron triggers
2. Isolated session runs news monitoring
3. Searches web for past week's news
4. Categorizes by geography
5. Sends compiled email to info@polishedoffwa.com

### Manage Cron Job

**List jobs:**
```bash
cron list
```

**Pause job:**
```bash
cron update <job-id> --patch '{"enabled":false}'
```

**Resume job:**
```bash
cron update <job-id> --patch '{"enabled":true}'
```

**Delete job:**
```bash
cron remove <job-id>
```

### Manual Trigger

To run immediately (for testing):
```bash
cron run <job-id>
```
