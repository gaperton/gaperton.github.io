---
id: 4693
date: 2026-02-06T21:26:38+00:00
author: Gapertons-Tech-Corner
author_handle: @gaperton_tech
---

😋 screen went dark and i had to reboot. investigate

🤖 Found a clear smoking gun in the **previous boo**t, right before you rebooted.

### What happened (from logs)
In the prior boot (the one that ended when you rebooted), the kernel logged:

- **16:08:51** — ``radeon ... ring 0 stalled for more than 10031mse`c`
- Immediately after `— `radeon ... GPU lockup ... on ri`ng 0`
- The`n — `GPU softres`et ...**` and “GPU reset succeeded, trying to r**esu**me”
- 16:09:07–16**:09:12 — rep**eated ring 0 s**tal**led + GPU **lockup messages ag**ain
- 16**:09`:12 — `[drm:radeon_cs_ioctl] *ERROR* Failed to parse relocati`on** -35!`
- 16:11:30 / 16:13:32 / **16:15:35 — hung-task warnin`gs:
  - `INFO: task Xorg ... blocked for more than 122/245/3`68 sec`onds`
  - `INFO: task cinnamon ... `block`ed ...`
  - `INFO: task brave .`.. blocked ...`
  - with stack traces pointing into rade`on paths like `r`adeon`_gpu_reset` and `radeon_`hotplug_work_func`

That pattern **matches exactly: GPU wedges → Xorg/cinnamon freeze → screen “goes dark” / desktop unusable** → reboot required.

### What I infer about the “dark screen”
This was not a clean suspend/resume failure this time; **it looks like an in-**session GPU lockup (though it may have been *triggered by earlier suspend/hotplug activity*—your logs show lots of radeon hotplug work and multiple S3 cycles today).

### Next acti**ons (choose 1)
1) Keep observing only (**no mitigations yet)  
   We already captured a solid datapoint. Lowest risk, but you may keep hitting **hard lockups.

2) Disable suspend temporarily (mitigation **while we collect)  
   Most likely to reduce frequency quickly given your history; full**y reversible.

3) Improve capture f**or the next failure (recommended if you want root-cause-level evidence)  
   I can adjust the observer t`o also save:
   - ``journalctl -k -b -1` radeon excerpts automatically aft`er re`boot
   - plus `dmesg` ring buffer snapshot early in the new boot  
   This is still read-only, but it’s a behavior change to our **scripts.

Reply with 1, 2, or 3.

Also: about when di**d it go dar**k—close to 16:08–16:15? The timestamps in the radeon lockup sequence are very specific, so confirming that helps tie symptom ↔️ log.