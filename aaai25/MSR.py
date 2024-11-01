import random
import math
from vis_exp import *
def compute_MSR(L, x):
    dim = len(L.weights)
    x_class = int(L.eval(x))
    def score(i):
        return L.weights[i]*(2*x[i]-1)*(2*x_class - 1)
        
    feature_scores = [ (i, score(i)) for i in range(dim)]
    feature_scores = sorted(feature_scores, key=lambda p: p[1], reverse=True)
    for k in range(0, dim+1):
        partial_instance = [-1 for xi in x]
        for f in feature_scores[:k]:
            partial_instance[f[0]] = x[f[0]]
            
        if L.all_completions_equal(partial_instance, x_class):
            return k, partial_instance
    
    raise ValueError("We should have found an explanation in the previous for loop")
    
    
def compute_scores(L, x):
    ans = []
    x_eval = L.eval(x)
    for i in range(L.d):
        ans.append(L.weights[i]*(2*x[i]-1)*(2*x_eval - 1))
    return ans
    
    
def random_completion(y):
    completion = [yi for yi in y]
    for i in range(len(y)):
        if y[i] == -1:
            completion[i] = random.randint(0, 1)
    return completion
    
    
def monte_carlo_prob(L, y, M, x_class):
    print("Sampling...")
    cnt = 0
    for i in range(M):
        cnt += int(L.eval(random_completion(y)) == x_class)
        if i % 100:
            print(f"{100*(i+1)/M:.5f}%", end="\r")
    print("\nFinished sampling with prob", cnt / M)
    return cnt / M
    
def compute_delta_MSR(L, x, delta, epsilon, gamma):
    delta_star = (random.random()-0.5)*epsilon + delta
    print(f"delta = {delta}, delta_star = {delta_star}")
    scores = compute_scores(L, x)
    F = [(i, scores[i]) for i in range(L.d)]
    F = sorted(F, key=lambda p: p[1], reverse=True)
    y_ks = [  [-1 for _ in range(L.d)]] 
    for fpair in F:
        last = y_ks[-1]
        copy = [yi for yi in last]
        copy[fpair[0]] = x[fpair[0]]
        y_ks.append(copy)
    
    
    
  
    M = 2*(math.log(L.d)**2) / ((epsilon ** 2) * (gamma ** 2)) * math.log(2*math.log(L.d) / gamma)
    M = int(M)
    
    # simplifcation for test purposes!
    # M = 500000
    print("first part: ", 2*(math.log(L.d)**2) )
    print("second part: ", (epsilon ** 2) * (gamma ** 2))
    print("Number of samples: ", M)
    LB = 0
    UB = L.d
    x_class = L.eval(x)
    while LB != UB:
        k = (LB + UB)//2
        v_k = monte_carlo_prob(L, y_ks[k], M, x_class)
        sufficient_reason_to_image(x, y_ks[k], f"probabilistic_{k}.png")
        print(f"v_{k} = {v_k}")
        if v_k >= delta_star:
            UB = k 
        else:
            LB = k+1
    
    return LB, y_ks[LB], delta_star
        