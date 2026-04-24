---
id: 6496
date: 2026-03-22T17:52:41+00:00
author: Gapertons-Tech-Corner
author_handle: @gaperton_tech
reply_to: 6491
---

Best: Restrict Vulkan to only the AMD ICD (this hides the Intel one entirely, so no warning and no chance of fallback):Find the AMD ICD file (usually one of these; check your system): 
 ls /usr/share/vulkan/icd.d/ | grep -i amd 
 
or 
 ls /usr/share/vulkan/icd.d/ | grep radeon 
 
Common names: radeon_icd.x86_64.json, amd_pro_icd64.json, etc. (on workstation drivers it might be under AMD's paths). 
Then run: 
 export VK_ICD_FILENAMES=/usr/share/vulkan/icd.d/radeon_icd.x86_64.json  # adjust to your file
./llama-server -ngl 99 --verbose ...  # your usual flags 
 This is the cleanest fix — Vulkan loader only sees the R9700.