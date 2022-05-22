def ucs( graph, start, goal):
    visited = []
    queue = [[start,0, [start]]]
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
            return visited,minPath
        else:
            visited.append(minNode)
            nextNodes = graph[minNode][1]
            for (cost,node) in nextNodes:
                queue.append((node, cost + min, minPath + [node]))


if __name__ == '__main__':
    graph = {
        'S': (0,[(2,'A'), (3,'B'), (5,'D')]),
        'A': (0,[(4,'C')]),
        'B': (0,[(4,'D')]),
        'C': (0,[(1,'D'), (2,'G')]),
        'D': (0,[(5,'G')]),
        'G': (0,[])
    }
    print(ucs(graph,'S',['G']))