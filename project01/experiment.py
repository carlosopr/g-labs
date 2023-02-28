import numpy as np

class CustomModel:
    
    def __init__(self):
        self.model = {}
        self.errors = []
    
    def train(self, x, y, epochs, print_error_interval, alpha):
        
        # Adding a column of 1s to the feature matrix
        x = np.c_[x, np.ones(x.shape[0])]
        
        # Initializing the model parameters randomly
        beta = np.random.rand(x.shape[1])
        
        for epoch in range(epochs):
            
            # Computing the predicted values
            y_pred = np.dot(x, beta)
            
            # Computing the error
            error = np.mean((y - y_pred)**2)
            self.errors.append(error)
            
            # Printing the error every print_error_interval epochs
            if epoch % print_error_interval == 0:
                print(f"Epoch {epoch}, error: {error}")
            
            # Computing the gradients
            gradients = -2 * np.mean(x * (y - y_pred).reshape(-1,1), axis=0)
            
            # Updating the parameters
            beta -= alpha * gradients
            
            # Storing the model parameters
            self.model[epoch] = beta.copy()
        
        return self.model, self.errors
