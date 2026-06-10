# RGAP Kernel v0.1

**Residual Geometric Admissibility Principle**

**Status:** Frozen kernel note  
**Scope:** Admissibility-constrained inference under degraded observability  
**Limit:** MH370-like arcs are motivating analogues only, not reconstruction claims.

---

## 1. Purpose

RGAP studies inference when observations are sparse, degraded, or partially collapsed.

The central question is not:

**What exact state occurred?**

but:

**What residual structure remains admissible under the surviving observations and constraints?**

---

## 2. Ambient State Space

Let \(S\) denote the ambient state space. A candidate state or trajectory is \(x \in S\). Observations at time \(t\) are denoted \(m_t\).

An observation operator maps candidate states into observation space:

\[
\mathcal{O}_t : S \rightarrow Y
\]

---

## 3. Measurement Residual

Define the observational residual:

\[
r_t(x; m_t) = \|\mathcal{O}_t(x) - m_t\|
\]

This measures how well a candidate state matches the available degraded observation.

---

## 4. Hard Admissibility Constraints

Let

\[
h_t(x) = 0
\]

encode hard constraints such as geometry, continuity, bounded dynamics, physical feasibility, and residual manifold consistency.

These constraints are not optional penalties. They define admissibility.

---

## 5. Residual-Admissible Set

Define the admissible set:

\[
\mathcal{A}_t(m,\epsilon) = \{x \in S : r_t(x;m) \le \epsilon,\; h_t(x)=0\}
\]

where \(\mathcal{A}_t\) is the surviving admissible structure, \(r_t\) is observational residual, \(h_t\) is the hard constraint system, and \(\epsilon\) is the residual tolerance.

---

## 6. Weighted Residual Functional

For computational comparison, define:

\[
\mathcal{R}(x) = \alpha r(x) + \beta d_M(x) + \gamma c(x)
\]

where \(r(x)\) is measurement misfit, \(d_M(x)\) is distance from the admissible manifold or shell, \(c(x)\) is continuity or dynamics penalty, and \(\alpha,\beta,\gamma\) are weighting coefficients.

Inference may then be written as:

\[
x^* = \arg\min_{x \in S} \mathcal{R}(x)
\]

subject to admissibility constraints.

---

## 7. Structural Drift

For an update sequence \(\{x_k\}_{k=1}^{n}\), define cumulative structural drift:

\[
D_n = \sum_{k=1}^{n} d_M(x_k)
\]

This measures how far the inference process moves away from the admissible residual geometry during optimization.

---

## 8. Update Law Comparison

RGAP compares three update classes:

### 8.1 Euclidean Update

Unconstrained residual minimization.

### 8.2 Ambient-Feasible Projection

Updates are projected back onto broad physical feasibility constraints, but not necessarily onto the residual-admissible set.

### 8.3 Residual-Admissible Retraction

Updates are transported along, or retracted back to, the residual-admissible geometry.

---

## 9. Proposition 1

Under degraded observability, residual-admissible retraction updates may accept equal or higher measurement misfit than unconstrained minimization while producing lower structural drift relative to the admissible set.

This is an empirical, falsifiable proposition for v0.1.

---

## 10. Integrity Boundary

| Category | Meaning |
|---|---|
| Observed | Directly measured inputs |
| Derived | Deterministic transformations of observations |
| Admissible | States satisfying residual and hard constraints |
| Speculative | Hypotheses not entailed by the model |

---

## 11. Scope Statement

This project studies admissibility-constrained inference under degraded observability and uses MH370-like arc systems only as motivating sparse-geometry analogues, not reconstruction claims.

---

## 12. v0.1 Deliverables

- `rgap_kernel_v0_1.md`
- `toy_arc_optimizer_free_state.py`
- `metrics_schema.json`
- residual-vs-structural-drift figure
- metrics table comparing Euclidean, ambient-feasible, and residual-admissible updates

---

## Frozen Claim

RGAP formalizes the distinction between best-fit inference and admissible inference under degraded observability.
