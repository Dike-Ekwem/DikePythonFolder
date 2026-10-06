"""
Case Study 1 (Mechanical): Mass-Spring-Damper System
ODE:  m*y'' + c*y' + k*y = 0

Reduction to 1st-order system:
    x1 = y      (displacement)
    x2 = y'     (velocity)

    x1' = x2
    x2' = ( -c*x2 - k*x1 ) / m

Damping regimes are set by comparing c to the critical damping value:
    c_cr = 2*sqrt(m*k)
    c < c_cr  -> underdamped
    c = c_cr  -> critically damped
    c > c_cr  -> overdamped
"""

import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import solve_ivp


def mass_spring_damper(t, x, m, c, k):
    x1, x2 = x
    dx1dt = x2
    dx2dt = (-c * x2 - k * x1) / m
    return [dx1dt, dx2dt]


# Parameters
m = 1.0     # mass (kg)
k = 20.0    # spring stiffness (N/m)

c_cr = 2 * np.sqrt(m * k)          # critical damping coefficient
c_values = [0.3 * c_cr, c_cr, 2 * c_cr]   # under, critical, over
labels = ['Underdamped', 'Critically damped', 'Overdamped']

x0 = [1.0, 0.0]     # y(0) = 1 m, y'(0) = 0 m/s
t_span = (0, 5)
t_eval = np.linspace(*t_span, 500)

plt.figure()
for c, label in zip(c_values, labels):
    sol = solve_ivp(mass_spring_damper, t_span, x0, args=(m, c, k),
                     t_eval=t_eval, method='RK45')
    plt.plot(sol.t, sol.y[0], linewidth=1.5, label=label)

plt.xlabel('Time (s)')
plt.ylabel('Displacement y(t) (m)')
plt.title('Mass-Spring-Damper: Underdamped vs Critically Damped vs Overdamped')
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.savefig('case1_mechanical.png', dpi=150)
plt.show()
