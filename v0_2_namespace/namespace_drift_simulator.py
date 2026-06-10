"""
RGAP v0.2 namespace-drift simulator scaffold.

Purpose
-------
This experimental simulator mirrors the v0.1 arc optimizer in semantic space.
It tests whether best-fit semantic continuation can drift away from an active
namespace manifold unless an explicit namespace projection/retraction law is applied.

Status
------
Experimental. v0.1 kernel semantics remain frozen.

Core analogy
------------
- Free embedding state        <-> free 3D trajectory state
- Namespace shell             <-> ambient sphere
- Residual semantic corridor  <-> residual arc
- Namespace retraction        <-> arc retraction
- Context velocity            <-> cumulative structural drift / reconciliation trigger
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, List, Tuple
import json
import numpy as np


@dataclass(frozen=True)
class NamespaceConfig:
    dim: int = 8
    n_points: int = 30
    n_iterations: int = 800
    lr: float = 0.08
    continuity_weight: float = 0.2
    noise_level: float = 0.12
    corridor_width: float = 0.05
    velocity_threshold: float = 0.05
    attractor_strength: float = 0.08
    attractor_power: float = 2.0
    seed: int = 42


def norm(x: np.ndarray) -> float:
    return float(np.linalg.norm(x))


def unit(x: np.ndarray) -> np.ndarray:
    n = np.linalg.norm(x)
    if n < 1e-12:
        return x
    return x / n


def make_active_corridor(config: NamespaceConfig) -> np.ndarray:
    """Create a deterministic semantic corridor inside an active namespace."""
    t = np.linspace(0.0, 1.0, config.n_points)
    corridor = np.zeros((config.n_points, config.dim))
    corridor[:, 0] = 1.0 + t
    corridor[:, 1] = 0.5 + 0.5 * t
    corridor[:, 2] = 0.25 * np.sin(np.pi * t)
    return corridor


def make_observations(corridor: np.ndarray, config: NamespaceConfig) -> np.ndarray:
    rng = np.random.default_rng(config.seed)
    return corridor + rng.normal(scale=config.noise_level, size=corridor.shape)


def make_off_namespace_attractors(config: NamespaceConfig) -> np.ndarray:
    """Tempting invalid semantic basins: immigration, course-code, Cisco-like namespaces."""
    attractors = np.zeros((3, config.dim))
    attractors[0, :4] = np.array([2.0, 1.5, 1.0, 0.8])     # immigration/visa analogue
    attractors[1, :4] = np.array([-1.5, 2.0, 1.2, 0.7])    # university/course analogue
    attractors[2, :4] = np.array([1.5, -1.8, 1.1, 0.6])    # Cisco/cert analogue
    return attractors


def attractor_force(x: np.ndarray, attractors: np.ndarray, strength: float, power: float) -> np.ndarray:
    """Continuous off-manifold pull toward semantically tempting invalid basins."""
    force = np.zeros_like(x)
    for a in attractors:
        diff = a - x
        d = np.linalg.norm(diff) + 1e-8
        force += diff / (d ** power)
    return strength * force


def project_namespace_shell(x: np.ndarray) -> np.ndarray:
    """Coarse namespace projection: preserve first three active dimensions, zero the rest."""
    y = np.array(x, copy=True)
    y[3:] = 0.0
    return y


def retract_corridor(x: np.ndarray, corridor: np.ndarray) -> np.ndarray:
    """Retract to nearest point on active residual semantic corridor."""
    distances = np.linalg.norm(corridor - x, axis=1)
    return corridor[int(np.argmin(distances))].copy()


def semantic_residual(state: np.ndarray, observations: np.ndarray) -> float:
    return float(np.mean(np.linalg.norm(state - observations, axis=1)))


def namespace_error(state: np.ndarray) -> float:
    projected = np.array(state, copy=True)
    projected[:, 3:] = 0.0
    return float(np.mean(np.linalg.norm(state - projected, axis=1)))


def corridor_error(state: np.ndarray, corridor: np.ndarray) -> float:
    vals = []
    for x in state:
        vals.append(np.min(np.linalg.norm(corridor - x, axis=1)))
    return float(np.mean(vals))


def context_velocity(history: List[np.ndarray]) -> float:
    if len(history) < 2:
        return 0.0
    return float(np.mean(np.linalg.norm(history[-1] - history[-2], axis=1)))


def continuity_penalty(state: np.ndarray) -> float:
    return float(np.mean(np.linalg.norm(np.diff(state, axis=0), axis=1)))


def run_method(method: str, observations: np.ndarray, corridor: np.ndarray, config: NamespaceConfig) -> Tuple[np.ndarray, Dict[str, float]]:
    attractors = make_off_namespace_attractors(config)
    state = observations.copy()
    history: List[np.ndarray] = [state.copy()]
    drift = 0.0
    reconciliations = 0

    for _ in range(config.n_iterations):
        grad = state - observations
        smooth = np.zeros_like(state)
        smooth[1:-1] = 2 * state[1:-1] - state[:-2] - state[2:]

        next_state = state - config.lr * (grad + config.continuity_weight * smooth)

        if method == "euclidean":
            for i in range(config.n_points):
                next_state[i] += attractor_force(next_state[i], attractors, config.attractor_strength, config.attractor_power)
        elif method == "namespace_projected":
            for i in range(config.n_points):
                next_state[i] += attractor_force(next_state[i], attractors, config.attractor_strength, config.attractor_power)
                next_state[i] = project_namespace_shell(next_state[i])
        elif method == "namespace_retracted":
            for i in range(config.n_points):
                next_state[i] += attractor_force(next_state[i], attractors, config.attractor_strength, config.attractor_power)
                next_state[i] = retract_corridor(next_state[i], corridor)
        else:
            raise ValueError(f"Unknown method: {method}")

        history.append(next_state.copy())
        drift += corridor_error(next_state, corridor)

        if method == "namespace_retracted" and context_velocity(history) > config.velocity_threshold:
            next_state = np.array([retract_corridor(x, corridor) for x in next_state])
            reconciliations += 1
            history[-1] = next_state.copy()

        state = next_state

    metrics = {
        "semantic_residual": semantic_residual(state, observations),
        "namespace_error": namespace_error(state),
        "corridor_error": corridor_error(state, corridor),
        "context_velocity": context_velocity(history),
        "continuity_penalty": continuity_penalty(state),
        "structural_drift": float(drift),
        "reconciliations": float(reconciliations),
    }
    return state, metrics


def verdict(metrics: Dict[str, float], config: NamespaceConfig) -> str:
    if metrics["namespace_error"] > config.corridor_width and metrics["corridor_error"] > config.corridor_width:
        return "INVALID_NAMESPACE_DRIFT"
    if metrics["namespace_error"] <= config.corridor_width and metrics["corridor_error"] > config.corridor_width:
        return "PARTIAL_NAMESPACE_ONLY"
    if metrics["namespace_error"] <= config.corridor_width and metrics["corridor_error"] <= config.corridor_width:
        return "FULLY_ADMISSIBLE_NAMESPACE"
    return "UNCLASSIFIED"


def main() -> None:
    config = NamespaceConfig()
    corridor = make_active_corridor(config)
    observations = make_observations(corridor, config)

    output = {"config": config.__dict__, "results": {}}
    for method in ["euclidean", "namespace_projected", "namespace_retracted"]:
        _, metrics = run_method(method, observations, corridor, config)
        metrics["verdict"] = verdict(metrics, config)
        output["results"][method] = metrics

    with open("namespace_drift_results.json", "w", encoding="utf-8") as f:
        json.dump(output, f, indent=2)

    print(json.dumps(output["results"], indent=2))


if __name__ == "__main__":
    main()
