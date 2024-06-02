import numpy as np
import pickle
import matplotlib.pyplot as plt
from sklearn import datasets
from sklearn.metrics import mean_squared_error
import argparse

def load_dataset_from_pickle(filename):
    with open(filename, "rb") as f:
        data = pickle.load(f)
    return data

def sgd_linear_regression(X_train, y_train, X_dev, y_dev, X_test, y_test, m, max_epochs=100, eta=0.01):
    n, d = X_train.shape
    w = np.zeros(d)
    b = 0

    mse_train = []
    mse_dev = []
    mse_test = []

    # Early stopping criteria
    no_improvement = 0
    best_dev_error = float('inf')

    for epoch in range(max_epochs):
        perm = np.random.permutation(n)
        mini_batches = [perm[k:k+m] for k in range(0, n, m)]

        for batch in mini_batches:
            X_batch = X_train[batch]
            y_batch = y_train[batch]

            y_pred = X_batch.dot(w) + b
            error = y_pred - y_batch

            w_grad = X_batch.T.dot(error) / m
            b_grad = np.mean(error)

            w -= eta * w_grad
            b -= eta * b_grad

        # Calculate MSE for training, dev, and test sets
        y_train_pred = X_train.dot(w) + b
        y_dev_pred = X_dev.dot(w) + b
        y_test_pred = X_test.dot(w) + b

        train_error = mean_squared_error(y_train, y_train_pred)
        dev_error = mean_squared_error(y_dev, y_dev_pred)
        test_error = mean_squared_error(y_test, y_test_pred)

        mse_train.append(train_error)
        mse_dev.append(dev_error)
        mse_test.append(test_error)

        print(f"Epoch {epoch+1}/{max_epochs} - Train MSE: {train_error}, Dev MSE: {dev_error}, Test MSE: {test_error}")

        if dev_error < best_dev_error:
            best_dev_error = dev_error
            best_w, best_b = w.copy(), b
            no_improvement = 0
        else:
            no_improvement += 1
            if no_improvement >= 10:
                print(f"Early stopping after {epoch+1} epochs")
                break

    return best_w, best_b, mse_train, mse_dev, mse_test

def test_sgd_with_datasets(m):
    # Load diabetes dataset from sklearn
    diabetes = datasets.load_diabetes()
    X, y = diabetes.data, diabetes.target

    # Split the diabetes dataset
    n_diabetes = X.shape[0]
    indices_diabetes = np.random.permutation(n_diabetes)
    train_end = int(0.85 * n_diabetes)
    dev_end = train_end + int(0.05 * n_diabetes)

    train_indices = indices_diabetes[:train_end]
    dev_indices = indices_diabetes[train_end:dev_end]
    test_indices = indices_diabetes[dev_end:]

    X_train_diabetes, y_train_diabetes = X[train_indices], y[train_indices]
    X_dev_diabetes, y_dev_diabetes = X[dev_indices], y[dev_indices]
    X_test_diabetes, y_test_diabetes = X[test_indices], y[test_indices]

    # Settings
    max_epochs = 100
    eta = 0.01  # Learning rate

    # Load our custom dataset
    custom_data = load_dataset_from_pickle("myrandomdataset1.pkl")
    X_custom_train, y_custom_train = custom_data['train']
    X_custom_dev, y_custom_dev = custom_data['dev']
    X_custom_test, y_custom_test = custom_data['test']
    true_w, true_b = custom_data['params']['w'], custom_data['params']['b']

    # Train on diabetes dataset
    w_diabetes, b_diabetes, mse_train_diabetes, mse_dev_diabetes, mse_test_diabetes = sgd_linear_regression(
        X_train_diabetes, y_train_diabetes, X_dev_diabetes, y_dev_diabetes, X_test_diabetes, y_test_diabetes, m, max_epochs, eta)

    print(f"Trained w on diabetes dataset: {w_diabetes}")
    print(f"Trained b on diabetes dataset: {b_diabetes}")

    # Train on custom dataset
    w_custom, b_custom, mse_train_custom, mse_dev_custom, mse_test_custom = sgd_linear_regression(
        X_custom_train, y_custom_train, X_custom_dev, y_custom_dev, X_custom_test, y_custom_test, m, max_epochs, eta)

    print(f"Trained w on custom dataset: {w_custom}")
    print(f"Trained b on custom dataset: {b_custom}")
    print(f"True w: {true_w}")
    print(f"True b: {true_b}")

    # Plot MSE for both datasets
    fig, axs = plt.subplots(2, 2, figsize=(15, 10))

    # Plot for diabetes dataset
    axs[0, 0].plot(mse_train_diabetes, label='Train MSE (Diabetes)')
    axs[0, 0].set_title('Train MSE (Diabetes)')
    axs[0, 0].set_xlabel('Epoch')
    axs[0, 0].set_ylabel('Mean Squared Error')
    axs[0, 0].plot(mse_dev_diabetes, label='Dev MSE (Diabetes)')
    axs[0, 0].plot(mse_test_diabetes, label='Test MSE (Diabetes)')

    # Plot for custom dataset
    axs[0, 1].plot(mse_train_custom, label='Train MSE (Custom)')
    axs[0, 1].set_title('Train MSE (Custom)')
    axs[0, 1].set_xlabel('Epoch')
    axs[0, 1].set_ylabel('Mean Squared Error')
    axs[0, 1].plot(mse_dev_custom, label='Dev MSE (Custom)')
    axs[0, 1].plot(mse_test_custom, label='Test MSE (Custom)')
    plt.legend()

    plt.tight_layout()
    plt.show()

def main(m):
    test_sgd_with_datasets(m)
    
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='options: --m --n --r')
    parser.add_argument('--m', type=int, default=10, help='Set batch size')
    args = parser.parse_args()
    main(args.m)