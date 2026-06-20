---
layout: blog_post
title: "PushT: Why a Tiny 2D Control Task Is Still Useful"
date: 2025-11-07
tags:
  - Benchmark
  - Control
  - Diffusion Policy
excerpt: "PushT is a single 2D pushing benchmark, but that simplicity makes it useful for debugging action chunks, policy outputs, and evaluation pipelines."
---

PushT is a small 2D contact-rich control task that became widely used through the Diffusion Policy evaluation suite. The agent must push a T-shaped object into a target T-shaped region. Its value comes from being simple, visual, and sensitive to action-sequence quality.

<figure class="blog-figure">
  <img src="{{ '/assets/images/blog/benchmarks/papers/pusht-paper-figure.jpg' | relative_url }}" alt="PushT and other simulated manipulation tasks from the Diffusion Policy paper">
  <figcaption>Paper figure from the <a href="https://arxiv.org/abs/2303.04137">Diffusion Policy</a> source package, where PushT appears as one of the simulated manipulation tasks.</figcaption>
</figure>

## What the Paper Context Adds

PushT is not a large benchmark suite by itself. In the Diffusion Policy paper, it is part of a broader evaluation over multiple manipulation tasks. That context matters: PushT is best treated as a diagnostic task for closed-loop action generation, not as evidence for general-purpose robot intelligence.

The task is still valuable because contact-rich pushing exposes errors in action normalization, action horizon, temporal smoothing, and rollout logging. A bad policy is easy to see in video.

## What PushT Tests

PushT tests whether a policy can produce a sequence of continuous actions that progressively moves an object into a target pose. The core difficulty is contact-rich control under partial progress: a small action error can rotate or displace the object in ways that later actions must correct.

It is often useful for debugging:

- action normalization;
- action chunk length;
- diffusion or sequence policy outputs;
- rollout logging;
- simple success metrics;
- video export and qualitative inspection.

## How to Use It

The practical workflow is:

```text
load policy -> run N PushT episodes -> save JSON/CSV metrics -> inspect rollout GIFs
```

When debugging, vary one setting at a time: action horizon, normalization, seed, or policy checkpoint. If multiple knobs change together, PushT loses its main advantage as a diagnostic tool.

## When To Use It

Use PushT early when building a new policy pipeline, especially if the method outputs action chunks or uses a sequence model. It is a good first target before moving into multi-task manipulation, language-conditioned benchmarks, or real robot data.

## Limits

PushT does not prove household manipulation, language understanding, object generalization, or real robot robustness. It is a control and pipeline sanity benchmark. Treat it as an early diagnostic, not a final robotics claim.

## Paper Source

This note was revised from the paper and its LaTeX source package: <a href="https://arxiv.org/abs/2303.04137">Diffusion Policy: Visuomotor Policy Learning via Action Diffusion</a>.
