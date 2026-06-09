import random
import copy
from algorithm import config
from algorithm.encoding import initialization
from algorithm.fitness import calculateFitness, calculateMissmatch
from algorithm.mutation import self_adaptive_Pm, mutation1, mutation2
from algorithm.crossover import Crossover, EdgeRecombination, EdgeRecombination2D
from algorithm.local_search import localSearch_VLNS
from algorithm.distance import build_distance_matrix
from algorithm.io_utils import write_file


def extra_population(population_X):
    '''
    Renew the worst population
    '''
    new_population=[]
    sigma=config.Rowsize*config.Colsize*0.5
    for _ in range(len(population_X)//2):
        random_parent=random.sample(range(0, len(population_X)), config.Window_Size)
        windows=[[i,population_X[i]] for i in random_parent]
        windows.sort(key=lambda x:calculateFitness(x[1]))
        parent1=windows[0][1]
        parent2=windows[1][1]
        random_select=random.randint(0,100)
        if random_select<10:
            child1,child2=Crossover(parent1,parent2,3,3)
        elif random_select<40:
            child1,child2=EdgeRecombination(parent1,parent2)
        elif random_select<90:
            child1,child2=EdgeRecombination2D(parent1,parent2)
        else:
            child1,child2=parent1,parent2
        child1=mutation1(child1,1,sigma)
        child2=mutation1(child2,1,sigma)
        child1=mutation2(child1,1,sigma)
        child2=mutation2(child2,1,sigma)
        
        child1 = localSearch_VLNS(child1)
        child2 = localSearch_VLNS(child2)
        new_population.append(child1)
        new_population.append(child2)
    # Prioritize retention of offspring regardless of results
    new_population+=population_X
    return new_population[:len(population_X)]

def main():
    from visualization.visualize import format_solution
    config.OutOrIN=1
    dict_fitness_value={"4":1,"1":4}# Used to record the variable penalization of edge area
    print("Initializing population...")
    population=initialization()
    fitness_board=list(map(calculateFitness,population))
    best_fitness=min(fitness_board)
    previous_best_fitness=best_fitness
    mutation_rate=config.initial_mutation_rate
    sigma=config.initial_sigma
    Generation=0
    fitness_list=[]
    real_best_fitness=999
    print('Starting evolution...')
    while fitness_board[fitness_board.index(min(fitness_board))]>0 and Generation<config.maxGeneration:
        distance_matrix=build_distance_matrix(population)
        '''
        Tournament Selection
        '''
        new_population=[]
        for _ in range(int(config.population_size*config.children_Percent)//2):
            random_parent=random.sample(range(0, config.population_size), config.Window_Size)
            windows=[[i,population[i]] for i in random_parent]
            windows.sort(key=lambda x:calculateFitness(x[1]))
            parent1=windows[0][1]  # choose the best parent follow the tournament selection method
            parent2=windows[1][1]
            xover_row=random.randint(1,config.Rowsize-1)
            xover_col=random.randint(1,config.Colsize-1)
            random_select=random.randint(0,100) # random select the crossover method
            if random_select<10:
                child1,child2=Crossover(parent1,parent2,xover_row,xover_col)
            elif random_select<40:
                child1,child2=EdgeRecombination(parent1,parent2)
            elif random_select<90:
                child1,child2=EdgeRecombination2D(parent1,parent2)
            else:
                child1,child2=parent1,parent2 # 10% chance of not crossover.
            child1=mutation1(child1,mutation_rate,sigma)
            child2=mutation1(child2,mutation_rate,sigma)
            child1=mutation2(child1,mutation_rate,sigma)
            child2=mutation2(child2,mutation_rate,sigma)
            child1 = localSearch_VLNS(child1)
            child2 = localSearch_VLNS(child2)
            new_population.append(child1)
            new_population.append(child2)
            new_population.append(parent1)
            new_population.append(parent2)
        new_population.sort(key=lambda x:calculateFitness(x))
        for index,old_population in enumerate(windows): #Keep, better solution
            population[random_parent[index]]=copy.deepcopy(new_population[index])
        #-----------------------------------------------------------------------------------------------------------------
        # Elitism
        fitness_board=list(map(calculateFitness,copy.deepcopy(population)))
        best_fitness=min(fitness_board)
        best_individual=population[fitness_board.index(best_fitness)]
        mismatch_Board=list(map(calculateMissmatch,copy.deepcopy(population)))
        best_individual=localSearch_VLNS(best_individual)
        population[fitness_board.index(best_fitness)]=best_individual
        # Random select individuals to do local search
        random_local_search=random.sample(range(0, config.population_size), config.population_size//2)
        for R_index in random_local_search:
            R_individual=population[R_index]
            R_individual = localSearch_VLNS(R_individual)
            population[R_index]=R_individual
        fitness_board=list(map(calculateFitness,copy.deepcopy(population)))
        best_fitness=min(fitness_board)
        fitness_list.append(best_fitness)
        
        
        if previous_best_fitness != 0:    #self-adaptive mutayion
            improvement_rate = (previous_best_fitness - best_fitness) / previous_best_fitness
        else:
            improvement_rate = 0
        mutation_rate = self_adaptive_Pm(mutation_rate,config.final_mutation_rate,config.initial_mutation_rate,improvement_rate)#self-adaptive mutayion
        sigma = self_adaptive_Pm(sigma,config.final_sigma,config.initial_sigma,improvement_rate)
        previous_best_fitness=best_fitness
        Generation+=1
        mismatch_Board=list(map(calculateMissmatch,population))
        best_solution=population[mismatch_Board.index(min(mismatch_Board))]
        best_mismatch=calculateMissmatch(best_solution)
        print(f'Generation {Generation}: -------------Best Mismatch = {best_mismatch}')
        if Generation % 5 ==0:
            if best_fitness==fitness_list[-3]:
                # if fitness did not improve for 3 times, update the penalty value to stimulate population to generate transformations
                config.OutOrIN=dict_fitness_value[str(config.OutOrIN)]
                num_replace = int(0.97 * config.population_size)
            else:
                # every 5 generations, update the worst 50% of population
                num_replace = int(0.5 * config.population_size)
            population.sort(key=lambda x:calculateFitness(x))
            
            new_individuals = extra_population(copy.deepcopy(population[-num_replace:])) #update the worst population
            population[-num_replace:] = copy.deepcopy(new_individuals)

        if best_fitness<real_best_fitness or best_mismatch<real_best_mismatch: # if generation fitness is better than the best fitness, update the best fitness, and write the file
            real_best_fitness=best_fitness
            real_best_mismatch=best_mismatch
            write_file(best_solution,best_mismatch)
    format_solution(best_solution)
    best_mismatch=calculateMissmatch(best_solution)
    write_file(best_solution,best_mismatch)
