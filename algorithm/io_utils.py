from algorithm import config
from utils.common import reshape


def write_file(best_solution,best_mismatch):
    '''
    write the best solution to the file
    '''
    best_solution=reshape(best_solution,config.Rowsize,config.Colsize)
    best_solution=[[x[1] for x in row] for row in best_solution]
    file_name = "{}.txt".format(config.output_file_name)
    # file_name = "{}_{}.txt".format(output_file_name,best_mismatch)
    with open(file_name, 'w') as f:
        f.write(f"The final result with mismatch count {best_mismatch}:\n")
        for row in best_solution:
            f.write(' '.join(row) + '\n')
