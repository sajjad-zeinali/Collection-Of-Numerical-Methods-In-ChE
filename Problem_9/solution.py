import numpy as np
from scipy.integrate import solve_ivp
import matplotlib.pyplot as plt

# Thermodynamic and physical constants
C_PA = 40.0  # Heat capacity of A, J/g-mol·K
C_PC = 80.0  # Heat capacity of C, J/g-mol·K
R = 8.314    # Universal gas constant, J/g-mol·K

# Reaction parameters
Delta_H_R = -40000  # Heat of reaction, J/g-mol
E_A = 41800         # Activation energy, J/g-mol
k_450 = 0.5         # Reaction rate constant at 450 K, dm^6/kg·min·mol
K_C_450 = 25000     # Equilibrium constant at 450 K, dm^3/g-mol

# Reactor feed conditions
F_A0 = 5.0          # Feed molar flow rate of A, g-mol/min
C_A0 = 0.271        # Initial concentration of A, g-mol/dm^3
T_0 = 450           # Initial temperature, K
P_0 = 10            # Initial pressure, atm
y_A0 = 1.0          # Initial reduced pressure (pure A feed)

# Heat transfer parameters
Ua = 0.8            # Heat transfer coefficient, J/kg·min·K
T_a = 500           # Ambient temperature, K

# Pressure drop parameter
alpha = 0.015       # Pressure drop constant, kg^-1

n = 100
w = np.linspace(0, 20, n)

# Define the system of ODEs
def dSdw(w, S):
    X, y, T = S
    
    # Concentrations
    C_C = (0.5 * C_A0 * X * y * T_0) / ((1 - 0.5*X) * T)
    C_A = (C_A0 * (1 - X) * y * T_0) / ((1 - 0.5*X) * T)

    # Equilibrium constant (Van't Hoff equation)
    K_C = K_C_450 * np.exp((Delta_H_R / R) * (1/450 - 1/T))
    
    # Reaction rate constant (Arrhenius equation)
    K = k_450 * np.exp((E_A / R) * (1/450 - 1/T))
    
    # Rate of reaction
    r_A_prime = -K * (C_A**2 - C_C/K_C)
    
    # Differential equations
    dXdw = -r_A_prime / F_A0
    dydw = (-alpha * (1 - 0.5*X) * T) / (2 * y * T_0)
    dTdw = (Ua * (T_a - T) + r_A_prime * Delta_H_R) / (F_A0 * C_PA)
    
    return [dXdw, dydw, dTdw]

sol = solve_ivp(fun=dSdw,
                y0=[0, 1, T_0],
                t_span=[min(w), max(w)],
                t_eval=w,
                method='RK45')

# Extract solutions
w = sol.t
X = sol.y[0]
y = sol.y[1]
T = sol.y[2]

# Plot results
plt.figure(figsize=(10, 8))

# Conversion X vs Catalyst weight W
plt.subplot(3, 1, 1)
plt.plot(w, X,'b', label="Conversion (X)")
plt.xlabel("Catalyst Weight (kg)")
plt.ylabel("Conversion (X)")
plt.grid(True)
plt.legend()

# Reduced Pressure y vs Catalyst weight W
plt.subplot(3, 1, 2)
plt.plot(w, y,'r', label="Reduced Pressure (y)")
plt.xlabel("Catalyst Weight (kg)")
plt.ylabel("Reduced Pressure (y)")
plt.grid(True)
plt.legend()

# Temperature T vs Catalyst weight W
plt.subplot(3, 1, 3)
plt.plot(w, T * 1e-3,'g', label="Temperature (T × 10⁻³)")
plt.xlabel("Catalyst Weight (kg)")
plt.ylabel("Temperature (T × 10⁻³ K)")
plt.grid(True)
plt.legend()
plt.tight_layout()
plt.show()

# ------------------ c ----------------------
C_A = (C_A0 * (1 - X) * y * (T_0 / T)) / (1 - 0.5 * X)
C_C = (0.5 * C_A0 * X * y * (T_0 / T)) / (1 - 0.5 * X)
plt.figure(figsize=(8, 6))

plt.plot(w, C_A,'b', label='Concentration of A (C_A)')
plt.plot(w, C_C,'g', label='Concentration of C (C_C)')

plt.xlabel('Weight of Catalyst (W) [kg]')
plt.ylabel('Concentration [mol/dm³]')
plt.title('Concentration Profiles of Reactant (A) and Product (C)')
plt.legend()
plt.grid()
plt.show()