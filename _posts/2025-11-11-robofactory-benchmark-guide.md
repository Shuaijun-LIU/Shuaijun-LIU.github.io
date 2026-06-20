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

RoboFactory and its OpenMARL-style workflows are useful for a different question than most manipulation benchmarks. Instead of only asking whether one robot can grasp or place an object, RoboFactory asks how robots coordinate across tasks, roles, scenes, and policies.

<figure class="blog-figure">
  <img src="{{ '/assets/images/blog/benchmarks/systems-coordination.svg' | relative_url }}" alt="Systems and coordination benchmark structure">
  <figcaption>RoboFactory-style evaluation is about agents, scene configuration, policy execution, and coordination metrics.</figcaption>
</figure>

## What It Tests

Representative tasks include lifting a barrier, aligning a camera, passing an object between robots, taking a photo, stacking cubes with one or more robots, striking a cube, picking food, placing food, and chain-style delivery.

The important benchmark dimension is coordination:

- Which robot should act?
- Does the task require passing, timing, or role allocation?
- Does the policy work in a table scene, a RoboCasa-like scene, or both?
- Can the evaluation separate individual agent failure from group-level failure?

## When To Use It

Use RoboFactory when the method claims multi-agent or multi-robot capability. It is a better match than DROID or OGBench for coordination claims, because those datasets are not primarily multi-agent manipulation benchmarks.

It is also useful for comparing policy carriers such as diffusion policies, OpenVLA-like policies, or Pi-style policies under the same task registry.

## What To Be Careful About

Multi-agent results are easy to overstate. A task with multiple robots is not automatically a coordination benchmark unless success depends on interaction between agents. Report whether the task actually requires cooperation, handoff, collision avoidance, or role assignment.

Also keep scene family separate from task ID. The same task name can behave differently in a table scene and a kitchen-like scene.

## A Minimal Usage Pattern

The generic workflow is:

```text
choose task ID -> choose scene family -> choose policy -> run rollout -> save video and per-agent metrics
```

For first experiments, start with one task and one scene family. Add the second scene family only after the policy and logging are stable.

## Takeaway

RoboFactory is most valuable when the research question is coordination. It helps prevent a common mistake: using single-agent benchmarks to support multi-agent claims.
