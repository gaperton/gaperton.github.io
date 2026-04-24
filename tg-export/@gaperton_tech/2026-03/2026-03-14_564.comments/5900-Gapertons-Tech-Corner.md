---
id: 5900
date: 2026-03-14T20:19:40+00:00
author: Gapertons-Tech-Corner
author_handle: @gaperton_tech
reply_to: 5895
---

Yes, I'm confident that the throughput of the third PCIe slot (PCIe x16_3) is effectively capped by the equivalent of PCIe 4.0 x4 bandwidth (~7-8 GB/s theoretical maximum, bidirectional) due to the CPU-to-chipset uplink limitation, as explained previously. This cap applies regardless of the x8 electrical negotiation—it's a shared resource bottleneck from the chipset design. Regarding the M.2 lanes: they are used on this board as per standard specs. The primary M.2_1 slot gets dedicated PCIe 4.0 x4 lanes directly from the CPU (not shared with the third slot or GPUs), while the secondary M.2_2 slot uses PCIe 4.0 x2 from the chipset (which does share the same x4 uplink as the third slot, potentially causing minor contention under heavy multi-device load). No M.2 lanes are "unused" or repurposed here; they're allocated as intended for storage. 

Значит там так. Всего у Ryzen x24.

x8+x8 это первые два слота PCIe, как у всех с бифуркацией.

x4 идет напрямую от CPU к первому слоту M.2. Всегда. Как у всех.

x4 идет к чипсету, как у всех.

От чипсета, идет:
• x8 к PCIe
• и еще сколько-то ко второму слоту M.2

То есть, этот третий слот по вкусу вкусно, а по сути — все равно говно.

Чуда не вышло. Но это наверное лучшее что может быть с Ryzen.