def greedy( graph, start, goal):
    visited = []
    queue = [[start,graph[start][0]]]
    while len(queue) > 0:
        newQueue = []
        min = 99999
        minNode = None
        while queue:
            (node,cost) = queue.pop(0)
            if cost < min:
                newQueue.append((minNode, min))
                min = cost
                minNode = node
            else:
                newQueue.append((node,cost))
        queue = newQueue
        if minNode in visited:
            continue
        if minNode in goal:
            visited.append(minNode)
            return visited
        else:
            visited.append(minNode)
            nextNodes = graph[minNode][1]
            for (cost, node) in nextNodes:
                queue.append((node, graph[node][0]))


if __name__ == '__main__':
    graph = {
        'S': (10,[(2,'A'), (3,'B'), (5,'D')]),
        'A': (3,[(4,'C')]),
        'B': (2,[(4,'D')]),
        'C': (1,[(1,'D'), (2,'G')]),
        'D': (8,[(5,'G')]),
        'G': (0,[])
    }
    solution = greedy(graph,'S','G')
    print('Solution is ', solution)