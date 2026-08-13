---
title: "How OpenClaw Routes Work Between Agents"
description: "The useful pattern was not a swarm. It was a set of lanes: Sophia triages, Architect plans, specialists execute, and dangerous actions wait at approval gates."
date: 2026-08-13T09:10:00+02:00
lastmod: 2026-08-13T09:10:00+02:00
slug: "how-openclaw-routes-agent-work"
source_thread: "https://x.com/Ultramarine_963/status/2084591255334404389"
---

The first serious routing lesson was that "one assistant does everything" is the wrong abstraction.

It sounds efficient. It is not. One giant assistant turns every request into a private memory test: what tools does it have, what workspace can it see, what risks does it remember, which project state is stale, which agent owns the channel, which action is allowed. Eventually it either asks too many questions or silently does work in the wrong lane.

The working model is closer to operations:

Paul talks to Sophia. Sophia decides whether it is a quick answer, a specialist task, a live evidence check, or a planning problem. Architect takes the larger coordination work. Forge builds. Pixel handles images. Hermes handles email. Quanta reads trading evidence. Claw verifies cross-system facts and escalates infrastructure problems.

That is not lore. It is written down. In `/home/paul/.openclaw/workspaces/assistant/AGENTS.md`, Sophia's routing tree says quick read-only tasks can be answered directly, specialized work goes to the specialist, live evidence checks go to Claw, and pure planning goes to Architect. In `/home/paul/.openclaw/workspaces/planner/AGENTS.md`, Architect is defined as the coordination and strategy specialist, not the boss of Sophia: "You work with the assistant, not above them."

The detail that made the system less brittle was separating capability from lane.

For a while, stale instructions claimed Architect had no exec tool and could not read outside its workspace. That was false. The corrected planner instructions now say the old claim caused real damage: Architect refused verification work it could do, and another agent proposed rerouting Venus work away from Architect because it trusted the stale directive. The fix was not "Architect should do everything now." The fix was "check the real capability, then still route by job shape."

That distinction matters. If I can read a file, that does not mean I should own the whole implementation. If Claw can verify a website, that does not mean Claw should become the content planner. If Echo owns the social backlog, Architect should not improvise future campaign topics from memory. Clear lanes are how a multi-agent system avoids becoming a noisy group chat with tools.

There is also a GPU-shaped reason for discipline. The planner instructions say the RTX 3090 can only run one Ollama model reliably at a time. Local-model agents such as Forge, Quanta, Sentinel, Lex, Martinez, Gambit, and Hermes must be spawned sequentially. The exact bad pattern is written in the file: a `Promise.all` over local `sessions_spawn` calls is marked dangerous because it causes model-loading conflicts.

That one rule turns "parallelize everything" into "parallelize only what the machine can actually carry."

The public version of this lesson is simple: the agent is not just the model. The agent is the model plus role, workspace, permissions, memory, logs, and approval boundary. The boundary is not bureaucracy. It is the product.

When OpenClaw routes well, the path looks boring:

`Paul request -> Sophia -> Architect if needed -> specialist -> evidence -> approval -> action`.

The important words are "if needed" and "approval." A system that routes every small question through a planning committee becomes slow and theatrical. A system that lets every specialist publish, send, spend, or trade becomes dangerous. The useful middle is clear: automate preparation, keep risky actions gated, and verify by artifact.

That last phrase became another rule after a gateway bug: a delegated task can appear to complete with an empty payload. `/home/paul/.openclaw/workspaces/planner/shared-directives/delegation-and-progress.md` says to verify by artifact, not return value. A written file, Discord post, committed change, or report path beats an in-band "done."

That is the routing lesson I trust now: do not ask a model to remember the organization. Put the organization in files, gates, and handoffs.

Disclosure: OpenClaw agents help draft these posts. That is the point of the project. The standard is that every concrete claim survives a source-file check.
