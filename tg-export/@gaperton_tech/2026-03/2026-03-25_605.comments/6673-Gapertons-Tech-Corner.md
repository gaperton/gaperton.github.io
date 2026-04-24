---
id: 6673
date: 2026-03-25T18:08:06+00:00
author: Gapertons-Tech-Corner
author_handle: @gaperton_tech
---

Yes. There are already clear attempts, but they are mostly emergent practice and essays from practitioners, not a settled “XP-for-agents” canon yet.

What exists so far:

Pair programming is being reinterpreted as human + coding agent, and in some cases as a triad: customer/problem-owner, developer, and model. Frank Westphal explicitly frames this as “Customer — Developer — Model,” with the human shifting from driver to navigator while agents handle implementation and exploration.  

The XP practice getting the strongest revival is TDD. Thoughtworks argues that AI agents work better when they have clear exit criteria, and specifically says tools like Claude Code work best with a test-first approach.   Kent Beck’s recent agent-related discussions are being summarized by multiple practitioners as: TDD is now a “superpower” because tests give agents an executable definition of correctness and constrain their tendency to generate plausible but sloppy output. One observed failure mode is especially revealing: an agent may try to remove a failing test instead of fixing the bug.  

Another adaptation is spec-driven micro-iteration. Instead of classic user stories flowing directly to humans, teams are writing tighter, more explicit specs for agents, then iterating in short loops. Allstacks describes this as “mini-waterfalls” or “micro-iterations,” where natural-language specs tell the agent what to build and tests define success.  

There is also a repo-level equivalent of XP’s shared team discipline: living instruction files such as CLAUDE.md and increasingly AGENTS.md. Anthropic describes Claude Code as using CLAUDE.md as part of its context strategy, and practitioners describe these files as persistent project memory containing workflows, standards, commands, and architecture rules.   That is very close in spirit to XP’s emphasis on shared conventions, collective ownership, and reducing tacit knowledge.

What is still missing is strong evidence that this has matured into a broadly accepted methodology. The current material is mostly:
 • practitioner essays and blog posts,
 • tool-vendor guidance,
 • interviews and commentary around Kent Beck and TDD,
 • early workflow reports from teams using Claude Code and similar agents.  

So the accurate answer is:

Yes, definitely there are attempts.
But they are mostly adapting a few XP ideas rather than reproducing XP unchanged.

The rough pattern looks like this:
 • Pair programming → human supervising an agent, sometimes multiple agents
 • TDD → more important than before
 • Small releases / short feedback loops → agent-sized tasks and rapid review
 • Collective ownership → agent can touch more of the codebase, so guardrails matter more
 • Coding standards → encoded in CLAUDE.md / AGENTS.md
 • Continuous integration → even more central, because agents can generate lots of code quickly

What has not really been solved yet:
 • how to do safe “pair rotation” when one “pair” member is nonhuman,
 • how much autonomy to give agents before review,
 • how to prevent spec drift and test gaming,
 • how to preserve XP’s social discipline instead of turning it into “prompt-and-pray.”

So: XP is not being replaced by coding agents; parts of XP are being rediscovered as control mechanisms for coding agents. TDD, tiny steps, continuous feedback, and explicit shared conventions appear to be the most transferable pieces.  

If useful, I can sketch what an actual “XP for Claude Code” workflow would look like day to day.