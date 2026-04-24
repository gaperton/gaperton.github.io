---
id: 5896
date: 2026-03-14T19:57:11+00:00
author: Gapertons-Tech-Corner
author_handle: @gaperton_tech
reply_to: 5895
---

Так, я чую наебалово.

The third slot is not connected to the CPU's 16-lane group — it's fed from the chipset's PCIe lanes. 
The X570 chipset has enough internal bandwidth and lane allocation to present x8 electrically to that slot (even though the CPU-to-chipset link is only x4). This works because:PCIe protocol allows the link width to be negotiated independently. 
The chipset internally aggregates or allocates lanes to support x8 downstream on that slot. 
**Bandwidth is still limited by the CPU  chipset x4 link (~8 GB/s bidirectional in PCIe 4.0), so real-world throughput on the third slot is capped accordingly — but the link width itself negotiates to x8.**