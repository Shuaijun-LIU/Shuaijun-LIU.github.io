---
layout: blog_post
title: 'A Small Multi-Agent GPU Deployment Demo'
date: 2026-06-21
tags:
  - Multi-Agent Systems
  - GPU Deployment
  - LLM Inference
  - Systems
excerpt: 'A practical look at a local demo that tests how eight role-specialized LLM agents behave under different GPU placement and orchestration strategies.'
---

Multi-agent systems often look simple at the diagram level: define several roles, give each role a task, then let the agents collaborate. The engineering reality is less tidy. If every agent owns a local language model, the system is no longer only an agent orchestration problem. It is also a GPU memory, process scheduling, model loading, and monitoring problem.

This demo is a small attempt to make that engineering layer visible. It uses eight role-specialized agents and compares several ways to run them on local GPUs. The goal is not to build a production serving system. The goal is to answer a more basic question:

> If we want multiple local LLM agents to run together, what breaks first: memory, latency, parallelism, or orchestration?

<figure class="blog-figure">
  <img src="{{ '/assets/images/blog/multi-agent-gpu-demo/execution-modes.svg' | relative_url }}" alt="Six execution modes used in the multi-agent GPU demo">
  <figcaption>The demo varies the deployment pattern while keeping the agent set fixed: independent GPU placement, automatic expansion after OOM, sequential execution, shared-model execution, cooperative chaining, and leader-worker hierarchy.</figcaption>
</figure>

## What the Demo Builds

The demo defines eight agents with different software-product roles:

- Product Manager
- System Architect
- AI Researcher
- Data Engineer
- Backend Developer
- Frontend Developer
- Security Specialist
- DevOps Engineer

Each agent is backed by the same locally cached Mistral-7B-Instruct-v0.3 model. The role and task abstractions come from CrewAI, while the local Hugging Face text-generation pipeline is wrapped through LangChain's `HuggingFacePipeline` interface. In other words, CrewAI provides the agent and crew structure, LangChain provides the LLM adapter layer, and Hugging Face Transformers plus PyTorch provide the actual model loading and CUDA execution.

The project then runs these agents under six execution modes:

| Mode | Main idea | What it tests |
| --- | --- | --- |
| Parallel Multi-GPU | Eight processes, one model copy per agent, one GPU per agent | Clean hardware isolation and true parallelism |
| Auto-expanded Parallel | Start with too few GPUs, retry after OOM, increase GPU count | Minimum GPU requirement under independent model copies |
| Sequential Single-GPU | Run agents one by one on one GPU | Memory-safe baseline with no task-level parallelism |
| Shared Model Single-GPU | Load one model once and share it across agents using threads | Memory efficiency versus compute contention |
| Cooperative Chain | Agents run sequentially and pass context forward | Role handoff and context accumulation |
| Hierarchical Leader-Worker | Leader plans, workers execute in parallel, leader summarizes | Coordination plus parallel worker execution |

Four modes use the same task prompt:

> Explain the concept and challenges of multi-agent multi-GPU execution.

The cooperative and hierarchical modes use different task structures because they are meant to demonstrate workflow patterns rather than serve as strict apples-to-apples latency baselines. That distinction matters when reading the numbers.

## The Technology Stack

The stack is intentionally small and inspectable.

CrewAI is used for the agent abstraction: each agent has a role, goal, and backstory, and each task is assigned to a particular agent. This is useful for quickly expressing role-specialized workflows without writing a custom planner. CrewAI's own documentation describes agents as autonomous units that perform tasks and can collaborate inside crews, which matches the structure of this demo.

LangChain is used as the bridge between agent orchestration and the local Hugging Face model. The demo wraps a Transformers text-generation pipeline as a LangChain-compatible LLM, then passes that object into each CrewAI agent.

Transformers and PyTorch handle the actual local inference path. The model loader uses:

```python
AutoTokenizer.from_pretrained(..., local_files_only=True)
AutoModelForCausalLM.from_pretrained(
    ...,
    device_map={"": f"cuda:{device_id}"},
    torch_dtype="auto",
    local_files_only=True,
)
```

The important part is `device_map={"": f"cuda:{device_id}"}`. Each model instance is pinned to a chosen CUDA device. This makes the GPU placement explicit, rather than leaving placement as a side effect of whichever process first touches CUDA.

Python multiprocessing is used for the independent-agent modes. The code sets the start method to `spawn`, which is the safer choice around CUDA initialization. PyTorch's multiprocessing notes specifically warn about CUDA and process start methods, and this demo follows that direction by creating each GPU-bound agent inside its worker process.

Python threading is used only in the shared-model single-GPU mode. That is a deliberate tradeoff: sharing a complex GPU-backed PyTorch model object across processes is not a simple or cheap operation. Threads let all agents reference the same model instance, but they also force all calls through one GPU-backed pipeline.

Finally, GPU monitoring is implemented with `pynvml`, the Python binding around NVIDIA's NVML. The monitor records GPU utilization, memory utilization, used memory, free memory, and a simple memory-change-rate estimate. This is enough to observe whether a mode is memory-bound, compute-bound, or simply serialized by the execution pattern.

## Why Multiprocessing Matters Here

For CPU-heavy Python code, people often talk about the GIL. For this demo, the more important issue is isolation. Each parallel agent needs to load a model, initialize CUDA state, and run inference without accidentally sharing the wrong device context.

In the independent parallel modes, each worker process:

1. Loads its own agent builder.
2. Loads a model copy on a specific GPU.
3. Runs a CrewAI task.
4. Reports model-load time, inference time, success or failure, and GPU snapshots.

This design is heavier than a production inference server, but it is useful for a demo because it makes one thing clear: independent local agents are expensive if each one owns a full model copy.

## What Happened in the Experiments

<figure class="blog-figure">
  <img src="{{ '/assets/images/blog/multi-agent-gpu-demo/multi-agent-gpu-results.svg' | relative_url }}" alt="Execution time and latency decomposition for the multi-agent GPU demo">
  <figcaption>Runtime and average-agent latency from the recorded JSON results. The strict parallel baselines use the same task prompt; cooperative and hierarchical modes are workflow demonstrations with different task structures.</figcaption>
</figure>

The most direct result is that parallel multi-GPU execution is fastest when every agent gets its own device. The eight-agent multi-GPU mode finished in 27.62 seconds, with average agent latency around 16.32 seconds. This is the cleanest setting: eight processes, eight model loads, and eight isolated GPU placements.

The auto-expanded parallel mode is more interesting. It starts as an intentionally aggressive setup: try to run eight independent model-owning agents with too few GPUs, detect OOM failures, and retry with more GPUs. In this run:

| Attempt | Result | Duration |
| --- | --- | --- |
| 1 GPU | Failed with OOM | 15.38s |
| 2 GPUs | Failed with OOM | 16.15s |
| 3 GPUs | Succeeded | 49.57s |

The final recorded runtime for the mode is 84.16 seconds because it includes the failed attempts. The useful takeaway is not merely "three GPUs worked." It is that the demo can empirically estimate a minimum GPU count for a given agent/model/task configuration.

Sequential single-GPU execution is slower overall, but each individual agent has low latency once it gets the GPU. It finished in 110.90 seconds, with average agent latency around 13.65 seconds. This tells us that the single-GPU sequential path is not inefficient per agent. It is slow because the work is serialized.

The shared-model single-GPU mode is the opposite tradeoff. It loads only one model copy, so it is memory-friendly. However, all eight agents contend for one shared GPU-backed pipeline. The mode completed successfully, but total runtime rose to 259.61 seconds and average agent latency was about 255.81 seconds. This is a good reminder that "sharing the model" solves one bottleneck while creating another.

The cooperative and hierarchical modes are best read as workflow prototypes. The cooperative chain demonstrates context passing across role-specialized agents. The hierarchical mode demonstrates a leader that plans, workers that execute, and the leader that summarizes. They are useful for studying orchestration patterns, but their task definitions differ from the strict baseline prompt, so their timings should not be over-interpreted as pure system performance comparisons.

## Main Lessons

The first lesson is that local multi-agent systems need explicit resource placement. An agent framework can express roles and tasks, but it does not automatically solve GPU allocation. The demo has to decide which process owns which CUDA device and whether model copies are independent or shared.

The second lesson is that model loading is part of latency. The demo records model-load time and inference time separately, which is important. In the multi-GPU run, average model loading took about 5.30 seconds per agent and average inference took about 10.90 seconds. In the sequential single-GPU run, average model loading was about 3.16 seconds and inference was about 10.49 seconds. Loading costs are not noise; they shape the deployment strategy.

The third lesson is that memory-safe does not mean fast. Sequential execution and shared-model execution both avoid the worst OOM behavior, but for different reasons. Sequential execution avoids concurrent model copies. Shared-model execution avoids duplicate model copies. Neither gives the same throughput as independent multi-GPU execution.

The fourth lesson is that workflow quality and system performance should be evaluated separately. Cooperative and hierarchical agents may produce more structured outputs for complex tasks, but they change the task graph. Once the task graph changes, runtime comparisons need careful interpretation.

## What This Is Not Yet

This demo is useful, but it is not a production multi-agent serving architecture.

It does not implement continuous batching, KV-cache scheduling, request preemption, tensor parallelism, or a dedicated model-serving layer. Systems such as vLLM are designed around those serving problems, including tensor parallel inference when a model needs multiple GPUs. This demo instead launches local model copies directly inside worker processes, which is simpler and easier to inspect but less efficient.

It also does not use a cluster scheduler or actor runtime. A production version might map agents to long-lived Ray actors, keep model instances warm, and schedule tasks onto actors according to GPU availability. Ray's actor abstraction is a natural next step because each actor can hold state, including a model instance, across method calls.

Finally, this is a one-run demo. The next version should run repeated trials, separate cold-start from warm-start latency, normalize token counts across agents, record peak memory per assigned GPU, and measure output quality in addition to runtime.

## Possible Next Steps

There are several natural extensions.

First, keep model workers warm. Instead of loading a model inside every experiment attempt, create persistent GPU workers and send tasks to them. That would separate cold-start cost from steady-state throughput.

Second, add a scheduler. The auto-expansion experiment already asks a scheduling question: how many GPUs are needed? A better system could choose between sequential, shared, and parallel execution based on memory budget, deadline, and task priority.

Third, replace independent full model copies with a serving backend. vLLM-style continuous batching and tensor parallelism would make the experiment closer to a real inference service.

Fourth, evaluate the agent workflow. The current metrics are mostly systems metrics: latency, OOM, model loads, and GPU utilization. For multi-agent research, we also need task quality, consistency across agents, and whether collaboration actually improves the result.

The demo is therefore a good starting point: it exposes the practical bottlenecks before the system becomes too complicated. The central message is simple: multi-agent LLM deployment is not only about making agents talk to each other. It is also about deciding where the models live, how often they are loaded, how GPU memory is shared, and when parallelism is actually worth its cost.

## Further Reading

- [CrewAI Agents](https://docs.crewai.com/en/concepts/agents) and [CrewAI Crews](https://docs.crewai.com/en/concepts/crews) for the agent, task, and crew abstraction.
- [LangChain Agents](https://docs.langchain.com/oss/python/langchain/agents) and [LangChain Tools](https://docs.langchain.com/oss/python/langchain/tools) for the broader agent interface and tool-calling context.
- [Hugging Face Accelerate: Big Model Inference](https://huggingface.co/docs/accelerate/en/usage_guides/big_modeling) for `device_map`-style model placement and memory-aware loading.
- [PyTorch Multiprocessing](https://docs.pytorch.org/docs/stable/multiprocessing.html) and [Multiprocessing Best Practices](https://docs.pytorch.org/docs/stable/notes/multiprocessing.html) for CUDA-aware process management.
- [NVIDIA NVML](https://developer.nvidia.com/management-library-nvml) and the [NVML API Reference](https://docs.nvidia.com/deploy/nvml-api/index.html) for GPU monitoring.
- [vLLM Parallelism and Scaling](https://docs.vllm.ai/en/v0.20.1/serving/parallelism_scaling.html) for production-oriented multi-GPU inference patterns.
- [Ray Actors](https://docs.ray.io/en/latest/ray-core/actors.html) for long-lived stateful workers that could host persistent model instances.
