import numpy as np

class PreprocessData:
    def load_data(self, path_file):
        
        # Binary file path is loaded
        data = np.load(path_file)

        # Print confirmation
        print('Data loaded!')
        
        return data
        

    #def handle_missing_values(self):
    #    pass

    def split_data(self, X, y, split_percentage):
        
        # Concatenate X and y to shuffle the data
        data = np.concatenate((X.reshape(-1, 1), y.reshape(-1, 1)), axis=1)
        np.random.shuffle(data)
        
        # Calculate the split index based on the split percentage
        split_index = int(len(data) * split_percentage)
        
        # Split data and extract the feature and label values
        train_data = data[:split_index]
        test_data = data[split_index:]
        
        X_train, y_train = train_data[:, 0], train_data[:, 1]
        X_test, y_test = test_data[:, 0], test_data[:, 1]
        
        return X_train, y_train, X_test, y_test
        


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
            if (epoch+1) % print_error_interval == 0:
                print(f"Epoch {(epoch+1)}, error: {error}")
            
            # Computing the gradients
            gradients = -2 * np.dot(x.T, y - y_pred) / x.shape[0]
            
            # Updating the parameters
            beta -= alpha * gradients
            
            # Storing the model parameters
            self.model[epoch+1] = beta.copy()
        
        return self.model, self.errors


# Define a plotter class