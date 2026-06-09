import numpy as np
from algorithm import config


def calculatRowMisMatch(puzzleRow1,puzzleRow2,r1,r2):
    '''
    Calculate the mismatch between two rows,
    used for calculate the fitness
    '''
    numberOfMisMatch=0
    for n,piece in enumerate(puzzleRow1):
        if piece[2]!=puzzleRow2[n][0]:
            if r1==0 or r2==config.Rowsize-1: 
                numberOfMisMatch+=config.OutOrIN # Variable penalization of edge area
            elif n==0 or n==config.Rowsize-1:
                numberOfMisMatch+=config.OutOrIN # Variable penalization of edge area
            else:
                numberOfMisMatch+=2
    return numberOfMisMatch

def calculatColMisMatch(puzzleCol1,puzzleCol2,c1,c2):
    '''
    Calculate the mismatch between two columns,
    used for calculate the fitness
    '''
    numberOfMisMatch=0
    for n,piece in enumerate(puzzleCol1):
        if piece[1]!=puzzleCol2[n][3]:
            if c1==0 or c2==config.Colsize-1: 
                numberOfMisMatch+=config.OutOrIN # Variable penalization of edge area
            elif n==0 or n==config.Colsize-1: 
                numberOfMisMatch+=config.OutOrIN # Variable penalization of edge area
            else:
                numberOfMisMatch+=2
    return numberOfMisMatch

def calculatRowMisMatch2(puzzleRow1,puzzleRow2):
    '''
    Calculate the mismatch between two rows,
    used for calculate the mismatch values
    '''
    numberOfMisMatch=0
    for n,piece in enumerate(puzzleRow1):
        if piece[2]!=puzzleRow2[n][0]:
            numberOfMisMatch+=1
    return numberOfMisMatch

def calculatColMisMatch2(puzzleCol1,puzzleCol2):
    '''
    Calculate the mismatch between two columns,
    used for calculate the mismatch values
    '''
    numberOfMisMatch=0
    for n,piece in enumerate(puzzleCol1):
        if piece[1]!=puzzleCol2[n][3]:
            numberOfMisMatch+=1
    return numberOfMisMatch

def calculateFitness(puzzle):
    '''
    Calculate the fitness of a puzzle
    '''
    puzzle=[x[1] for x in puzzle]
    puzzle=np.array(puzzle).reshape(config.Rowsize, config.Colsize).tolist()
    fitness=0
    for n in range(config.Rowsize-1):
        fitness+=calculatRowMisMatch(puzzle[n],puzzle[n+1],n,n+1)
    for n in range(config.Colsize-1):
        col1,col2=[],[]
        for i in range(config.Rowsize):
            col1.append(puzzle[i][n])
            col2.append(puzzle[i][n+1])
        fitness+=calculatColMisMatch(col1,col2,n,n+1)
    return fitness

def calculateMissmatch(puzzle):
    '''
    Calculate the missmatch of a puzzle
    '''
    puzzle=[x[1] for x in puzzle]
    puzzle=np.array(puzzle).reshape(config.Rowsize, config.Colsize).tolist()
    Missmatch=0
    for n in range(config.Rowsize-1):
        Missmatch+=calculatRowMisMatch2(puzzle[n],puzzle[n+1])
    for n in range(config.Colsize-1):
        col1,col2=[],[]
        for i in range(config.Rowsize):
            col1.append(puzzle[i][n])
            col2.append(puzzle[i][n+1])
        Missmatch+=calculatColMisMatch2(col1,col2)
    return Missmatch
