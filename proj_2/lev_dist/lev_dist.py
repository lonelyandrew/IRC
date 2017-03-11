#! /usr/local/bin Python3


def lev_distance(str_one, str_two):
    '''Calculate the levenshtein-distance between two strings.

    Args:
        str_one: The first string in the calculation.
        str_two: The second string in the calculation.

    Returns:
        An integer distance.
    '''

    dims = (len(str_two) + 1, len(str_one) + 1)
    matrix = [[0 for i in range(dims[1])] for j in range(dims[0])]

    for i in range(dims[0]):
        for j in range(dims[1]):
            if i == 0 or j == 0:
                matrix[i][j] = i if j == 0 else j
            else:
                insert_dist = matrix[i][j-1] + 1
                delete_dist = matrix[i-1][j] + 1
                replace_dist = matrix[i-1][j-1]
                if str_one[j-1] != str_two[i-1]:
                    replace_dist += 1
                matrix[i][j] = min([insert_dist, delete_dist, replace_dist])

    return matrix[len(str_two)][len(str_one)]
