"""
Case Study 3 (Electrical): RLC Series Circuit Transient Response

ODE (in terms of charge q, with current i = q'):
    L*q'' + R*q' + q/C = V(t)

Reduction to 1st-order system:
    x1 = q     (charge)
    x2 = q'    (current, i)

    x1' = x2
    x2' = ( V(t) - R*x2 - x1/C ) / L

This is the electrical analogue of the mass-spring-damper system:
    L <-> m,   R <-> c,   1/C <-> k

Damping regimes set by comparing R to critical resistance:
    R_cr = 2*sqrt(L/C)
    R < R_cr  -> underdamped
    R = R_cr  -> critically damped
    R > R_cr  -> overdamped
"""

import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import solve_ivp


def V(t):
    """Source voltage. 0 = pure transient decay; change for step/AC input."""
    return 0.0


def rlc_circuit(t, x, L, R, C):
    x1, x2 = x
    dx1dt = x2
    dx2dt = (V(t) - R * x2 - x1 / C) / L
    return [dx1dt, dx2dt]


# Parameters
L = 1.0     # inductance (H)
C = 0.01    # capacitance (F)

R_cr = 2 * np.sqrt(L / C)
R_values = [0.3 * R_cr, R_cr, 2 * R_cr]
labels = ['Underdamped', 'Critically damped', 'Overdamped']

x0 = [0.01, 0.0]    # q(0) = 0.01 C (initial charge), i(0) = 0 A
t_span = (0, 0.5)
t_eval = np.linspace(*t_span, 1000)

plt.figure()
for R, label in zip(R_values, labels):
    sol = solve_ivp(rlc_circuit, t_span, x0, args=(L, R, C),
                     t_eval=t_eval, method='RK45')
    plt.plot(sol.t, sol.y[1], linewidth=1.5, label=label)  # current i(t)

plt.xlabel('Time (s)')
plt.ylabel('Current i(t) (A)')
plt.title('RLC Circuit: Underdamped vs Critically Damped vs Overdamped')
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.savefig('case3_electrical.png', dpi=150)
plt.show()
