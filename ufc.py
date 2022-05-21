def ucs( graph, start, goal):
    visited = []
    queue = [[start,0]]
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
            for (cost,node) in nextNodes:
                queue.append((node, cost + min))


if __name__ == '__main__':
    graph = {
        'S': (0,[(2,'A'), (3,'B'), (5,'D')]),
        'A': (0,[(4,'C')]),
        'B': (0,[(4,'D')]),
        'C': (0,[(1,'D'), (2,'G')]),
        'D': (0,[(5,'G')]),
        'G': (0,[])
    }
    solution = ucs(graph,'S',['G', 'D'])
    print('Solution is ', solution)