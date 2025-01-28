import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import solve_ivp
W = 100
Cp = 2
T0 = 20
UA = 10
M = 100
Tsteam = 250

def fun(Ta, Tb):
    return (W * Cp * (Ta - Tb) + UA * (Tsteam - Tb)) / (M * Cp)

def dSdt(t,S):
    T1,T2,T3 = S
    return [fun(T0,T1),
            fun(T1,T2),
            fun(T2,T3)]
    
t = np.linspace(0,15,200)
# solve eqs
sol = solve_ivp(dSdt, y0=[20,20,20], t_span=[min(t),max(t)], t_eval=t)

# show T over t
for i in range(len(sol.y)):
    plt.plot(t, sol.y[i],'o--',label=f'T{i+1}' )

# find the time to reach 99% of steady state
target_T = sol.y[2][-1] * 0.99
# horizontal line for 99% steady state
plt.axhline(target_T, color='red', linestyle='--', label='99% Steady State (T3)')
for i in range(1,len(t)):
    if sol.y[2][i] > target_T:
        print(f"T3 steady-state: {sol.y[2][-1]:.2f} °C")
        print(f"T3 reaches 99% of steady-state at time: {t[i]:.2f} minutes")
        # vertical line
        plt.axvline(t[i], color='green', linestyle='--', label=f'Time to 99%: {t[i]:.2f} min')
        break
    
plt.title('Temperature Profiles in Three Heated Tanks', fontsize=14)
plt.xlabel('Time (minutes)', fontsize=12)
plt.ylabel('Temperature (°C)', fontsize=12)
plt.legend()
plt.grid()
plt.tight_layout()
plt.show()