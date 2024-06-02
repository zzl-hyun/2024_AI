import numpy as np
import pickle

def generate_dataset(N, d, R=10, alpha=0.1):
    w = np.random.uniform(-R, R, d)
    b = np.random.uniform(-R, R)
    X = np.random.uniform(-R, R, (N, d))
    sigma = alpha * R
    y = X @ w + b + np.random.normal(0, sigma, N)
    return X, y, w, b

def split_dataset(X, y, train_ratio=0.85, dev_ratio=0.05, test_ratio=0.10):
    total_samples = X.shape[0]
    indices = np.random.permutation(total_samples)
    
    # Calculate number of samples for each set
    train_end = int(train_ratio * total_samples)
    dev_end = train_end + int(dev_ratio * total_samples)
    
    # Split the indices for training, development and test sets
    train_indices = indices[:train_end]
    dev_indices = indices[train_end:dev_end]
    test_indices = indices[dev_end:]
    
    # Create subsets for training, development, and test sets
    X_train, y_train = X[train_indices], y[train_indices]
    X_dev, y_dev = X[dev_indices], y[dev_indices]
    X_test, y_test = X[test_indices], y[test_indices]
    
    return (X_train, y_train), (X_dev, y_dev), (X_test, y_test)

def save_dataset(data, filename="myrandomdataset.pkl"):
    with open(filename, "wb") as f:
        pickle.dump(data, f)

if __name__ == "__main__":
    #N = 1000 
    #N = 10000 
    N = 100000 
    d = 5     
    R = 10  
    alpha = 0.1  

    # Generate dataset
    X, y, w, b = generate_dataset(N, d, R, alpha)
    
    # Split dataset
    (X_train, y_train), (X_dev, y_dev), (X_test, y_test) = split_dataset(X, y)

    # Save datasets
    data_to_save = {
        'train': (X_train, y_train),
        'dev': (X_dev, y_dev),
        'test': (X_test, y_test),
        'params': {'w': w, 'b': b}
    }
    save_dataset(data_to_save)

    print("Datasets saved successfully.")
