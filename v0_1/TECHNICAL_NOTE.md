# Residual Geometric Admissibility Principle: Constrained Inference Under Observability Collapse

RGAP is a geometry-aware admissibility framework for constrained inference under partial observability. It differs from ordinary manifold optimization because the manifold is not assumed a priori as a design constraint. Instead, the admissible geometry is induced by the surviving observational structure after observability degradation or collapse.[cite:4][cite:25]

The executable core is simple: admissibility is enforced by the update law rather than repaired after inference. In practical manifold optimization, retractions are used to keep iterates on a manifold when exact geodesic updates are too costly, which makes them a natural computational mechanism for admissibility-preserving transport.[cite:4][cite:7]

## 1. Problem

When a hidden state is only partially observed, direct reconstruction may become underdetermined. Standard optimization can still find excellent data fits, but those fits need not remain lawful relative to the surviving constraints. RGAP addresses this by treating inference as motion on a residual admissible geometry rather than unconstrained search in the ambient state space.[cite:4][cite:34]

## 2. Formal definition of \(\mathcal{M}\)

Let \(x\in\mathcal{X}\) denote a hidden state, let \(\mathcal{O}(x)=y\) denote partial observations, and let \(\mathcal{C}(x)=0\) encode hard structural or physical constraints. Define the residual admissible set as

\[
\mathcal{M}=\{x\in\mathcal{X}\mid \mathcal{C}(x)=0,\ \|\mathcal{O}(x)-y\|\leq \epsilon\}
\]

Inference then proceeds on \(\mathcal{M}\), not on unconstrained \(\mathcal{X}\). Depending on the observability operator and surviving constraints, the residual admissible manifold may exhibit strong anisotropy, degeneracy, disconnected components, or locally singular structure. These geometric properties encode the remaining distinguishability structure of the degraded system and explain ambiguity basins, narrowing admissible tubes, and collapse boundaries.[cite:28][cite:32]

## 3. v3 demo

The v3 artifact uses a unit sphere as ambient feasible space and a curved arc on that sphere as the residual admissible manifold. From a common initial state, one noisy observation is fitted under three update laws: Euclidean descent, sphere retraction, and arc retraction. This creates a computable distinction between fit and admissibility.

## 4. Results

The frozen v3 metrics are:

| Method | Final misfit | Final sphere error | Final arc error | Final admissibility | Verdict |
|---|---:|---:|---:|---:|---|
| Euclidean | 5.09e-11 | 4.33e-06 | 0.0289 | 0.2890 | Invalid |
| Sphere-retracted | 7.02e-11 | 0.0000 | 0.0289 | 0.2890 | Physically plausible, observationally invalid |
| Arc-retracted | 0.00088 | 0.0000 | 0.0000 | 0.0000 | Admissible |

These results prove the intended toy-model claim: best fit is not necessarily admissible fit. They also show that a path may remain physically plausible while still being observationally inadmissible relative to the residual arc.

## 5. Applications and limits

The framework is intended primarily as a structural doctrine for constrained inference under partial observability rather than as a domain-specific predictive method. The examples discussed here illustrate homologous geometric structures across inverse problems without implying identical physical mechanisms.[cite:17][cite:30]

MH370 is used here only as a motivating toy-model analogue for arc-constrained inference, not as a solved reconstruction claim. The strongest immediate technical extension is pathwise recovery: replacing single-point recovery by trajectory recovery under both observational admissibility and continuity constraints.
