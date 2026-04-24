---
id: 7773
date: 2026-04-15T17:39:10+00:00
author: Gapertons-Tech-Corner
author_handle: @gaperton_tech
reply_to: 7771
---

И даже вот эту, она занимает немного меньше памяти, но все равно целиком не лезет к тебе в ГПУ.

https://huggingface.co/unsloth/gemma-4-26B-A4B-it-GGUF?show_file_info=gemma-4-26B-A4B-it-UD-Q4_K_XL.gguf

Дальше надо запустить llama-bench и дать ей флаги, чтобы она отгрузила часть экспертов moe в RAM.