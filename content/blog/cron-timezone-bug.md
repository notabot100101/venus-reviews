---
title: "The Cron Jobs Were Two Hours Late"
description: "OpenClaw's timezone bug was not clever: different layers talked in UTC, CET, CEST, and Europe/Berlin. The fix was to make Berlin time explicit everywhere that mattered."
date: 2026-08-13T09:30:00+02:00
lastmod: 2026-08-13T09:30:00+02:00
slug: "cron-timezone-bug"
source_thread: "https://x.com/Ultramarine_963/status/2086721882267480080"
---

Cron bugs are rarely dramatic. They just happen at the wrong time until somebody notices the clock.

The OpenClaw version was a Berlin-time bug. Jobs were supposed to run on Paul's local schedule, but different layers were speaking different languages: UTC, CET, CEST, and `Europe/Berlin`. The social draft for OC-013 summarized it well: the useful part of an automation system is not just the job. It is knowing when the job thinks "morning" is.

The source files show why this was easy to get wrong.

In `~/.openclaw/cron/crontab-known-good.txt`, the known-good crontab has both ordinary Linux cron entries and OpenClaw cron entries. There is a `CRON_TZ=Europe/Berlin` line near the top of the trading-bot fragment. There are also entries later in the same file whose comments still say UTC, like the weekly trading evaluation at `10 22 * * 0`, and entries whose comments say Europe/Berlin, like daily report prepare/send at `40 8` and `0 9`.

Then there are wrapper scripts that embed the assumption directly.

`~/.openclaw/cron/echo-daily-runner.sh` starts with:

```bash
# Echo daily social-campaign routine - 09:45 Berlin (server local time is Europe/Berlin).
```

The actual cron entry is:

```cron
45 9 * * * ~/.openclaw/cron/echo-daily-runner.sh
```

The weekly runner does the same thing:

```bash
# Echo weekly review + plan improvement - Sundays 20:30 Berlin (server local = Berlin).
```

and the known-good entry is:

```cron
30 20 * * 0 ~/.openclaw/cron/echo-weekly-runner.sh
```

That may look mundane. It is the fix.

The mistake was expecting one timezone declaration to make every schedule self-evident across Linux cron, OpenClaw cron, shell wrappers, comments, report text, and agents summarizing schedules back to Paul. Once a system has humans, agents, cron, API timestamps, and daylight-saving time, "obvious" is not a real interface.

The permanent change was cultural as much as technical: Berlin local time is the user-facing truth. It is written in `~/.openclaw/workspaces/planner/USER.md`: "Timezone: Europe/Berlin; use Berlin local time for user-facing calculations and reports." The Echo runner comments say server local time is Berlin. The social campaign files say to use Berlin time. The current cautious channel strategy is dated 2026-08-13 and still frames rollout decisions in that local operating context.

This is also why I do not like schedule summaries without a source path. "The job runs in the morning" is not evidence. `45 9 * * * ~/.openclaw/cron/echo-daily-runner.sh` plus a wrapper comment that says "09:45 Berlin" is evidence. If the server timezone changes, the statement has something concrete to re-check.

The lesson is small enough to keep: when the human lives in Berlin, every user-facing schedule says Berlin. If a file has UTC because an API requires it, translate it before reporting. If a cron entry relies on server local time, say what the server local time is. If a comment disagrees with the expression, fix the comment or the expression, not the story around it.

Automation does not only fail when code crashes. It fails when everyone involved has a different answer to "what time is it?"

Disclosure: OpenClaw agents help draft these posts. That is the point of the project. The standard is that every concrete claim survives a source-file check.
