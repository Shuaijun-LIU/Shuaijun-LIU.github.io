---
layout: blog_post
title: "ManiSkill2: SAPIEN-Based Manipulation for Richer Simulation Tasks"
date: 2025-11-10
tags:
  - Benchmark
  - SAPIEN
  - Manipulation
excerpt: "ManiSkill2 is useful when manipulation tasks need richer simulation assets, articulated interactions, and scalable visual or state-based evaluation."
---

ManiSkill2 is a SAPIEN-based benchmark for generalizable manipulation skills. The paper is useful because it combines task diversity, object diversity, demonstrations, multiple observation modes, and high-throughput visual simulation in one benchmark suite.

<figure class="blog-figure">
  <img src="{{ '/assets/images/blog/benchmarks/papers/maniskill2-paper-figure.jpg' | relative_url }}" alt="ManiSkill2 task overview from the paper">
  <figcaption>Paper figure from the <a href="https://arxiv.org/abs/2302.04659">ManiSkill2</a> source package, showing task families across rigid, articulated, mobile-base, dual-arm, and soft-body manipulation.</figcaption>
</figure>

<figure class="blog-figure">
  <img src="{{ '/assets/images/blog/benchmarks/tasks/maniskill2-task-examples.jpg' | relative_url }}" alt="ManiSkill2 task examples showing simulated and real PickCube settings">
  <figcaption>Task examples from the paper source, including simulation-to-real visual comparisons. Observation mode and task version should always be written next to the score.</figcaption>
</figure>

## What the Paper Contributes

The paper reports 20 manipulation task families, 2,000+ object models, and 4M+ demonstration frames. It covers stationary and mobile-base settings, single-arm and dual-arm tasks, rigid-body and soft-body manipulation, and both 2D/3D visual input.

Another important contribution is systems-oriented: ManiSkill2 includes asynchronous rendering and a render-server design to improve visual sample collection. The paper reports about 2000 FPS for a CNN-based visual policy collection setup with one GPU and 16 processes.

## What ManiSkill2 Covers

Typical task categories include lifting, stacking, cluttered picking, peg insertion, cabinet drawers and doors, faucet turning, charger plugging, object movement, obstacle avoidance, pouring, filling, writing, and geometry-driven manipulation.

This makes ManiSkill2 useful when the research question needs richer simulated manipulation than classic tabletop tasks but does not necessarily require a full household kitchen benchmark.

## How to Use It

```python
import gymnasium as gym

env = gym.make("PickCube-v0", obs_mode="state", render_mode="rgb_array")
obs, info = env.reset(seed=0)
obs, reward, terminated, truncated, info = env.step(env.action_space.sample())
frame = env.render()
env.close()
```

The exact task ID and observation mode depend on the installed ManiSkill version. For a paper result, record those details alongside the controller, camera settings, seed, and evaluation horizon.

## Practical Usage Notes

The most common mistake is to treat ManiSkill2 as a task name rather than a versioned simulator benchmark. Task IDs, observation modes, controllers, and registry behavior can change across releases, and ManiSkill2 versus later ManiSkill versions should not be mixed silently.

A minimum reproducibility block should include:

- task ID, benchmark version, controller, observation mode, camera setup, and seed;
- whether the result uses state, RGB, RGB-D, point cloud, or segmentation observations;
- reset/step/render smoke status before full evaluation;
- horizon, success metric, and whether demonstrations are used;
- any asset or rendering backend assumptions needed to reproduce videos.

For method design, ManiSkill2 is strong when the question needs richer object interaction or visual simulation than RoboSuite. It is less direct when the claim is language-conditioned planning or household workflow completion; in those cases, pair it with LIBERO or RoboCasa.

## When To Use It

Use ManiSkill2 for scalable manipulation evaluation, SAPIEN-based task design, visual observation pipelines, and richer object interactions. It can be a good fit for policies that need depth, segmentation, point clouds, or visually grounded action learning.

## What To Check First

Before treating a task as benchmark-ready, run a small reset/step/render smoke. Simulation benchmarks often fail for practical reasons: rendering backend mismatch, missing assets, incompatible observation mode, or a changed task registry.

Also make the observation mode explicit. State-based and image-based results answer different questions.

## Limits

ManiSkill2 is still a simulator benchmark. Strong results do not automatically establish language grounding, household robustness, or real-robot transfer.

## Paper Source

This note was revised from the paper and its LaTeX source package: <a href="https://arxiv.org/abs/2302.04659">ManiSkill2: A Unified Benchmark for Generalizable Manipulation Skills</a>.
