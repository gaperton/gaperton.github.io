---
id: 7121
date: 2026-04-04T19:11:20+00:00
author: Valéry-Pavlovitch
author_handle: @Valeriy_Pavlovich
---

• Провёл deep research + live-прогоны, итог: блокер подтверждён и сейчас это не “неправильные флаги”, а лимит/совместимость для Qwen3.5-27B на текущем single-GPU
  профиле.

  - Upstream подтверждает класс проблем вокруг GDN/Triton для Qwen3.5 и недавние фиксы в vLLM:
      - issue #36598, PR #36599, PR #38343, release v0.19.0.
  - На хосте уже стоит vLLM 0.19.0 (проверено в runtime-venv /data/iqdoctor/llm-serving/.venv).
  - Контрольные запуски Qwen/Qwen3.5-27B-GPTQ-Int4 с official флагами (--quantization moe_wna16 --language-model-only --reasoning-parser qwen3 --enforce-eager) и
    несколькими envelope (gpu_memory_utilization=0.90/0.80/0.75, max_model_len=2048/1024, плюс --cpu-offload-gb 10) все падают до /health с CUDA OOM при
    инициализации модели (дефицит ~170–340 MiB).

Источники:

  - https://github.com/vllm-project/vllm/issues/36598
  - https://github.com/vllm-project/vllm/pull/36599
  - https://github.com/vllm-project/vllm/pull/38343
  - https://github.com/vllm-project/vllm/releases
  - https://huggingface.co/Qwen/Qwen3.5-27B-GPTQ-Int4

**❔** **Что я делаю не так?**

GeForce RTX 5090, 32 GB GDDR7