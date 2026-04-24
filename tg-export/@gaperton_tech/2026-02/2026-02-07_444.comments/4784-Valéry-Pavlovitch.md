---
id: 4784
date: 2026-02-08T23:34:19+00:00
author: Valéry-Pavlovitch
author_handle: @Valeriy_Pavlovich
---

Я обычно AGENTS.md для проектов через codex cli пишу, точнее он пишет и это именно описание структуры и правил принятых repo, а не сам агент. 

туда я пихаю всякие Coding Conventions/Coding Principles, как все по папкам разложено, где логи, как билдить-тестить. Вряд ли это интересно: но [вот](https://github.com/strato-space/call/blob/main/AGENTS.md)

еcли брать непосредственно репо fast-agent:
https://github.com/evalstate/fast-agent/

то оно как бе агент-агностик и просто платформа для ваших агентов, т.е. не содержит агентов которых надо запускать. 

но содержит мини-примеры: 

``````---
type: agent
name: PMO-orchestrator
default: true
agents:
- NY-Project-Manager
- London-Project-Manager
max_parallel: 128
child_timeout_sec: 120
max_display_instances: 20
---
Get project updates from the New York and London project managers. Ask NY-Project-Manager three times about different projects: Anthropic, evalstate/fast-agent, and OpenAI, and London-Project-Manager for economics review. Return a brief, concise combined summary with clear city/time/topic labe```ls.```

типа таких

https://github.com/evalstate/fast-agent/tree/main/examples/workflows-md/agents_as_tools_extended

а в приватном репо мы стараемся project'а запускать, но он просто по cron и переписки/тикеты/транскрибации читает раз в сутки.