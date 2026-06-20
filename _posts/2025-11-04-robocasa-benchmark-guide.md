---
layout: blog_post
title: "RoboCasa: Kitchen-Scale Manipulation Beyond Toy Tabletop Tasks"
date: 2025-11-04
tags:
  - Benchmark
  - Household Robotics
  - Manipulation
excerpt: "RoboCasa extends MuJoCo/RoboSuite-style manipulation into large kitchen task spaces with appliances, objects, fixtures, and composite household workflows."
---

RoboCasa is a simulation framework and benchmark for household-scale kitchen manipulation. The paper extends the RoboSuite ecosystem from compact tabletop tasks toward realistic kitchens with many scenes, objects, robot embodiments, tasks, and generated demonstrations.

<figure class="blog-figure">
  <img src="{{ '/assets/images/blog/benchmarks/papers/robocasa-paper-figure.jpg' | relative_url }}" alt="RoboCasa overview figure from the paper">
  <figcaption>Paper figure from the <a href="https://arxiv.org/abs/2406.02523">RoboCasa</a> source package, summarizing scenes, objects, embodiments, tasks, and demonstration data.</figcaption>
</figure>

## What the Paper Contributes

The paper highlights four pillars:

| Pillar | Practical meaning |
| --- | --- |
| 120 kitchen scenes | Layout and style variation beyond a single demo room |
| 2,500+ 3D objects | Object diversity across many kitchen-relevant categories |
| Cross-embodiment support | Mobile manipulators and humanoid robots can be studied in the same domain |
| 100 tasks and 100K+ trajectories | A larger task/data regime than small tabletop suites |

This matters because many robotics methods look strong in toy tabletop settings but become fragile when fixtures, appliances, receptacles, and scene layout matter.

## Atomic and Composite Tasks

Atomic tasks focus on a smaller skill or fixture interaction, such as opening, closing, placing, cleaning, or manipulating a specific appliance-related element.

Composite tasks combine these pieces into larger household workflows, such as arranging, preparing, serving, loading, cleaning, or setting up kitchen items.

This split is useful when designing experiments. Atomic tasks help isolate a skill bottleneck. Composite tasks test whether a policy can remain coherent across longer kitchen workflows.

## How to Use It

The conceptual workflow is:

```text
choose task -> choose scene/layout -> choose embodiment -> roll out policy -> score success and save media
```

For a first smoke test, pick a simple task, render a short rollout, and verify assets, cameras, object placement, and success conditions. For a benchmark table, state the task subset, scene split, object registry, robot embodiment, and demonstration source.

## What To Be Careful About

Large task spaces are powerful, but they are also easier to misuse. Before reporting a result, make clear which split, task subset, object registry, camera setting, and evaluation protocol were used.

Another practical issue is asset completeness. Kitchen benchmarks depend on object and scene assets. If a project uses fallback assets or a reduced object registry, that should be documented because it can change task semantics.

## Limits

RoboCasa improves household simulation coverage, but it is still simulated. Real kitchens add compliance, sensor noise, safety constraints, and unmodeled object behavior.

## Paper Source

This note was revised from the paper and its LaTeX source package: <a href="https://arxiv.org/abs/2406.02523">RoboCasa: Large-Scale Simulation of Everyday Tasks for Generalist Robots</a>.
