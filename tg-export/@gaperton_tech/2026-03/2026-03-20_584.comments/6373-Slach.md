---
id: 6373
date: 2026-03-21T16:27:59+00:00
author: Slach
author_handle: @BloodJazMan
---

под llama.cpp 
10t/s generation, 500-1000t/s context parsing почему то плавает, надо еще vLLM и sglang проверить, но они блин глючат и не стабильные...

unsloth/Qwen3.5-27B - даже UD-Q4_K_XL

unsloth/Qwen3.5-35B-A10B - тоже плавает 1500-2500 prefill и 35-50 t/s генерация на тойже квантизации, но это более разреженая моделька

под vLLM удалось запустить https://huggingface.co/Qwen/Qwen3.5-27B-FP8
и получить прямо какие то магические 4000 prefill и 45-50 прегенерации, но она в памяти отжирает больше 64G с контектом в fp8 ;) а мне хочется еще ComfyUI паралельно погонять...