---
id: 6750
date: 2026-03-29T00:54:59+00:00
author: Alexander-Luchkov
author_handle: @WatchTh15
---

Вроде вот так пока:

``````$ curl http://192.168.88.170:8080/v1/chat/completions   -H 'Content-Type: application/json'   -d '{
    "model": "qwen35-35b-q8",
    "messages": [
      {"role": "system", "content": "Ты полезный ассистент по software architecture."},
      {"role": "user", "content": "Как архитектор ПО, распиши процесс выбора версии Python для локального MCP-сервера. Сгенерируй всё в формате Markdown в ADR"}
    ],
    "temperature": 0.2,
    "max_tokens": 12000```
  }'``````

```[48563] slot print_timing: id  3 | task 6961 | 
[48563] prompt eval time =     214.84 ms /    57 tokens (    3.77 ms per token,   265.31 tokens per second)
[48563]        eval time =   67264.65 ms /  3013 tokens (   22.32 ms per token,    44.79 tokens per second)
[48563]       total time =   67479.49 ms /  3070 tokens
[48563] slot      release: id  3 | task 6961 | stop processing: n_tokens = 3069, trun```cated = 0```