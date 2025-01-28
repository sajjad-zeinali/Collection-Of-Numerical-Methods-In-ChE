import matplotlib.pyplot as plt
g = 9.80665
rho_p = 1800
D_p = 0.208 * 10**(-3)
rho = 994.6
mu = 8.931 * 10**(-4)
tol = 0.00001 # tolerance

# calculate drag coefficient (Cd)
def CD_cal(Re):
    if Re < 0.1:
        return 24/Re
    elif 0.1 < Re < 1000:
        return 24/Re * (1 + 0.14*Re**0.7)
    elif 1000 < Re < 350000:
        return 0.44
    return 0.19 - 8 * 10**4 / Re

# calculate Reynolds number
def Re_cal(D,v,rho,mu):
    return D * v * rho / mu

# calculate terminal velocity
def vt_cal(g,rho_p,rho,D_p,CD):
    return ((4 * g * (rho_p - rho) * D_p) / (3 * CD * rho)) ** 0.5

vt_init = 1 # initial guess

# main function for iteration
def fun(gravity):
    vt_list = [vt_init]
    
    while True:
        Re = Re_cal(D_p,vt_list[-1] ,rho,mu)
        CD = CD_cal(Re)
        vt = vt_cal(gravity,rho_p,rho,D_p,CD)
        vt_list.append(vt)
        
        # Check convergence
        if abs(vt_list[-2] - vt_list[-1]) < tol:
            break
    print(f'Terminal velocity for gravity {gravity:.2f} m/s² is: {vt:.6f} m/s')
   
    plt.plot(range(len(vt_list)),vt_list,'o--', label=f'g = {gravity:.2f} m/s^2' )
    plt.axhline(vt, color='gray', linestyle='--', alpha=0.5, label=f'Final vt for g = {gravity:.2f}')

fun(g) # (a) normal gravity
fun(30 * g) # (b) centrifugal acceleration

plt.legend()
plt.xlabel('Iteration')
plt.ylabel('Terminal velocity (m/s)')
plt.title('Convergence Rate')
plt.tight_layout()
plt.show()