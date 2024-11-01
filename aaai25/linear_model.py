from sklearn.linear_model import LogisticRegression

class LinearModel:
    def __init__(self, weights, t):
        self.weights = weights
        self.d = len(weights)
        self.threshold = t 
        
    def eval(self, instance):
        assert len(instance) == self.d
        ans = 0
        for i in range(self.d):
            ans += instance[i]*self.weights[i]
        return int(ans >= self.threshold)
        
    @staticmethod
    def from_SKLearn(model):
        return LinearModel(model.coef_[0], - model.intercept_[0])
        
        
    def all_completions_equal(self, partial_instance, target_class):
        dotprod = 0
        for i in range(len(partial_instance)):
            if partial_instance[i] != -1:
                dotprod += partial_instance[i]*self.weights[i]
            else:
                if int(self.weights[i] < 0)  == target_class:
                    dotprod += self.weights[i]
        return int(dotprod >= self.threshold) == target_class
            