---
id: 7620
date: 2026-04-13T21:37:39+00:00
author: Gapertons-Tech-Corner
author_handle: @gaperton_tech
reply_to: 695
reply_quote: И пишут что у крестьян с 16GB VRAM тоже заработает, если есть много обычной RAM. Проверим. Не верится что-то.
---

Best practice (2025–2026):Set --n-gpu-layers 999 (offload all layers/blocks to GPU as the base). 
Offload routed experts to CPU using one of these:--ot "exps=CPU" or --cpu-moe (simple global expert offload). 
--n-cpu-moe N (offload experts from the last N layers to CPU; start low and increase until it fits or performance peaks). 
Or targeted: --ot "blk\.(25|37|...)\.ffn_.*_exps\.weight=CPU" for specific blocks. 
 Keep attention, dense FFN, and shared experts on GPU for best speed. 
 
This hybrid approach lets you run huge MoE models (100B+ active params) on consumer GPUs (e.g., 8–24 GB VRAM) while maintaining usable speeds (10–40+ t/s depending on hardware). Offloading only experts minimizes slowdown because experts are sparsely activated.