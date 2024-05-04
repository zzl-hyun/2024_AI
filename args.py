import argparse

def main(m=10, n=10):
    # Your main logic here
    print("Grid world size:", m, "x", n)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Set up a maze of size m x n.')
    parser.add_argument('--m', type=int, default=10, help='Number of rows in the grid')
    parser.add_argument('--n', type=int, default=10, help='Number of columns in the grid')
    args = parser.parse_args()
    main(args.m, args.n)
