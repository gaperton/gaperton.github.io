---
id: 8063
date: 2026-04-17T14:38:22+00:00
author: Dmitry-Osovsky
---

Для ~~~~нищеброд~~ов~~ экономных пользователей, можно урезать квантизацию контекста до 8 бит, добавив заклинание --cache-type-k q8_0 --cache-type-v q8_0
и тогда получается вообще чудо

llama_params_fit_impl: projected to **use 3976 **MiB of device memory vs. 14801 MiB of free device memory

Меньше 4 гигов, Карл! Налетай, подешевело!