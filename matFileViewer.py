import argparse

import scipy.io

def view_mat_file(file_path):
    mat_contents = scipy.io.loadmat(file_path)
    for key, value in mat_contents.items():
        if not key.startswith('__'):
            print(f"{key}: {value}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='View contents of a .mat file.')
    parser.add_argument('input_path', type=str, help='Path to the .mat file')
    args = parser.parse_args()
    
    view_mat_file(args.input_path)