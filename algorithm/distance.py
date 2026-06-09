import numpy as np
from algorithm import config


def build_distance_matrix(population):
    '''
    build the distance matrix to record the distance between each individual
    '''
    dis_value=np.zeros((config.population_size, config.population_size)).tolist()
    for i in range(len(population)):
        for j in range(i,len(population)):
            if i ==j:
                dis_value[i][j]=[999,j]
            else:
                dis_value[i][j]=[cal_distance(population[i],population[j]),j]
    for i in range(len(population)):
        for j in range(i):
            dis_value[i][j] = dis_value[j][i]
    return dis_value

def cal_distance(puzzle1,puzzle2):
    '''
    calculate the distance between two puzzles
    '''
    for idv_tile in range(config.Colsize*config.Rowsize):
        angle=abs((puzzle1[idv_tile][2]-puzzle2[idv_tile][2])%3+(puzzle1[idv_tile][2]-puzzle2[idv_tile][2])//3) #calculate the angle difference
        id_diff=puzzle1[idv_tile][0]-puzzle2[idv_tile][0]
        if id_diff !=0:
            distance=8     #set the weight
        else:
            distance=angle
    return distance
