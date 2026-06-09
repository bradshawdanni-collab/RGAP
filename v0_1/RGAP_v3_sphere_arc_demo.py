import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D  # noqa: F401

np.random.seed(11)


def normalize(x):
    n = np.linalg.norm(x)
    return x if n == 0 else x / n


def normalize_rows(x):
    n = np.linalg.norm(x, axis=1, keepdims=True)
    n = np.where(n == 0, 1.0, n)
    return x / n


def generate_arc(n=500):
    t = np.linspace(-1.05, 1.05, n)
    lon = 0.9 * t
    lat = 0.38 + 0.22 * np.sin(1.6 * t)
    x = np.cos(lat) * np.cos(lon)
    y = np.cos(lat) * np.sin(lon)
    z = np.sin(lat)
    return np.column_stack([x, y, z]), t


def loss(x, z):
    return np.linalg.norm(x - z) ** 2


def grad_loss(x, z):
    return 2 * (x - z)


def sphere_retract(x):
    return normalize(x)


def project_to_arc(x, arc):
    d = np.linalg.norm(arc - x, axis=1)
    return arc[np.argmin(d)]


def euclidean_step(x, z, eta):
    return x - eta * grad_loss(x, z)


def sphere_step(x, z, eta):
    x_trial = x - eta * grad_loss(x, z)
    return sphere_retract(x_trial)


def arc_step(x, z, eta, arc):
    x_trial = x - eta * grad_loss(x, z)
    x_sphere = sphere_retract(x_trial)
    return project_to_arc(x_sphere, arc)


def run_descent(x0, z, arc, eta=0.1, steps=50):
    paths = {
        'euclidean': [x0.copy()],
        'sphere': [x0.copy()],
        'arc': [project_to_arc(x0, arc)]
    }
    for _ in range(steps):
        paths['euclidean'].append(euclidean_step(paths['euclidean'][-1], z, eta))
        paths['sphere'].append(sphere_step(paths['sphere'][-1], z, eta))
        paths['arc'].append(arc_step(paths['arc'][-1], z, eta, arc))
    return {k: np.array(v) for k, v in paths.items()}


def sphere_error(x):
    return abs(np.linalg.norm(x) - 1)


def arc_error(x, arc):
    return np.min(np.linalg.norm(arc - x, axis=1))


def admissibility_score(x, arc, alpha=1.0, beta=10.0):
    return alpha * sphere_error(x) + beta * arc_error(x, arc)


def evaluate_path(path, z, arc):
    return {
        'misfit': np.array([loss(x, z) for x in path]),
        'sphere_error': np.array([sphere_error(x) for x in path]),
        'arc_error': np.array([arc_error(x, arc) for x in path]),
        'admissibility': np.array([admissibility_score(x, arc) for x in path])
    }


arc, t = generate_arc()
true_idx = 340
true_point = arc[true_idx]
noise = np.array([0.06, -0.035, 0.04])
z = normalize(true_point + noise)
x0 = normalize(np.array([0.3, -0.85, 0.45]))
eta = 0.13
steps = 40

paths = run_descent(x0, z, arc, eta=eta, steps=steps)
evals = {k: evaluate_path(v, z, arc) for k, v in paths.items()}
finals = {k: v[-1] for k, v in paths.items()}
summary = {
    k: {
        'misfit_final': evals[k]['misfit'][-1],
        'sphere_error_final': evals[k]['sphere_error'][-1],
        'arc_error_final': evals[k]['arc_error'][-1],
        'admissibility_final': evals[k]['admissibility'][-1],
    }
    for k in paths
}

fig = plt.figure(figsize=(15, 10))
ax = fig.add_subplot(221, projection='3d')
u = np.linspace(0, 2*np.pi, 80)
v = np.linspace(0, np.pi, 40)
xs = np.outer(np.cos(u), np.sin(v))
ys = np.outer(np.sin(u), np.sin(v))
zs = np.outer(np.ones_like(u), np.cos(v))
ax.plot_surface(xs, ys, zs, color='#cfcfcf', alpha=0.10, linewidth=0)
ax.plot(arc[:,0], arc[:,1], arc[:,2], color='#1f77b4', lw=3.2, label='Residual arc manifold')
ax.scatter(*x0, color='#9467bd', s=60, label='Initial state')
ax.scatter(*z, color='black', s=60, label='Noisy observation')
ax.scatter(*true_point, color='#7f7f7f', s=40, label='True arc point')
colors = {'euclidean':'#d62728', 'sphere':'#2ca02c', 'arc':'#17becf'}
labels = {'euclidean':'Euclidean', 'sphere':'Sphere-retracted', 'arc':'Arc-retracted'}
for k in ['euclidean','sphere','arc']:
    p = paths[k]
    ax.plot(p[:,0], p[:,1], p[:,2], color=colors[k], lw=2.6, label=labels[k])
    ax.scatter(*p[-1], color=colors[k], s=50)
ax.set_title('Iterative RGAP descent v3')
ax.set_box_aspect([1,1,1])
ax.view_init(elev=24, azim=38)
ax.legend(loc='upper left', bbox_to_anchor=(0.0, 1.02), fontsize=9)

ax2 = fig.add_subplot(222)
for k in ['euclidean','sphere','arc']:
    ax2.plot(evals[k]['misfit'], color=colors[k], lw=2.3, label=f'{labels[k]} misfit')
ax2.set_title('Observation misfit over iterations')
ax2.set_xlabel('Iteration')
ax2.set_ylabel('Squared misfit')
ax2.grid(alpha=0.25)
ax2.legend(fontsize=8)

ax3 = fig.add_subplot(223)
for k in ['euclidean','sphere','arc']:
    ax3.plot(evals[k]['admissibility'], color=colors[k], lw=2.3, label=f'{labels[k]} admissibility')
ax3.set_title('Admissibility over iterations')
ax3.set_xlabel('Iteration')
ax3.set_ylabel('A(x)')
ax3.grid(alpha=0.25)
ax3.legend(fontsize=8)

ax4 = fig.add_subplot(224)
ax4.axis('off')
text = (
    'Canonical v3 finding\n'
    'Admissibility is enforced by the update law, not repaired after inference.\n\n'
    'Final metrics\n'
    f"Euclidean        misfit={summary['euclidean']['misfit_final']:.4f}  sphere={summary['euclidean']['sphere_error_final']:.4f}  arc={summary['euclidean']['arc_error_final']:.4f}  A={summary['euclidean']['admissibility_final']:.4f}\n"
    f"Sphere-retracted misfit={summary['sphere']['misfit_final']:.4f}  sphere={summary['sphere']['sphere_error_final']:.4f}  arc={summary['sphere']['arc_error_final']:.4f}  A={summary['sphere']['admissibility_final']:.4f}\n"
    f"Arc-retracted    misfit={summary['arc']['misfit_final']:.4f}  sphere={summary['arc']['sphere_error_final']:.4f}  arc={summary['arc']['arc_error_final']:.4f}  A={summary['arc']['admissibility_final']:.4f}\n\n"
    'Update rules\n'
    'Euclidean: x_{k+1} = x_k - eta grad L\n'
    'Sphere:    x_{k+1} = R_S(x_k - eta grad L)\n'
    'Arc:       x_{k+1} = R_A(R_S(x_k - eta grad L))'
)
ax4.text(0.02, 0.98, text, va='top', ha='left', family='monospace', fontsize=10.5)

plt.tight_layout()
fig.savefig('output/rgap_v3_iterative_retraction.png', dpi=220, bbox_inches='tight')
print(summary)
print('saved output/rgap_v3_iterative_retraction.png')
