from scipy.optimize import fsolve
CA0 = 1.5
CB0 = 1.5
KC1 = 1.06
KC2 = 2.63
KC3 = 5

def eqs(S):
    CA, CB, CC, CD, CX, CY, CZ = S
    return [
        CA0 - CD - CZ - CA,
        CB0 - CD - CY - CB,
        CD - CY - CC,
        CX + CZ - CY,
        - CC * CD / (CA * CB) + KC1,
        - CX * CY / (CB * CC) + KC2,
        - CZ / (CA * CX) + KC3,
    ]

# Note: This iterative solution is highly sensitive to the initial guesses.
# Based on observations, only the initial guesses provided in part (b) of the question
# lead to convergence. Other initial guesses fail to converge or result in incorrect solutions.
initial_guess = [0.5, 0.5, 0.5, 1, 1, 0.1, 1]
CA, CB, CC, CD, CX, CY, CZ = fsolve(eqs, initial_guess)
print(f"CA = {CA:.3f}, CB = {CB:.3f}, CC = {CC:.3f}, CD = {CD:.3f}, CX = {CX:.3f}, CY = {CY:.3f}, CZ = {CZ:.3f}")
print(f'KC1 = {CC*CD/CA/CB:.2f}')
print(f'KC2 = {CX*CY/CB/CC:.2f}')
print(f'KC3 = {CZ/CA/CX:.2f}')