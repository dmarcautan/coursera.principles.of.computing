"""
Merge function for 2048 game.
"""

def merge(line):
    """
    Function that merges a single row or column in 2048.
    """
    
    merged = line[:]
    iterations = len(merged) - 1
    iteration = 0
    
    while iteration < iterations:
        next_index = iteration + 1
        while next_index < len(merged) - 1 and merged[next_index] == 0:
            next_index += 1
            
        if merged[iteration] == 0:
            merged[iteration] = merged[next_index]
            merged[next_index] = 0
            if next_index == iterations:
                break
        elif merged[iteration] == merged[next_index]:
            merged[iteration] = 2 * merged[next_index]
            merged[next_index] = 0
            iteration += 1
        else:
            iteration += 1
            
        
        
    return merged
