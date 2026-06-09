import os
import sys

# Make the package importable no matter which directory you launch from.
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from visualization.visualize import run

if __name__ == '__main__':
    # Run with the default data file and interactive prompts.
    # To use another puzzle / settings, e.g.:
    # run(input_file='data/puzzle_input.txt', population_size=200, maxGeneration=50)
    run()
