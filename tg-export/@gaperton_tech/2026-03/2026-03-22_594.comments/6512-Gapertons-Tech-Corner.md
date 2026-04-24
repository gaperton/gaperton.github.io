---
id: 6512
date: 2026-03-23T03:17:22+00:00
author: Gapertons-Tech-Corner
author_handle: @gaperton_tech
reply_to: 6500
reply_quote: Запусти 'llama-server ... 2>&1 | tee 1.log'
---

llama_model_loader: - kv  21:                qwen35.attention.head_count u32              = 24
llama_model_loader: - kv  22:             qwen35.attention.head_count_kv u32              = 4
llama_model_loader: - kv  23:             qwen35.rope.dimension_sections arr[i32,4]       = [11, 11, 10, 0]
llama_model_loader: - kv  24:                      qwen35.rope.freq_base f32              = 10000000.000000
llama_model_loader: - kv  25:    qwen35.attention.layer_norm_rms_epsilon f32              = 0.000001
llama_model_loader: - kv  26:                qwen35.attention.key_length u32              = 256
llama_model_loader: - kv  27:              qwen35.attention.value_length u32              = 256
llama_model_loader: - kv  28:                     qwen35.ssm.conv_kernel u32              = 4
llama_model_loader: - kv  29:                      qwen35.ssm.state_size u32              = 128
llama_model_loader: - kv  30:                     qwen35.ssm.group_count u32              = 16
llama_model_loader: - kv  31:                  qwen35.ssm.time_step_rank u32              = 48
llama_model_loader: - kv  32:                      qwen35.ssm.inner_size u32              = 6144
llama_model_loader: - kv  33:             qwen35.full_attention_interval u32              = 4
llama_model_loader: - kv  34:                qwen35.rope.dimension_count u32              = 64
llama_model_loader: - kv  35:                       tokenizer.ggml.model str              = gpt2
llama_model_loader: - kv  36:                         tokenizer.ggml.pre str              = qwen35
llama_model_loader: - kv  37:                      tokenizer.ggml.tokens arr[str,248320]  = ["!", "\"", "#", "$", "%", "&", "'", ...
llama_model_loader: - kv  38:                  tokenizer.ggml.token_type arr[i32,248320]  = [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, ...
llama_model_loader: - kv  39:                      tokenizer.ggml.merges arr[str,247587]  = ["Ġ Ġ", "ĠĠ ĠĠ", "i n", "Ġ t",...
llama_model_loader: - kv  40:                tokenizer.ggml.eos_token_id u32              = 248046
llama_model_loader: - kv  41:            tokenizer.ggml.padding_token_id u32              = 248055
llama_model_loader: - kv  42:                    tokenizer.chat_template str              = {%- set image_count = namespace(value...
llama_model_loader: - kv  43:               general.quantization_version u32              = 2
llama_model_loader: - kv  44:                          general.file_type u32              = 17
llama_model_loader: - kv  45:                      quantize.imatrix.file str              = Qwen3.5-27B-GGUF/imatrix_unsloth.gguf
llama_model_loader: - kv  46:                   quantize.imatrix.dataset str              = unsloth_calibration_Qwen3.5-27B.txt
llama_model_loader: - kv  47:             quantize.imatrix.entries_count u32              = 496
llama_model_loader: - kv  48:              quantize.imatrix.chunks_count u32              = 80
llama_model_loader: - type  f32:  353 tensors
llama_model_loader: - type  f16:   96 tensors
llama_model_loader: - type q8_0:   48 tensors
llama_model_loader: - type q4_K:   16 tensors
llama_model_loader: - type q5_K:  181 tensors
llama_model_loader: - type q6_K:  157 tensors
print_info: file format = GGUF V3 (latest)
print_info: file type   = Q5_K - Medium
print_info: file size   = 18.78 GiB (6.00 BPW) 
load: 0 unused tokens
load: printing all EOG tokens:
load:   - 248044 ('<|endoftext|>')
load:   - 248046 ('<|im_end|>')
load:   - 248063 ('<|fim_pad|>')
load:   - 248064 ('<|repo_name|>')
load:   - 248065 ('<|file_sep|>')
load: special tokens cache size = 33
load: token to piece cache size = 1.7581 MB
print_info: arch                  = qwen35
print_info: vocab_only            = 0
print_info: no_alloc              = 0
print_info: n_ctx_train           = 262144
print_info: n_embd                = 5120
print_info: n_embd_inp            = 5120
print_info: n_layer               = 64
print_info: n_head                = 24
print_info: n_head_kv             = 4
print_info: n_rot                 = 64
print_info: n_swa                 = 0