---
id: 6596
date: 2026-03-23T21:52:35+00:00
author: Yura-Sheliah
author_handle: @drcha0s
---

Спасибо.
Я сейчас вижу значимую разницу в только процессорах.
Ядро я перепроверил

``````< system info: n_threads = 4, n_threads_batch = 4, total_threads = 4
---
> system info: n_threads = 8, n_threads_batch = 8, total_threads = 16

< system_info: n_threads = 4 (n_threads_batch = 4) / 4 | CPU : SSE3 = 1 | SSSE3 = 1 | AVX = 1 | F16C = 1 | LLAMAFILE = 1 | OPENMP = 1 | REPACK = 1 | 
---
> system_info: n_threads = 8 (n_threads_batch = 8) / 16 | CPU : SSE3 = 1 | SSSE3 = 1 | AVX = 1 | AVX2 = 1 | F16C = 1 | FMA = 1 | BMI2 = 1 | LLAMAFILE = 1 | OPENMP = 1 | REPACK =``` 1 |```