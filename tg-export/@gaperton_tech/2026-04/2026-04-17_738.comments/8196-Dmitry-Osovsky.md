---
id: 8196
date: 2026-04-18T05:25:12+00:00
author: Dmitry-Osovsky
reply_to: 8194
---

Хм, походу под это дело отжирается VRAM. Раньше было вот так

``````llama_params_fit_impl: projected to use 27950 MiB of device memory vs. 14801 MiB of free device memory
llama_params_fit_impl: cannot meet free memory target of 1048 MiB, need to reduce device memory by 14197 MiB
llama_params_fit_impl: context size set by user to 131072 -> no change
llama_params_fit_impl: with only dense weights in device memory there is a total surplus of 8576``` MiB```
с этими параметрами ```стало
```llama_params_fit_impl: projected to use 31401 MiB of device memory vs. 14801 MiB of free device memory
llama_params_fit_impl: cannot meet free memory target of 2048 MiB, need to reduce device memory by 18648 MiB
llama_params_fit_impl: context size set by user to 131072 -> no change
llama_params_fit_impl: with only dense weights in device memory there is a total surplus of``` 4147 MiB```