'''
General purpose helpers. To be expanded later.
'''


def reshape(matrix,row,col):
    '''
    Reshape our solution to a 2D form (8*8)
    '''
    total_elements = row*col
    if total_elements != len(matrix):
        raise ValueError("Size Error")
    result=[]
    result=[matrix[i:i+col] for i in range(0, len(matrix), col)]
    return result

def flatten(matrix):
    '''
    Reshape our solution to a 1D form (1*64)
    '''
    flattened_arr = [item for submatrix in matrix for item in submatrix]
    return flattened_arr
