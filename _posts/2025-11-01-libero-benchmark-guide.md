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

LIBERO is a benchmark for lifelong robot learning from language-conditioned manipulation tasks. The paper is useful because it separates several kinds of generalization pressure instead of treating tabletop manipulation as one monolithic success-rate number.

<figure class="blog-figure">
  <img src="{{ '/assets/images/blog/benchmarks/papers/libero-paper-figure.jpg' | relative_url }}" alt="LIBERO benchmark suite overview from the paper">
  <figcaption>Paper figure from the <a href="https://arxiv.org/abs/2306.03310">LIBERO</a> source package, showing the benchmark suites and the lifelong-learning questions the paper was designed to study.</figcaption>
</figure>

## What the Paper Contributes

The core design is a set of procedurally generated task suites for language-conditioned manipulation. The paper highlights four major suites:

| Suite | What it stresses |
| --- | --- |
| LIBERO-Spatial | Generalization over spatial relations and object placements |
| LIBERO-Object | Generalization over object identity and visual variation |
| LIBERO-Goal | Generalization over goal predicates |
| LIBERO-100 | A larger task set for broader lifelong-learning evaluation |

This structure is why LIBERO is a good benchmark for vision-language-action models. A policy must connect language, perception, action, and a task-level success predicate, while the evaluation can isolate which kind of transfer is breaking.

## How to Use It

Use LIBERO when the claim involves language-conditioned manipulation, lifelong learning, VLA fine-tuning, or controlled transfer across objects, goals, and layouts. A minimal exploration usually starts by loading a suite and inspecting the task language:

```python
from libero.libero import benchmark

suite = benchmark.get_benchmark_dict()["libero_10"]()
task = suite.get_task(0)
print(task.language)
```

For a real experiment, also record the suite name, observation mode, camera preprocessing, action scaling, initial-state protocol, and success predicate. Those details matter because the benchmark is often used to compare small changes in policy architecture or test-time strategy.

## What to Look For

The paper frames LIBERO as more than a task collection. It is a way to ask whether a method can keep learning across a stream of related manipulation problems. When reading a LIBERO result, check whether the method improves uniformly or only on one suite. For example, an object-centric improvement may not help with goal-predicate transfer.

It is also worth inspecting rollout videos. A single failure rate can hide different problems: language grounding, perception, object contact, action drift, or a strict predicate that does not match visual progress.

## Limits

LIBERO is simulated and tabletop-oriented. Strong performance does not by itself prove real-robot reliability, household interaction, multi-arm coordination, or robust deployment under uncontrolled scene changes.

## Paper Source

This note was revised from the paper and its LaTeX source package: <a href="https://arxiv.org/abs/2306.03310">LIBERO: Benchmarking Knowledge Transfer for Lifelong Robot Learning</a>.
