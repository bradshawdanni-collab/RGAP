# RGAP v0.2 Namespace Drift Simulator

**Status:** Experimental scaffold.  
**Kernel status:** RGAP v0.1 remains frozen and unchanged.

## Purpose

This v0.2 layer tests whether the RGAP hinge generalizes from geometric trajectory inference to semantic namespace transport.

The simulator mirrors the v0.1 arc optimizer:

| v0.1 Arc Optimizer | v0.2 Namespace Simulator |
|---|---|
| Free 3D trajectory state | Free semantic embedding state |
| Ambient sphere | Coarse active namespace shell |
| Residual arc | Residual semantic corridor |
| Arc retraction | Namespace/corridor retraction |
| Structural drift | Namespace drift / context velocity |

## Hypothesis

Best-fit semantic continuation may reduce local residual while drifting away from the active namespace manifold.

Namespace retraction should preserve admissible semantic transport, potentially at the cost of higher local residual.

## Update Laws

1. **Euclidean semantic update** — unconstrained embedding motion with continuous off-namespace attractor force.
2. **Namespace-projected update** — coarse projection into the active namespace shell.
3. **Namespace-retracted update** — retraction to the residual semantic corridor with context-velocity reconciliation.

## Run

```bash
python v0_2_namespace/namespace_drift_simulator.py
```

This writes:

```text
namespace_drift_results.json
```

## Scope Boundary

This is not a production retrieval system, agent runtime, or live vector database integration. It is a deterministic toy simulator for testing whether RGAP's best-fit/admissibility separation appears in semantic namespace dynamics.
