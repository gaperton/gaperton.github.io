---
id: 7991
date: 2026-04-17T03:04:13+00:00
author: Gapertons-Tech-Corner
author_handle: @gaperton_tech
---

-cmoe, --cpu-moe keep all Mixture of Experts (MoE) weights in the CPU
(env: LLAMA_ARG_CPU_MOE)

-ncmoe, --n-cpu-moe N keep the Mixture of Experts (MoE) weights of the first N layers in the CPU
(env: LLAMA_ARG_N_CPU_MOE)

Кароч попробуй сначала F16 контекст и Q5, а затем руками насовать экспертов в VRAM. Быстрее может стать.