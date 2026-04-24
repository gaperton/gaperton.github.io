---
id: 3680
date: 2025-11-26T17:42:21+00:00
author: Gapertons-Tech-Corner
author_handle: @gaperton_tech
reply_to: 3662
---

Все что вы хотели знать о том, как работает бактерия. Но боялись спросить.

Beliefs: B(t) = (C(t), ∂C/∂t(t)) ∈ ℝ × ℝ
Desire: D = {x(t+Δt) ≥ θ} — максимизировать вероятность/время выполнения
Intention: I(t) = argmax_{a∈{Run,Tumble}} ℙ(x(t+Δt) ≥ θ | B(t), a)
Но поскольку бактерия не умеет считать вероятности, эволюция заменила argmax на эвристику:
I(t) = Run   если ∂C/∂t ≥ 0
I(t) = Tumble если ∂C/∂t < 0