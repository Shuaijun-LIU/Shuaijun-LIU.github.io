---
layout: blog_post
title: 'Why TD3 Came Back: Fast Off-Policy RL for Humanoid Control'
date: 2026-05-11
tags:
  - Robotics
  - Reinforcement Learning
  - Humanoid Control
  - Simulation
excerpt: 'FastTD3 is a useful reminder that off-policy RL did not disappear from robotics. It needed parallel simulation, large-batch updates, distributional critics, and a training loop designed for wall-clock speed.'
---

For a long time, the practical recipe for reinforcement learning in simulated robotics was simple: use massive parallel simulation, train with PPO, tune the reward, and wait for a deployable policy. PPO became popular for good reasons. It is stable, easy to scale across thousands of environments, and often forgiving enough for difficult locomotion tasks.

But PPO also has an awkward weakness: it is on-policy. Once the policy changes, old data quickly becomes less useful. This is acceptable when simulation is cheap and fully parallel, but it becomes limiting when we want sample reuse, demonstration-driven training, or real-world fine-tuning where every interaction is expensive.

FastTD3 is interesting because it asks a direct question: can a simple off-policy method become fast enough for modern humanoid control if we scale it the right way?

<figure class="blog-figure">
  <img src="{{ '/assets/images/blog/fasttd3/fasttd3-tasks.png' | relative_url }}" alt="FastTD3 task suite across HumanoidBench, MuJoCo Playground, and IsaacLab">
  <figcaption>FastTD3 is evaluated on humanoid and dexterous control tasks from HumanoidBench, MuJoCo Playground, and IsaacLab. Figure adapted from the FastTD3 paper source.</figcaption>
</figure>

## The Old Reputation of Off-Policy RL

Off-policy RL has always had a theoretical advantage: it can reuse data. Instead of throwing away past experience after every policy update, an off-policy method stores transitions in a replay buffer and learns from them repeatedly. This is attractive for robotics because robot data is expensive, and even simulated data can become costly when the task is complex.

The practical reputation was more mixed. In high-dimensional continuous control, off-policy methods such as DDPG, SAC, and TD3 can be sensitive to implementation details, critic instability, exploration noise, replay distribution, and reward scaling. PPO, by contrast, often gives a strong baseline with less engineering.

So the community's default split became:

| Method Family | Practical Strength | Practical Weakness |
| --- | --- | --- |
| PPO-style on-policy RL | Stable and easy to scale with many environments | Poor sample reuse and less natural for real-world fine-tuning |
| TD3/SAC-style off-policy RL | Reuses data and fits replay or demonstration settings | Historically harder to make fast and stable at humanoid scale |

FastTD3 does not claim that TD3 was secretly perfect all along. The more useful interpretation is that the surrounding systems context changed. Modern simulation stacks can run many environments in parallel, GPUs can handle large batches, and replay buffers can be fed with enough diverse data to make off-policy updates behave better.

## What FastTD3 Changes

The core recipe is intentionally plain. FastTD3 is still based on TD3: a deterministic actor, twin critics, delayed policy updates, target networks, and replay-based learning. The difference is how the old algorithm is scaled and stabilized.

The key ingredients are:

1. **Parallel simulation.** Many environments generate diverse experience quickly.
2. **Large-batch updates.** The critic sees a broad slice of replay data in each gradient step.
3. **Distributional critic.** Instead of predicting only a scalar value, the critic models a return distribution, which can make learning more stable.
4. **Careful hyperparameters.** Noise schedules, update ratios, model size, replay size, and normalization details matter.
5. **Simple implementation.** The method avoids complex asynchronous infrastructure, making it easier to reproduce and modify.

This combination is important because the bottleneck in robot RL is not only the algorithm. It is the whole training loop: environment throughput, batch construction, GPU utilization, replay freshness, and reward iteration speed.

<figure class="blog-figure">
  <img src="{{ '/assets/images/blog/fasttd3/fasttd3-design-choices.png' | relative_url }}" alt="FastTD3 design choice ablations">
  <figcaption>Several design choices matter together: parallel environments, large batch size, a distributional critic, and clipped double Q-learning. Figure adapted from the FastTD3 paper source.</figcaption>
</figure>

## Why Parallel Simulation Helps Off-Policy RL

A replay buffer is only useful if the data distribution is healthy. If a robot collects data slowly from one narrow behavior distribution, the critic can overfit to a stale or biased slice of experience. With many parallel environments, the buffer receives more varied transitions: different states, resets, contacts, falls, recoveries, and terrain conditions.

This changes the role of the large batch. A large batch is not just a bigger tensor. It becomes a way to average over a more diverse slice of robot experience. That can reduce critic noise and make deterministic policy gradients less brittle.

The tradeoff is that "large batch" is not free. It requires enough environment throughput, enough replay data, enough GPU memory, and a training loop where batch construction does not become the new bottleneck. This is why FastTD3 is better understood as an algorithm-systems recipe rather than a single trick.

## The Main Result

The reported result is striking because it targets wall-clock time, not just sample efficiency. FastTD3 solves a range of HumanoidBench tasks in under three hours on a single A100 GPU, and it is compared across HumanoidBench, IsaacLab, and MuJoCo Playground.

<figure class="blog-figure">
  <img src="{{ '/assets/images/blog/fasttd3/fasttd3-summary.png' | relative_url }}" alt="FastTD3 summary of results">
  <figcaption>The central claim is wall-clock acceleration for humanoid control across several popular benchmark suites. Figure adapted from the FastTD3 paper source.</figcaption>
</figure>

This matters because reward design in robotics is iterative. A practitioner rarely writes the final reward on the first try. They train a policy, inspect the gait, adjust penalties, re-run, and repeat. Cutting training time from tens of hours to a few hours changes how quickly a researcher can debug behavior.

<figure class="blog-figure">
  <img src="{{ '/assets/images/blog/fasttd3/fasttd3-selected-curves.png' | relative_url }}" alt="FastTD3 selected learning curves across tasks">
  <figcaption>Selected learning curves across HumanoidBench, IsaacLab, and MuJoCo Playground. The useful view is not only final score, but how quickly the method reaches a usable behavior. Figure adapted from the FastTD3 paper source.</figcaption>
</figure>

## Why This Does Not Make PPO Obsolete

The wrong conclusion would be: "FastTD3 proves PPO is outdated." That is too simple.

PPO remains a strong default when stability, implementation simplicity, and broad baseline comparability matter. It is also deeply embedded in many robot learning pipelines. FastTD3 instead shows that PPO is not the only practical wall-clock path for humanoid control.

The more precise lesson is:

- On-policy RL is still convenient when simulation is abundant and reward tuning is mature.
- Off-policy RL becomes more attractive when data reuse, demonstrations, or real-world fine-tuning matter.
- Large-scale simulation can help off-policy RL by feeding replay buffers with diverse data.
- Algorithm choice and reward design are coupled; the same reward may not produce the same behavior under different optimizers.

That last point is easy to miss. A reward that works well for PPO may produce poor gaits with FastTD3, and a reward tuned for FastTD3 may not suit PPO.

<figure class="blog-figure">
  <img src="{{ '/assets/images/blog/fasttd3/fasttd3-reward-gaits.png' | relative_url }}" alt="Different reward functions can produce different gaits for PPO and FastTD3">
  <figcaption>The paper highlights that different RL algorithms may require different reward functions. This is a practical warning: reward engineering is not algorithm-independent. Figure adapted from the FastTD3 paper source.</figcaption>
</figure>

## The Sim-to-Real Angle

Fast off-policy training is especially relevant for sim-to-real because it shortens the policy development loop. The paper includes a transfer example where a policy trained in MuJoCo Playground is deployed on a Booster T1 humanoid.

<figure class="blog-figure">
  <img src="{{ '/assets/images/blog/fasttd3/fasttd3-sim2real.png' | relative_url }}" alt="FastTD3 sim-to-real transfer to Booster T1">
  <figcaption>Sim-to-real deployment is where iteration speed becomes concrete: faster training means more chances to tune rewards, domain randomization, and deployment details. Figure adapted from the FastTD3 paper source.</figcaption>
</figure>

The key point is not that one algorithm solves sim-to-real by itself. The deployment still depends on task modeling, observation design, domain randomization, actuation details, safety checks, and reward tuning. FastTD3 makes the iteration loop cheaper, which can make those engineering steps less painful.

## What I Would Watch Next

FastTD3 points to a broader direction: off-policy RL may become more useful for robotics when it is designed together with modern simulation and deployment infrastructure.

The next questions are practical:

1. Can the same recipe handle richer observations, such as vision or tactile inputs?
2. Can replay buffers combine simulation, human demonstrations, and limited real-world rollouts?
3. How stable is the method under aggressive domain randomization?
4. Can fast off-policy training support online adaptation after deployment?
5. How much of the recipe transfers to multi-agent or distributed robot settings?

These questions matter because humanoid control is not only about one benchmark suite. It is about building an RL loop that can support repeated engineering decisions under realistic time budgets.

## Takeaway

FastTD3 is useful because it reframes an old algorithm family in a modern systems setting. TD3 did not come back because deterministic policy gradients suddenly became easy. It came back because parallel simulation, large-batch training, distributional critics, and careful implementation made off-policy RL practical enough to compete on wall-clock speed.

For robotics, that is the real lesson: algorithm design and systems design are no longer separable. The best policy optimizer is not just the one with the cleanest objective; it is the one that fits the data pipeline, simulator, hardware, reward iteration loop, and deployment plan.

## Further Reading

- [FastTD3 project page](https://younggyo.me/fast_td3/)
- [FastTD3 arXiv paper](https://arxiv.org/abs/2505.22642)
- [FastTD3 code](https://github.com/younggyoseo/FastTD3)
- [TD3: Addressing Function Approximation Error in Actor-Critic Methods](https://arxiv.org/abs/1802.09477)
- [Parallel Q-Learning: Scaling Off-Policy Reinforcement Learning Under Massively Parallel Simulation](https://arxiv.org/abs/2307.12955)
