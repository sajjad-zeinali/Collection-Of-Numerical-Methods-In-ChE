import numpy as np
from scipy.optimize import fsolve
from scipy.integrate import solve_ivp
import matplotlib.pyplot as plt

A1, B1, C1 = 6.90565, 1211.033, 220.79 
A2, B2, C2 = 6.95464, 1344.8, 219.482   

P_total = 1.2 * 760  # mmHg

x1_0, x2_0 = 0.6, 0.4 
x1_f, x2_f = 0.2, 0.8 
x2 = np.linspace(x2_0,x2_f,100)

def Antoine(A, B, C, T):
    return 10 ** (A - (B / (T + C)))

def find_T(x2):
    f = lambda T: Antoine(A1, B1, C1, T) / P_total * (1 - x2) + Antoine(A2, B2, C2, T) / P_total * x2 - 1
    T_init = 90  
    sol = fsolve(f, T_init)
    return sol[0]

print(f"initial temperature {find_T(x2_0):.2f}°C")
print(f"final temperature   {find_T(x2_f):.2f}°C")

def main():
    k2 = lambda x2: Antoine(A2,B2,C2,find_T(x2)) / P_total
    f = lambda x2,L: L / (x2 * (k2(x2) - 1))
    sol = solve_ivp(fun=f,
                    t_span=[min(x2),max(x2)],
                    y0=[100],
                    method='RK45',
                    t_eval=x2)
    return sol

sol = main()
print(f"Remaining liquid at x2 = {x2_f}: {sol.y[0][-1]:.2f} moles")

plt.plot(sol.t, sol.y[0], '--', label='Liquid Remaining')
plt.xlabel('Mole Fraction of Toluene (x2)')
plt.ylabel('Liquid Remaining (L)')
plt.title('Batch Distillation: Liquid Remaining vs x2')
plt.legend()
plt.grid(True)
plt.show()