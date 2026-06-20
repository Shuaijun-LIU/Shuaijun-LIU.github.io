---
layout: blog_post
title: 'LoRA: Fine-Tuning Large Models with Low-Rank Updates'
date: 2024-05-08
tags:
  - Large Language Models
  - Fine-Tuning
  - PEFT
---

Fine-tuning a large language model sounds straightforward: take a pretrained model, train it on a smaller task-specific dataset, and obtain a model that behaves better for the target use case. The difficulty is that "the model" may contain billions of parameters. Updating all of them is expensive, storing a separate full copy for every downstream task is wasteful, and serving many task-specific variants quickly becomes operationally messy.

Low-Rank Adaptation, usually called **LoRA**, is a simple idea that became one of the standard tools for parameter-efficient fine-tuning. Instead of changing the entire pretrained weight matrix, LoRA freezes the original model and learns a small low-rank update. The result is a compact adapter that can be trained, stored, shared, merged, and swapped much more cheaply than a full model checkpoint.

<figure class="blog-figure">
  <img src="{{ '/assets/images/blog/lora-low-rank-update.svg' | relative_url }}" alt="LoRA represents a weight update with two small low-rank matrices">
  <figcaption>LoRA keeps the pretrained weight matrix frozen and learns a low-rank residual update. In practice, the trainable matrices are much smaller than the original layer.</figcaption>
</figure>

## The Problem with Full Fine-Tuning

Suppose a model contains a weight matrix $W$ inside an attention or feed-forward layer. In full fine-tuning, training directly changes $W$. This gives the optimizer maximum freedom, but it also means every task needs its own copy of all updated weights.

That creates three practical problems.

First, training memory is high. Fine-tuning does not only store model weights. It also needs gradients, optimizer states, activations, and often mixed-precision copies. Adam-style optimizers can multiply the memory footprint substantially.

Second, checkpoint storage is high. A full fine-tuned model is often almost the same size as the base model. If a team has one model for summarization, another for customer support, and another for domain-specific extraction, the storage cost grows linearly with the number of tasks.

Third, deployment becomes awkward. Serving ten fine-tuned variants may require ten large checkpoints, even if most parameters remain close to the same pretrained starting point.

LoRA addresses these problems by asking a sharper question: do we really need to update the full parameter space to adapt the model?

## The Low-Rank Assumption

LoRA starts from the observation that the useful task-specific update may have much lower intrinsic rank than the original matrix. If the original layer has a large weight matrix $W$, the adapted layer can be written as:

$$
W' = W + \Delta W
$$

Instead of learning the full $\Delta W$, LoRA parameterizes it as the product of two smaller matrices:

$$
\Delta W = BA
$$

Here, $A$ projects the input down to a low-dimensional rank-$r$ space, and $B$ projects it back up. If $r$ is small, then $A$ and $B$ contain far fewer trainable parameters than a full update matrix.

For a layer with input dimension $d$ and output dimension $k$, a full update contains $d \times k$ trainable parameters. A LoRA update contains approximately $r(d + k)$ parameters. When $r$ is 4, 8, 16, or 32, the reduction can be dramatic.

The pretrained matrix $W$ stays frozen. Only the LoRA matrices are trained.

## What Changes During Training?

During training, the forward pass uses both the frozen base layer and the LoRA branch:

$$
h = Wx + BAx
$$

The frozen base layer still provides the general language, vision, or multimodal capability learned during pretraining. The LoRA branch learns a small task-specific correction.

This design has a useful side effect: the adapter begins as a near-zero perturbation of the base model. In many implementations, one of the low-rank matrices is initialized to zero, so the model initially behaves like the original pretrained model. Fine-tuning then gradually learns a controlled residual.

LoRA is usually applied to selected linear projections inside transformer blocks. Common targets include attention query and value projections, and sometimes key, output, gate, up, and down projections depending on the architecture and task. The right target modules are not universal. Instruction tuning, classification, visual adaptation, and diffusion models may benefit from different choices.

## Why It Is Useful

The most visible benefit is efficiency. LoRA reduces the number of trainable parameters, which reduces optimizer state and checkpoint size. This makes it easier to fine-tune larger models on limited hardware.

The second benefit is modularity. A base model can remain fixed while multiple LoRA adapters are stored separately. One deployment can load a general base model and attach different adapters for different domains or users.

The third benefit is mergeability. After training, the low-rank update can be merged into the original weight matrix:

$$
W_{\text{merged}} = W + BA
$$

This means LoRA does not necessarily add inference latency. A merged model behaves like an ordinary model with updated weights. When adapters need to be swapped dynamically, they can also remain separate.

<figure class="blog-figure">
  <img src="{{ '/assets/images/blog/lora-adapter-serving.svg' | relative_url }}" alt="One frozen base model can serve multiple task adapters">
  <figcaption>A common deployment pattern is one shared base model plus small task adapters. This avoids storing a full model copy for every downstream task.</figcaption>
</figure>

## LoRA Is Not Just Compression

It is tempting to think of LoRA as a compression trick, but that misses the point. LoRA does not first train a full model and then compress it. It constrains the training update itself to a low-rank subspace.

That constraint can be helpful. Full fine-tuning has enormous freedom, which can overfit small datasets or move the model too far from its pretrained behavior. LoRA limits how much the model can change, while still giving it a flexible path to adapt.

The constraint can also be limiting. If the task requires a large structural change, a very low rank may underfit. Increasing the rank, tuning more modules, using better data, or combining LoRA with other adaptation strategies may be necessary.

## QLoRA: Quantization Plus LoRA

QLoRA extends the idea by reducing memory for the frozen base model as well. It keeps the pretrained model in a quantized format, commonly 4-bit, and backpropagates through it into LoRA adapters. The trainable part remains small, while the frozen base model consumes much less memory.

The important distinction is this:

- **LoRA** reduces the number of trainable parameters.
- **QLoRA** combines LoRA with quantized storage of the frozen base model to reduce memory further.

This is why QLoRA made it practical to fine-tune much larger models on smaller hardware. The adapter is still the part being learned; quantization mainly changes how the frozen base model is stored and used during training.

## Practical Knobs

Several LoRA hyperparameters are worth understanding before using it blindly.

**Rank $r$** controls the capacity of the adapter. A small rank is cheaper but less expressive. A larger rank can fit more task-specific change but increases memory and storage.

**Alpha** scales the LoRA update. Many implementations use a scaling factor like $\alpha / r$ so that changing the rank does not automatically change the update magnitude too aggressively.

**Target modules** determine where LoRA is inserted. Training only attention projections may be enough for some tasks. Other tasks need feed-forward layers or more modules.

**Dropout** can regularize the LoRA branch, especially when the adaptation dataset is small.

**Merging** matters for deployment. If only one adapter is needed, merging can simplify serving. If many adapters must be switched at runtime, keeping them separate may be better.

## Common Failure Modes

LoRA is efficient, but it is not magic.

If the dataset is poor, LoRA will efficiently learn poor behavior. Low-rank adaptation does not fix label noise, weak prompts, inconsistent formatting, or missing task coverage.

If the rank is too small, the model may not adapt enough. This often appears as outputs that stay close to the base model and fail to learn domain-specific patterns.

If the target modules are wrong, training may look cheap but ineffective. Some architectures need attention-only LoRA; others benefit from adapting MLP projections too.

If users expect LoRA to "add knowledge" permanently, they may be disappointed. Fine-tuning can shape behavior and encode some facts, but it is not a substitute for retrieval, tool use, or maintaining an external knowledge base when facts change.

If too many adapters are stacked or merged without care, interactions can become unpredictable. Adapters are not guaranteed to compose cleanly.

## When to Use LoRA

LoRA is a strong default when the goal is to adapt a large pretrained model to a task, style, domain, or instruction format without paying the cost of full fine-tuning.

It is especially useful when:

- the base model is large;
- training hardware is limited;
- many task-specific variants are needed;
- the adaptation dataset is moderate in size;
- the deployment system can benefit from small swappable adapters.

Full fine-tuning can still be appropriate when maximum task performance matters, data is large and high-quality, and compute is available. Retrieval can be more appropriate when the main problem is fresh or private knowledge. Prompting can be enough when the task is simple and the base model already knows the behavior.

## Takeaway

LoRA works because adaptation often does not require changing every parameter. By freezing the pretrained model and learning a low-rank residual update, it turns fine-tuning from a heavyweight model-copying problem into a lightweight adapter-learning problem.

The key intuition is simple: keep the general capability in the base model, and learn only the small task-specific correction. That is why LoRA became a central technique for practical LLM customization.

## Further Reading

- [LoRA: Low-Rank Adaptation of Large Language Models](https://arxiv.org/abs/2106.09685)
- [LoRA on OpenReview, ICLR 2022](https://openreview.net/forum?id=nZeVKeeFYf9)
- [Microsoft LoRA implementation](https://github.com/microsoft/LoRA)
- [Hugging Face PEFT LoRA guide](https://huggingface.co/docs/peft/main/en/conceptual_guides/lora)
- [QLoRA: Efficient Finetuning of Quantized LLMs](https://arxiv.org/abs/2305.14314)
