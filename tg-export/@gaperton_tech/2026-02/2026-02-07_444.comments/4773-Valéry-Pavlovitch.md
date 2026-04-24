---
id: 4773
date: 2026-02-08T04:20:59+00:00
author: Valéry-Pavlovitch
author_handle: @Valeriy_Pavlovich
reply_to: 4771
---

Review notes for ``https://github.com/gaperton/openclaw/blob/system-prompts/docs/reference/templates/AGENTS.m`d` (preparing an issue):

- L146-L154: “Ask first before … any action that leaves the machine” conflicts with “Safe without asking: web research and calendar checks” (both leave the machine).
- L123-L129 vs L146-L148: “Commit and push your own changes” conflicts with “ask first before any action that leaves the machine” (push is an external side effect).
- L172-L177 vs L66-L70: “Stay silent (HEARTBEAT_OK) when …” mixes contexts`; `HEARTBEAT`_OK` is defined as a heartbeat-poll reply, not a generic group-chat “stay silent” behavior.
- L109-L121: “Reach out when … silent for over 8h” can conflict with “Quiet hours (23:00-08:00)” (9h); priority between rules isn’t defined.
- L13-L25: “First Run: complete BOOTSTRAP.md … remove it” isn’t ordered relative to “Every Session: do this before any other work” (what comes first on the first run is unclear).
- L15 vs L137-L140: “remove BOOTSTRAP.md” is a destructive action, but the destructive-actions section says to ask first; exception/clarification missing.
- L195 vs L144-L148: “Use voice (ElevenLabs TTS)” likely “leaves the machine” but isn’t reconciled with the approval rule.