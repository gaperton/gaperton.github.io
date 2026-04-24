---
id: 6453
date: 2026-03-22T04:57:49+00:00
author: Slach
author_handle: @BloodJazMan
---

о, напоролся на баг с llama.cpp router

короче если модель меняется и --max-models=1 
то после выгрузки предыдущей модели иногда, не находит GPU =)
``````ggml_cuda_init: failed to initialize CUDA: no CUDA-capable device is detec```ted```

интересно на долго ли... и стоит ли это репортить...