---
id: 7060
date: 2026-04-04T15:42:58+00:00
author: Valéry-Pavlovitch
author_handle: @Valeriy_Pavlovich
---

любопытный проект для рефакторинга

https://github.com/peteromallet/desloppify

Desloppify gives your AI coding agent the tools to identify, understand, and systematically improve codebase quality. It combines mechanical detection (dead code, duplication, complexity) with subjective LLM review (naming, abstractions, module boundaries), then works through a prioritized fix loop. State persists across scans so it chips away over multiple sessions, and the scoring is designed to resist gaming.

The score gives your agent a north-star, and the tooling helps it plan, execute, and resolve issues until it hits your target — with a lot of tricks to keep it on track. A score above 98 should correlate with a codebase a seasoned engineer would call beautiful.