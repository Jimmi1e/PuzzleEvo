import random
from algorithm import config
from utils.common import reshape, flatten


def self_adaptive_Pm(current_value,min_value,max_value,improvement_rate,threshold_high=0.01,threshold_low=0.001,decay_factor=0.9,growth_factor=1.1):
    '''
    self-daptive probability of mutation
    '''
    if improvement_rate>threshold_high: # if improvement_rate is high, decrease the mutation rate
        new_value=max(current_value*decay_factor, min_value)
    elif improvement_rate<threshold_low:   #if improvement_rate is low, increase the mutation rate
        new_value=min(current_value*growth_factor, max_value)
    else:
        new_value = current_value
    return new_value

def mutation1(puzzle, mutation_rate, sigma):
    '''
    Exchange by block
    Size 1x1,1x2,2x1,2x2. These sizes of blocks will be randomly selected.
    '''
    if random.random()<mutation_rate:
        swap_numb=int(sigma)
        puzzle_2d=reshape(puzzle, config.Rowsize, config.Colsize)
        used_positions=set()
        for _ in range(swap_numb):
            block_sizes=[(1,1), (1,2), (2,1), (2,2)]
            block_size=random.choice(block_sizes)
            rows_block, cols_block = block_size
            # Trying to find blocks to prevent overlap
            for _ in range(100):  # Number of attempts
                # The first piece
                row1=random.randint(0,config.Rowsize-rows_block)
                col1=random.randint(0,config.Colsize-cols_block)
                # Check if it has been used by a previous block
                positions1=[(row1+r,col1+c) for r in range(rows_block) for c in range(cols_block)]
                if any(pos in used_positions for pos in positions1):
                    continue
                #The second piece
                row2=random.randint(0,config.Rowsize-rows_block)
                col2=random.randint(0,config.Colsize-cols_block)
                positions2=[(row2+r,col2+c) for r in range(rows_block) for c in range(cols_block)]
                if any(pos in used_positions for pos in positions2):
                    continue
                # Overlap or not, exchange if not
                if set(positions1).isdisjoint(set(positions2)):
                    for r in range(rows_block):
                        for c in range(cols_block):
                            temp_piece=puzzle_2d[row1+r][col1+c]
                            puzzle_2d[row1+r][col1+c]=puzzle_2d[row2+r][col2+c]
                            puzzle_2d[row2+r][col2+c]=temp_piece
                    # Marks the block as being used
                    used_positions.update(positions1)
                    used_positions.update(positions2)
                    break
        puzzle=flatten(puzzle_2d)
    return puzzle

def mutation2(puzzle, mutation_rate, sigma):
    '''
    Rotate the puzzle block and the pieces rotate with it.
    '''
    if random.random()<mutation_rate:
        puzzle_2d=reshape(puzzle, config.Rowsize, config.Colsize)
        used_positions=set()
        num_blocks=int(sigma)
        for _ in range(num_blocks):
            block_size=random.randint(1, 3) #Block sizes are 1x1, 2x2, 3x3
            rows_block=cols_block=block_size
            # Trying to find blocks to prevent overlap
            for _ in range(100):
                row=random.randint(0,config.Rowsize-rows_block)
                col=random.randint(0,config.Colsize-cols_block)
                positions=[(row+r,col+c) for r in range(rows_block) for c in range(cols_block)]
                if any(pos in used_positions for pos in positions):
                    continue
                rotate_times = random.randint(1,3)
                block=[puzzle_2d[row+r][col+c] for r in range(rows_block) for c in range(cols_block)]
                block_2d=[block[i*cols_block:(i+1)*cols_block] for i in range(rows_block)]
                for _ in range(rotate_times):
                    block_2d=[list(x) for x in zip(*block_2d[::-1])]
                rotated_block=[item for sublist in block_2d for item in sublist]
                idx=0
                for r in range(rows_block):
                    for c in range(cols_block):
                        piece=rotated_block[idx]
                        piece[2]=(piece[2]+rotate_times)%4
                        piece[1]=piece[1][-rotate_times:]+piece[1][:-rotate_times]
                        puzzle_2d[row+r][col+c] = piece
                        idx +=1
                # Marks the block as being used
                used_positions.update(positions)
                break
        puzzle=flatten(puzzle_2d)
    return puzzle
