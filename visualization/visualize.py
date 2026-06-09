import os
import sys

# Make the package importable when this file is run directly as a script.
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from algorithm import config
from algorithm.encoding import Creat_code_dictionary
from utils.common import reshape


def format_solution(best_solution):
    '''
    format the best solution and print it
    '''
    print('Best Result: ')
    best_solution=reshape(best_solution,config.Rowsize,config.Colsize)
    best_solution=[[x[1] for x in row] for row in best_solution]
    for row in best_solution:
        print('|-----|'*len(row))
        up_number_list=[x[0] for x in row]
        left_right_list=[x[1:4:2][::-1] for x in row]
        down_number_list=[x[2] for x in row]
        for up_num in up_number_list:
            print(f"|  {up_num}  |",end='')
        print('')
        for left_right_num in left_right_list:
            print(f"|{left_right_num[0]}   {left_right_num[1]}|",end='')
        print('')
        for down_num in down_number_list:
            print(f"|  {down_num}  |",end='')
        print('')
    print('|-----|'*len(row))
    return best_solution


def run(input_file=None, output_file=None, population_size=None, maxGeneration=None):
    '''
    Set up the puzzle data / parameters, run the evolution and visualize the result.
    Any argument left as None falls back to the default data file or an interactive prompt.
    '''
    from algorithm.evolution import main

    PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

    # Specify the data file to solve here (change these paths as needed).
    config.input_file_path = input_file or os.path.join(PROJECT_ROOT, 'data', 'puzzle_input.txt')
    config.output_file_name = output_file or os.path.join(PROJECT_ROOT, 'data', 'output', 'output')

    # hyper parameter
    if population_size is None:
        population_size = int(input("Enter the population size [100,1000]: "))
    if maxGeneration is None:
        maxGeneration = int(input('Enter the maxGeneration [1,100]: '))
    config.population_size = population_size
    config.maxGeneration = maxGeneration
    # hyper parameter

    output_dir = os.path.dirname(config.output_file_name)
    if output_dir and not os.path.exists(output_dir):
        os.makedirs(output_dir)
    config.Code_dictionary = Creat_code_dictionary()
    main()


if __name__ == '__main__':
    run()