Rowsize = 8
Colsize = 8
children_Percent = 0.4
VLNS_Size = 21  # contorl the number of non-adjacent puzzle pieces removed and reinserted during each VLNS iteration.
Window_Size = 5
population_size = 100
maxGeneration = 100
initial_mutation_rate = 0.95
final_mutation_rate = 0.0001
initial_sigma = Rowsize * Colsize * 0.4
final_sigma = 1.0
input_file_path = r'data/puzzle_input.txt'
output_file_name = r'data/output/output'

# runtime state (mutated while the algorithm runs)
OutOrIN = 1
Code_dictionary = {}
