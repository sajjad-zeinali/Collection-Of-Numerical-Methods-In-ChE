import numpy as np
from scipy.integrate import solve_ivp
import matplotlib.pyplot as plt

def main(part):
    # Given system parameters
    rho_V_Cp = 4000  # kJ/°C
    W_Cp = 500  # kJ/min⋅°C
    T_is = 60  # °C
    T_r = 80  # °C
    Tau_d = 1  # min
    Tau_m = 5  # min
    K_c = 50  # kJ/min⋅°C
    Tau_I = 2  # min
    T_i = 40  # °C
    
    # Time settings
    t = np.arange(0, 60, 0.1)  # More precise time steps

    if part == 'Part a':
        K_c = 0
    elif part == 'Part b':
        pass
    elif part == 'Part c':
        K_c = 500  # kJ/min⋅°C
    elif part == 'Part d':
        Tau_I = np.inf
    elif part == 'Part e':
        T_r = 90 # °C

    # Differential equations
    def dSdt(t, S):
        T, T0, Tm, errsum = S
        
        # Thermocouple dynamics
        dTmdt = (T0 - Tm) / Tau_m
        
        # Integral of error
        derrsumdt = T_r - Tm
        
        # Heater energy input with PI control and saturation
        q = W_Cp * (T_r - T_is) + K_c * (T_r - Tm) + (K_c / Tau_I) * errsum
        
        if part == 'Part e':
            q = np.clip(q, 0, 2.6 * W_Cp * (T_r - T_is))  # Apply limits on q
        
        # Energy balance equation for the tank
        dTdt = (W_Cp * (T_i - T) + q) / rho_V_Cp
        
        # Padé approximation for dead time
        dT0dt = (T - T0 - (Tau_d / 2) * dTdt) * (2 / Tau_d)
        
        return [dTdt, dT0dt, dTmdt, derrsumdt]


    # Solve the ODE system
    sol = solve_ivp(fun=dSdt,
                    y0=[T_r, T_r, T_r, 0],
                    t_eval=t,
                    t_span=[min(t), max(t)],
                    method='RK45')

    # Extract solutions
    T = sol.y[0]
    T0 = sol.y[1]
    Tm = sol.y[2]

    # Plot results
    plt.figure(figsize=(10, 8))
    plt.title(part)
    plt.subplot(311)
    plt.plot(t, T, label='T (Tank Temperature)')
    plt.ylabel("Tank Temperature (°C)")
    plt.legend()

    plt.subplot(312)
    plt.plot(t, T0, label='T0 (Delayed Temperature)', color='orange')
    plt.ylabel("Delayed Temperature (°C)")
    plt.legend()

    plt.subplot(313)
    plt.plot(t, Tm, label='Tm (Measured Temperature)', color='red')
    plt.ylabel("Measured Temperature (°C)")
    plt.xlabel("Time (min)")
    plt.legend()

    plt.tight_layout()
    plt.show()
    
main('Part a')
main('Part b')
main('Part c')
main('Part d')
main('Part e')