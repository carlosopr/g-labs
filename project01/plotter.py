import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

class DataPlotter:

    def plot_distribution(dataframe, target, title):
        # Get the label column
        label = dataframe[target]

        # Create a figure for 2 subplots (2 rows, 1 column)
        fig, ax = plt.subplots(2, 1, figsize = (9,12))

        # Plot the histogram   
        ax[0].hist(label, bins=100)
        ax[0].set_ylabel('Frequency')

        # Add lines for the mean, median, and mode
        ax[0].axvline(label.mean(), color='magenta', linestyle='dashed', linewidth=2)
        ax[0].axvline(label.median(), color='cyan', linestyle='dashed', linewidth=2)

        # Plot the boxplot   
        ax[1].boxplot(label, vert=False)
        ax[1].set_xlabel(target)

        # Add a title to the Figure
        fig.suptitle(title)

        # Show the figure
        fig.show()


    def plot_features(dataframe, feature):
        # Create a figure for the plot
        fig, ax = plt.subplots(figsize=(9, 6))

        # Define a histogram with seaborn and graph the mean and median values
        sns.histplot(data=dataframe[feature], ax=ax, kde=True, bins=100, edgecolor='none')
        ax.axvline(dataframe[feature].mean(), color='magenta', linestyle='dashed', linewidth=1)
        ax.axvline(dataframe[feature].median(), color='orange', linestyle='dashed', linewidth=1)
        
        # Setting up the plot
        ax.set_ylabel('Frequency')
        ax.set_title(feature)

        # Show the plot
        plt.show()

    
    def plot_correlation(dataframe, feature,  target):
        # Create the figure for the plot
        fig = plt.figure(figsize=(9, 6))
        ax = fig.gca()

        # Define the feature and target values from dataframe
        ft = dataframe[feature]
        label = dataframe[target]

        # Get the correlation
        correlation = ft.corr(label)

        # Set up the plot
        plt.scatter(x=ft, y=label, s=5, alpha=0.7)
        plt.xlabel(feature)
        plt.ylabel(target)
        ax.set_title(target + ' ' + feature + ' - Correlation: ' + str(correlation), fontweight='bold')
        
        # Show the plot
        plt.show()


    def plot_error(iter_error):
        # Create a figure for the plot
        fig, ax = plt.subplots()

        # Setting up the plot
        ax.plot(range(1, len(iter_error) + 1), iter_error)
        ax.set_xlabel('Iterations')
        ax.set_ylabel('Error')
        ax.set_title('Error vs. Iterations')

        # Show the plot
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
        
        # Setting up the plot
        plt.xlabel("X")
        plt.ylabel("y")
        plt.title("Model prediction")

        # Show the plot
        plt.show()



