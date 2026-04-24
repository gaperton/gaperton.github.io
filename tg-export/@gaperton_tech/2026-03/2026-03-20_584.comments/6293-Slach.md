---
id: 6293
date: 2026-03-20T15:57:17+00:00
author: Slach
author_handle: @BloodJazMan
---

вообще llama.cpp есть режим router
и вместо llama-swap он отлично работает
как apache 1.3 =) там форкается router и в него грузится модель, кол-во слотов регулируешь сам

все пресеты для моделей держишь в ini файле

примерно так
https://github.com/Slach/nvidia-spark/blob/main/llama.cpp.models.ini

https://github.com/Slach/nvidia-spark/blob/main/docker-compose.yaml#L116-L125