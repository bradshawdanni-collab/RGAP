import numpy as np

"""
RGAP v0.1 toy optimizer.

Demonstrates:
- Euclidean optimization
- Sphere projection
- Residual arc retraction

This is a bounded demonstrator for admissibility-preserving optimization under degraded observability.
"""

np.random.seed(42)

N_POINTS = 30
NOISE_LEVEL = 0.15
RADIUS = 1.0


def normalize(x):
    norm = np.linalg.norm(x)
    if norm == 0:
        return x
    return x / norm


def sphere_project(x):
    return normalize(x) * RADIUS


def arc_retract(x):
    x = sphere_project(x)
    x[2] = 0.0
    return sphere_project(x)


def residual(a, b):
    return np.linalg.norm(a - b)


true_arc = []
for t in np.linspace(-1.0, 1.0, N_POINTS):
    p = np.array([np.cos(t), np.sin(t), 0.0])
    true_arc.append(p)

true_arc = np.array(true_arc)
noise = np.random.normal(scale=NOISE_LEVEL, size=true_arc.shape)
observations = true_arc + noise

results = {
    "euclidean": [],
    "sphere_projected": [],
    "arc_retracted": []
}

for obs in observations:
    results["euclidean"].append(obs)
    results["sphere_projected"].append(sphere_project(obs))
    results["arc_retracted"].append(arc_retract(obs))

print('RGAP v0.1 demo complete')
