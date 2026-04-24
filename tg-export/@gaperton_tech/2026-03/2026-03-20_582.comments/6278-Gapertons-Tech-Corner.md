---
id: 6278
date: 2026-03-20T08:16:39+00:00
author: Gapertons-Tech-Corner
author_handle: @gaperton_tech
---

В общем, нафиг lm studio.

1. llama.cpp vulkan, собирается из исходников
2. ставится llama-swap, пишется к нему конфиг с запуском моделей
3. модели обязательно кладутся на nvme.
4. делается пункт в grub загрузки без гуя
5. пишется в нем запуск llama-swap

???

Все, вот вам простой сервер.