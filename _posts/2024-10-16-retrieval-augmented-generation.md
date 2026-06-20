---
layout: blog_post
title: 'RAG: Retrieval-Augmented Generation from Indexing to Answers'
date: 2024-10-16
tags:
  - Large Language Models
  - Retrieval
  - RAG
---

Large language models are powerful, but they have a practical weakness: their knowledge is stored in parameters that are expensive to inspect, update, and verify. If a model does not know a new document, a private policy, a recent paper, or a company database, prompting alone cannot reliably recover that missing information.

Retrieval-Augmented Generation, usually shortened to **RAG**, addresses this by letting the model read relevant external context before answering. Instead of asking the model to rely only on parametric memory, a RAG system retrieves documents from an external knowledge source and places the most useful passages into the model context.

The core idea is simple: retrieve first, generate second.

<figure class="blog-figure">
  <img src="{{ '/assets/images/blog/rag-pipeline.svg' | relative_url }}" alt="A RAG pipeline retrieves relevant passages before generation">
  <figcaption>A typical RAG system has two phases: build an index over documents, then retrieve relevant chunks at query time and pass them to the generator.</figcaption>
</figure>

## Parametric and Non-Parametric Memory

The original RAG framing distinguishes between two kinds of memory.

**Parametric memory** is knowledge stored inside model weights. It is compact and fast to use, but hard to update precisely. If the world changes, updating model weights is expensive and may have side effects.

**Non-parametric memory** is external knowledge stored outside the model, such as documents, passages, database records, or vector indexes. It can be updated without retraining the model.

RAG combines both. The language model supplies general reasoning, language fluency, and instruction following. The retriever supplies task-specific or up-to-date evidence.

This distinction explains why RAG is useful for enterprise search, technical assistants, customer support, legal document analysis, scientific literature exploration, and personal knowledge bases. The model does not need to memorize every document. It needs to retrieve the right evidence and use it faithfully.

## The Indexing Phase

A RAG system begins before the user asks a question. The system first prepares a knowledge base.

The usual indexing pipeline has four steps.

First, documents are loaded from sources such as PDFs, Markdown files, web pages, issue trackers, or internal databases.

Second, documents are split into chunks. Chunking matters more than it looks. If chunks are too small, each retrieved result may lose context. If chunks are too large, retrieval becomes noisy and the model context fills quickly.

Third, each chunk is converted into an embedding vector. The embedding model maps semantically similar text into nearby points in a vector space.

Fourth, the vectors and their metadata are stored in an index. A vector index such as Faiss can search dense vectors efficiently, even when the document collection is large.

The output of this phase is not an answer. It is a searchable memory structure.

## The Query-Time Phase

When the user asks a question, the system runs a second pipeline.

The query is embedded using a compatible embedding model. The vector index then returns candidate chunks that are close to the query vector. Some systems also use keyword search, metadata filters, hybrid retrieval, or reranking to improve precision.

The selected chunks are inserted into a prompt together with the user question. The generator then answers based on both the retrieved evidence and its own general capabilities.

In a well-designed RAG system, the generated answer should be grounded in retrieved context. The model should not silently invent missing evidence. For high-stakes settings, the answer should include citations, source snippets, or enough traceability for a human to inspect the evidence.

## Sparse, Dense, and Hybrid Retrieval

Retrieval is not one method.

**Sparse retrieval** uses lexical overlap. BM25-style systems are strong when the query and document share exact terms, identifiers, names, or code symbols.

**Dense retrieval** uses embeddings. It can retrieve semantically related passages even when the wording differs. Dense Passage Retrieval showed that learned dense representations can be very effective for open-domain question answering.

**Hybrid retrieval** combines both. This is often a practical default because real user queries contain both semantic intent and exact-match constraints. A question about "LoRA alpha" should probably match the exact term "alpha" while also understanding the broader fine-tuning context.

Reranking is another common layer. The first retriever returns a larger candidate set, and a more expensive model reranks the candidates before generation.

## Why RAG Helps

RAG helps because it separates knowledge storage from language generation.

It makes knowledge easier to update. Re-indexing documents is usually cheaper and safer than fine-tuning a model every time a file changes.

It improves traceability. Retrieved passages can be shown to the user, logged, evaluated, and audited.

It reduces some hallucinations. The model has relevant evidence in context, so it has less need to guess from memory.

It supports private data. A model can answer questions over a local or organization-specific corpus without that corpus being part of pretraining.

It also lets smaller models behave more usefully in domain-specific settings. Good retrieval can compensate for limited model memory.

## Where RAG Breaks

RAG can fail at any stage of the pipeline.

The index may be incomplete. If the right document was never loaded, retrieval cannot find it.

Chunking may be poor. A passage can contain the answer but miss the surrounding definitions needed to interpret it.

The embedding model may retrieve semantically related but actually irrelevant chunks. This is common when two concepts use similar words but require different constraints.

The retriever may return too many chunks. More context is not always better. Irrelevant passages can distract the generator and push useful evidence out of the context window.

The model may ignore the retrieved context. Even with the right passage, generation can be unfaithful if the prompt, model, or decoding behavior is weak.

The answer may need computation or actions, not retrieval. If the user asks for a live account balance, a database query or tool call may be necessary. RAG over stale text is not enough.

<figure class="blog-figure">
  <img src="{{ '/assets/images/blog/rag-evaluation-loop.svg' | relative_url }}" alt="RAG systems should evaluate retrieval quality, faithfulness, answer quality, and latency">
  <figcaption>RAG quality is a system property. Evaluation should cover retrieval, grounding, answer quality, and operational cost rather than only final text fluency.</figcaption>
</figure>

## Evaluation: More Than Answer Quality

Evaluating a RAG system requires looking at both retrieval and generation.

For retrieval, useful questions include:

- Did the system retrieve a passage that contains the answer?
- Is the top result actually relevant, or only superficially similar?
- How much irrelevant context is being passed to the model?
- Does retrieval work for exact terms, synonyms, long queries, and ambiguous questions?

For generation, useful questions include:

- Is the answer faithful to the retrieved evidence?
- Does it cite the right source?
- Does it admit when the retrieved context is insufficient?
- Is the answer concise enough for the user?

RAGAS and related evaluation work made this point explicit by separating dimensions such as context relevance, faithfulness, and answer relevance. A RAG answer can be fluent but unsupported, supported but incomplete, or correct but too slow to serve.

Latency and cost also matter. Embedding, retrieval, reranking, and long-context generation all add overhead. A production system needs to balance quality with response time.

## RAG Versus Fine-Tuning

RAG and fine-tuning solve different problems.

Use RAG when the main issue is external knowledge: private documents, changing facts, source-grounded answers, or auditability.

Use fine-tuning when the main issue is behavior: output format, domain style, tool-use patterns, instruction following, or task-specific reasoning habits.

In practice, strong systems often use both. Fine-tuning teaches the model how to follow a domain-specific answering protocol, while RAG supplies the evidence needed for each specific query.

## Practical Design Checklist

A useful RAG system usually needs decisions in five areas.

**Corpus design.** Decide which documents are allowed, how often they update, what metadata is stored, and how old versions are handled.

**Chunking.** Choose chunk size, overlap, section awareness, and document structure handling. Tables, code, formulas, and scanned PDFs often need special care.

**Retrieval.** Decide whether to use sparse, dense, hybrid, metadata filtering, query rewriting, or reranking.

**Prompting.** Tell the model how to use evidence, when to cite sources, and what to do when evidence is missing.

**Evaluation.** Build a test set of real questions, expected evidence, expected answers, and failure cases. Do not rely only on demos.

## Takeaway

RAG is best understood as an evidence pipeline around a language model. The model is still important, but the system quality depends on ingestion, chunking, retrieval, reranking, prompting, evaluation, latency, and source traceability.

The useful mental model is not "RAG prevents hallucination." A better mental model is: RAG gives the model a chance to answer from inspectable evidence. Whether it succeeds depends on the whole pipeline.

## Further Reading

- [Retrieval-Augmented Generation for Knowledge-Intensive NLP Tasks](https://arxiv.org/abs/2005.11401)
- [Dense Passage Retrieval for Open-Domain Question Answering](https://arxiv.org/abs/2004.04906)
- [Faiss documentation](https://faiss.ai/index.html)
- [Hugging Face RAG documentation](https://huggingface.co/docs/transformers/en/model_doc/rag)
- [LlamaIndex introduction to RAG](https://developers.llamaindex.ai/python/framework/understanding/rag/)
- [Self-RAG: Learning to Retrieve, Generate, and Critique through Self-Reflection](https://openreview.net/forum?id=hSyW5go0v8)
- [RAGAS: Automated Evaluation of Retrieval Augmented Generation](https://aclanthology.org/2024.eacl-demo.16/)
