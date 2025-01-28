import numpy as np
from scipy.optimize import fsolve
import matplotlib.pyplot as plt

# Constants for ammonia
R = 0.08206  # L·atm/(mol·K)
TC = 405.5  # K (critical temperature of ammonia)
PC = 111.3  # atm (critical pressure of ammonia)
T = 450  # K (given temperature)

# Van der Waals constants
a = 27 / 64 * (R**2 * TC**2 / PC)
b = R * TC / (8 * PC)
def v_fun(P):
    return lambda V:P * V**3 - (P*b + R*T) * V**2 + a*V - a*b
def z_cal(P,V):
    return P * V / (R * T)

print('----------   a   ----------')
v_at56atm = fsolve(v_fun(56),[1])[0]
print('v at 56atm and 450K: ' ,v_at56atm)
print('z: ' , z_cal(56,v_at56atm))

print('----------   b   ----------')
Pr_list = np.array([1, 2, 4, 10, 20])
P_list = Pr_list * PC
z_list = []
for P,Pr in zip(P_list , Pr_list):
    v = fsolve(v_fun(P),[1])[0]
    z = z_cal(P,v)
    z_list.append(z)
    print(f'Pr: {Pr} => v: {v:.4f} and z: {z:.4f} ')
plt.plot(Pr_list,z_list,'bo--')
plt.axhline(1,color='red' ,label='IG')
plt.xlabel('Pr')
plt.ylabel('Z')
plt.legend()
plt.show()