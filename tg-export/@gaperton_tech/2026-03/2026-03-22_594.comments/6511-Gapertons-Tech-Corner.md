---
id: 6511
date: 2026-03-23T03:17:21+00:00
author: Gapertons-Tech-Corner
author_handle: @gaperton_tech
---

WARNING: radv is not a conformant Vulkan implementation, testing use only.
ggml_vulkan: Found 1 Vulkan devices:
ggml_vulkan: 0 = AMD Radeon Graphics (RADV GFX1201) (radv) | uma: 0 | fp16: 1 | bf16: 0 | warp size: 64 | shared memory: 65536 | int dot: 0 | matrix cores: KHR_coopmat
build: 8477 (ec2b787eb) with GNU 13.3.0 for Linux x86_64
system info: n_threads = 8, n_threads_batch = 8, total_threads = 16

system_info: n_threads = 8 (n_threads_batch = 8) / 16 | CPU : SSE3 = 1 | SSSE3 = 1 | AVX = 1 | AVX2 = 1 | F16C = 1 | FMA = 1 | BMI2 = 1 | LLAMAFILE = 1 | OPENMP = 1 | REPACK = 1 | 

init: using 15 threads for HTTP server
start: binding port with default address family
main: loading model
srv    load_model: loading model 'models/Qwen3.5-27B-UD-Q5_K_XL.gguf'
common_init_result: fitting params to device memory, for bugs during this step try to reproduce them with -fit off, or provide --verbose logs if the bug only occurs with -fit on
llama_params_fit_impl: projected to use 35754 MiB of device memory vs. 30733 MiB of free device memory
llama_params_fit_impl: cannot meet free memory target of 400 MiB, need to reduce device memory by 5420 MiB
llama_params_fit_impl: context size reduced from 262144 to 177152 -> need 5421 MiB less memory in total
llama_params_fit_impl: entire model can be fit by reducing context
llama_params_fit: successfully fit params to free device memory
llama_params_fit: fitting params to free memory took 0.70 seconds
llama_model_load_from_file_impl: using device Vulkan0 (AMD Radeon Graphics (RADV GFX1201)) (0000:09:00.0) - 30878 MiB free
llama_model_loader: loaded meta data with 49 key-value pairs and 851 tensors from models/Qwen3.5-27B-UD-Q5_K_XL.gguf (version GGUF V3 (latest))
llama_model_loader: Dumping metadata keys/values. Note: KV overrides do not apply in this output.
llama_model_loader: - kv   0:                       general.architecture str              = qwen35
llama_model_loader: - kv   1:                               general.type str              = model
llama_model_loader: - kv   2:                     general.sampling.top_k i32              = 20
llama_model_loader: - kv   3:                     general.sampling.top_p f32              = 0.950000
llama_model_loader: - kv   4:                      general.sampling.temp f32              = 0.600000
llama_model_loader: - kv   5:                               general.name str              = Qwen3.5-27B
llama_model_loader: - kv   6:                           general.basename str              = Qwen3.5-27B
llama_model_loader: - kv   7:                       general.quantized_by str              = Unsloth
llama_model_loader: - kv   8:                         general.size_label str              = 27B
llama_model_loader: - kv   9:                            general.license str              = apache-2.0
llama_model_loader: - kv  10:                       general.license.link str              = https://huggingface.co/Qwen/Qwen3.5-2...
llama_model_loader: - kv  11:                           general.repo_url str              = https://huggingface.co/unsloth
llama_model_loader: - kv  12:                   general.base_model.count u32              = 1
llama_model_loader: - kv  13:                  general.base_model.0.name str              = Qwen3.5 27B
llama_model_loader: - kv  14:          general.base_model.0.organization str              = Qwen
llama_model_loader: - kv  15:              general.base_model.0.repo_url str              = https://huggingface.co/Qwen/Qwen3.5-27B
llama_model_loader: - kv  16:                               general.tags arr[str,3]       = ["qwen3_5_moe", "unsloth", "image-tex...
llama_model_loader: - kv  17:                         qwen35.block_count u32              = 64
llama_model_loader: - kv  18:                      qwen35.context_length u32              = 262144
llama_model_loader: - kv  19:                    qwen35.embedding_length u32              = 5120
llama_model_loader: - kv  20:                 qwen35.feed_forward_length u32              = 17408