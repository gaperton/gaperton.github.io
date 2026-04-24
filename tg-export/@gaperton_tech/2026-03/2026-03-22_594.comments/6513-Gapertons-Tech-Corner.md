---
id: 6513
date: 2026-03-23T03:17:22+00:00
author: Gapertons-Tech-Corner
author_handle: @gaperton_tech
---

print_info: is_swa_any            = 0
print_info: n_embd_head_k         = 256
print_info: n_embd_head_v         = 256
print_info: n_gqa                 = 6
print_info: n_embd_k_gqa          = 1024
print_info: n_embd_v_gqa          = 1024
print_info: f_norm_eps            = 0.0e+00
print_info: f_norm_rms_eps        = 1.0e-06
print_info: f_clamp_kqv           = 0.0e+00
print_info: f_max_alibi_bias      = 0.0e+00
print_info: f_logit_scale         = 0.0e+00
print_info: f_attn_scale          = 0.0e+00
print_info: n_ff                  = 17408
print_info: n_expert              = 0
print_info: n_expert_used         = 0
print_info: n_expert_groups       = 0
print_info: n_group_used          = 0
print_info: causal attn           = 1
print_info: pooling type          = 0
print_info: rope type             = 40
print_info: rope scaling          = linear
print_info: freq_base_train       = 10000000.0
print_info: freq_scale_train      = 1
print_info: n_ctx_orig_yarn       = 262144
print_info: rope_yarn_log_mul     = 0.0000
print_info: rope_finetuned        = unknown
print_info: mrope sections        = [11, 11, 10, 0]
print_info: ssm_d_conv            = 4
print_info: ssm_d_inner           = 6144
print_info: ssm_d_state           = 128
print_info: ssm_dt_rank           = 48
print_info: ssm_n_group           = 16
print_info: ssm_dt_b_c_rms        = 0
print_info: model type            = 27B
print_info: model params          = 26.90 B
print_info: general.name          = Qwen3.5-27B
print_info: vocab type            = BPE
print_info: n_vocab               = 248320
print_info: n_merges              = 247587
print_info: BOS token             = 11 ','
print_info: EOS token             = 248046 '<|im_end|>'
print_info: EOT token             = 248046 '<|im_end|>'
print_info: PAD token             = 248055 '<|vision_pad|>'
print_info: LF token              = 198 'Ċ'
print_info: FIM PRE token         = 248060 '<|fim_prefix|>'
print_info: FIM SUF token         = 248062 '<|fim_suffix|>'
print_info: FIM MID token         = 248061 '<|fim_middle|>'
print_info: FIM PAD token         = 248063 '<|fim_pad|>'
print_info: FIM REP token         = 248064 '<|repo_name|>'
print_info: FIM SEP token         = 248065 '<|file_sep|>'
print_info: EOG token             = 248044 '<|endoftext|>'
print_info: EOG token             = 248046 '<|im_end|>'
print_info: EOG token             = 248063 '<|fim_pad|>'
print_info: EOG token             = 248064 '<|repo_name|>'
print_info: EOG token             = 248065 '<|file_sep|>'
print_info: max token length      = 256
load_tensors: loading model tensors, this can take a while... (mmap = false, direct_io = false)
load_tensors: offloading output layer to GPU
load_tensors: offloading 63 repeating layers to GPU
load_tensors: offloaded 65/65 layers to GPU
load_tensors:      Vulkan0 model buffer size = 18392.73 MiB
load_tensors:  Vulkan_Host model buffer size =   833.59 MiB
............................................................................................
common_init_result: added <|endoftext|> logit bias = -inf
common_init_result: added <|im_end|> logit bias = -inf
common_init_result: added <|fim_pad|> logit bias = -inf
common_init_result: added <|repo_name|> logit bias = -inf
common_init_result: added <|file_sep|> logit bias = -inf
llama_context: constructing llama_context
llama_context: n_seq_max     = 1
llama_context: n_ctx         = 177152
llama_context: n_ctx_seq     = 177152
llama_context: n_batch       = 2048
llama_context: n_ubatch      = 512
llama_context: causal_attn   = 1
llama_context: flash_attn    = enabled
llama_context: kv_unified    = false
llama_context: freq_base     = 10000000.0
llama_context: freq_scale    = 1
llama_context: n_ctx_seq (177152) < n_ctx_train (262144) -- the full capacity of the model will not be utilized
llama_context: Vulkan_Host  output buffer size =     0.95 MiB
llama_kv_cache:    Vulkan0 KV buffer size = 11072.00 MiB
llama_kv_cache: size = 11072.00 MiB (177152 cells,  16 layers,  1/1 seqs), K (f16): 5536.00 MiB, V (f16): 5536.00 MiB