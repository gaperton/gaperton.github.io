---
id: 6083
date: 2026-03-17T06:18:31+00:00
author: Gapertons-Tech-Corner
author_handle: @gaperton_tech
reply_to: 6057
---

# Qwen Benchmark Report
_Date: 2026-03-17_

---

## System Configuration

### Hardware

| component | details |
|---|---|
| CPU | AMD Ryzen 7 5700X (8-core) |
| Motherboard | ASUS ROG STRIX B450-I GAMING (Mini-ITX, AM4) |
| RAM | 64 GiB DDR4 |
| GPU | NVIDIA GeForce RTX 3090 24 GiB (GA102), 936 GB/s, max mem clock 9751 MHz |
| Storage | Samsung 970 EVO Plus 1TB NVMe |
| Display | Headless — no framebuffer attached |

### Software

| component | details |
|---|---|
| OS | Linux 6.8.0-106-generic |
| NVIDIA driver | 580.126.09 |
| CUDA | 13.0 (driver) / 12.0 (toolkit) |
| llama.cpp | build 9e2e2198b (8368) |

---

## Models Tested

| label | model | quant | size |
|---|---|---|---|
| unsl-27b | Qwen3.5-27B Q4_K_M | dense | 15.58 GiB |
| unsl-35b-xl | Qwen3.5-35B-A3B UD-Q4_K_XL | MoE (3B active) | 20.70 GiB |

Test parameters: ``-ngl 99 -fa 1 -r 5 -d 4096 -p 512 -n 512 -pg 512,12`8`

---

## Results

| model | pp512 @ d4096 (t/s) | tg512 @ d4096 (t/s) | pp512+tg128 @ d4096 (t/s) |
|---|---|---|---|
| unsl-27b | 1221 ± 16 | 38.84 ± 0.01 | 172 ± 0.1 |
| unsl-35b-xl | 2892 ± 9 | 129.1 ± 0.1 | 546 ± 1.4 |

---

## Key Findings

### 1. MoE wins decisively over dense

**- 2.4× faster prefi**ll (2892 vs 1221 t/s)
**- 3.3× faster generati**on (129 vs 38.8 t/s)

Despite the 35B label, the MoE model is faster than the dense 27B in every dimension.

### 2. Why MoE generation is so fast

Token generation is memory-bandwidth bound — each token requires loading model weights from VRAM. For a dense model, all weights are loaded every token. For a MoE model, only the active experts are loaded.

Qwen 35B-A3B activates ~3B parameters per token. At inference time, the GPU reads roughly 1.7 GiB of weights per token instead of the full 15.6 GiB of the dense 27B. This is why a nominally "35B" MoE model generates tokens faster than a 27B dense model.

### 3. KV cache quantization has no impact

Tested q4_0, q8_0, and f16 KV cache types. Differences were under 1.5% for prefill and unmeasurable for generation. KV cache bandwidth is negligible compared to weight bandwidth for these models**. f16 KV cache can be used free**ly (better quality, no speed cost).

### 4. Batch size has no impact

Teste`d `-b` 512` `and `-b` 2048`. Results were within noise (<0.2%). The GPU is compute-bound for prefill and bandwidth-bound for generation regardless of batch chunking at these sizes.

### 5. Comparison with community benchmarks

Community benchmarks for the 35B-A3B on an RTX 3090 Ti (1008 GB/s) using Q4_0 report tg128 ≈ 107 t/s at d0, and 94–98 t/s at d1024–d10240. Our tg512 @ d4096 = 129 t/s on a regular 3090 (936 GB/s) is still ~20% higher. Three factors explain thi**s:

- UD-Q4_K_XL **quant — Unsloth Dynamic applies mixed precision per layer, reducing average bytes loaded per token compared to uniform Q**4_0
- Newer llama.cpp **build — build 8368 vs 8155 in the closest community reference; MoE kernels have been actively optimi**zed
- Headless **setup — no display attached means no framebuffer consuming VRAM, no compositor competing for memory bandwidth, and no background GPU workload; community benchmarks are typically run on a desktop with a display

---

## Recommenda**tion

Use unsl-**35b-xl (Qwen3.5-35B-A3B UD-Q4_K_XL) for all workloads. It uses 5 GiB more VRAM than the dense 27B but is 2–3× faster in every metric. The MoE architecture makes it strictly better for single-user local inference.