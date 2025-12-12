import sys

def solve():
    input_str = sys.stdin.read()
    lines = input_str.split('\n')
    
    raw_shapes = {}
    queries = []
    
    current_shape_idx = -1
    current_shape_rows = []
    
    for line in lines:
        line = line.strip()
        if not line:
            continue
            
        if ':' in line and 'x' in line.split(':')[0]: # this line is a query
            # save previous shape being parsed
            if current_shape_idx != -1 and current_shape_rows:
                raw_shapes[current_shape_idx] = parse_shape(current_shape_rows)
                current_shape_idx = -1
                current_shape_rows = []
            
            parts = line.split(':')
            dims = parts[0].strip().split('x')
            W, H = int(dims[0]), int(dims[1])
            counts = list(map(int, parts[1].strip().split()))
            queries.append({'W': W, 'H': H, 'counts': counts})
                

        elif ':' in line: # this line introduces a new shape
            # save previous shape
            if current_shape_idx != -1 and current_shape_rows:
                raw_shapes[current_shape_idx] = parse_shape(current_shape_rows)
            
            # start new shape

            idx_str = line.split(':')[0]
            current_shape_idx = int(idx_str)
            current_shape_rows = []
        
        # otherwise its a row of the current shape
        else:
            if current_shape_idx != -1:
                current_shape_rows.append(line)

    # save the very last shape if file ended while parsing one
    if current_shape_idx != -1 and current_shape_rows:
        raw_shapes[current_shape_idx] = parse_shape(current_shape_rows)

    # pre-compute 8 orientations (normalized coords) for each shape
    shape_orientations = {}
    for sid, coords in raw_shapes.items():
        shape_orientations[sid] = generate_orientations(coords)

    solved_count = 0
    
    for q in queries:
        W, H = q['W'], q['H']
        counts = q['counts']
        
        presents = [] # present list for each query
        for s_idx, count in enumerate(counts):
            if count > 0:
                if s_idx in raw_shapes:
                    area = len(raw_shapes[s_idx])
                    for _ in range(count):
                        presents.append((area, s_idx))
        
        # sort by area descending heuristic
        presents.sort(key=lambda x: x[0], reverse=True)
        
        present_ids = [p[1] for p in presents]
        total_presents = len(presents)
        
        # suffix sum for pruning check
        suffix_area = [0] * (total_presents + 1)
        for i in range(total_presents - 1, -1, -1):
            suffix_area[i] = suffix_area[i+1] + presents[i][0]

        total_needed = suffix_area[0]
        if total_needed > W * H:
            continue 

        # generate integer bitmasks for this specific W
        shape_meta = {}
        unique_ids = set(present_ids)
        valid_shapes = True
        
        for sid in unique_ids:
            meta_list = []
            for shape_coords in shape_orientations[sid]:
                h_s = max(r for r, c in shape_coords) + 1
                w_s = max(c for r, c in shape_coords) + 1
                
                if h_s > H or w_s > W:
                    continue
                
                mask = 0
                for r, c in shape_coords:
                    mask |= (1 << (r * W + c))
                
                meta_list.append((mask, h_s, w_s))
            
            # sort for deterministic behavior
            meta_list.sort(key=lambda x: x[0], reverse=True)
            shape_meta[sid] = meta_list
            
            if not meta_list:
                valid_shapes = False
                break
        
        if not valid_shapes:
            continue
        def dfs(index, board, occupied_count, last_pos):
            if index == total_presents:
                return True
            
            # pruning
            if (W * H) - occupied_count < suffix_area[index]:
                return False
            
            pid = present_ids[index]

            start_pos = last_pos
            
            for base_mask, h_s, w_s in shape_meta[pid]:
                limit_r = H - h_s + 1
                limit_c = W - w_s + 1
                
                start_r = start_pos // W
                
                for r in range(start_r, limit_r):
                    c_start = 0
                    if r == start_r:
                        c_start = start_pos % W
                    
                    for c in range(c_start, limit_c):
                        shift = r * W + c
                        
                        move_mask = base_mask << shift
                        if (board & move_mask) == 0:
                            if dfs(index + 1, board | move_mask, occupied_count + presents[index][0], shift):
                                return True
            return False

        if dfs(0, 0, 0, 0):
            solved_count += 1

    print(solved_count)

def parse_shape(rows):
    coords = set()
    for r, line in enumerate(rows):
        for c, char in enumerate(line):
            if char == '#':
                coords.add((r, c))
    return normalize_shape(coords)

def normalize_shape(coords):
    if not coords: return frozenset()
    min_r = min(r for r, c in coords)
    min_c = min(c for r, c in coords)
    return frozenset((r - min_r, c - min_c) for r, c in coords)

def generate_orientations(base_coords):
    variations = set()
    current = list(base_coords)
    for _ in range(2): 
        for _ in range(4): 
            variations.add(normalize_shape(current))
            current = [(c, -r) for r, c in current]
        current = [(r, -c) for r, c in current]
    return list(variations)

if __name__ == "__main__":
    solve()