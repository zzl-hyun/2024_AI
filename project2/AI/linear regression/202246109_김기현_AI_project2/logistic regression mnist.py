from sklearn import datasets
import matplotlib.pyplot as plt
import numpy as np
from sklearn.metrics import accuracy_score
import argparse

def sigmoid(z):
    return 1 / (1 + np.exp(-z))

def sgd_logistic_regression(X_train, y_train, X_dev, y_dev, X_test, y_test, m, max_epochs=100, learning_rate=0.01):
    n, d = X_train.shape
    w = np.zeros(d)
    b = 0

    train_losses = []
    dev_losses = []
    test_losses = []

    no_improvement = 0
    best_dev_loss = float('inf')

    for epoch in range(max_epochs):
        perm = np.random.permutation(n)
        mini_batches = [perm[k:k+m] for k in range(0, n, m)]

        for batch in mini_batches:
            X_batch = X_train[batch]
            y_batch = y_train[batch]

            z = np.dot(X_batch, w) + b
            y_pred = sigmoid(z)
            
            w_grad = np.dot(X_batch.T, (y_pred - y_batch)) / len(X_batch)
            b_grad = np.mean(y_pred - y_batch)
        
            w -= learning_rate * w_grad
            b -= learning_rate * b_grad

        # 손실 계산
        z_train = np.dot(X_train, w) + b
        y_train_pred = sigmoid(z_train)
        
        z_dev = np.dot(X_dev, w) + b
        y_dev_pred = sigmoid(z_dev)
        
        z_test = np.dot(X_test, w) + b
        y_test_pred = sigmoid(z_test)

        train_loss = -np.mean(y_train * np.log(y_train_pred) + (1 - y_train) * np.log(1 - y_train_pred))
        dev_loss = -np.mean(y_dev * np.log(y_dev_pred) + (1 - y_dev) * np.log(1 - y_dev_pred))
        test_loss = -np.mean(y_test * np.log(y_test_pred) + (1 - y_test) * np.log(1 - y_test_pred))

        train_losses.append(train_loss)
        dev_losses.append(dev_loss)
        test_losses.append(test_loss)

        print(f"Epoch {epoch+1}/{max_epochs} - Train Loss: {train_loss}, Dev Loss: {dev_loss}, Test Loss: {test_loss}")

        if dev_loss < best_dev_loss:
            best_dev_loss = dev_loss
            best_w, best_b = w.copy(), b
            no_improvement = 0
        else:
            no_improvement += 1
            if no_improvement > 10:
                print(f"Early stopping after {epoch+1} epochs")
                break

    return best_w, best_b, train_losses, dev_losses, test_losses

def test_sgd_with_datasets(m, e):
    # diabetes 로딩
    X, y = datasets.fetch_openml('mnist_784', version=1, return_X_y=True)

    # diabetes dataset 분할
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

    # 세팅
    max_epochs = e
    learning_rate = 0.01  


    # diabetes dataset 학습
    w_diabetes, b_diabetes, mse_train_diabetes, mse_dev_diabetes, mse_test_diabetes = sgd_logistic_regression(
        X_train_diabetes, y_train_diabetes, X_dev_diabetes, y_dev_diabetes, X_test_diabetes, y_test_diabetes, m, max_epochs, learning_rate)

    print(f"Trained w on diabetes dataset: {w_diabetes}")
    print(f"Trained b on diabetes dataset: {b_diabetes}")


    # Plot MSE
    fig, axs = plt.subplots(2, 2, figsize=(10, 10))

    axs[0, 0].plot(mse_train_diabetes, label='Train MSE (Diabetes)')
    axs[0, 0].plot(mse_dev_diabetes, label='Dev MSE (Diabetes)')
    axs[0, 0].plot(mse_test_diabetes, label='Test MSE (Diabetes)')
    axs[0, 0].set_title('Train MSE (Diabetes)')
    axs[0, 0].set_xlabel('Epoch')
    axs[0, 0].set_ylabel('Mean Squared Error')
    plt.legend()
    plt.tight_layout()
    plt.show()

def main(m, e):
    test_sgd_with_datasets(m, e)
    
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='options: --m')
    parser = argparse.ArgumentParser(description='options: --e')
    parser.add_argument('--m', type=int, default=10, help='Set batch size')
    parser.add_argument('--e', type=int, default=100, help='Set epoch size')
    args = parser.parse_args()
    main(args.m, args.e)