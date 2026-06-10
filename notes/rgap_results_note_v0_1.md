# RGAP Results Note v0.1

## Methodology

A free-state optimizer operating on unconstrained 3D trajectory points compares three update laws:

1. Euclidean descent
2. Sphere projection
3. Residual-arc retraction

All methods share identical state representations. Admissibility is imposed only through the update operator.

## Results

| Method | Misfit | Sphere Error | Arc Error | Verdict |
|---|---:|---:|---:|---|
| Euclidean | 0.068 | 0.074 | 0.096 | Inadmissible |
| Sphere-projected | 0.122 | 0.000 | 0.096 | Physically admissible only |
| Arc-retracted | 0.182 | 0.000 | 0.000 | Fully admissible |

## Proposition

Admissibility-preserving optimization may intentionally accept higher residual misfit in order to preserve surviving observational geometry.

## Interpretation

The experiment demonstrates that:

- best-fit optimization is not equivalent to admissibility,
- ambient geometric feasibility alone is insufficient,
- admissibility must be enforced during transport and update.

## Limitations

- Toy manifold only
- No operational search capability
- No MH370 reconstruction claim
- No proof of global optimality
- No physical flight model
- Demonstration-only computational kernel
