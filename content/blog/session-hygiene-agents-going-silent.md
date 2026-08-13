---
title: "The Agents Did Not Get Worse. The Sessions Did."
description: "When long-running agents started going silent, the fix was not a smarter model. It was archiving bloated sessions and writing durable state to files."
date: 2026-08-13T09:20:00+02:00
lastmod: 2026-08-13T09:20:00+02:00
slug: "session-hygiene-agents-going-silent"
source_thread: "https://x.com/Ultramarine_963/status/2086360317576045025"
---

The phrase "the agents are going senile" was useful because it sounded exactly like the failure.

An agent would be fine for days. Then it would stop answering mentions. Sometimes its scheduled jobs still worked. Sometimes a delegated task would appear to finish but return no useful payload. The tempting explanation was model quality: maybe the local model was too small, maybe the prompt was too hard, maybe the agent was confused.

The real issue was uglier and more mechanical. The sessions were too big.

The source file for the fix is `/home/paul/.openclaw/workspaces/planner/shared-directives/session-hygiene.md`. Its first section says the top cause of "a crucial agent fails after a few days" is unbounded session growth. Agent sessions accumulate across days. Gateway auto-compaction was broken. A bloated session eventually overflows with the exact error `prompt too large for the model (precheck)`, or goes silent while cron/email paths still work.

The design doc behind it, `/home/paul/.openclaw/docs/agent-orchestration-reliability-design-2026-08-04.md`, captured the live failures on 2026-08-03/04:

- Architect spawned a subagent and `sessions_yield` returned no payload, so the turn ended with no file and no Discord post.
- Claw overflowed on `gpt-5.5` with `prompt too large for the model (precheck)`.
- An agent reported "no AI renders live" while five products still had AI renders.
- One agent's git operation wiped another agent's uncommitted file.

That list is uncomfortable, which is why it is useful. It moved the conversation away from vibes and into failure modes.

The first fix was a cron job: `/home/paul/.openclaw/cron/session-hygiene.py`, scheduled at 04:30 Berlin. The shared directive says it archives live sessions that are oversized, roughly above 1.5 MB, or older than about three days, excluding the active or locked one. The archive path is `agents/<id>/sessions/auto-archive/`. The point is not to preserve the chat forever. The point is to let the next turn start fresh.

That is a little counterintuitive if you are used to treating chat history as memory. In OpenClaw, the session is scratch. Durable state belongs in files: `memory/YYYY-MM-DD.md`, the second-brain vault, project state files, report files, and source-controlled docs. The session can disappear overnight and the system should still know what matters.

The second fix was behavioral. The directive tells agents not to pull large blobs into context. Full logs, giant pages, and multi-thousand-line outputs should be summarized or written to a file path. The running chat is not a data warehouse.

The third fix was monitoring. The same reliability design doc says the first dry run of the agent-failure monitor exposed 59 previously invisible failures. The shipped cron now runs every 30 minutes and alerts `#sentinel` on failed, timed-out, cancelled, and empty-payload runs. It is listed in `/home/paul/.openclaw/cron/crontab-known-good.txt` right after the session-hygiene job.

The lesson I took from this is that reliability work often looks like cleaning, not intelligence.

Do not ask an agent to carry a week of raw context in its head. Do not paste every log into the chat. Do not trust a delegated return value without an artifact. Do write the conclusion to a file. Do let stale sessions be archived. Do make failure visible within an hour instead of days later.

The model did not need to become more magical. The operating environment needed to stop slowly poisoning the next turn.

Disclosure: OpenClaw agents help draft these posts. That is the point of the project. The standard is that every concrete claim survives a source-file check.
