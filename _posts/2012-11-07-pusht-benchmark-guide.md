---
layout: blog_post
title: "PushT: Why a Tiny 2D Control Task Is Still Useful"
date: 2012-11-07
tags:
  - Benchmark
  - Control
  - Diffusion Policy
excerpt: "PushT is a single 2D pushing benchmark, but that simplicity makes it useful for debugging action chunks, policy outputs, and evaluation pipelines."
---

PushT is a small 2D control benchmark where the agent must push a T-shaped object into a target T-shaped region. It is not a broad task suite. Its strength is the opposite: it is simple enough that policy, action scaling, and evaluation bugs become easier to see.

<figure class="blog-figure">
  <img src="{{ '/assets/images/blog/benchmarks/navigation-control.svg' | relative_url }}" alt="Navigation and control benchmark loop">
  <figcaption>PushT is useful because the closed-loop control problem is easy to visualize: observe, choose action, push, and measure overlap with the target.</figcaption>
</figure>

## What PushT Tests

PushT tests whether a policy can produce a sequence of continuous actions that progressively moves an object into a target pose. The core difficulty is contact-rich control under partial progress: a small action error can rotate or displace the object in ways that later actions must correct.

It is often useful for debugging:

- action normalization;
- action chunk length;
- diffusion or sequence policy outputs;
- rollout logging;
- simple success metrics;
- video export and qualitative inspection.

## Why It Remains Valuable

Small benchmarks are not automatically weak benchmarks. PushT is valuable because it gives fast feedback. A full VLA evaluation can fail for many reasons at once: perception, language, model loading, action scaling, environment setup, or success detection. PushT strips most of that away and makes the control loop visible.

## When To Use It

Use PushT early when building a new policy pipeline, especially if the method outputs action chunks or uses a sequence model. It is a good first target before moving into multi-task manipulation or language-conditioned benchmarks.

## What It Does Not Prove

PushT does not prove household manipulation, language understanding, object generalization, or real robot robustness. It is a control and pipeline sanity benchmark. Treat it as an early diagnostic, not a final robotics claim.

## A Minimal Usage Pattern

The practical workflow is:

```text
load policy -> run N PushT episodes -> save JSON/CSV metrics -> inspect rollout GIFs
```

When debugging, vary one setting at a time: action horizon, normalization, seed, or policy checkpoint. If multiple knobs change together, PushT loses its main advantage as a diagnostic tool.

## Takeaway

PushT is useful because it is small. It gives a fast, visual answer to a basic question: can this policy produce coherent closed-loop actions at all?
