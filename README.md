# RGAP — Residual Geometric Admissibility Principle

RGAP is a bounded computational framework for admissibility-constrained inference under degraded observability.

The repository demonstrates a computable distinction between:

- unconstrained optimization,
- ambient physical feasibility,
- residual observational admissibility,
- and, experimentally in v0.2, semantic namespace admissibility.

Core finding:

> Lower residual misfit is not automatically higher admissibility. Admissibility must be preserved by the update law itself.

## Repository status

- **v0.1:** frozen kernel and computational proof.
- **v0.2 namespace:** experimental scaffold for semantic namespace drift; not yet a validated result.

## Structure

```text
RGAP/
├── README.md
├── LICENSE
├── .gitignore
├── rgap_kernel_v0_1.md
├── metrics_schema.json
├── RELEASE_NOTES_v0_1.md
├── notes/
│   └── rgap_results_note_v0_1.md
├── results/
│   └── toy_arc_optimizer_free_state_results.json
├── src/
│   └── toy_arc_optimizer_free_state.py
├── v0_1/
│   ├── TECHNICAL_NOTE.md
│   ├── RGAP_v3_sphere_arc_demo.py
│   ├── RGAP_v3_metrics.csv
│   ├── metrics.json
│   ├── metrics.md
│   ├── environment.txt
│   └── environment.yml
├── v0_2_namespace/
│   ├── README.md
│   ├── namespace_drift_simulator.py
│   ├── metrics_schema_namespace.json
│   └── namespace_drift_note_v0_2.md
├── figures/
│   ├── rgap_v01_sphere_arc.png
│   ├── RGAP_v3_results.png
│   ├── rgap_canonical_three_paths.png
│   ├── rgap_v4_metrics.png
│   └── rgap_v4_animation.gif
└── v4_pathwise/
    ├── metrics.json
    └── environment.yml
```

## v0.1 Demonstrated distinction

The frozen v0.1 free-state optimizer compares three update rules:

| Method | Misfit | Sphere Error | Arc Error | Verdict |
|---|---:|---:|---:|---|
| Euclidean | 0.068 | 0.074 | 0.096 | Inadmissible |
| Sphere-projected | 0.122 | 0.000 | 0.096 | Physically admissible only |
| Arc-retracted | 0.182 | 0.000 | 0.000 | Fully admissible |

The key result is that Euclidean optimization can achieve the lowest residual misfit while remaining structurally inadmissible. Arc-retracted recovery accepts an explicit misfit premium to preserve residual geometry.

## v0.2 experimental namespace scaffold

The `v0_2_namespace/` directory extends the same update-law comparison into semantic namespace transport.

It compares:

| Method | Meaning |
|---|---|
| Euclidean semantic update | unconstrained embedding-space optimization |
| Namespace projection | coarse namespace validity |
| Namespace retraction | residual semantic corridor preservation |

The v0.2 layer is experimental and should not be treated as a validated result until metrics demonstrate clear three-tier separation.

## Run

```bash
python src/toy_arc_optimizer_free_state.py
python v0_2_namespace/namespace_drift_simulator.py
```

## Scope boundary

This repository is not a domain-specific predictive method, operational search tool, accident-reconstruction method, production retrieval system, or claim to solve MH370. It provides toy computational demonstrations of admissibility-preserving inference under degraded observability.

## License

MIT License. See `LICENSE`.
