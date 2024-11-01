

probs = [0.5]*100 + [0.02]*100
values = [100]*100 + [15000]*100

MEMO = {}
def DP(i, k, V):
    """
    Optimal probability of reaching at least V, using at most k out of the first i indices
    Returns the probability and the list of selected items
    """
    if (i, k, V) in MEMO:
        return MEMO[(i, k, V)]
        
    if V <= 0:
        return 1, []
        
    if k == 0 or i < 0:
        return 0, []
   
    prob_with_i = probs[i] * DP(i-1, k-1, V-values[i])[0] + (1-probs[i]) * DP(i-1, k-1, V)[0]
    prob_without_i = DP(i-1, k, V)[0]
    
    if prob_with_i > prob_without_i:
        prob, selected = DP(i-1, k-1, V-values[i])
        selected.append(i)
        ans = (probs[i] * prob + (1-probs[i]) * DP(i-1, k-1, V)[0], selected)
    else:
        ans = DP(i-1, k, V)
    
    MEMO[(i, k, V)] = ans
    return ans
    
    
def compute(k, V):
    prob, selected = DP(len(probs)-1, k, V)
    print(f"Probability: {prob}")
    print(f"Selected items: {selected}")
    
    
compute(50, 1500)

