"""
Solver Comparison: RK45 vs Radau across all three case studies

RK45   -> explicit Runge-Kutta, MATLAB's ode45 equivalent
          (usually fastest for smooth, non-stiff systems)
Radau  -> implicit solver, MATLAB's ode15s equivalent
          (designed for STIFF systems -- shines when dynamics have
           widely separated time scales, e.g. strongly overdamped
           mass-damper/RLC systems)

Timing with N repeated runs to average out timing noise.
"""

import time
import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import solve_ivp

N = 20  # number of repetitions for stable timing average


def timeit_avg(fcn, n=N):
    times = []
    for _ in range(n):
        start = time.perf_counter()
        fcn()
        times.append(time.perf_counter() - start)
    return np.mean(times)


results = {}

# --- Case 1: Mechanical (overdamped, most likely to show stiffness) ---
m, k = 1.0, 20.0
c = 4 * 2 * np.sqrt(m * k)   # strongly overdamped
x0 = [1.0, 0.0]
t_span = (0, 5)

def f1(t, x):
    return [x[1], (-c * x[1] - k * x[0]) / m]

t_rk45 = timeit_avg(lambda: solve_ivp(f1, t_span, x0, method='RK45'))
t_radau = timeit_avg(lambda: solve_ivp(f1, t_span, x0, method='Radau'))
results['Mechanical'] = (t_rk45, t_radau)

# --- Case 2: Biological (Lotka-Volterra, non-stiff, nonlinear) ---
a, b, d, g = 1.1, 0.4, 0.1, 0.4
x0 = [10.0, 5.0]
t_span = (0, 50)

def f2(t, x):
    return [a * x[0] - b * x[0] * x[1], d * x[0] * x[1] - g * x[1]]

t_rk45 = timeit_avg(lambda: solve_ivp(f2, t_span, x0, method='RK45'))
t_radau = timeit_avg(lambda: solve_ivp(f2, t_span, x0, method='Radau'))
results['Biological'] = (t_rk45, t_radau)

# --- Case 3: Electrical (RLC, overdamped -> stiffer) ---
L, C = 1.0, 0.01
R = 4 * 2 * np.sqrt(L / C)
x0 = [0.01, 0.0]
t_span = (0, 0.5)

def f3(t, x):
    return [x[1], (0 - R * x[1] - x[0] / C) / L]

t_rk45 = timeit_avg(lambda: solve_ivp(f3, t_span, x0, method='RK45'))
t_radau = timeit_avg(lambda: solve_ivp(f3, t_span, x0, method='Radau'))
results['Electrical'] = (t_rk45, t_radau)

# --- Report ---
print(f"{'System':<15}{'RK45 (s)':>12}{'Radau (s)':>12}")
for name, (t_rk45, t_radau) in results.items():
    print(f"{name:<15}{t_rk45:>12.5f}{t_radau:>12.5f}")

# --- Bar chart ---
labels = list(results.keys())
rk45_times = [results[k][0] for k in labels]
radau_times = [results[k][1] for k in labels]

x = np.arange(len(labels))
width = 0.35

fig, ax = plt.subplots()
ax.bar(x - width/2, rk45_times, width, label='RK45 (ode45 equiv.)')
ax.bar(x + width/2, radau_times, width, label='Radau (ode15s equiv.)')
ax.set_xticks(x)
ax.set_xticklabels(labels)
ax.set_ylabel('Average execution time (s)')
ax.set_title(f'Solver Execution Time Comparison (avg of {N} runs)')
ax.legend()
ax.grid(True, axis='y')
plt.tight_layout()
plt.savefig('compare_solvers.png', dpi=150)
plt.show()
