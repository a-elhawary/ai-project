def greedy( graph, start, goal):
    visited = []
    queue = [[start,graph[start][0],[start]]]
    while len(queue) > 0:
        newQueue = []
        min = 99999
        minNode = None
        minPath = []
        while queue:
            (node,cost, path) = queue.pop(0)
            if cost < min:
                newQueue.append((minNode, min, minPath))
                min = cost
                minNode = node
                minPath = path
            else:
                newQueue.append((node,cost, path))
        queue = newQueue
        if minNode in visited:
            continue
        if minNode in goal:
            visited.append(minNode)
            return visited, minPath
        else:
            visited.append(minNode)
            nextNodes = graph[minNode][1]
            for (cost, node) in nextNodes:
                queue.append((node, graph[node][0], minPath + [node]))


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