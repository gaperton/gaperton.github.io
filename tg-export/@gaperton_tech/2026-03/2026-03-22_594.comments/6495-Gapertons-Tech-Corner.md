---
id: 6495
date: 2026-03-22T17:51:52+00:00
author: Gapertons-Tech-Corner
author_handle: @gaperton_tech
reply_to: 6491
---

У грока теория, что у тебя ллама пытается какие-то слои на встроенную графику положить. Поддержка у нее крива и сама она говно, из-за чего все тормозит.

llama.cpp's Vulkan backend enumerates all visible Vulkan devices at startup (Intel iGPU first in many cases due to how the loader prioritizes integrated graphics), and it can default to or partially fall back to the slower Intel one — especially on older Ivy Bridge hardware where the partial ANV driver might interfere with device selection. Even with the warning only printing once, parts of the workload (or the entire thing) can end up on the iGPU if selection fails silently. The Ivy Bridge Vulkan is incomplete/slow, so offloading there tanks performance — often to 40-60% (or worse) of what the R9700 should deliver.Other possible contributors:Partial offload (not all layers on GPU due to VRAM limits or bugs). 
Vulkan picking the wrong device index. 
Driver/Mesa version quirks (RADV on AMD side is strong for R9700 in 2026, but mixed setups can confuse it). 
No explicit device forcing.