import random
import numpy as np
from scipy.optimize import linear_sum_assignment
from algorithm import config
from algorithm.fitness import calculateFitness


#VLNS
def select_non_adjacent_positions(k):
    positions = []
    attempts = 0
    max_attempts = 1000
    while len(positions) < k and attempts < max_attempts:
        row = random.randint(0, config.Rowsize - 1)
        col = random.randint(0, config.Colsize - 1)
        pos = (row, col)
        # Check for proximity to the selected position
        adjacent = False
        for p in positions:
            if abs(p[0] - row) + abs(p[1] - col) == 1:
                adjacent = True
                break
        if not adjacent and pos not in positions:
            positions.append(pos)
        attempts += 1
    return positions


def rotate_piece(piece, r):
    '''
    Rotate a piece by r degrees (0, 90, 180, or 270)
    '''
    id, edges, angle = piece
    new_angle = (angle + r) % 4
    new_edges = edges[-r:] + edges[:-r]
    return [id, new_edges, new_angle]

def compute_matching_edges(puzzle, idx):
    '''
    Calculate the number of mismatching sides for a given puzzle piece placement
    '''
    total_mismatch = 0
    row = idx // config.Colsize
    col = idx % config.Colsize
    piece = puzzle[idx]
    piece_edges = piece[1]
    # Check the neighbors in each direction
    # Up neighbor
    if row > 0:
        neighbor_idx = (row - 1) * config.Colsize + col
        neighbor_piece = puzzle[neighbor_idx]
        if neighbor_piece:
            neighbor_edge = neighbor_piece[1][2]
            if piece_edges[0] != neighbor_edge:
                total_mismatch += 1
    else:
        total_mismatch += config.OutOrIN  # Edge Penalty
    # right neighbor
    if col < config.Colsize - 1:
        neighbor_idx = row * config.Colsize + (col + 1)
        neighbor_piece = puzzle[neighbor_idx]
        if neighbor_piece:
            neighbor_edge = neighbor_piece[1][3]
            if piece_edges[1] != neighbor_edge:
                total_mismatch += 1
    else:
        total_mismatch += config.OutOrIN # Edge Penalty
    # down neighbor
    if row < config.Rowsize - 1:
        neighbor_idx = (row + 1) * config.Colsize + col
        neighbor_piece = puzzle[neighbor_idx]
        if neighbor_piece:
            neighbor_edge = neighbor_piece[1][0]
            if piece_edges[2] != neighbor_edge:
                total_mismatch += 1
    else:
        total_mismatch += config.OutOrIN # Edge Penalty
    # left neighbor
    if col > 0:
        neighbor_idx = row * config.Colsize + (col - 1)
        neighbor_piece = puzzle[neighbor_idx]
        if neighbor_piece:
            neighbor_edge = neighbor_piece[1][1]
            if piece_edges[3] != neighbor_edge:
                total_mismatch += 1
    else:
        total_mismatch += config.OutOrIN # Edge Penalty
    return total_mismatch

def VLNS(puzzle, k):
    '''
    Vary large neighborhood search algorithm
    '''
    # Step 1: Select k non-adjacent positions
    positions = select_non_adjacent_positions(k)
    positions_indices = [row * config.Colsize + col for (row, col) in positions]

    # Step 2: Remove the pieces at the selected positions
    removed_pieces = [puzzle[idx] for idx in positions_indices]
    
    # Step 3: Mark Remove Puzzle as Empty
    temp_puzzle = puzzle.copy()
    for idx in positions_indices:
        temp_puzzle[idx] = None  #Mark as empty

    n = len(removed_pieces)
    w_matrix = np.zeros((n, n))
    r_matrix = np.zeros((n, n), dtype=int)

    # Step 4: Compute the mismatching edges for each pair of removed pieces
    for i, piece in enumerate(removed_pieces):
        for j, hole_pos in enumerate(positions):
            min_w = float('inf')
            best_r = 0
            for r in range(4):
                rotated_piece = rotate_piece(piece, r)
                idx = hole_pos[0] * config.Colsize + hole_pos[1]
                temp_puzzle_copy = temp_puzzle.copy()
                temp_puzzle_copy[idx] = rotated_piece
                w = compute_matching_edges(temp_puzzle_copy, idx)
                if w < min_w:
                    min_w = w
                    best_r = r
            w_matrix[i][j] = min_w  # Record the lowest number of mismatches
            r_matrix[i][j] = best_r

    # Using the Hungarian algorithm to find the best match
    row_ind, col_ind = linear_sum_assignment(w_matrix)

    # Step 5: Place the pieces back into the puzzle
    for i, j in zip(row_ind, col_ind):
        piece = removed_pieces[i]
        rotate_times = r_matrix[i][j]
        rotated_piece = rotate_piece(piece, rotate_times)
        hole_pos = positions[j]
        idx = hole_pos[0] * config.Colsize + hole_pos[1]
        temp_puzzle[idx] = rotated_piece

    return temp_puzzle


def localSearch_VLNS(puzzle):
    '''
    Vary large neighborhood search
    '''
    best_puzzle = VLNS(puzzle, config.VLNS_Size)
    best_fitness = calculateFitness(best_puzzle)
    original_fitness = calculateFitness(puzzle)
    if best_fitness < original_fitness:
        return best_puzzle
    else:
        return puzzle
