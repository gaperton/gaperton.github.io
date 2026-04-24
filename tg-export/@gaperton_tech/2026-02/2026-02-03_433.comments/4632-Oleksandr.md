---
id: 4632
date: 2026-02-04T20:26:14+00:00
author: Oleksandr
author_handle: @oleksandr_now
reply_to: 4630
---

Ключевой примитив который делает это все composable - это не нужно думать в терминах "доступ", нужно думать в терминах data diode. RPC - двусторонняя херня, она не composable. А диоды (опционально фильтрованные) composable.