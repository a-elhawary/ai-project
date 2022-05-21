def a_star( graph, start, goal):
    visited = []
    queue = [[start,0]]
    while len(queue) > 0:
        print(queue)
        newQueue = []
        min = 99999
        minNode = None
        while queue:
            (node,cost) = queue.pop(0)
            cost += graph[node][0]
            if (cost < min):
                if minNode is not None:
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
            print("goal reached")
            print(visited)
            return minNode
        else:
            visited.append(minNode)
            nextNodes = graph[minNode][1]
            for (cost,node) in nextNodes:
                queue.append((node, cost + min))


if __name__ == '__main__':
    graph = {
        'S': (10,[(2,'A'), (3,'B'), (5,'D')]),
        'A': (6,[(4,'C')]),
        'B': (2,[(4,'D')]),
        'C': (8,[(1,'D'), (2,'G')]),
        'D': (1,[(5,'G')]),
        'G': (0,[])
    }
    solution = a_star(graph, 'S', 'G')
    print('Solution is ', solution)