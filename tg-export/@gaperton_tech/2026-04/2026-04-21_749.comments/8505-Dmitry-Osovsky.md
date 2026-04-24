---
id: 8505
date: 2026-04-21T06:00:24+00:00
author: Dmitry-Osovsky
reply_to: 8457
---

короче джинн не осилил, а я заебался искать и править ошибки. Башем под винду там тоже не обойтись, там тебе и гит, и авк, и юнейм, you name it (pun intended)

могу тупо запустить бенч вот так:

c:\temp\llama-bench.exe -ngl 999 -fa on -r 3 -b 2048 -sm none -mg 0 --n-cpu-moe 64,32,16,8,4,0 -p 512 -p 2048 -n 256 -ub 512 -ub 1024 -ub 2048 -m f:\Qwen3.6-35B-A3B-UD-Q5_K_XL.gguf -o md

и посмотреть, что вышло