---
layout: blog_post
title: 'From VLM to VLA to WAM: What Changes When Models Start Acting?'
date: 2026-03-25
tags:
  - Embodied AI
  - Vision-Language-Action
  - World Models
  - Robotics
---

The recent path from vision-language models to robot foundation models can be read as a sequence of increasingly strict commitments.

A **vision-language model** can look at an image and answer questions about it. A **vision-language-action model** is asked to turn that understanding into robot actions. A **world action model** goes one step further: it does not only ask "what should I do now?", but also "what will the world look like if I do it?"

That extra question changes the problem. Once a model acts in the physical world, the output is no longer harmless text. It can move a gripper, collide with an object, push the wrong item, or waste time by replanning too often. Acting systems therefore need a tighter link between semantic understanding, physical prediction, and closed-loop control.

<figure class="blog-figure">
  <img src="{{ '/assets/images/blog/vlm-vla-wam-stack.svg' | relative_url }}" alt="A conceptual stack from VLM to VLA to WAM">
  <figcaption>VLMs ground language in perception. VLAs add an action interface. WAMs make future world state part of the modeling target, so action is tied to predicted physical consequence.</figcaption>
</figure>

## The Short Version

At a high level, the three model families answer different questions:

<div class="blog-comparison-grid">
  <div class="blog-mini-card blog-mini-blue">
    <h3>VLM</h3>
    <p><strong>Question:</strong> What is in the scene?</p>
    <p><strong>Output:</strong> Text, labels, captions, answers, or plans.</p>
  </div>
  <div class="blog-mini-card blog-mini-green">
    <h3>VLA</h3>
    <p><strong>Question:</strong> What action should the robot take?</p>
    <p><strong>Output:</strong> Robot commands, action tokens, or short action chunks.</p>
  </div>
  <div class="blog-mini-card blog-mini-amber">
    <h3>WAM</h3>
    <p><strong>Question:</strong> What action should the robot take, and what future will it create?</p>
    <p><strong>Output:</strong> Actions jointly modeled with future observations, states, or video.</p>
  </div>
</div>

This distinction is more than naming. It changes the training data, the loss function, the inference loop, and the failure modes.

## VLMs: Understanding Without Physical Commitment

The first step is visual grounding. Models such as [CLIP](https://arxiv.org/abs/2103.00020) showed that image representations can be learned at scale from image-text pairs, enabling flexible zero-shot recognition through language. Later multimodal instruction-following systems such as [LLaVA](https://arxiv.org/abs/2304.08485) made the interface more conversational: an image enters the model, a human asks a question, and the model replies in text.

For robotics, this is powerful but incomplete. A VLM can often identify a red mug, infer that a sponge is useful for cleaning, or describe that a drawer is open. It may even produce a high-level plan such as "pick up the mug, move it to the sink, and release it." But the model is still outside the control loop. It is not directly responsible for the motion, timing, contact, or recovery behavior.

That difference matters because the physical world is not only semantic. A robot needs to know where the mug is, how it can be grasped, how the gripper should approach it, what to do if the mug slips, and when a plan has become invalid. VLMs provide useful priors, but the action interface is missing.

## VLA Models: Turning Understanding Into Control

Vision-language-action models close that gap by making action a first-class output. Instead of producing only text, the model maps camera observations, language instructions, and sometimes robot state into a robot command.

A simplified VLA objective looks like this:

$$
p(a_t \mid o_t, l)
$$

where \(o_t\) is the current observation, \(l\) is the language instruction, and \(a_t\) is the next action or action chunk. Different systems instantiate this idea differently. Some tokenize actions so they can be generated like language. Others attach continuous action heads, diffusion policies, or flow-matching heads.

Several systems are useful landmarks. [RT-1](https://arxiv.org/abs/2212.06817) studied scalable robot transformer policies trained on diverse real robot data. [PaLM-E](https://arxiv.org/abs/2303.03378) connected large language models to embodied sensory inputs for reasoning and planning. [RT-2](https://arxiv.org/abs/2307.15818) made the VLA framing especially concrete by co-training web-scale vision-language tasks with robot trajectories, letting web knowledge transfer into end-to-end robotic control. [Open X-Embodiment](https://arxiv.org/abs/2310.08864) then pushed the data question by aggregating demonstrations across many robots. [Octo](https://arxiv.org/abs/2405.12213), [OpenVLA](https://arxiv.org/abs/2406.09246), and [pi0](https://arxiv.org/abs/2410.24164) made the generalist robot policy direction more practical and open.

The key conceptual shift is that the model is no longer just explaining the world. It is participating in it.

## What Actually Changes When a Model Acts?

The jump from VLM to VLA creates five new pressures.

First, **time becomes part of correctness**. A caption can be late and still be useful. A robot action that arrives too late may miss a moving object or make closed-loop control unstable.

Second, **small errors compound**. A slightly wrong description may be corrected in a follow-up prompt. A slightly wrong grasp can knock over the object, making the next observation harder than the original one.

Third, **the output space becomes embodiment-specific**. A sentence is mostly platform-independent. An action depends on the robot's arm, gripper, camera placement, controller, and control frequency.

Fourth, **evaluation becomes physical**. Text accuracy, VQA accuracy, or caption quality cannot tell us whether the robot finishes the task safely. We need success rate, robustness, recovery behavior, latency, and generalization under distribution shift.

Fifth, **planning and execution become entangled**. The model must decide not only what goal is intended, but how much to think before acting, when to replan, and how to trade off semantic reasoning against low-level control frequency.

These pressures explain why VLA systems are not simply "VLMs with action tokens." Once the output changes the world, the model becomes part of a dynamical system.

## Why VLA May Still Be Too Reactive

Many VLA policies can be described as observation-to-action mappings. They see the current scene and instruction, then output an action. This can work well when the correct action is visible from the current observation and the task horizon is short.

But some failures require explicit prediction. Consider a robot asked to move a cup behind a plate, open a drawer before placing an object inside, or coordinate with another robot in a narrow workspace. The action is not only a response to the current image; it is a bet about how the world will evolve.

Classical world-model thinking already emphasized this idea. In [World Models](https://arxiv.org/abs/1803.10122), an agent learns a compressed model of the environment and can train behavior inside imagined rollouts. In [DreamerV3](https://arxiv.org/abs/2301.04104), the agent learns a world model and improves behavior by imagining future scenarios. The embodied foundation model question is how to combine that predictive idea with the semantic generality of VLMs and VLAs.

This is where WAMs enter the story.

<figure class="blog-figure">
  <img src="{{ '/assets/images/blog/vlm-vla-wam-timeline.svg' | relative_url }}" alt="Timeline from VLMs to VLAs and WAMs">
  <figcaption>A compact timeline of representative ideas before March 25, 2026. The important trend is not just larger models, but a shift from recognition, to action generation, to action-conditioned future modeling.</figcaption>
</figure>

## WAMs: Predictive Action Models

In this post, I use **World Action Model** in a narrow embodied-AI sense: a model that links action generation with prediction of future world states. A simplified target is:

$$
p(a_t, o_{t+1:t+k} \mid o_t, l)
$$

Instead of predicting only the next action, the model also predicts what the next observations, states, or video frames may look like under that action. This future prediction can serve several roles:

1. It can teach the model physical dynamics during training.
2. It can provide a stronger representation of contact, motion, and object permanence.
3. It can support planning by comparing imagined futures before execution.
4. It can expose when the model's intended action is physically implausible.

[DreamZero](https://arxiv.org/abs/2602.15922) is an early example of this framing. It describes WAMs as models that learn physical dynamics by predicting both future world states and actions, using video as a dense representation of how the world evolves. The paper argues that this can improve generalization to unseen physical motions and environments compared with standard VLA policies.

The idea is attractive, but it also raises a systems question: do we need to generate future video at test time, or is video prediction mainly useful as a training signal? [Fast-WAM](https://arxiv.org/abs/2603.16666) asks exactly this. Its result suggests that video co-training may matter more than explicit future imagination during inference, while skipping test-time future generation can reduce latency.

That distinction is important. A WAM is not automatically practical just because it predicts futures. If imagination is slow, the robot may become less responsive. The useful question is not "should the model imagine?", but "where should prediction enter the system: training, representation learning, planning, or every control step?"

## The Practical Trade-Off

The VLM-to-VLA-to-WAM story is not a clean replacement chain. Each layer keeps something useful and adds a new burden.

<div class="blog-note">
  <strong>VLM:</strong> strong semantic prior, weak physical commitment.<br>
  <strong>VLA:</strong> grounded action output, but often reactive.<br>
  <strong>WAM:</strong> action tied to predicted consequence, but with extra compute and modeling complexity.
</div>

For real robots, the strongest design may combine all three. A VLM-like backbone can provide semantic knowledge. A VLA head can produce fast action chunks. A WAM-style objective can teach the model richer physical representations. A separate runtime policy can decide when explicit future imagination is worth the latency.

This also connects to deployment. A large semantic model may run offboard, a smaller action model may run on the robot, and a predictive module may be used only at key decision points. In long-horizon tasks, the system must allocate compute across fast control, replanning, and predictive simulation.

## A Useful Mental Model

Here is the simplest way I think about the hierarchy:

- **VLMs** are useful when the main uncertainty is semantic: "What am I seeing?"
- **VLAs** are useful when the main uncertainty is control: "What should I do next?"
- **WAMs** are useful when the main uncertainty is consequence: "What will happen if I do this?"

Robotics needs all three. A robot that only understands language cannot act. A robot that only acts reactively can fail when the current frame is misleading. A robot that always imagines futures may be too slow for real-time control.

The interesting research problem is therefore not just choosing one acronym. It is designing the right loop:

$$
\text{understand} \rightarrow \text{act} \rightarrow \text{predict} \rightarrow \text{observe} \rightarrow \text{replan}
$$

## Takeaway

The move from VLM to VLA to WAM is a move from interpretation to intervention. VLMs teach models to connect words and pixels. VLAs teach them to output actions. WAMs ask them to connect those actions to future physical consequences.

That last step is where embodied AI becomes especially interesting. Acting agents need semantics, but semantics alone is not enough. They need fast control, uncertainty-aware replanning, data-efficient adaptation, and enough predictive structure to avoid treating the physical world as a sequence of unrelated images.

The open question is where prediction should live. Should it be an explicit test-time simulator, a training-time representation learner, a planner used only at decision bottlenecks, or all of the above? For practical robots, the answer will likely depend on the task horizon, latency budget, hardware, and cost of failure.

## Further Reading

- [CLIP: Learning Transferable Visual Models From Natural Language Supervision](https://arxiv.org/abs/2103.00020)
- [Visual Instruction Tuning / LLaVA](https://arxiv.org/abs/2304.08485)
- [RT-1: Robotics Transformer for Real-World Control at Scale](https://arxiv.org/abs/2212.06817)
- [PaLM-E: An Embodied Multimodal Language Model](https://arxiv.org/abs/2303.03378)
- [RT-2: Vision-Language-Action Models Transfer Web Knowledge to Robotic Control](https://arxiv.org/abs/2307.15818)
- [Open X-Embodiment: Robotic Learning Datasets and RT-X Models](https://arxiv.org/abs/2310.08864)
- [Octo: An Open-Source Generalist Robot Policy](https://arxiv.org/abs/2405.12213)
- [OpenVLA: An Open-Source Vision-Language-Action Model](https://arxiv.org/abs/2406.09246)
- [pi0: A Vision-Language-Action Flow Model for General Robot Control](https://arxiv.org/abs/2410.24164)
- [World Models](https://arxiv.org/abs/1803.10122)
- [DreamerV3: Mastering Diverse Domains through World Models](https://arxiv.org/abs/2301.04104)
- [DreamZero: World Action Models are Zero-shot Policies](https://arxiv.org/abs/2602.15922)
- [Fast-WAM: Do World Action Models Need Test-time Future Imagination?](https://arxiv.org/abs/2603.16666)
