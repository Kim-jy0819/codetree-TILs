from collections import deque

N, Q = map(int, input().split())

temp = list(map(int, input().split()))
parents = [0] + temp[1:N+1]
power_list = [0] + temp[N+1:2*N+1]
alarm_settings = [1 for _ in range(N+1)]


for _ in range(Q-1):
    command_line = input().split()
    if command_line[0] == '200':
        node = int(command_line[1])
        if alarm_settings[node]:
            alarm_settings[node] = 0
        else:
            alarm_settings[node] = 1
    elif command_line[0] == '300':
        node, power = map(int, command_line[1:])
        power_list[node] = power
    elif command_line[0] == '400':
        node1, node2 = map(int, command_line[1:])
        temp = parents[node1]
        parents[node1] = parents[node2]
        parents[node2] = temp
    else:
        node = int(command_line[1])
        q = deque([[node, 1]])
        all_child = []

        while q:
            p_node, depth = q.popleft()
            for child_node in range(1, N+1):
                if parents[child_node] == p_node and alarm_settings[child_node]==1:
                    q.append([child_node, depth + 1])
                    if power_list[child_node] >= depth:
                        all_child.append(child_node)
            
        # print(parents)
        # print(all_child)
        # print(alarm_settings)
        # print(power_list)
        print(len(all_child))