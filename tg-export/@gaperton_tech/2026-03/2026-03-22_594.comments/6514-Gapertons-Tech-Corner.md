---
id: 6514
date: 2026-03-23T03:17:22+00:00
author: Gapertons-Tech-Corner
author_handle: @gaperton_tech
---

llama_memory_recurrent:    Vulkan0 RS buffer size =   149.62 MiB
llama_memory_recurrent: size =  149.62 MiB (     1 cells,  64 layers,  1 seqs), R (f32):    5.62 MiB, S (f32):  144.00 MiB
sched_reserve: reserving ...
sched_reserve: resolving fused Gated Delta Net support:
sched_reserve: fused Gated Delta Net (autoregressive) enabled
sched_reserve: fused Gated Delta Net (chunked) enabled
sched_reserve:    Vulkan0 compute buffer size =   579.02 MiB
sched_reserve: Vulkan_Host compute buffer size =   366.03 MiB
sched_reserve: graph nodes  = 3657
sched_reserve: graph splits = 2
sched_reserve: reserve took 86.65 ms, sched copies = 1
common_init_from_params: warming up the model with an empty run - please wait ... (--no-warmup to disable)
srv    load_model: initializing slots, n_slots = 1
common_speculative_is_compat: the target context does not support partial sequence removal
srv    load_model: speculative decoding not supported by this context
slot   load_model: id  0 | task -1 | new slot, n_ctx = 177152
srv    load_model: prompt cache is enabled, size limit: 8192 MiB
srv    load_model: use ``--cache-ram` 0` to disable the prompt cache
srv    load_model: for more info see https://github.com/ggml-org/llama.cpp/pull/16391
init: chat template, example_format: '<|im_start|>system
You are a helpful assistant<|im_end|>
<|im_start|>user
Hello<|im_end|>
<|im_start|>assistant
Hi there<|im_end|>
<|im_start|>user
How are you?<|im_end|>
<|im_start|>assistant
<think>
'
srv          init: init: chat template, thinking = 1
main: model loaded
main: server is listening on http://127.0.0.1:5801
main: starting the main loop...
srv  update_slots: all slots are idle
srv  log_server_r: done request: GET / 127.0.0.1 200
srv    operator(): operator(): cleaning up before exit...
llama_memory_breakdown_print: | memory breakdown [MiB]                | total   free     self   model   context   compute    unaccounted |
llama_memory_breakdown_print: |   - Vulkan0 (Graphics (RADV GFX1201)) | 32624 =  640 + (30193 = 18392 +   11221 +     579) +        1789 |
llama_memory_breakdown_print: |   - Host                              |                  1199 =   833 +       0 +     366                |