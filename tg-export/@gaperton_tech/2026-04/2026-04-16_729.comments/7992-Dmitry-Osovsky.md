---
id: 7992
date: 2026-04-17T03:04:58+00:00
author: Dmitry-Osovsky
reply_to: 7991
reply_quote: Кароч попробуй сначала F16 контекст и Q5, а затем руками насовать экспертов в VRAM
---

да вот же это все щас с Q5 и F16 работает

.\llama-server -m f:\Qwen3.6-35B-A3B-UD-Q5_K_XL.gguf -ngl 99 -ot "exps=CPU" -c 131072 -np 1 -fa on --webui-mcp-proxy --host 0.0.0.0