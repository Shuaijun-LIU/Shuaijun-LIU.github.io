---
layout: blog_post
title: "UniLab: Robot RL Benchmarking as a Systems Problem"
date: 2012-11-13
tags:
  - Benchmark
  - Reinforcement Learning
  - Systems
excerpt: "UniLab is best treated as a robot-RL infrastructure benchmark where simulator throughput, learner speed, data movement, and synchronization all matter."
---

UniLab is not just another list of robot tasks. It is best read as a robot reinforcement learning infrastructure stack. The central question is not only "how fast can the simulator step?" but "how efficiently does the whole simulation-learning loop train a policy?"

<figure class="blog-figure">
  <img src="{{ '/assets/images/blog/benchmarks/systems-coordination.svg' | relative_url }}" alt="Systems and coordination benchmark structure">
  <figcaption>UniLab-style benchmarking includes simulation workers, policy learning, data transfer, synchronization, logging, and final rollout evaluation.</figcaption>
</figure>

## What UniLab Emphasizes

Modern robot RL can become bottlenecked in different places:

- simulator stepping;
- policy network updates;
- data transfer between simulator and learner;
- replay or rollout buffer organization;
- parameter synchronization;
- video export and logging.

UniLab makes these systems questions part of the benchmark story. That is why it is useful for comparing runtime organization, not only final task success.

## What It Covers

UniLab-style projects can involve arms, quadrupeds, humanoids, dexterous hands, wheeled-leg systems, locomotion, mobile manipulation, and hand tasks. The exact task list depends on the local checkout and configuration, but the important idea is embodiment-diverse robot RL under a shared training infrastructure.

## When To Use It

Use UniLab when the research question involves training throughput, end-to-end robot RL efficiency, simulator/learner separation, cross-embodiment policies, or long rollout visualization from trained checkpoints.

It is also useful when generating robot-control rollouts that may later become data for VLA or world-model projects.

## What It Does Not Replace

UniLab does not replace language-conditioned manipulation benchmarks such as LIBERO, kitchen benchmarks such as RoboCasa, or real-robot datasets such as DROID. It answers a different question: how should robot RL workloads be organized and evaluated as systems?

## A Minimal Usage Pattern

The workflow is:

```text
choose task -> train policy -> export checkpoint -> run evaluation playback -> report metrics and videos
```

For reproducible reports, record the task, simulator backend, algorithm, number of environments, rollout horizon, seed, checkpoint, video settings, and hardware assumptions.

## Takeaway

UniLab is useful because it treats robot RL as a full pipeline. For systems-oriented robotics research, that is often the benchmark that matters most.
