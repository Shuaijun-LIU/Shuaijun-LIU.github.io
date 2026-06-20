---
layout: blog_post
title: "LIBERO: A Practical Guide to Language-Conditioned Manipulation Benchmarks"
date: 2025-11-01
tags:
  - Benchmark
  - Robotics
  - VLA
excerpt: "LIBERO is useful when a robot policy must connect language instructions, visual observations, and task-level success in a controlled manipulation setting."
---

LIBERO is a language-conditioned manipulation benchmark built around tabletop robot tasks, demonstrations, and suite-level evaluation. The important thing is that it does not only ask whether a controller can move an end effector. It asks whether a policy can interpret an instruction, act in a scene, and satisfy a task predicate.

<figure class="blog-figure">
  <img src="{{ '/assets/images/blog/benchmarks/language-manipulation.svg' | relative_url }}" alt="Language-conditioned manipulation benchmark workflow">
  <figcaption>LIBERO-style evaluation connects instruction understanding, visual feedback, policy execution, and task-level success checks.</figcaption>
</figure>

## What LIBERO Tests

LIBERO is best understood as a suite family rather than a single task. The common suites separate different generalization pressures: spatial relations, object variation, goal predicates, long-horizon tasks, and larger multitask training sets.

The usual suite names are:

| Suite | Typical role |
| --- | --- |
| `libero_spatial` | spatial relation transfer |
| `libero_object` | object-centric transfer |
| `libero_goal` | goal and predicate transfer |
| `libero_10` | long-horizon downstream evaluation |
| `libero_90` | larger multitask training or pretraining |
| `libero_100` | combined view of `libero_90` and `libero_10` in some local setups |

This structure is why LIBERO is useful for vision-language-action models. A VLA policy can be evaluated not only on raw motion quality, but also on whether it preserves the meaning of the language instruction under object, scene, and horizon changes.

## When It Is a Good Choice

Use LIBERO when the research question involves language-conditioned manipulation, imitation learning, VLA fine-tuning, long-horizon robot instructions, or failure analysis under controlled object layouts.

It is especially useful for comparing a base policy against variants such as memory, replanning, action correction, visual perturbation handling, or task-specific fine-tuning.

## What It Does Not Prove

LIBERO is still a simulated benchmark. Strong LIBERO performance does not by itself prove real-robot deployment, multi-arm coordination, or robust household behavior in unconstrained homes. For those claims, pair it with real robot data, a broader simulator, or hardware evaluation.

## A Minimal Usage Pattern

The high-level workflow is:

```python
from libero.libero import benchmark

suite = benchmark.get_benchmark_dict()["libero_10"]()
print("number of tasks:", suite.n_tasks)
task = suite.get_task(0)
print(task.language)
```

After that, a real evaluation loop usually needs three additional pieces: an environment wrapper, initial states or demonstrations, and a policy interface that maps observations plus instruction text to robot actions.

## Practical Advice

Start with `libero_10` for a small, interpretable evaluation. Move to `libero_object`, `libero_spatial`, or `libero_goal` when the goal is to isolate a specific kind of generalization. Use `libero_90` or `libero_100` only when the experiment really needs a broader multitask distribution.

The most common mistake is treating success rate as a single number without inspecting failure modes. For a VLA policy, it matters whether failure comes from language misunderstanding, perception, action scale, compounding control error, or a task predicate that is too strict.
