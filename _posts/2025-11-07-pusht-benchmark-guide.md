---
layout: blog_post
title: "PushT: Why a Tiny 2D Control Task Is Still Useful"
date: 2025-11-07
tags:
  - Benchmark
  - Control
  - Diffusion Policy
excerpt: "PushT is a single 2D pushing benchmark, but that simplicity makes it useful for debugging action chunks, policy outputs, and evaluation pipelines."
---

PushT is a small 2D contact-rich control task that became widely used through the Diffusion Policy evaluation suite. The agent must push a T-shaped object into a target T-shaped region. It is not a broad manipulation benchmark, and it should not be presented as one. Its value is narrower and more useful: it is a fast diagnostic for whether a policy can produce coherent closed-loop action sequences.

<figure class="blog-figure">
  <img src="{{ '/assets/images/blog/benchmarks/tasks/pusht-task-examples.jpg' | relative_url }}" alt="PushT task mockup showing a T-shaped object and target region">
  <figcaption>PushT task mockup from the Diffusion Policy source package. The visual simplicity is the point: it isolates temporal action quality under contact.</figcaption>
</figure>

## What the Paper Context Adds

PushT is not a large benchmark suite by itself. In the Diffusion Policy paper, it is part of a broader evaluation over multiple manipulation tasks. That context matters: PushT is best treated as a diagnostic task for closed-loop action generation, not as evidence for general-purpose robot intelligence.

This is also why it should be used carefully. A method that performs well on PushT may only have learned a narrow kind of 2D contact control. A method that performs poorly on PushT, however, is giving a much stronger warning: something may be wrong with the action representation, control horizon, normalization, rollout loop, or temporal consistency of the policy.

## Why I Still Like It

Small benchmarks are easy to dismiss, but they can be useful precisely because they are small. In a full robotics stack, failure is ambiguous. A VLA model can fail because of language grounding, visual preprocessing, camera mismatch, embodiment mismatch, action scaling, simulator settings, object geometry, or the success detector. PushT removes most of that noise.

My own view is that PushT is best used like a microscope. It is not the final claim. It is the thing you put under the model early to see whether the basic temporal behavior makes sense. If a sequence policy jitters, over-commits, stalls, or produces actions with the wrong scale, PushT usually makes that visible quickly.

The task is also a good reminder that contact-rich control is not solved by making the benchmark visually impressive. Even in a simple 2D environment, the policy must manage partial progress. A bad push can rotate the object into an inconvenient pose, and later actions must recover. That makes the task more informative than a one-step reaching target, even though it is much smaller than household manipulation.

## What PushT Actually Tests

PushT mostly tests whether a policy can turn observations into a temporally coherent sequence of continuous actions under contact. It is especially useful for checking:

- action normalization;
- action chunk length;
- diffusion or sequence policy outputs;
- closed-loop correction after imperfect pushes;
- whether rollout videos and metrics agree with each other;
- whether a policy is smooth, decisive, and recoverable rather than merely producing plausible single actions.

This is a narrower claim than "robot manipulation." It is closer to "does this policy interface produce usable control behavior at all?"

## How I Would Use It

I would use PushT near the beginning of a policy pipeline, especially for methods that predict action chunks, diffusion trajectories, or other short-horizon action sequences. It is a good place to check whether the model's output distribution has the right scale and whether the closed-loop behavior remains stable after several steps.

I would not spend too much time optimizing a leaderboard-style number on it. Once the policy is stable, the next question should be whether the same design survives more realistic observation, task, and embodiment variation. PushT is a gate, not a destination.

When debugging, change only one variable at a time. Action horizon, normalization, seed, checkpoint, and observation preprocessing can all change the rollout. If several knobs move together, PushT stops being a clean diagnostic and becomes just another confusing experiment.

## Practical Usage Notes

The cleanest mental model is "one task, many policy interfaces." PushT is often used through evaluation wrappers that vary observation history, action horizon, chunk size, normalization, checkpoint, and seed. Those details define the experiment as much as the task itself.

For a fair PushT run, I would record:

- the environment wrapper and task variant;
- observation history length and action prediction horizon;
- whether actions are normalized, clipped, or denormalized by the evaluator;
- seed count, score aggregation, and success threshold;
- JSON or CSV summaries together with rollout videos.

The videos are not cosmetic. PushT can show the difference between a policy that solves the task through smooth correction and one that occasionally gets a lucky collision. If a method claims better temporal modeling, the rollout should visibly support that claim.

## What It Cannot Tell You

PushT does not tell you whether a robot understands language. It does not test object-category generalization, household interaction, real-robot robustness, multi-stage task planning, or safe deployment. It also does not reveal much about semantic perception because the visual structure is intentionally simple.

This is not a weakness if the claim is scoped correctly. The problem starts when a tiny diagnostic task is used as if it validates a broad robotics story. A good PushT result should usually be followed by harder manipulation suites, language-conditioned tasks, real robot data, or at least a more diverse simulated benchmark.

## How to Read Results

For PushT, I care about the rollout videos as much as the final score. A policy that reaches the target through smooth correction is different from one that succeeds by unstable lucky contacts. The aggregate number should be paired with qualitative inspection, failure cases, and sensitivity to action horizon.

The most useful question is not "is the benchmark hard enough?" The useful question is "what failure does this benchmark isolate?" For PushT, the answer is temporal action quality under simple contact dynamics. That is a small question, but it is a question worth answering before moving to larger robotics experiments.

## Paper Source

This note was revised from the paper and its LaTeX source package: <a href="https://arxiv.org/abs/2303.04137">Diffusion Policy: Visuomotor Policy Learning via Action Diffusion</a>.
