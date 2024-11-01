from sklearn.linear_model import LogisticRegression
import numpy as np
from linear_model import LinearModel


# Define the input features and target labels
X = np.array([[1, 0, 0, 1], [0, 0, 1, 0], [1, 1, 0, 0]])
y = np.array([1, 0, 0])

# Create and train the logistic regression model
model = LogisticRegression()
model.fit(X, y)

# Print the model coefficients and intercept
print("Coefficients:", model.coef_)
print("Intercept:", model.intercept_)

L = LinearModel.fromSKLearn(model)

for i in range(len(y)):
    print('y[i] = ', y[i], " eval = ", L.eval(list(X[i])), "predict =", model.predict([X[i]]))
    
    
print(model.predict_proba(X))