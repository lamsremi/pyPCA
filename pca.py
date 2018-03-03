"""PCA implementation in pure python + scipy library.
"""
from scipy.linalg import eig


# Step 1:  Substract the mean

def substract_mean(matrix):
    """Substract the mean from each of the data dimensions.
    Args:
        matrix (array like): matrix of data.
    """
    # Dimension
    dimension, size = len(matrix[0]), len(matrix)
    # Get the mean for
    means = [sum([row[col] for row in matrix])/size for col in range(dimension)]
    # Compute the new matrix
    new_matrix = [
        [row[col] - means[col] for col in range(dimension)] for row in matrix
    ]
    return new_matrix


# Step 2: Calculate the covariance matrix

def covariance(vect_X, vect_Y):
    """Compute the covariance betwwen 2 variables.
    """
    # Compute the means
    mean_X, mean_Y = sum(vect_X)/len(vect_X), sum(vect_Y)/len(vect_Y)
    # Compute the covariance
    cov = [(x - mean_X)*(y - mean_Y)
        for x, y in zip(vect_X, vect_Y)]
    cov = sum(cov)/(len(cov)-1)
    return cov


def covariance_matrix(matrix):
    """ Compute the covariance matrix.
    Args:
        matrix (array like): matrix of data.
    Return:
        cov_matrix (array like): covariance squared matrix.
    """
    dimension = len(matrix[0])
    cov_matrix = []
    for col_x in range(dimension):
        cov_row = []
        vect_x = [row[col_x] for row in matrix]
        for col_y in range(dimension):
            vect_y = [row[col_y] for row in matrix]
            cov_row.append(covariance(vect_x, vect_y))
        cov_matrix.append(cov_row)
    return cov_matrix


# Step 3: Calculate the eigenvectors and eigenvalues of the covariance matrix

def scipy_eig(sq_matrix):
    """Compute the eigenvalues and eigenvectors using scipy library.
    Args:
        sq_matrix (array like): square matrix.
    Return:
        eig_values (list): eigenvalues vector of length 1.
        eig_vectors (array like): eigenvectors matrix of length 1
    """
    outputs = eig(sq_matrix)
    eig_values = [eig_val.real for eig_val in outputs[0].tolist()]
    matrix_eig_vectors = outputs[1].tolist()
    eig_vectors = []
    eig_vectors = [list(eig_vect) for eig_vect in zip(*matrix_eig_vectors)]
    return eig_values, eig_vectors


# Step 4: Choose components and form a feature vector

def filter(eig_values, eig_vectors):
    """Filter & sort the eigenvalues and eigenvectors."""
    # Combine
    eig_tuples = [(eig_val, eig_vec) for eig_val, eig_vec in zip(eig_values, eig_vectors)]
    # Filter the components by the eigenvalues : greater than 1
    filt_eig_tuples = [(eig_val, eig_vec) for eig_val, eig_vec in eig_tuples if eig_val >= 1]
    # Sort the tuples based on first value
    sort_eig_tuples = sorted(filt_eig_tuples, reverse=True, key=lambda x: x[0])
    # Uncombine
    filt_eig_values, filt_eig_vectors = zip(*sort_eig_tuples)
    return list(filt_eig_values), list(filt_eig_vectors)


# Step 5: Deriving the new dataset

def multiply(matrix, eig_vectors):
    """Derive the new dataset.
    Args:
        matrix (array like): matrix of data. shape (n, p)
        p is the initial dimension
        n is the number of instances
        eig_vectors (list): list of eigenvectors. shape (m, p)
    Return:
        final_matrix (array like): new matrix. shape (n, m)
        m is the new dimension.
    """
    final_matrix = []
    for row in matrix:
        row_vect = []
        for eig_vec in eig_vectors:
            row_vect.append(sum([eig_vec_val*row_val for eig_vec_val, row_val in zip(eig_vec, row)]))
        final_matrix.append(row_vect)
    return final_matrix


def print_matrix(matrix):
    for row in matrix:
        print(row)


if __name__ == '__main__':

    display = False

    # Initial matrix
    matrix = [
        [2.5, 2.4],
        [0.5, 0.7],
        [2.2, 2.9,],
        [1.9, 2.2],
        [3.1, 3.0],
        [2.3, 2.7],
        [  2, 1.6],
        [  1, 1.1],
        [1.5, 1.6],
        [1.1, 0.9]
    ]
    # cols = ["x", "y"]
    # index = ["1", "2", "3", "4", "5", "6", "7", "8", "9", "10"]

    # Step 1:  Substract the mean.
    new_matrix = substract_mean(matrix)

    # Step 2: Calculate the covariance matrix.
    cov_matrix = covariance_matrix(new_matrix)

    # Step 3: Compute the eigenvectors and eigenvalues of the covariance matrix.
    eig_values, eig_vectors = scipy_eig(cov_matrix)

    # Step 4: Choose components and form a feature vector.
    eig_values, eig_vectors = filter(eig_values, eig_vectors)

    # Step 5: Deriving the new dataset
    final_matrix = multiply(new_matrix, eig_vectors)

    if display:
        print("\n* Substract mean :")
        print_matrix(new_matrix)

        print("\n* Covariance matrix :")
        print_matrix(cov_matri)

        print("\n* Eigenvalues before filtering :")
        print(eig_values)

        print("\n* Eigenvectors before filtering :")
        print_matrix(eig_vectors)

        print("\n* Eigenvalues after filtering :")
        print(eig_values)

        print("\n* Eigenvectors after filtering :")
        print_matrix(eig_vectors)

        print("\n* After PCA :")
        print_matrix(final_matrix)

        """
        # Expected Results if no components filtered
        matrix = [
            [-0.827970186, -0.175115307],
            [1.77758033, 0.142857227],
            [-0.992197494, 0.384374989],
            [-0.274210416, 0.130417207],
            [-1.67580142, -0.209498461],
            [-0.912949103, 0.175282444],
            [0.0991094375, -0.349824698],
            [1.14457216, 0.0464172582],
            [0.438046137, 0.0177646297],
            [1.22382056, -0.162675287]
        ]
        """

