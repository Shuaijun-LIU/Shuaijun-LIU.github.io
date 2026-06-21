---
layout: blog_post
title: "RoboFactory: Multi-Robot Tasks for Coordination and Role Allocation"
date: 2025-11-11
tags:
  - Benchmark
  - Multi-Agent
  - Robotics
excerpt: "RoboFactory is useful when a robotics project needs multi-robot coordination tasks rather than another single-arm manipulation benchmark."
---

RoboFactory is a benchmark and automated data collection framework for embodied multi-agent manipulation. The paper is useful because it does not treat multi-robot learning as simply "single-robot learning times N." It introduces compositional constraints to make collaboration safer and more structured.

<figure class="blog-figure">
  <img src="{{ '/assets/images/blog/benchmarks/papers/robofactory-paper-figure.jpg' | relative_url }}" alt="RoboFactory pipeline overview from the paper">
  <figcaption>Paper figure from the <a href="https://arxiv.org/abs/2503.16408">RoboFactory</a> source package, showing how RoboBrain generates subgoals and constraints while RoboChecker validates multi-agent trajectories.</figcaption>
</figure>

<figure class="blog-figure">
  <img src="{{ '/assets/images/blog/benchmarks/tasks/robofactory-task-examples.jpg' | relative_url }}" alt="RoboFactory multi-robot task examples">
  <figcaption>Task examples from the paper source. The benchmark is most informative when the task requires explicit role allocation, handoff, timing, or collision-aware coordination.</figcaption>
</figure>

## What the Paper Contributes

The paper proposes logical, spatial, and temporal constraints for multi-agent embodied systems. Its framework has two central components:

| Component | Role |
| --- | --- |
| RoboBrain | Generates subgoals and textual compositional constraints from task descriptions and observations |
| RoboChecker | Converts textual constraints into interfaces that validate generated multi-agent trajectories |

This is important because multi-agent manipulation failures are often about coordination, not only low-level control. A plan can be locally reasonable for each robot while still violating timing, collision, role, or ordering constraints.

## What It Tests

Representative tasks include lifting a barrier, aligning a camera, passing an object between robots, taking a photo, stacking cubes with one or more robots, striking a cube, picking food, placing food, and chain-style delivery.

The important benchmark dimension is coordination:

- Which robot should act?
- Does the task require passing, timing, or role allocation?
- Does the policy work in a table scene, a RoboCasa-like scene, or both?
- Can the evaluation separate individual agent failure from group-level failure?

## How to Use It

The generic workflow is:

```text
choose task -> choose scene family -> generate or load multi-agent trajectories -> validate constraints -> train/evaluate policy
```

For first experiments, start with one task and one scene family. Add more agents or a second scene family only after logging, videos, and per-agent metrics are stable.

## Practical Usage Notes

Task identity should be separated from scene family. A table-scene task and a RoboCasa-like kitchen task can share a name while stressing different perception, clearance, and coordination behavior.

Useful reporting details:

- task ID, scene family, number of agents, and robot embodiments;
- whether success requires cooperation, handoff, ordering, collision avoidance, or role assignment;
- per-agent metrics alongside group-level success;
- videos or trajectory summaries for failed coordination cases;
- policy carrier, data source, and constraint checker configuration.

For a first benchmark pass, I would use one task from each coordination pattern rather than many visually similar tasks. The point is to test whether the method can allocate roles and maintain temporal structure, not merely whether multiple robots are present in the scene.

## When To Use It

Use RoboFactory when the method claims multi-agent or multi-robot capability. It is a better match than DROID or OGBench for coordination claims, because those datasets are not primarily multi-agent manipulation benchmarks.

It is also useful for comparing policy carriers such as diffusion policies, OpenVLA-like policies, or Pi-style policies under the same task registry.

## What To Be Careful About

Multi-agent results are easy to overstate. A task with multiple robots is not automatically a coordination benchmark unless success depends on interaction between agents. Report whether the task actually requires cooperation, handoff, collision avoidance, or role assignment.

Also keep scene family separate from task ID. The same task name can behave differently in a table scene and a kitchen-like scene.

## Paper Source

This note was revised from the paper and its LaTeX source package: <a href="https://arxiv.org/abs/2503.16408">RoboFactory: Exploring Embodied Agent Collaboration with Compositional Constraints</a>. The paper also provides a project page at <a href="https://iranqin.github.io/robofactory/">https://iranqin.github.io/robofactory/</a>.
