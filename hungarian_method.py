def hungarian_step(mat):
    """
        Step 1 – In the given cost matrix, subtract the least cost element of each row from all the entries in that row. Make sure that each row has at least one zero.
        Step 2 – In the resultant cost matrix produced in step 1, subtract the least cost element in each column from all the components in that column, ensuring that each column contains at least one zero.
    """
    for row_num in range(len(mat)):
        min_val = min(mat[row_num])
        mat[row_num] = [ele - min_val for ele in mat[row_num]]

    for col_num in range(len(mat[0])):
        column = [mat[row_num][col_num] for row_num in range(len(mat))]
        min_val = min(column)
        for row_num in range(len(mat)):
            mat[row_num][col_num] -= min_val

    return mat

def min_zeros(zero_mat, mark_zero):
    """
     Step 3 - Mark zeros in the matrix to identify a possible assignment of tasks to agents.
    """
    min_row = [99999, -1]

    for row_num in range(len(zero_mat)):
        count_zeros = zero_mat[row_num].count(True)
        if count_zeros > 0 and min_row[0] > count_zeros:
            min_row = [count_zeros, row_num]

    zero_index = zero_mat[min_row[1]].index(True)
    mark_zero.append((min_row[1], zero_index))
    zero_mat[min_row[1]] = [False] * len(zero_mat[0])
    for row in zero_mat:
        row[zero_index] = False

def mark_matrix(mat):
    """
     Step 4 - Mark rows and columns to cover all zeros in the matrix and create as many assignments as possible.
    """
    zero_bool_mat = [[ele == 0 for ele in row] for row in mat]
    zero_bool_mat_copy = [row[:] for row in zero_bool_mat]

    marked_zero = []
    while any(True in row for row in zero_bool_mat_copy):
        min_zeros(zero_bool_mat_copy, marked_zero)

    marked_zero_row = [ele[0] for ele in marked_zero]
    marked_zero_col = [ele[1] for ele in marked_zero]

    non_marked_row = list(set(range(len(mat))) - set(marked_zero_row))
    marked_cols = []
    check_switch = True

    while check_switch:
        check_switch = False
        for row_num in non_marked_row:
            row_array = zero_bool_mat[row_num]
            for col_num in range(len(row_array)):
                if row_array[col_num] and col_num not in marked_cols:
                    marked_cols.append(col_num)
                    check_switch = True

        for row_num, col_num in marked_zero:
            if row_num not in non_marked_row and col_num in marked_cols:
                non_marked_row.append(row_num)
                check_switch = True

    marked_rows = list(set(range(len(mat))) - set(non_marked_row))
    return marked_zero, marked_rows, marked_cols

def adjust_matrix(mat, cover_rows, cover_cols):
    """
    Step 5 - Adjust the cost matrix to create more zeros without violating the assignment constraints.
    """
    non_zero_element = [mat[row][col] for row in range(len(mat)) if row not in cover_rows
                        for col in range(len(mat[row])) if col not in cover_cols]

    min_num = min(non_zero_element)

    for row in range(len(mat)):
        if row not in cover_rows:
            for col in range(len(mat[row])):
                if col not in cover_cols:
                    mat[row][col] -= min_num

    for row in cover_rows:
        for col in cover_cols:
            mat[row][col] += min_num

    return mat

def hungarian_algorithm(cost_matrix):
    """
        The main algorithm which uses the prior functions to iteratively conduct each steps.
    """
    n = len(cost_matrix)
    print("new hungarian input size:", n)
    cur_mat = [row[:] for row in cost_matrix]

    cur_mat = hungarian_step(cur_mat)

    count_zero_lines = 0

    while count_zero_lines < n:
        ans_pos, marked_rows, marked_cols = mark_matrix(cur_mat)
        count_zero_lines = len(marked_rows) + len(marked_cols)

        if count_zero_lines < n:
            cur_mat = adjust_matrix(cur_mat, marked_rows, marked_cols)

    return ans_pos

# Get the total sum from the hungarian algorithm result
def get_sum(cost_matrix, result):
    total_sum = 0
    for i in range(len(result)):
        total_sum += cost_matrix[result[i][0]][result[i][1]]
    return total_sum


if __name__ == "__main__":
    cost_matrix = [
    [20, 15, 18, 20, 25],
    [18, 20, 12, 14, 15],
    [21, 23, 25, 27, 25],
    [17, 18, 21, 23, 20],
    [18, 18, 16, 19, 20]
    ]
    result = hungarian_algorithm(cost_matrix)
    print("Total:", get_sum(cost_matrix, result), "Resulting matrix:", result)

# cost_matrix = [
#     [16, 59, 74, 42, 35, 31, 43, 59, 6, 38],
#     [14, 43, 84, 26, 36, 49, 12, 21, 22, 19],
#     [87, 77, 83, 27, 26, 38, 83, 84, 91, 44],
#     [5, 67, 89, 9, 62, 40, 79, 71, 86, 62],
#     [39, 10, 63, 69, 97, 56, 64, 63, 62, 72],
#     [34, 31, 30, 62, 72, 79, 51, 65, 17, 53],
#     [61, 20, 75, 78, 75, 17, 14, 9, 24, 57],
#     [85, 94, 70, 22, 70, 33, 25, 5, 18, 64],
#     [30, 52, 4, 58, 62, 40, 28, 88, 45, 3],
#     [75, 98, 15, 16, 54, 49, 10, 50, 4, 60]
# ]

# cost_matrix = [
#     [20, 15, 18, 20, 25],
#     [18, 20, 12, 14, 15],
#     [21, 23, 25, 27, 25],
#     [17, 18, 21, 23, 20],
#     [18, 18, 16, 19, 20]
# ]

# cost_matrix = [
#     [31, 53, 8, 34, 29], 
#     [98, 11, 49, 56, 2], 
#     [48, 69, 34, 60, 34], 
#     [73, 76, 15, 80, 25], 
#     [19, 70, 78, 86, 86]
# ]      

# cost_matrix = [
#     [82, 83, 69, 92],
#     [77, 37, 49, 92],
#     [11, 69, 5, 86],
#     [8, 9, 98, 23]
# ]

# result = hungarian_algorithm(cost_matrix)
# print(result)

# https://brc2.com/the-algorithm-workshop/
# https://software.clapper.org/munkres/
# https://software.clapper.org/munkres/