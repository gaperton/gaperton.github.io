---
id: 7694
date: 2026-04-15T01:36:35+00:00
author: Gapertons-Tech-Corner
author_handle: @gaperton_tech
reply_to: 7671
---

@drcha0s Если вот такую переменную среды дать то оно на 30% быстрее работает. И догоняет 3090. Хоть бы один пидор сказал.

RADV_DEBUG=nocompute ./llama.cpp/llama-bench -m models/Qwen3.5-35B-A3B-UD-Q5_K_XL.gguf -ngl 99 -fa 1 -p 512,1024,2048 -n 128 -r 2