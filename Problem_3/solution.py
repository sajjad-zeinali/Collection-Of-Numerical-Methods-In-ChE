import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit

# Data for temperature and pressure
T = np.array([-36.7, -19.6, -11.5, -2.6, 7.6, 15.4, 26.1, 42.2, 60.6, 80.1])
P = np.array([1, 5, 10, 20, 40, 60, 100, 200, 400, 760])

# Polynomial fitting function of degree 3
def a():
    T_fit = np.linspace(min(T), max(T), 200)
    co = np.polyfit(T, P, 3)  # Fit with degree 3
    P_fit = np.polyval(co, T_fit)
    # Calculate R^2
    TSS = sum((P - np.mean(P))**2)
    RSS = sum((P - np.polyval(co, T))**2)
    R2 = 1 - (RSS / TSS)
    print(f'R^2 for polynomial fit (degree 3) (a): {R2:.4f}')
    return [T_fit, P_fit]

# Clausius-Clapeyron linear fit function
def b():
    # y = A + B*x
    y = np.log10(P)
    x = 1 / (T + 273.15) 
    x_fit = np.linspace(min(x), max(x), 200)
    co = np.polyfit(x, y, 1)  # Linear fit
    y_fit = np.polyval(co, x_fit)
    T_fit = 1 / x_fit - 273.15 
    P_fit = 10 ** y_fit
    # Calculate R^2
    TSS = sum((np.log10(P) - np.mean(np.log10(P)))**2)
    RSS = sum((np.log10(P) - np.polyval(co, x))**2)
    R2 = 1 - (RSS / TSS)
    print(f'R^2 for linear fit (Clausius-Clapeyron) (b): {R2:.4f}')
    return [T_fit, P_fit]

# Custom model fitting function: A - B / (T + C)
def c():
    def fun(T, A, B, C):
        return (A - B / (T + C))  # Custom model
    
    init = [10, 2000, 273.15]  # Initial guess for A, B, C
    sol = curve_fit(fun, T, np.log10(P), p0=init)
    co = sol[0]
    T_fit = np.linspace(min(T), max(T), 200)
    logP_fit = fun(T_fit, co[0], co[1], co[2])
    P_fit = 10 ** logP_fit
    # Calculate R^2
    TSS = sum((np.log10(P) - np.mean(np.log10(P)))**2)
    RSS = sum((np.log10(P) - fun(T, co[0], co[1], co[2]))**2)
    R2 = 1 - (RSS / TSS)
    print(f'R^2 for model fit (c): {R2:.4f}')
    return [T_fit, P_fit]

# Execute fitting functions and store results
Ta, Pa = a()
Tb, Pb = b()
Tc, Pc = c()

# Plot the results
plt.subplot(131)
plt.plot(Ta, Pa)
plt.plot(T, P, 'ro--')
plt.title('a')
plt.xlabel('Temperature (C)')
plt.ylabel('Pressure (mmHg)')

plt.subplot(132)
plt.plot(Tb, Pb)
plt.plot(T, P, 'ro--')
plt.title('b')
plt.xlabel('Temperature (C)')
plt.ylabel('Pressure (mmHg)')

plt.subplot(133)
plt.plot(Tc, Pc)
plt.plot(T, P, 'ro--')
plt.title('c')
plt.xlabel('Temperature (C)')
plt.ylabel('Pressure (mmHg)')

# Adjust layout and show the plots
plt.tight_layout()
plt.show()