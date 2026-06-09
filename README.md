# RGAP — Residual Geometric Admissibility Principle

RGAP is a geometry-aware admissibility framework for constrained inference under degraded observability.

The repository demonstrates a computable distinction between:

- unconstrained optimization,
- ambient physical feasibility,
- and residual observational admissibility.

Core finding:

> Physically feasible recovery can remain observationally inadmissible relative to surviving constraint geometry, and admissibility must be preserved by the update law itself.

## Repository status

This package contains a frozen RGAP v0.1 reference artifact and available v4 pathwise recovery outputs.

## Structure

```text
RGAP/
├── README.md
├── LICENSE
├── .gitignore
├── artifact_register.md
├── figures/
│   ├── rgap_v01_sphere_arc.png
│   ├── RGAP_v3_results.png
│   ├── rgap_canonical_three_paths.png
│   ├── rgap_v4_metrics.png
│   └── rgap_v4_animation.gif
├── v0_1/
│   ├── TECHNICAL_NOTE.md
│   ├── RGAP_v3_sphere_arc_demo.py
│   ├── RGAP_v3_metrics.csv
│   ├── metrics.json
│   ├── metrics.md
│   ├── environment.txt
│   └── environment.yml
└── v4_pathwise/
    ├── metrics.json
    └── environment.yml
```

## Demonstrated distinction

The v0.1 sphere/arc experiment compares three update rules:

| Method | Interpretation |
|---|---|
| Euclidean | unconstrained fit |
| Sphere-retracted | ambient-feasible recovery |
| Arc-retracted | residual-manifold admissibility |

The key result is that Euclidean and sphere-retracted recovery can achieve near-zero observation misfit while remaining off the residual admissible manifold. Arc-retracted recovery accepts an explicit misfit premium to preserve residual geometry.

## v4 pathwise result

| Method | Misfit | Sphere Err | Arc Err | Cont. Err | Verdict |
|---|---:|---:|---:|---:|---|
| Euclidean | 0.0000 | 0.0000 | 0.0655 | 0.1227 | Invalid |
| Sphere-retracted | 0.0000 | 0.0000 | 0.0655 | 0.1227 | Ambient-feasible |
| Arc-retracted | 0.1052 | 0.0000 | 0.0000 | 0.0883 | Admissible |

Admissibility premium: `+0.1052` misfit accepted to preserve residual geometry and improve pathwise continuity.

## Scope boundary

This repository is not a domain-specific predictive method, operational search tool, accident-reconstruction method, or claim to solve MH370. It provides toy computational demonstrations of admissibility-preserving inference under degraded observability.

## License

MIT License. See `LICENSE`.
