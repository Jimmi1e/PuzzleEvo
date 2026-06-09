import random
from algorithm import config


def Creat_code_dictionary():
    '''
    Read raw puzzle file to creat Genotype dictionary
    '''
    input_puzzle=[]
    with open(config.input_file_path, 'r') as f:
        for line in f:
            input_puzzle.append(line.strip().split(' '))
    if len(input_puzzle)==config.Rowsize+1:
        input_puzzle=input_puzzle[1:]
    Code_dictionary={}
    code=1
    for i in range(1,config.Rowsize+1):
        for j in range(1,config.Colsize+1):
            Code_dictionary[str(code)]=input_puzzle[i-1][j-1]
            code+=1
    return Code_dictionary

def decode_dictionary(piece):
    '''
    Decode Genotype to puzzle
    '''
    return config.Code_dictionary[piece]

def initialization():
    '''
    Initialize population
    Our genotype of each solution like 
    [[piece_id_1, piece_1, piece_1 angle],[piece_id_2, piece_2, piece_2 angle],...]
    A list of 1*64
    '''
    population=[]
    for i in range(config.population_size):
        Code_puzzle=random.sample(range(1, config.Rowsize*config.Colsize+1), config.Rowsize*config.Colsize)
        puzzle=[[x,decode_dictionary(str(x)),0]for x in Code_puzzle]
        population.append(puzzle)
    return population

def encode_dictionary(puzzle):
    '''
    encode the puzzle into a dictionary
    '''
    codeDictionary={}
    for i in range(1,config.Rowsize*config.Colsize+1):
        codeDictionary[str(puzzle[i-1][0])]=[puzzle[i-1][1],puzzle[i-1][2]]
    return codeDictionary
