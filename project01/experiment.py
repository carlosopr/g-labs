import numpy as np
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error, r2_score

class PreprocessData:
    
    def load_data(self, path_file):
        
        # Binary file path is loaded
        data = np.load(path_file)

        # Print confirmation
        print('Data loaded!')
        
        return data
    

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

        print(f"Total elements for X_train: {len(X_train)}, X_test: {len(X_test)}")
        print(f"Total elements for y_train: {len(y_train)}, y_test: {len(y_test)}")
        
        return X_train, y_train, X_test, y_test


    def scale_and_normalize(self, X):

        # Min-Max scaling
        X_scaled = (X - X.min(axis=0)) / (X.max(axis=0) - X.min(axis=0))

        # Z-score normalization
        X_normalized = (X_scaled - X_scaled.mean(axis=0)) / X_scaled.std(axis=0)

        return X_normalized


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
    

    def train_with_skl(self, X, y):
        
        # Train the linear regression model on the input data
        skl_model = LinearRegression().fit(X.reshape(-1, 1), y)
        print("Trained!")

        return skl_model
    

    def predict_from_custom_model(self, custom_model, x, y):
        
        # Add a column of ones to x for the intercept term to evaluate the custom model
        X = np.c_[x, np.ones(x.shape[0])]
        
        # Get the parameters for the last iteration
        last_iteration = len(custom_model)
        beta0, beta1 = custom_model[last_iteration]

        # Calculate the predicted values
        predictions = np.dot(X, [beta0, beta1])

        print("Metrics for the Custom Model:")
        mse = mean_squared_error(y, predictions)
        print("MSE:", mse)
        rmse = np.sqrt(mse)
        print("RMSE:", rmse)
        r2 = r2_score(y, predictions)
        print("R2:", r2)
        
        return predictions


    def predict_from_skl_model(self, skl_model, x, y):
        
        # Evaluate the skl model using the test data
        predictions = skl_model.predict(x.reshape(-1, 1))

        print("Metrics for the Scikit-learn Model:")
        mse = mean_squared_error(y, predictions)
        print("MSE:", mse)
        rmse = np.sqrt(mse)
        print("RMSE:", rmse)
        r2 = r2_score(y, predictions)
        print("R2:", r2)

        return predictions
    
    def evaluate_models(self, custom_predictions, skl_predictions, y):

        predictions_avg = np.mean([custom_predictions, skl_predictions], axis=0)

        print("Metrics for the avg predictions:")
        mse = mean_squared_error(y, predictions_avg)
        print("MSE:", mse)
        rmse = np.sqrt(mse)
        print("RMSE:", rmse)
        r2 = r2_score(y, predictions_avg)
        print("R2:", r2)

        return predictions_avg
