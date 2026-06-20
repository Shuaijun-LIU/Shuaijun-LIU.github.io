---
layout: blog_post
title: "OGBench: Offline Goal-Conditioned RL Before Real-Robot Complexity"
date: 2012-11-05
tags:
  - Benchmark
  - Offline RL
  - Goal-Conditioned RL
excerpt: "OGBench is a controlled benchmark for offline RL and offline goal-conditioned RL, useful before moving a method into real robot data or VLA evaluation."
---

OGBench is designed for offline reinforcement learning and offline goal-conditioned reinforcement learning. It is useful when you want to test whether an algorithm can learn from fixed datasets and reach goals without immediately paying the cost of real robot data or complex VLA evaluation.

<figure class="blog-figure">
  <img src="{{ '/assets/images/blog/benchmarks/offline-real-data.svg' | relative_url }}" alt="Offline and real-robot data benchmark workflow">
  <figcaption>OGBench-style experiments center on datasets, goals, policies, and offline evaluation rather than live robot deployment.</figcaption>
</figure>

## What OGBench Tests

OGBench covers several task families:

| Family | Typical use |
| --- | --- |
| Locomotion | navigation, stitching, long-horizon goal reaching |
| Manipulation | object control, puzzle-like goals, sequential state changes |
| Drawing | discrete action planning and structured state transitions |

This makes it a good early benchmark for algorithms that need controlled variation: failure recovery, latent steering, action selection, goal representation, and offline policy improvement.

## Why It Is Useful for Embodied AI

Many embodied-AI ideas are expensive to validate directly in a full VLA stack. OGBench gives a lower-cost test. If a replanning or action-correction mechanism cannot help in a controlled offline manipulation setting, it is unlikely to become reliable after adding language, vision encoders, and real robot noise.

## When To Use It

Use OGBench when the method is about offline learning, goal-conditioned action selection, short-horizon feasibility, or algorithmic ablation. It is also useful when you want a fast development loop before moving to LIBERO, DROID, or a real robot dataset.

## What It Does Not Prove

OGBench should not be the only evidence for real-world VLA generalization. It does not by itself prove hardware deployment, language understanding, or multi-agent coordination. Treat it as a mechanism benchmark: it can show whether an idea works under controlled offline assumptions.

## A Minimal Usage Pattern

The official-style API usually creates both an environment and datasets:

```python
import ogbench

env, train_dataset, val_dataset = ogbench.make_env_and_datasets(
    "pointmaze-medium-navigate-v0",
    compact_dataset=True,
)

obs, info = env.reset(options={"task_id": 1, "render_goal": True})
action = env.action_space.sample()
next_obs, reward, terminated, truncated, info = env.step(action)
env.close()
```

For manipulation work, start with an environment-only smoke before downloading large datasets. Then download one task dataset, log observation and action shapes, and only then scale to larger families.

## Takeaway

OGBench is a good benchmark for proving that the algorithmic core works. It is not the final destination for robot-learning claims, but it is often the right first filter.
