---
layout: blog_post
title: 'What Is Replanning in Embodied AI?'
date: 2026-04-30
tags:
  - Embodied AI
  - Replanning
  - Robotics
---

Embodied AI agents do not live in a clean text box. They move through homes, labs, kitchens, warehouses, streets, or simulators that only partially reveal the state of the world. A plan that sounded correct five seconds ago can become wrong after a failed grasp, an unexpected obstacle, a newly observed object, a changed human preference, or a safety constraint that was not obvious at the start.

That is why replanning is becoming a central idea in embodied AI. It is the mechanism that turns a static "think once, act many times" pipeline into a feedback-driven loop: plan, act, observe, decide whether the plan is still valid, and revise it when needed.

<figure class="blog-figure">
  <img src="{{ '/assets/images/blog/replanning-loop.svg' | relative_url }}" alt="Diagram comparing open-loop execution with feedback-driven replanning in embodied AI">
  <figcaption>Replanning treats execution as a loop. The agent does not only ask "What should I do?" It also asks "Did that work?", "Has the world changed?", and "Is it worth spending more computation to revise the plan?"</figcaption>
</figure>

## A Simple Definition

In embodied AI, replanning is the process of updating an agent's future actions after new information arrives during execution. The new information can come from perception, success detectors, low-level controllers, a human, another robot, a simulator, or a learned world model.

The key point is that replanning is not just "planning again." It is planning again with context:

- What has already been done?
- Which subgoals are complete?
- Which action failed, and why?
- What is now visible in the scene?
- What constraints became active?
- How much time, energy, or inference budget remains?

For a household robot, the first plan for "bring me a clean mug" may be:

1. Go to the cabinet.
2. Pick up a mug.
3. Check whether it is clean.
4. Bring it to the user.

If the cabinet is empty, a rigid agent fails. A replanning agent can revise the plan: search the drying rack, ask a human, inspect the sink, or switch to another cup if the task allows it.

## Planning, Execution, and Replanning

It helps to separate three layers:

| Layer | Question | Example |
| --- | --- | --- |
| Planning | What sequence of subgoals should solve the task? | "Find mug, pick mug, deliver mug." |
| Execution | How do I perform the next action in the current state? | Navigate to the cabinet; run a grasp controller. |
| Replanning | Should the current plan be kept, repaired, or replaced? | The mug is missing, so search a nearby rack. |

Classical robotics has studied feedback, receding-horizon control, and task-and-motion planning for decades. What is new in current embodied AI is the role of large vision-language and language models as semantic planners. These models are good at proposing human-like task decompositions, but they are not automatically grounded in a robot's current abilities, observations, or safety constraints.

That creates the central tension: foundation models can write useful plans, but embodied agents need those plans to survive contact with the world.

## Why Static Plans Break

A static plan is attractive because it is simple. Ask a model once, get a list of actions, execute them. This works for short tasks in stable environments. It breaks as the horizon grows.

Long-horizon embodied tasks create several compounding problems:

- Partial observability: the agent cannot know all object locations or states before it moves.
- Non-reversible actions: after pouring, cutting, heating, opening, or moving objects, some mistakes cannot simply be undone.
- Execution uncertainty: navigation, grasping, pushing, and placing can fail even when the high-level plan is correct.
- Ambiguous language: human instructions often omit constraints that matter physically.
- Safety constraints: some plans are semantically plausible but physically unsafe.

Benchmarks such as ALFRED were designed to make this difficulty explicit: agents must follow language instructions through long, compositional household tasks with object interactions and non-reversible state changes. More recent safety-oriented benchmarks, such as SafeAgentBench and VestaBench, push this further by testing whether agents can handle hazardous, adversarial, or multi-constraint tasks.

## What Counts as Feedback?

Replanning needs feedback. The feedback does not have to be perfect, but it must say something useful about the gap between the plan and the world.

Common feedback channels include:

- Perception: object detections, scene descriptions, segmentation, maps, visual question answering.
- Controller status: whether a skill succeeded, failed, timed out, or became unsafe.
- Affordance estimates: whether a proposed action is physically possible from the current state.
- Progress monitors: which subgoals have been achieved.
- Human input: corrections, preferences, disambiguation, or explicit intervention.
- Memory: what the agent has already tried, where objects were seen, and which failures repeated.

This is why work such as SayCan matters: it shows how a language model's semantic preference can be grounded by action affordances. Inner Monologue takes another step by feeding language-form feedback, such as scene descriptions and success signals, back into the planner. LLM-Planner and FLARE similarly highlight the need for plans that are updated using current environmental observations rather than only linguistic common sense.

## Different Forms of Replanning

Not all replanning systems are the same. A useful taxonomy is:

1. Event-triggered replanning: replan only when something important happens, such as a failed skill or a new object observation.
2. Periodic replanning: replan every fixed number of steps, similar to receding-horizon control.
3. Hierarchical replanning: update high-level subgoals less often, while low-level controllers adapt continuously.
4. Repair-based replanning: keep most of the old plan and patch the broken step.
5. Full replanning: discard the old plan and generate a new one from the current state.
6. Budgeted replanning: decide whether replanning is worth its computational, latency, or energy cost.

The last one is especially important. Replanning can improve robustness, but it is not free. A large model call can be slow, expensive, and unstable. A robot with limited onboard compute, a UAV with limited battery, or a fleet of agents sharing network resources cannot simply replan after every observation.

The practical question is not "Should we replan?" but "When is replanning worth it?"

## Why We Should Care

Replanning is worth attention because it sits at the boundary between impressive demos and deployable embodied systems.

First, it is a robustness problem. A robot that cannot recover from minor mismatches is not useful outside a scripted demo. Replanning lets an agent use failures as information rather than treating them as terminal states.

Second, it is a grounding problem. Language models can produce plans that sound reasonable but ignore the specific robot, room, object state, or safety constraint. Replanning connects semantic reasoning to current observations and action feasibility.

Third, it is a safety problem. Embodied agents can affect the physical world. If an instruction, intermediate state, or generated action becomes hazardous, the system needs a mechanism to stop, revise, or ask for clarification.

Fourth, it is an efficiency problem. Long-horizon behavior requires selective computation. The best agent is not the one that thinks the most; it is the one that spends planning effort when the expected value of revising the plan is high.

Finally, it is a coordination problem. In multi-agent systems or distributed robot deployments, replanning is how agents adapt to each other's actions, communication delays, changing task assignments, and limited compute resources.

## Open Research Questions

Several questions are still open:

- Triggering: what signal should cause a replan?
- State summarization: what should be passed to the planner without overwhelming it?
- Granularity: should the system revise a single action, a subgoal, or the whole task plan?
- Cost modeling: how should latency, compute, energy, and risk be traded against expected improvement?
- Evaluation: should we measure only task success, or also recovery quality, wasted actions, unsafe attempts, and planning cost?
- Multi-agent replanning: how should agents coordinate local plan revisions without creating global conflicts?

These questions make replanning a rich direction for embodied intelligence. It is not only a patch for failure. It is a way to make planning interactive, grounded, and resource-aware.

## Further Reading

- [ReAct: Synergizing Reasoning and Acting in Language Models](https://openreview.net/forum?id=WE_vluYUL-X). A general reasoning-and-acting framework where reasoning traces help update plans and handle exceptions.
- [SayCan: Grounding Language in Robotic Affordances](https://say-can.github.io/). A robot planning system that combines language-model scores with affordance estimates for feasible skill selection.
- [Inner Monologue: Embodied Reasoning through Planning with Language Models](https://innermonologue.github.io/). A closed-loop approach that feeds environment feedback into language-model planning.
- [LLM-Planner: Few-Shot Grounded Planning for Embodied Agents](https://dki-lab.github.io/LLM-Planner/). A few-shot planner that updates high-level plans using feedback from the environment.
- [FLARE: Multi-Modal Grounded Planning and Efficient Replanning](https://ojs.aaai.org/index.php/AAAI/article/view/32455). A 2025 AAAI paper focused on environment-grounded planning and adaptive replanning.
- [ALFRED](https://a11y2.apps.allenai.org/paper?id=95061c101ff643dbff73945a8fb2e6ee8e2d010a). A long-horizon household instruction-following benchmark with object interactions and non-reversible state changes.
- [SafeAgentBench](https://safeagentbench.github.io/) and [VestaBench](https://aclanthology.org/2025.emnlp-industry.149/). Benchmarks that emphasize safety-aware and multi-constraint embodied planning.
