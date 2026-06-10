# RGAP v0.2 Namespace Drift Note

## Status

Experimental extension. This note does not modify or supersede the frozen v0.1 kernel.

## Motivation

The v0.1 arc optimizer demonstrated that lowest residual misfit is not necessarily the most admissible inference state. The v0.2 namespace simulator tests whether the same structure appears in semantic retrieval/orchestration contexts.

## Core Idea

A retrieval or agent system can optimize broad semantic proximity while leaving the active operational namespace. This is analogous to Euclidean geometric optimization leaving the residual admissible arc.

## Namespace Constraint

Let the active namespace be a constrained semantic manifold:

```text
N_active subset X
```

where `X` is the ambient embedding space.

A namespace projection/retraction operator constrains candidate continuations back into the active namespace or residual semantic corridor.

## Update-Law Comparison

| Method | Meaning | Expected Failure / Success |
|---|---|---|
| Euclidean semantic update | Unconstrained embedding optimization | May minimize semantic residual while drifting off namespace |
| Namespace projection | Coarse namespace validity | May remain domain-valid but leave residual semantic corridor |
| Namespace retraction | Residual corridor preservation | Preserves admissible semantic transport |

## Drift-Containment Principle

The simulator encodes two correction layers:

1. Continuous constraint: namespace projection/retraction.
2. Discrete cleanup: context-velocity threshold and reconciliation.

This mirrors drift containment patterns in calendars, ledgers, payment retries, and constrained optimization.

## Scope Boundary

This is a deterministic toy simulator. It is not a production retrieval system, live vector database, agent harness, or general theorem.

## Validation Requirement

The v0.2 result should only be considered validated if the metrics show clear three-tier separation:

| Method | Semantic Residual | Namespace Error | Corridor Error | Verdict |
|---|---:|---:|---:|---|
| Euclidean | lowest or competitive | high | high | invalid |
| Namespace-projected | medium | low | high | partial |
| Namespace-retracted | higher or constrained | low | low | admissible |

Until those metrics are produced and checked, v0.2 remains experimental.
