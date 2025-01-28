import numpy as np

# Feed composition
Feed = 70
Fx, Fs, Ft, Fb = 0.15, 0.25, 0.40, 0.20
# D1 compositions
D1x, D1s, D1t, D1b = 0.07, 0.04, 0.54, 0.35
# D2 compositions
D2x, D2s, D2t, D2b = 0.15, 0.10, 0.54, 0.21
# B1 compositions
B1x, B1s, B1t, B1b = 0.18, 0.24, 0.42, 0.21
# B2 compositions
B2x, B2s, B2t, B2b = 0.24, 0.65, 0.10, 0.01

def overal():
    A = np.array([[D1x, D2x, B1x, B2x],
                  [D1s, D2s, B1s, B2s],
                  [D1t, D2t, B1t, B2t],
                  [D1b, D2b, B1b, B2b]])
    
    b = np.array([Fx, Fs, Ft, Fb]) * Feed
    
    x = np.linalg.solve(A, b) 
    x = [float(i) for i in x]
    return {'D1' : x[0],
            'D2' : x[1],
            'B1' : x[2],
            'B2' : x[3]}

print('----------   a   ----------')
sol = overal()

for key,value in sol.items():
    print(key ,':', value , 'mole')
    
print('----------   b   ----------')
print('D :', sol['B1'] + sol['D1'] , 'mole')
print('B :', sol['B2'] + sol['D2'] , 'mole')