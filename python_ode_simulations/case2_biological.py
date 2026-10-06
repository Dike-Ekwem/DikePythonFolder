"""
Case Study 2 (Biological): Lotka-Volterra Predator-Prey Model

This system is ALREADY first order, so no order-reduction is needed --
it is naturally a coupled system of two 1st-order ODEs:

    x1 = prey population
    x2 = predator population

    x1' = a*x1 - b*x1*x2      (prey growth - predation losses)
    x2' = d*x1*x2 - g*x2      (predator growth from predation - death)
"""

import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import solve_ivp


def lotka_volterra(t, x, a, b, d, g):
    x1, x2 = x
    dx1dt = a * x1 - b * x1 * x2
    dx2dt = d * x1 * x2 - g * x2
    return [dx1dt, dx2dt]


# Parameters
a = 1.1   # prey growth rate
b = 0.4   # predation rate coefficient
d = 0.1   # predator growth rate from consuming prey
g = 0.4   # predator death rate

x0 = [10.0, 5.0]    # initial prey, predator populations
t_span = (0, 50)
t_eval = np.linspace(*t_span, 1000)

sol = solve_ivp(lotka_volterra, t_span, x0, args=(a, b, d, g),
                 t_eval=t_eval, method='RK45')

# Population dynamics over time
plt.figure()
plt.plot(sol.t, sol.y[0], 'b-', linewidth=1.5, label='Prey')
plt.plot(sol.t, sol.y[1], 'r-', linewidth=1.5, label='Predator')
plt.xlabel('Time')
plt.ylabel('Population')
plt.title('Lotka-Volterra Predator-Prey Dynamics')
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.savefig('case2_biological_timeseries.png', dpi=150)

# Phase portrait (prey vs predator)
plt.figure()
plt.plot(sol.y[0], sol.y[1], linewidth=1.5)
plt.xlabel('Prey population')
plt.ylabel('Predator population')
plt.title('Phase Portrait: Predator vs Prey')
plt.grid(True)
plt.tight_layout()
plt.savefig('case2_biological_phase.png', dpi=150)

plt.show()
