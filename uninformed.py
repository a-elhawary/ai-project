def bfs(graph, start, goal):  # function for BFS
    visited = []
    queue = []
    queue.append([start, [start]])

    while queue:  # Creating loop to visit each node
        m = queue.pop(0)
        visited.append(m[0])
        if m[0] in goal:
            return visited, m[1]
        for neighbour in graph[m[0]][1]:
            if neighbour[1] not in visited:
                queue.append([neighbour[1], m[1] + [neighbour[1]]])


def dfs(graph, start, goal):  # function for dfs
    visited = []
    queue = [(0,start, [start])]
    while len(queue) > 0:
        newQueue = []
        maxValue = -1
        minNode = None
        minPath = []
        while queue:
            (cost, node, path) = queue.pop(0)
            if cost is not None and cost > maxValue:
                newQueue.append((maxValue, minNode, minPath))
                maxValue = cost
                minNode = node
                minPath = path
            else:
                newQueue.append((cost, node, path))
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
                queue.append((1 + maxValue, node, minPath + [node]))


if __name__ == '__main__':
    graph = {
        '1': (0, [(0, '2'),(0,'3')]),
        '2': (0, [(0, '4'),(0,'5')]),
        '3': (0, [(0, '6'),(0,'7')]),
        '4': (0, []),
        '5': (0, []),
        '6': (0, []),
        '7': (0, [])
    }
    print(dfs(graph, '1', ['6']))