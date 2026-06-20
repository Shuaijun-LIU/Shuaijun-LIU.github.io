---
layout: blog_post
title: "OGBench: Offline Goal-Conditioned RL Before Real-Robot Complexity"
date: 2025-11-05
tags:
  - Benchmark
  - Offline RL
  - Goal-Conditioned RL
excerpt: "OGBench is a controlled benchmark for offline RL and offline goal-conditioned RL, useful before moving a method into real robot data or VLA evaluation."
---

OGBench is a benchmark for offline goal-conditioned reinforcement learning. The paper is useful because it separates several algorithmic challenges that are often mixed together: stitching behavior from offline data, long-horizon reasoning, stochastic control, and learning from high-dimensional observations.

<figure class="blog-figure">
  <img src="{{ '/assets/images/blog/benchmarks/papers/ogbench-paper-figure.jpg' | relative_url }}" alt="OGBench environment overview from the paper">
  <figcaption>Paper figure from the <a href="https://arxiv.org/abs/2410.20092">OGBench</a> source package, showing state- and pixel-based locomotion, manipulation, and drawing tasks.</figcaption>
</figure>

## What the Paper Contributes

OGBench focuses on fixed-dataset learning, where the policy cannot collect new experience online. Its task families include:

| Family | Typical use |
| --- | --- |
| Locomotion | Navigation, stitching, long-horizon goal reaching |
| Manipulation | Object control, puzzle-like goals, sequential state changes |
| Drawing | Structured state transitions and goal-conditioned behavior |

The paper emphasizes that offline goal-conditioned RL is not just "offline RL with a goal vector." A method may need to infer useful intermediate behavior from the dataset, stitch partial trajectories, and reason over long horizons without fresh exploration.

## How to Use It

The official-style API usually creates both an environment and datasets:

```python
import ogbench

env, train_dataset, val_dataset = ogbench.make_env_and_datasets(
    "pointmaze-medium-navigate-v0",
    compact_dataset=True,
)

obs, info = env.reset(options={"task_id": 1, "render_goal": True})
next_obs, reward, terminated, truncated, info = env.step(env.action_space.sample())
env.close()
```

For manipulation work, start with an environment-only smoke before downloading large datasets. Then inspect observation/action shapes, goal fields, dataset keys, and evaluation horizons.

## When To Use It

Use OGBench when the method is about offline learning, goal-conditioned action selection, latent planning, replay-buffer composition, action correction, or algorithmic ablation. It gives faster feedback than a full VLA stack and has cleaner failure modes than real robot data.

It is also a good first filter for replanning ideas. If an idea cannot help in a controlled offline goal-reaching benchmark, it is unlikely to become reliable after adding language, vision encoders, and real robot noise.

## Limits

OGBench does not prove language understanding, hardware deployment, or real-world VLA generalization. Treat it as a mechanism benchmark for offline goal-conditioned learning.

## Paper Source

This note was revised from the paper and its LaTeX source package: <a href="https://arxiv.org/abs/2410.20092">OGBench: Benchmarking Offline Goal-Conditioned RL</a>.
