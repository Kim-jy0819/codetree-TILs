def find_santa_direction(santa_idx):
    global coord, N, fail, knockdown
    santa_r, santa_c = coord[santa_idx]
    rudolph_r, rudolph_c = coord[0]
    dr = [-1, 0, 1, 0]
    dc = [0, 1, 0, -1]
    direction = []
    if fail[santa_idx]:
        return None
    elif knockdown[santa_idx]:
        return None
    for i in range(4):
        next_r, next_c = santa_r + dr[i], santa_c + dc[i]
        if {next_r, next_c} < set(range(1, N + 1)) and [next_r, next_c] not in coord[1:]:
            distance = (next_r - rudolph_r) ** 2 + (next_c - rudolph_c) ** 2
            direction.append([distance, i])
    if direction:
        direction_idx = sorted(direction, key=lambda x: (x[0], x[1]))[0][1]
        return [dr[direction_idx], dc[direction_idx]]
    return None


def find_rudolph_direction():
    global coord, N, P

    rudolph_r, rudolph_c = coord[0]
    santa_distance = []
    for santa_idx in range(1, P+1):
        if fail[santa_idx] == 1:
            continue
        santa_r, santa_c = coord[santa_idx]
        distance = (rudolph_r - santa_r) ** 2 + (rudolph_c - santa_c) ** 2
        santa_distance.append([distance, santa_r, santa_c, santa_idx])
    if len(santa_distance) == 0:
        return None
    santa_distance = sorted(santa_distance, key=lambda x: (x[0], -x[1], -x[2]))
    _, santa_r, santa_c, santa_idx = santa_distance[0]
    dr = [-1, -1, 0, 1, 1, 1, 0, -1]
    dc = [0, 1, 1, 1, 0, -1, -1, -1]
    direction = []

    for i in range(8):
        next_r, next_c = rudolph_r + dr[i], rudolph_c + dc[i]
        if {next_r, next_c} < set(range(1, N + 1)):
            distance = (next_r - santa_r) ** 2 + (next_c - santa_c) ** 2
            direction.append([distance, i])
    if direction:
        direction_idx = sorted(direction, key=lambda x: (x[0], x[1]))[0][1]
        return [dr[direction_idx], dc[direction_idx], santa_idx]
    return None


def collision(santa_idx, rudolph_collision, direction):
    global scores, C, D, coord, knockdown, turn_idx, knockdown_turn_list
    dr, dc = direction
    if rudolph_collision:  # 루돌프가 박치기했을 때
        score = C
    else:
        score = D
        dr, dc = -dr, -dc

    scores[santa_idx] += score
    santa_r, santa_c = coord[santa_idx]
    knockdown_turn_list[turn_idx].append(santa_idx)
    next_r, next_c = santa_r + score * dr, santa_c + score * dc
    knockdown[santa_idx] = 1
    if not ({next_r, next_c} < set(range(1, N + 1))):
        fail[santa_idx] = 1
    elif [next_r, next_c] in coord:
        interaction_list[coord.index([next_r, next_c])] = 1
    coord[santa_idx] = [next_r, next_c]


def interaction(direction):
    global interaction_list, fail, coord
    while sum(interaction_list) > 0:
        interactive_santa_idx = interaction_list.index(1)
        interaction_list[interactive_santa_idx] = 0
        r, c = coord[interactive_santa_idx]
        dr, dc = direction
        next_r, next_c = r - dr, c - dc
        if not ({next_r, next_c} < set(range(1, N + 1))):
            fail[interactive_santa_idx] = 1
        elif [next_r, next_c] in coord:
            interaction_list[coord.index([next_r, next_c])] = 1
        coord[interactive_santa_idx] = [next_r, next_c]




N, M, P, C, D = map(int, input().split())
coord = [[] for _ in range(P + 1)]
coord[0] = list(map(int, input().split()))
knockdown = [0 for _ in range(P + 1)]
dropout = [0 for _ in range(P + 1)]
scores = [0 for _ in range(P + 1)]
fail = [0 for _ in range(P + 1)]
interaction_list = [0 for _ in range(P + 1)]
knockdown_turn_list = [[] for _ in range(M)]
for i in range(P):
    p, r, c = map(int, input().split())
    coord[p] = [r, c]

for turn_idx in range(M):
    if turn_idx > 0:
        knockdown = [0 for _ in range(P + 1)]
        for knocked_santa_idx in knockdown_turn_list[turn_idx-1]:
            knockdown[knocked_santa_idx] = 1
    rudolph_direction = find_rudolph_direction()
    if rudolph_direction is None:
        break
    rudolph_dr, rudolph_dc, nearest_santa_idx = rudolph_direction
    cur_rudolph_r, cur_rudolph_c = coord[0]
    coord[0] = [cur_rudolph_r+rudolph_dr, cur_rudolph_c+rudolph_dc]
    if coord[0] in coord[1:]:
        collision(nearest_santa_idx, True, [rudolph_dr, rudolph_dc])
        interaction([rudolph_dr, rudolph_dc])
    for j in range(1, P+1):
        santa_direction = find_santa_direction(j)
        if santa_direction is not None:
            santa_dr, santa_dc = santa_direction
            cur_santa_r, cur_santa_c = coord[j]
            coord[j] = [cur_santa_r+santa_dr, cur_santa_c+santa_dc]
            if coord[j] == coord[0]:
                collision(j, False, santa_direction) # 충돌
                interaction(santa_direction) # 상호작용
    if sum(fail) < P:
        for j in range(1, P+1): # interaction 끝난 이후 살아남은 산타 점수 +1
            if not fail[j]:
                scores[j] += 1
    # print(f'{turn_idx+1} scores: {scores}')
    # print(f'{turn_idx+1} cooord: {coord}')
    # print(f'{turn_idx+1} fail: {fail}')
    # print(f'{turn_idx+1} knockdown: {knockdown}')
print(' '.join(map(str,scores[1:])))