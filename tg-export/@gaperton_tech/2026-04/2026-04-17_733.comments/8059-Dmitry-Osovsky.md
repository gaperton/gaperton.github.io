---
id: 8059
date: 2026-04-17T14:29:46+00:00
author: Dmitry-Osovsky
reply_to: 8047
---

Вот смотри,
.\llama-server -m f:\Qwen3.6-35B-A3B-UD-Q5_K_XL.gguf -ngl 99 -ot "exps=CPU" -np 1 -fa on
(т.е. Q5 с полной точностью и дефолтовым 256K контекстом)

Говорит, что:
llama_params_fit_impl: projected to use 8216 MiB of device memory vs. 14801 MiB of free device memory

А на контекст 128K, думаю, что хватит и 8 гигов, и останется еще место для виндового гуя