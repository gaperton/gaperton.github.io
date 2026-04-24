---
id: 6752
date: 2026-03-29T01:55:38+00:00
author: Alexander-Luchkov
author_handle: @WatchTh15
---

В 32 гига R9700 35B_Q8 модель не влезет физически в память. Даже просто веса не влезают, там 36 гигабайт весов.
``````user@minisforum:~/models/qwen3.5-122b-q4$ ls -lah ../qwen3.5-35b-q8/
total 35G
drwxrwxr-x 3 user user 4.0K Mar 29 00:12 .
drwxrwxr-x 9 user user 4.0K Mar 29 00:18 ..
-rw-r--r-- 1 user user  35G Mar 28 23:47 Qwen3.5-35B-A3B-Q8_0.gguf
drwxr-xr-x 3 user user 4.0K Mar 28 23:49 hf```.co```
 Так что вы либо про другую модель, либо про другую конфигурацию видеокарт, либо что-то ещё недоговариваете.

Например параметры запуска, количество используемых слоёв и т.п.