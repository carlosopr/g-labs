import numpy as np
import matplotlib.pyplot as plt

class DataPlotter:

    def plot_error(iter_error):
        fig, ax = plt.subplots()
        ax.plot(range(1, len(iter_error) + 1), iter_error)
        ax.set_xlabel('Iterations')
        ax.set_ylabel('Error')
        ax.set_title('Error vs. Iterations')
        plt.show()


    def plot_evolution(model_dict, n, X, y):
        # Extract the model parameters at intervals of n
        keys = range(0, len(model_dict), n)
        models = [model_dict[k] for k in keys if k in model_dict]
        
        # Plot the data
        plt.scatter(X, y, s=5, alpha=0.7)
        
        # Plot the predicted values for each model
        for model in models:
            X_aug = np.c_[X, np.ones(X.shape[0])]
            y_pred = np.dot(X_aug, model)
            plt.plot(X, y_pred)
        
        plt.xlabel("X")
        plt.ylabel("y")
        plt.title("Model prediction")
        plt.show()



