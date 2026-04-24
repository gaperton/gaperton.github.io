---
id: 5910
date: 2026-03-14T21:00:00+00:00
author: Gapertons-Tech-Corner
author_handle: @gaperton_tech
reply_to: 5908
---

Да, и в линукс с драйверами у AMD все прям сильно лучше.

I acquired two of these GPUs a month ago and have spent some time understanding them. My focus is on AI content creation, not gaming. The GPU is in dual configuration with 64 GB shared memory and is capable of handling anything I throw at it. From a 48.5GB sharded Llama Scout LLM using LM Studio and image to video generation using ComfyUI Zluda with AMD ROCm+Pytorch 2.9. Currently Pytorch doesn't have the drivers you have to download them from the AMD website. I am using the AMD 25.20.01.17 Windows preview driver, which allows me to use Windows, and it is flawless. AMD is entering a new world with RDNA4. Linux works flawlessly without any effort as usual. The only thing that bothers me is how AMD describes FP8 acceleration. Yes, it can input, process, and output FP8, but it lacks the FP8 Tensor cores, so it internally translates to FP16/BF16 for hardware acceleration. Definitely not a deal breaker, but now I understand why it's 20% slower than Team Green. As I understand it the Navi48 die is maxed out with the current generation with 32gb and a 256 bit bus. Makes me wonder what the next generation RDNA5 will look like with true FP8 tensor cores. I love these GPUs!