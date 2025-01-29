import numpy as np
import matplotlib.pyplot as plt

CA0 = 0.2       
k = 1e-3        
D_AB = 1.2e-9 
L = 1e-3       
alpha = k / D_AB 

n = 100
z = np.linspace(0,L,n)
dz = z[1] - z[0]
A = np.zeros((n,n))
b = np.zeros(n)

# CA = CA0 at z = 0
A[0,0] = 1
b[0] = CA0
# dCA/dz = 0 at z= L
A[-1,-1] = 1
A[-1,-2] = -1
b[-1] = 0

for i in range(1,n-1):
    A[i,i-1] = 1
    A[i,i] = -2 - alpha * dz**2
    A[i,i+1] = 1
    b[i] = 0
CA = np.linalg.solve(A,b)

def exactSol(z):
    return (CA0 * np.cosh(L * np.sqrt(alpha) * (1 - z/L))) / (np.cosh(L * np.sqrt(alpha)))

plt.plot(z, CA, '--', label="Numerical Solution (FDM)")
plt.plot(z, exactSol(z), label="Exact Solution")
plt.xlabel("z (m)")
plt.ylabel("CA (kg mol/m³)")
plt.legend()
plt.tight_layout()
plt.grid()
plt.show()