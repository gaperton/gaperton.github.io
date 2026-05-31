# How to run a MoE model with llama.cpp on Windows

*A practical walkthrough on the example of an **RTX 5080 (16 GB)** running
**Qwen3.6‑35B‑A3B** from Unsloth at the **Q5\_K\_XL** quant.*

## The core idea: why MoE changes the math

A Mixture‑of‑Experts (MoE) model has a large *total* parameter count but only
activates a small slice per token. **Qwen3.6‑35B‑A3B** has **35 B total**
parameters but only **~3 B active** (`A3B`) on any given forward pass: a router
picks a handful of "expert" FFNs per layer and ignores the rest.

This is the trick that makes a 35 B model usable on a 16 GB card:

| Part of the model | Used per token? | Where it should live |
|---|---|---|
| Token embeddings, attention (Q/K/V/O), norms | **every token** | **GPU** |
| Shared expert / dense FFN (if present) | **every token** | **GPU** |
| Routed experts (the bulk of the weights) | only a few per token | **CPU / system RAM** |

The routed experts are most of the bytes but are touched sparingly, so parking
them in fast system RAM and computing only the active ones on the CPU costs
surprisingly little. The always‑active parts stay on the GPU where latency
matters most.

### The numbers for this example

- **GPU:** RTX 5080 — **16 GB GDDR7**, ~960 GB/s, PCIe 5.0.
- **Quant:** Unsloth dynamic `UD-Q5_K_XL` ≈ **26.6 GB** on disk.

26.6 GB of weights will **not** fit in 16 GB of VRAM. Without MoE offloading you
would be stuck at a ~Q3 quant or spilling everything to RAM and crawling. With
offloading you keep the hot path on the GPU and let ~10–13 GB of cold expert
weights sit in RAM, getting most of the speed of a fully‑resident model.

## Step 0 — NVIDIA driver and CUDA

Before anything else, the GPU side has to be set up.

**1. NVIDIA driver (mandatory).** RTX 50‑series (Blackwell) needs a recent
driver — install the latest **Game Ready** or **Studio** driver from
<https://www.nvidia.com/Download/index.aspx> (or via the NVIDIA App). The driver
ships its own CUDA runtime; check what it supports:

```powershell
nvidia-smi   # top-right shows the max "CUDA Version" this driver supports
```

For an RTX 5080 you want a driver advertising **CUDA 12.x or newer**.

**2. CUDA runtime**

**Prebuilt binaries** you do **not**
  need the full CUDA Toolkit. The llama.cpp release ships a matching
  `cudart-llama-bin-win-cuda-*.zip` with the runtime DLLs it needs — unzip it
  next to the exes (Step 1) and you're done. The driver above provides the rest.

## Step 1 — Get a CUDA build of llama.cpp for Windows

You do **not** need to compile anything. Grab a prebuilt CUDA binary:

1. Go to <https://github.com/ggml-org/llama.cpp/releases>.
2. Download the asset named like `llama-bXXXX-bin-win-cuda-x64.zip`
   (match it to your CUDA — the CUDA 12.x build is right for Blackwell/RTX 50xx).
3. Also download the matching `cudart-llama-bin-win-cuda-*.zip` and unzip it
   into the **same folder** so the CUDA runtime DLLs sit next to the exes.
4. Unzip somewhere like `C:\llama.cpp`.

You should now have `llama-server.exe`, `llama-cli.exe`, and `llama-bench.exe`.

Verify the GPU is seen:

```powershell
cd C:\llama.cpp
.\llama-cli.exe --version
nvidia-smi   # confirm the RTX 5080 and your driver/CUDA version
```

> **Blackwell note:** RTX 50‑series needs a recent driver and a CUDA 12.x (or
> newer) build. If the binary reports "no CUDA devices found", you grabbed a
> too‑old release or the CPU‑only zip — get a newer CUDA asset.

## Step 2 — Get the model

Download the GGUF by hand from the model's Hugging Face page, then point
llama.cpp at it with `-m`. Pick a drive with room — the Q5\_K\_XL file is ~27 GB.

On each model page, open the **Files and versions** tab, find the
**`UD-Q5_K_XL`** quant, and click the download arrow. Save it somewhere like
`D:\models\`.

Model pages (Unsloth dynamic GGUF) for three MoE models:

- **Gemma 4 26B‑A4B (MoE) — ~21.2 GB, single file** — needs **≥ 32 GB RAM**
  <https://huggingface.co/unsloth/gemma-4-26B-A4B-it-GGUF>
- **Qwen3.6 35B‑A3B (MoE) — ~26.6 GB, single file** — needs **≥ 32 GB RAM** *(this guide's example)*
  <https://huggingface.co/unsloth/Qwen3.6-35B-A3B-GGUF>
- **Qwen3.5 122B‑A10B (MoE) — ~92 GB, split into 3 parts** — needs **128 GB RAM**
  <https://huggingface.co/unsloth/Qwen3.5-122B-A10B-GGUF>
  *(There is no Qwen3.6 122B yet; the largest Unsloth MoE at this tier is
  Qwen**3.5**‑122B‑A10B.)*

Then run with the local path, e.g.:

```powershell
.\llama-server.exe -m D:\models\Qwen3.6-35B-A3B-UD-Q5_K_XL.gguf ...
```

> **Split files:** for the 122B the `UD-Q5_K_XL` quant lives in a subfolder and
> comes as three parts (`...-00001-of-00003.gguf` …). Download **all** parts
> into the same folder, then point `-m` at the **first** part only — llama.cpp
> loads the remaining shards automatically.

**On RAM:** the figures above are the **total memory** (system RAM + the 16 GB
of VRAM) that must hold the model plus its KV cache. The RTX 5080's 16 GB
carries the hot path; system RAM holds the offloaded experts, so RAM needs to
cover roughly *file size − VRAM used + headroom*. All three run on a single
5080 — the only requirement is having enough system RAM. The 122B at ~92 GB
needs **128 GB** of RAM.

## Step 3 — Run it (let auto‑fit do the offloading)

Recent llama.cpp **auto‑fits** MoE models: it offloads everything to the GPU,
then automatically moves the routed‑expert tensors of the last layers to CPU /
system RAM until the rest fits in VRAM — choosing the split for you, even at the
tensor‑group level. You don't need `-ngl`, `--cpu-moe`, or `--n-cpu-moe`; just
point it at the model and run:

```powershell
.\llama-server.exe `
  -m D:\models\Qwen3.6-35B-A3B-UD-Q5_K_XL.gguf `
  -c 131072 `
  -np 1 `
  -fa on `
  --jinja `
  --host 127.0.0.1 --port 8080
```

What each flag does:

- **`-c 131072`** — context length: the full **128K** Qwen3.6 supports.
- **`-np 1`** — one server slot. `-np` defaults to *auto*, which can open
  several slots and **split the `-c` budget across them** — so a single chat
  would only get a fraction of the 128K. Pin it to `1` to give one conversation
  the whole context. (Raise it only if you're serving concurrent requests.)
- **`-fa on`** — Flash Attention. Lower KV‑cache memory and faster attention.
- **`--jinja`** — use the model's built‑in chat template (correct prompt
  formatting and tool‑calling).

On load you'll see llama.cpp log its fitting attempts and report how many layers
landed on `CUDA0` versus CPU. Open <http://127.0.0.1:8080> for the built‑in chat
UI, or point an OpenAI‑compatible client at `http://127.0.0.1:8080/v1`.


## Step 4 — Benchmark throughput

Once it loads, measure real throughput with `llama-bench` — same model, same
flags. It reports **pp** (prompt processing, tokens/s) and **tg** (generation,
tokens/s):

```powershell
.\llama-bench.exe `
  -m D:\models\Qwen3.6-35B-A3B-UD-Q5_K_XL.gguf `
  -fa 1 `
  -p 512 `
  -n 128
```

- **`-p 512`** — prompt‑processing benchmark over a 512‑token prompt.
- **`-n 128`** — generation benchmark of 128 new tokens.
- **`-fa 1`** — Flash Attention on, to match the server.

`llama-bench` auto‑fits the same way the server does. To benchmark a *specific*
split instead, add the same offload flag you'd use above, e.g. `--n-cpu-moe 28`
or `-ot "exps=CPU"`. Compare runs to see how much each extra expert layer on the
GPU buys you in tg tokens/s.

## Step 5 — Sampling settings (don't skip this)

Qwen3.6 is sensitive to sampling. Unsloth/Qwen's recommended settings:

**Thinking mode (default, general tasks):**

```powershell
  --temp 1.0 --top-p 0.95 --top-k 20 --min-p 0.0 --presence-penalty 1.5
```

**Non‑thinking mode (faster, general tasks):**

```powershell
  --temp 0.7 --top-p 0.8 --top-k 20 --min-p 0.0 --presence-penalty 1.5 `
  --chat-template-kwargs "{\"enable_thinking\":false}"
```

For **coding** in thinking mode, use `--temp 0.6` and drop the presence penalty
to `0.0`. Wrong temperature (e.g. the 0.7 you'd use for a dense model) makes
this model noticeably worse.

## Putting it all together

A solid everyday command for the RTX 5080 + Qwen3.6‑35B‑A3B Q5\_K\_XL, in
thinking mode, ready for OpenAI‑compatible clients:

```powershell
.\llama-server.exe `
  -m D:\models\Qwen3.6-35B-A3B-UD-Q5_K_XL.gguf `
  -c 131072 -np 1 -fa on `
  --fit-target 2048 `
  --jinja `
  --temp 1.0 --top-p 0.95 --top-k 20 --min-p 0.0 --presence-penalty 1.5 `
  --host 127.0.0.1 --port 8080
```

Auto‑fit handles the GPU/CPU split, so there's no number to tune — and you have
a 35 B‑class model running comfortably on a 16 GB consumer card.

---

### Sources

- [Unsloth — Qwen3.6: How to Run Locally](https://unsloth.ai/docs/models/qwen3.6)
- [unsloth/Qwen3.6-35B-A3B-GGUF · Hugging Face (quant sizes)](https://huggingface.co/unsloth/Qwen3.6-35B-A3B-GGUF)
- [Performant local MoE CPU inference with GPU acceleration in llama.cpp](https://huggingface.co/blog/Doctor-Shotgun/llamacpp-moe-offload-guide)
- [Understanding MoE Offloading — DEV Community](https://dev.to/someoddcodeguy/understanding-moe-offloading-5co6)
- [llama.cpp releases (Windows CUDA binaries)](https://github.com/ggml-org/llama.cpp/releases)
