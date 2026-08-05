# micrograd

A tiny **automatic differentiation** engine and neural-network library, built from scratch to
understand how backpropagation actually works — no PyTorch, no autograd black box.

## What's inside

- **`Value`** — a scalar that records the operations performed on it, forming a computation graph.
- **Reverse-mode autodiff** — calling `.backward()` walks the graph in topological order and
  accumulates gradients via the chain rule.
- **A small MLP** — neurons, layers, and a multi-layer perceptron built on top of `Value`, trained
  with gradient descent.
- **Graph visualization** — `draw_dot` renders the computation graph (nodes, operations, gradients)
  with Graphviz.

## Why

Frameworks hide the mechanics of backprop. Implementing autodiff over a dynamically constructed
graph — including the topological sort and gradient accumulation — makes the ideas behind every deep
learning framework concrete. Inspired by Karpathy's micrograd.

## Run it

Open `micrograd.ipynb` (Jupyter). It walks through finite-difference gradient checking, the `Value`
class, a trained MLP, and graph visualization.
