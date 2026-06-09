import random
import numpy as np
import copy
from algorithm import config
from algorithm.encoding import encode_dictionary
from utils.common import reshape, flatten


def Crossover(puzzle1,puzzle2,window_row,window_col):
    '''
    Order Crossover, exange by region
    '''

    parent1=reshape(puzzle1,config.Rowsize,config.Colsize)
    parent2=reshape(puzzle2,config.Rowsize,config.Colsize)
    # Randomly select the location of the extraction block
    rand_row_index=random.randint(0,config.Rowsize-window_row)
    rand_col_index=random.randint(0,config.Colsize-window_col)
    part1,part2=[],[] #used to record the pieces in the parent
    record_p1,record_p2=[],[] #used to record the pieces in the window, to avoid duplication
    for row in parent1[rand_row_index:rand_row_index+window_row]:
        part1+=row[rand_col_index:rand_col_index+window_col]
        record_p1+=[x[0] for x in row[rand_col_index:rand_col_index+window_col]]
    for row in parent2[rand_row_index:rand_row_index+window_row]:
        part2+=row[rand_col_index:rand_col_index+window_col]
        record_p2+=[x[0] for x in row[rand_col_index:rand_col_index+window_col]]
    # Initialize a blank puzzle to create the child
    c1=np.zeros((config.Rowsize,config.Colsize),int).tolist()
    c2=np.zeros((config.Rowsize,config.Colsize),int).tolist()
    star=0
    # Putting the blocks extracted from the parent directly into the children
    for row_i in range(rand_row_index,rand_row_index+window_row):
        c1[row_i][rand_col_index:rand_col_index+window_col]=part1[star:star+window_col]
        c2[row_i][rand_col_index:rand_col_index+window_col]=part2[star:star+window_col]
        star+=window_col
    c1=flatten(c1)
    c2=flatten(c2)
    c1_index,c2_index=0,0
    # Put the rest of the non-duplicated pieces from the parent into the child in order.
    for i in range(config.Rowsize*config.Colsize):
        if  c1_index<config.Rowsize*config.Colsize and c1[c1_index]==0:
            if puzzle1[i][0] not in record_p1: # If it's not being used, put it in to the child
                c1[c1_index]=puzzle1[i]
                c1_index+=1
        else:
            c1_index+=window_col
        if c2_index<config.Rowsize*config.Colsize and c2[c2_index]==0 :
            if puzzle2[i][0] not in record_p2: # If it's not being used, put it in to the child
                c2[c2_index]=puzzle2[i]
                c2_index+=1
        else:
            c2_index+=window_col
    return c1,c2

def find_puzzle2_edge(puzzle_list,element):
    '''
    find the edge from the puzzle 2 in 1d edge table
    '''
    index2=puzzle_list.index(element)
    if index2 == config.Rowsize*config.Colsize-1:
        return 0,index2-1
    else:
        return index2+1,index2-1

def buildEdgeTable(puzzle1,puzzle2):
    '''
    Build the edge table for 21 Dimension, each piece has 2 edges
    '''
    
    puzzle1_list=[x[0] for x in puzzle1]
    puzzle2_list=[x[0] for x in puzzle2]

    edge_table={}
    for i in range(config.Rowsize*config.Colsize):
        edge_table[str(puzzle1_list[i])]=[]
        if i == config.Rowsize*config.Colsize-1:
            edge_table[str(puzzle1_list[i])].append(puzzle1_list[0])
            edge_table[str(puzzle1_list[i])].append(puzzle1_list[i-1])
        else:
            edge_table[str(puzzle1_list[i])].append(puzzle1_list[i-1])
            edge_table[str(puzzle1_list[i])].append(puzzle1_list[i+1])
        puzzle2_edges_index1,puzzle2_edges_index2=find_puzzle2_edge(puzzle2_list,puzzle1_list[i])
        edge_table[str(puzzle1_list[i])].append(puzzle2_list[puzzle2_edges_index1])
        edge_table[str(puzzle1_list[i])].append(puzzle2_list[puzzle2_edges_index2])
    return edge_table,puzzle1_list,puzzle2_list

def find_puzzle2_2dedge(puzzle_list,element):
    '''
    find the edge from the puzzle 2 in 2d edge table
    '''
    index2=puzzle_list.index(element)
    puzzle2_row=index2//config.Rowsize
    puzzle2_col=index2%config.Rowsize
    puzzle2_edge_result=[]
    # find the up and down edge
    if puzzle2_col == config.Rowsize-1:
        puzzle2_edge_result.append([puzzle2_row,0])
        puzzle2_edge_result.append([puzzle2_row,puzzle2_col-1])
    else:
        puzzle2_edge_result.append([puzzle2_row,puzzle2_col+1])
        puzzle2_edge_result.append([puzzle2_row,puzzle2_col-1])
    # find the left and right edge
    if puzzle2_row == config.Colsize-1:
        puzzle2_edge_result.append([0,puzzle2_col])
        puzzle2_edge_result.append([puzzle2_row-1,puzzle2_col])
    else:
        puzzle2_edge_result.append([puzzle2_row+1,puzzle2_col])
        puzzle2_edge_result.append([puzzle2_row-1,puzzle2_col])
    return puzzle2_edge_result

def build2DEdgeTable(puzzle1,puzzle2):
    '''
    Build the edge table for 2 Dimension, each piece has 4 edges
    '''
    puzzle1_2D=reshape(puzzle1,config.Rowsize,config.Colsize)
    puzzle2_2D=reshape(puzzle2,config.Rowsize,config.Colsize)
    puzzle1_list=[x[0] for x in puzzle1]
    puzzle2_list=[x[0] for x in puzzle2]
    edge2d_table={}
    for i in range(config.Rowsize*config.Colsize):
        edge2d_table[str(puzzle1_list[i])]=[]
        puzzle1_row=i//config.Rowsize
        puzzle1_col=i%config.Rowsize
        # find the up and down edge
        if puzzle1_col == config.Rowsize-1:
            edge2d_table[str(puzzle1_list[i])].append(puzzle1_2D[puzzle1_row][0][0])
            edge2d_table[str(puzzle1_list[i])].append(puzzle1_2D[puzzle1_row][puzzle1_col-1][0])
        else:
            edge2d_table[str(puzzle1_list[i])].append(puzzle1_2D[puzzle1_row][puzzle1_col+1][0])
            edge2d_table[str(puzzle1_list[i])].append(puzzle1_2D[puzzle1_row][puzzle1_col-1][0])
        # find the left and right edge
        if puzzle1_row == config.Colsize-1:
            edge2d_table[str(puzzle1_list[i])].append(puzzle1_2D[0][puzzle1_col][0])
            edge2d_table[str(puzzle1_list[i])].append(puzzle1_2D[puzzle1_row-1][puzzle1_col][0])
        else:
            edge2d_table[str(puzzle1_list[i])].append(puzzle1_2D[puzzle1_row+1][puzzle1_col][0])
            edge2d_table[str(puzzle1_list[i])].append(puzzle1_2D[puzzle1_row-1][puzzle1_col][0])
            
        puzzle2_edge_result=find_puzzle2_2dedge(puzzle2_list,puzzle1_list[i])
        for x,y in puzzle2_edge_result:
            edge2d_table[str(puzzle1_list[i])].append(puzzle2_2D[x][y][0])
    return edge2d_table,puzzle1_list,puzzle2_list

def update_edge_table(edge_table,element):
    '''
    Remove the selected element from the Edge table
    '''
    for key in edge_table:
        if element in edge_table[key]:
            edge_table[key]=[x for x in edge_table[key] if x != element]
    return edge_table

def find_min_or_random(lst):
    '''
    Find the shortest or random select from the Edge table
    '''
    min_value = min(lst)
    min_values = [x for x in lst if x == min_value]
    if len(min_values) == 1:
        return min_value
    else:
        return random.choice(min_values)

def select_perfect_element(edge_table,element):
    '''
    Select the perfect element from the edge table
    '''
    edges_list=edge_table[str(element)]
    edge_table={key: value for key, value in edge_table.items() if key!=str(element)} # Remove the selected element from the edge table
    if not edges_list: # If the edge list is empty, random select an element from the edge table
        
        element=random.choice(list(edge_table.items()))[0]
        perfect_element=int(element)
        edge_table=update_edge_table(edge_table,perfect_element) # Remove the selected element from the edge table
        return perfect_element,edge_table
    edge_length_list=[len(edge_table[str(x)]) for x in edges_list]
    temp_list=[]
    for edge in edges_list:
        if edge not in temp_list:
            temp_list.append(edge)
        else:
            perfect_element=edge # find the common edge
            edge_table=update_edge_table(edge_table,perfect_element) # Remove the selected element from the edge table
            return perfect_element,edge_table
    select_index=edge_length_list.index(find_min_or_random(edge_length_list)) # if cannot find the common edge, select the shortest edge or reandom select
    perfect_element=edges_list[select_index]
    edge_table=update_edge_table(edge_table,perfect_element) # Remove the selected element from the edge table
    return perfect_element,edge_table

def EdgeRecombination(puzzle1,puzzle2):
    '''
    Do edge recombination in one dimension
    '''
    puzzle1_code=encode_dictionary(puzzle1)
    puzzle2_code=encode_dictionary(puzzle2)
    edge_table,puzzle1_list,puzzle2_list=buildEdgeTable(puzzle1,puzzle2)
    random_num=random.randint(0,config.Rowsize*config.Colsize-1)
    select_element1=puzzle1_list[random_num]
    select_element2=puzzle2_list[random_num]

    edge_table1=copy.deepcopy(edge_table)
    edge_table2=copy.deepcopy(edge_table)
    edge_table1=update_edge_table(edge_table1,select_element1)
    edge_table2=update_edge_table(edge_table2,select_element2)
    c1,c2=[],[]
    for i in range(1,config.Rowsize*config.Colsize):
        c1.append(select_element1)
        c2.append(select_element2)
        select_element1,edge_table1=select_perfect_element(edge_table1,select_element1)
        select_element2,edge_table2=select_perfect_element(edge_table2,select_element2)
    c1.append(select_element1)
    c2.append(select_element2)
    child1=[[x,puzzle1_code[str(x)][0],puzzle1_code[str(x)][1]]for x in c1]
    child2=[[x,puzzle2_code[str(x)][0],puzzle2_code[str(x)][1]]for x in c2]
    return child1,child2

def EdgeRecombination2D(puzzle1,puzzle2):
    '''
    Do edge recombination in two dimension
    '''
    puzzle1_code=encode_dictionary(puzzle1)
    puzzle2_code=encode_dictionary(puzzle2)
    # Step1: creat the edge table
    edge2d_table,puzzle1_list,puzzle2_list=build2DEdgeTable(puzzle1,puzzle2)
    
    random_num=random.randint(0,config.Rowsize*config.Colsize-1)
    # Step2: random select the first element
    select_element1=puzzle1_list[random_num]
    select_element2=puzzle2_list[random_num]

    edge_table1=copy.deepcopy(edge2d_table)
    edge_table2=copy.deepcopy(edge2d_table)
    # remove the selected element from the edge table
    edge_table1=update_edge_table(edge_table1,select_element1)
    edge_table2=update_edge_table(edge_table2,select_element2)
    # initialize the child
    c1,c2=[[0 for _ in range(config.Colsize)] for _ in range(config.Rowsize)],[[0 for _ in range(config.Colsize)] for _ in range(config.Rowsize)]
    for i in range(config.Rowsize):
        for j in range(config.Colsize):
            # follow the S sequence to select the element
            if i%2==0:
                c1[i][j]=select_element1
                c2[i][j]=select_element2
            else:
                c1[i][-j-1]=select_element1
                c2[i][-j-1]=select_element2
            if i==config.Rowsize-1 and j==config.Colsize-1:
                break
            # Step3: select the next element
            select_element1,edge_table1=select_perfect_element(edge_table1,select_element1)
            select_element2,edge_table2=select_perfect_element(edge_table2,select_element2)
    c1=flatten(c1)
    c2=flatten(c2)
    child1=[[x,puzzle1_code[str(x)][0],puzzle1_code[str(x)][1]]for x in c1]
    child2=[[x,puzzle2_code[str(x)][0],puzzle2_code[str(x)][1]]for x in c2]
    return child1,child2
