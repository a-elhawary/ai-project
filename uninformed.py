def bfs(graph, start, goal):  # function for BFS
    visited = []
    queue = []
    queue.append(start)

    while queue:  # Creating loop to visit each node
        m = queue.pop(0)
        visited.append(m)
        if m in goal:
            return visited
        for neighbour in graph[m][1]:
            if neighbour[1] not in visited:
                queue.append(neighbour[1])


def dfs(graph, start, goal):  # function for dfs
    visited = []
    queue = [[0,start]]
    while len(queue) > 0:
        newQueue = []
        maxValue = -1
        minNode = None
        while queue:
            (cost, node) = queue.pop(0)
            if cost is not None and cost > maxValue:
                newQueue.append((maxValue, minNode))
                maxValue = cost
                minNode = node
            else:
                newQueue.append((cost, node))
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
                queue.append((1 + maxValue, node))


if __name__ == '__main__':
    graph = {
        '5': (0, [(0, '3'),(0,'7')]),
        '3': (0, [(0, '2'),(0,'4')]),
        '7': (0, [(0, '8')]),
        '2': (0, []),
        '4': (0, [(0, '8')]),
        '8': (0, [])
    }
    print(bfs(graph, '5', ['8']))