---
layout: blog_post
title: '3D Gaussian Splatting for Embodied Perception'
date: 2026-05-15
tags:
  - Robotics
  - 3D Vision
  - Gaussian Splatting
---

Robots need world representations that are both useful for perception and cheap enough to update or query during operation. A map that looks beautiful but renders slowly may be hard to use in a control loop. A map that is fast but visually sparse may miss the details needed for manipulation.

3D Gaussian Splatting, or 3DGS, is interesting because it offers a different point in this trade-off. It represents a scene with many 3D Gaussian primitives and renders them efficiently through splatting. The result can be high-fidelity novel-view rendering at interactive rates.

For graphics, that is already exciting. For robotics, the deeper question is: can this kind of representation help an embodied agent remember, inspect, simulate, and act in a physical scene?

<figure class="blog-figure">
  <img src="{{ '/assets/images/blog/gaussian-splatting/3dgs-garden.png' | relative_url }}" alt="Example rendering from 3D Gaussian Splatting">
  <figcaption>3D Gaussian Splatting can represent real scenes with high visual fidelity and render them efficiently from novel viewpoints. Image source: <a href="https://repo-sam.inria.fr/fungraph/3d-gaussian-splatting/" target="_blank">3D Gaussian Splatting project page</a>.</figcaption>
</figure>

## The Basic Idea

Traditional neural radiance fields often store a scene implicitly in a neural network. To render a view, the model samples many points along camera rays and queries the network. This can produce impressive images, but rendering can be expensive.

3D Gaussian Splatting uses a more explicit representation. A scene is modeled as a set of Gaussian primitives, each with parameters such as position, shape, opacity, and color. During rendering, these Gaussians are projected into the camera view and composited efficiently.

The practical advantage is speed. Instead of repeatedly querying a heavy neural field along many rays, the system can rasterize explicit primitives. This makes high-quality real-time rendering much more feasible.

<figure class="blog-figure">
  <img src="{{ '/assets/images/blog/gaussian-splatting/3dgs-quality.png' | relative_url }}" alt="3D Gaussian Splatting quality comparison">
  <figcaption>The original 3DGS paper emphasizes the quality-speed trade-off: high visual quality without giving up real-time rendering. Image source: <a href="https://repo-sam.inria.fr/fungraph/3d-gaussian-splatting/" target="_blank">3D Gaussian Splatting project page</a>.</figcaption>
</figure>

## Why Embodied Agents Care About Rendering Speed

Rendering speed is not only a graphics metric. For an embodied agent, speed affects how a representation can be used.

A robot may need to:

- check what an object would look like from a new viewpoint;
- localize itself in a reconstructed scene;
- plan camera motion to reduce uncertainty;
- compare current observations against memory;
- generate synthetic views for training;
- inspect whether a planned manipulation would occlude important objects.

If rendering is slow, these operations become offline tools. If rendering is fast, they can become part of the perception and planning loop.

## 3DGS as Robot Memory

A robot memory needs to be more than a list of detected objects. It should preserve spatial layout, appearance, and view-dependent information. 3DGS can act as a visually rich memory of a scene, especially when the agent revisits the same environment.

This is useful for navigation and manipulation. If a robot has mapped a kitchen, it can render likely views from unvisited camera poses, compare new observations with the stored representation, or maintain a visual record of object locations.

For mobile robots, 3DGS connects naturally to SLAM. Systems such as SplaTAM explore how Gaussian representations can support dense RGB-D tracking and mapping. The appeal is that the same representation can support localization, reconstruction, and novel-view rendering.

## 3DGS as a Digital Twin

A second use is digital-twin construction. A robot can scan a real scene, reconstruct it as a Gaussian representation, and use that reconstruction for visualization, debugging, data generation, or policy evaluation.

This is especially relevant when simulation and real-world deployment need to meet. A digital twin does not have to be a perfect physics model to be useful. It can still provide realistic visual contexts, camera viewpoints, and scene geometry approximations.

<figure class="blog-figure">
  <img src="{{ '/assets/images/blog/gaussian-splatting/3dgs-performance.png' | relative_url }}" alt="3D Gaussian Splatting performance comparison">
  <figcaption>Interactive rendering makes Gaussian scene representations attractive for robot debugging, synthetic view generation, and digital-twin workflows. Image source: <a href="https://repo-sam.inria.fr/fungraph/3d-gaussian-splatting/" target="_blank">3D Gaussian Splatting project page</a>.</figcaption>
</figure>

## What 3DGS Does Not Solve

3DGS is not a complete robot world model by itself.

First, visual realism is not physical realism. A Gaussian scene may render beautifully while still lacking mass, friction, articulation, force, or contact dynamics.

Second, semantics are not automatic. A robot needs to know what objects are, what can be grasped, what is dangerous, and which parts are movable. A plain Gaussian representation stores appearance and geometry, not task semantics.

Third, dynamic scenes are difficult. Robots operate around humans, moving objects, deformable materials, opening doors, drawers, and tools. Maintaining a consistent Gaussian map under change is harder than reconstructing a static scene.

Fourth, action requires affordances. A robot does not only need to render a mug; it needs to know how to pick it up, whether it is full, and where it can be placed.

This is why robotics applications often combine 3DGS with tracking, segmentation, physics, or learned policies.

## From Pretty Scenes to Actionable Scenes

For embodied perception, the research direction is to make Gaussian representations more actionable.

Some useful extensions include:

- **semantic Gaussians:** attach labels, features, or language embeddings to Gaussians;
- **dynamic Gaussians:** update scene elements as objects move;
- **object-aware Gaussians:** separate objects from background to support manipulation;
- **physics-aware Gaussians:** connect visual primitives to particles, meshes, or dynamics models;
- **planning-aware maps:** expose uncertainty and free space, not only rendered color.

This is where work such as SplaTAM and Physically Embodied Gaussian Splatting becomes relevant. They move the idea from static novel-view synthesis toward representations that can support mapping, correction, and physical interaction.

## A Practical Mental Model

A robot perception stack can use different representations for different questions:

| Representation | Good For | Weakness |
| --- | --- | --- |
| 2D image features | recognition and language grounding | limited spatial memory |
| point clouds | geometry and distance reasoning | sparse or noisy appearance |
| meshes | collision and simulation | hard to reconstruct cleanly |
| NeRF-style fields | high-quality view synthesis | often expensive to render |
| 3D Gaussians | fast photorealistic rendering | needs semantics and dynamics for action |

3DGS is powerful because it sits between visual fidelity and real-time usability. It is not the whole stack, but it can become a useful layer inside it.

## Takeaway

3D Gaussian Splatting matters for embodied AI because it makes visually rich 3D scene representations faster to render and easier to inspect. That opens doors for robot memory, SLAM, digital twins, synthetic views, and debugging.

The open problem is not whether 3DGS can make scenes look good. It can. The harder question is how to turn a visually rich scene into an actionable scene: one with objects, affordances, uncertainty, physical constraints, and update rules that a robot can trust.

## Further Reading

- [3D Gaussian Splatting for Real-Time Radiance Field Rendering](https://arxiv.org/abs/2308.04079)
- [3D Gaussian Splatting project page](https://repo-sam.inria.fr/fungraph/3d-gaussian-splatting/)
- [SplaTAM: Splat, Track and Map 3D Gaussians for Dense RGB-D SLAM](https://arxiv.org/abs/2312.02126)
- [SplaTAM project page](https://spla-tam.github.io/)
- [Physically Embodied Gaussian Splatting](https://arxiv.org/abs/2406.10788)
- [Physically Embodied Gaussian Splatting project page](https://embodied-gaussians.github.io/)
- [Object-Aware Gaussian Splatting for Robotic Manipulation](https://object-aware-gaussian.github.io/)
