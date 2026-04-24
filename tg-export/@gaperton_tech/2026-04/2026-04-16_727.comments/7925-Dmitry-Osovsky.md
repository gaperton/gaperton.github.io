---
id: 7925
date: 2026-04-16T18:26:25+00:00
author: Dmitry-Osovsky
---

Да никакой особой методы, я скачал готовые бинари llama.cpp под винду и интел+CUDA (12-й версии, потому как 13-я хочет новых дров для нвидии а я их апдейтить не хочу — меня устраивают те, что уже стоят).
Скачал модель с https://huggingface.co/ и положил рядом в поддиректорию models.
Запустил бенч вот так:
llama-bench -m models\Qwen3.6-35B-A3B-UD-Q4_K_XL.gguf -ngl 99 -ot "exps=CPU" -fa 1 -p 512,2048,4096 -n 256 -r 2

Сервис же для работы и досуга запускается с почти такими же параметрами, только экзешник другой:
llama-server -m models\Qwen3.6-35B-A3B-UD-Q4_K_XL.gguf -ngl 99 -ot "exps=CPU" -c 131072 -np 1 --cache-type-k q8_0 --cache-type-v q8_0 -fa on --webui-mcp-proxy