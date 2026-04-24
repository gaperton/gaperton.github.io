---
id: 6267
date: 2026-03-20T04:03:17+00:00
author: Gapertons-Tech-Corner
author_handle: @gaperton_tech
reply_to: 6265
---

llama.cpp Vulkan.

# Benchmark Report - Thu Mar 19 08:39:37 PM EDT 2026

## unsl-27b
| model                          |       size |     params | backend    | ngl | fa |            test |                  t/s |
| ------------------------------ | ---------: | ---------: | ---------- | --: | -: | --------------: | -------------------: |
| qwen35 27B Q4_K - Medium       |  15.58 GiB |    26.90 B | Vulkan     |  99 |  1 |   pp512 @ d4096 |        880.78 ± 1.94 |
| qwen35 27B Q4_K - Medium       |  15.58 GiB |    26.90 B | Vulkan     |  99 |  1 |   tg512 @ d4096 |         30.46 ± 0.06 |
| qwen35 27B Q4_K - Medium       |  15.58 GiB |    26.90 B | Vulkan     |  99 |  1 | pp512+tg128 @ d4096 |        132.71 ± 0.15 |

build: 811397745 (8422)

## unsl-35b-xl
| model                          |       size |     params | backend    | ngl | fa |            test |                  t/s |
| ------------------------------ | ---------: | ---------: | ---------- | --: | -: | --------------: | -------------------: |
| qwen35moe 35B.A3B Q4_K - Medium |  20.70 GiB |    34.66 B | Vulkan     |  99 |  1 |   pp512 @ d4096 |      2599.98 ± 16.05 |
| qwen35moe 35B.A3B Q4_K - Medium |  20.70 GiB |    34.66 B | Vulkan     |  99 |  1 |   tg512 @ d4096 |        107.24 ± 0.16 |
| qwen35moe 35B.A3B Q4_K - Medium |  20.70 GiB |    34.66 B | Vulkan     |  99 |  1 | pp512+tg128 @ d4096 |        452.98 ± 1.89 |

build: 811397745 (8422)