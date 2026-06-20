---
layout: blog_post
title: "MetaWorld: A Compact Benchmark for Multi-Task Tabletop Manipulation"
date: 2025-11-09
tags:
  - Benchmark
  - Manipulation
  - Multi-Task Learning
excerpt: "MetaWorld is a MuJoCo tabletop manipulation benchmark with many compact tasks, useful for multi-task RL, meta-learning, and controlled task heterogeneity."
---

MetaWorld is a MuJoCo tabletop manipulation benchmark built around many compact manipulation tasks. It is less about photorealism and more about breadth: reach, push, pick-place, drawers, doors, buttons, windows, sweeping, peg insertion, and related single-arm skills.

<figure class="blog-figure">
  <img src="{{ '/assets/images/blog/benchmarks/simulator-manipulation.svg' | relative_url }}" alt="Simulator manipulation benchmark map">
  <figcaption>MetaWorld is useful when you want many small manipulation tasks under a consistent simulation and action interface.</figcaption>
</figure>

## What MetaWorld Tests

MetaWorld is designed for multi-task reinforcement learning and meta-learning. The common benchmark families include MT-style and ML-style splits, where the key issue is whether a policy can adapt or generalize across task variations.

In local guides, a smaller four-task subset is also useful for federated or multi-client experiments:

| Alias | Task |
| --- | --- |
| door-lock | lock the door |
| close-drawer | close the drawer |
| open-window | open the window |
| sweep-into | sweep object into hole |

This kind of subset is useful when the full benchmark is unnecessary but task heterogeneity still matters.

## When To Use It

Use MetaWorld when the experiment needs a clean multi-task manipulation testbed, task/client heterogeneity, policy adaptation, or quick simulation feedback.

It is a good middle ground between very small control tasks such as PushT and larger scene-rich benchmarks such as RoboCasa.

## What It Does Not Prove

MetaWorld is not a language-rich VLA benchmark by default, and it is not a real-world dataset. It also does not capture the visual complexity of household scenes. Use it for controlled manipulation learning, not as the only proof of embodied intelligence.

## A Minimal Usage Pattern

The pattern is usually:

```python
import metaworld

benchmark = metaworld.MT1("door-lock-v3")
env = benchmark.train_classes["door-lock-v3"]()
task = benchmark.train_tasks[0]
env.set_task(task)
obs = env.reset()
obs, reward, done, truncated, info = env.step(env.action_space.sample())
env.close()
```

For fair comparison, report the task set, seed, horizon, success definition, and whether the evaluation uses state observations or rendered images.

## Takeaway

MetaWorld is useful because it is compact and broad. It is a practical benchmark for multi-task manipulation ideas before moving into heavier language, vision, or household simulation.
