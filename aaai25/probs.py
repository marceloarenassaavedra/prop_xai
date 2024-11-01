from fractions import Fraction 


class Lin:
    def __init__(self, weights, t):
        self.weights = weights
        self.d = len(weights)
        self.threshold = t 
        
    def eval(self, instance):
        assert len(instance) == self.d
        ans = 0
        for i in range(self.d):
            ans += instance[i]*self.weights[i]
        return ans >= self.threshold
        
    
def gen_completions(y):
    def backtrack(index, current):
        if index == len(y):
            result.append(current[:])
            return
        
        if y[index] == 1 or y[index] == 0:
            current.append(y[index])
            backtrack(index + 1, current)
            current.pop()
        else:  # y[index] == -1
            for val in [0, 1]:
                current.append(val)
                backtrack(index + 1, current)
                current.pop()

    result = []
    backtrack(0, [])
    return result
    

def compute_prob(L, x, y):
    assert len(x) == len(y)
    x_eval = L.eval(x)
    comp_y = gen_completions(y)
    num = 0
    for z in comp_y:
        if L.eval(z) == x_eval:
            num += 1
    return Fraction(num, len(comp_y))
    
    
def generate_y_vectors(x, k):
    def backtrack(index, current, non_negative_count):
        if index == len(x):
            if non_negative_count == k:
                result.append(current[:])
            return
        
        # Always try -1
        current.append(-1)
        backtrack(index + 1, current, non_negative_count)
        current.pop()
        
        # If we haven't used up all our non-negative values and it matches x
        if non_negative_count < k and x[index] in [0, 1]:
            current.append(x[index])
            backtrack(index + 1, current, non_negative_count + 1)
            current.pop()

    result = []
    backtrack(0, [], 0)
    return result
    
    
L = Lin([5, 1, -3, 2, -1], 5)
x = [1, 0, 0, 1, 1]

assert L.eval(x)

data = []
for y in generate_y_vectors(x, 2):
    y_indices = list(filter(lambda i: y[i] != -1, range(len(y))) )
    prob = compute_prob(L, x, y)
    print(y, "indices:", y_indices, "prob: ", prob)
    data.append((y, y_indices, prob))
    
data = sorted(data, key=lambda datum: float(datum[2]), reverse=True)

print('\n')

def to_table(y, y_indices, prob):
    ans = []
    def p_inst(partial):
        str_partial = list(map(lambda f: str(f) if f != -1 else r'\bot', partial))
        return '$(' + ', \,'.join(str_partial) + ')$'
        
    ans.append(p_inst(y))
    
    def to_set(indices):
        indp = [ind + 1 for ind in indices]
        return '$\{' +  ', \,'.join(list(map(str, indp))) + '\}$'
        
    if y_indices is not None:
        ans.append(to_set(y_indices))
    
    def to_nice_frac(prob):
        return rf'$\nicefrac{{ {prob.numerator} }}{{ {prob.denominator} }}$'
    
    ans.append(to_nice_frac(prob))
    return ' & '.join(ans) + r'\\'

for datum in data:
    y, y_indices, prob = datum
    print(to_table(y, y_indices, prob))


y_ks = []
scores = [(i, L.weights[i]*(2*x[i]-1)) for i in range(len(x))]
sscores = sorted(scores, key=lambda p: p[1], reverse=True)
for k in range(len(x)+1):
    y_k = [-1 for _ in range(len(x))]
    for l in range(k):
        y_k[sscores[l][0]] = x[sscores[l][0]]
    y_ks.append(y_k)
print("\n===========================\n")
data = [(y_ks[i], None, compute_prob(L, x, y_ks[i])) for i in range(k+1)]
for datum in data:
    y, y_indices, prob = datum
    print(to_table(y, y_indices, prob))
    # print(y, "indices:", y_indices, "prob: ", prob)
# print(generate_y_vectors(x, 2))


            
    
   
