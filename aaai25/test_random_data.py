from sklearn.linear_model import LogisticRegression
import numpy as np
from linear_model import LinearModel
import random 



def generate_random_vec(dim):
    return [random.randint(0, 1) for _ in range(dim)]
    
def generate_random_dataset(dim=10, n_samples=100):
    X = []
    y = []
    for _ in range(n_samples):
        y.append(random.randint(0, 1))
        X.append(generate_random_vec(dim))
    return X, y
        
        

X, y = generate_random_dataset()
model = LogisticRegression()
model.fit(np.array(X), np.array(y))

linear_model = LinearModel.from_SKLearn(model)


for i in range(10):
    x = generate_random_vec(10)
    print(model.predict([x]), linear_model.eval(x))