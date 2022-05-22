def depthLimited(graph, start, goal, limit):  # function for dfs
    visited = []
    queue = [[0,start, [start]]]
    while len(queue) > 0:
        newQueue = []
        maxValue = -1
        minNode = None
        minPath = []
        while queue:
            (cost, node, path) = queue.pop(0)
            if cost is not None and cost > maxValue:
                if node is not None:
                    newQueue.append((maxValue, minNode, minPath))
                maxValue = cost
                minNode = node
                minPath = path
            else:
                if node is not None:
                    newQueue.append((cost, node, path))
        queue = newQueue
        if minNode in visited:
            continue
        if maxValue > limit:
            continue
        if minNode == None:
            break
        if minNode in goal:
            visited.append(minNode)
            return visited, path
        else:
            visited.append(minNode)
            nextNodes = graph[minNode][1]
            for (cost, node) in nextNodes:
                queue.append((1 + maxValue, node, minPath + [node]))
    return visited, []

def iterative(graph, start, goal):
    i = 0
    isGoalFound = False
    visited = []
    path = []
    while not isGoalFound and len(graph) >= i:
        newVisited, newPath = depthLimited(graph, start, goal, i)
        isGoalFound = len(newPath) > 0
        path = newPath
        visited.append(newVisited)
        i+= 1
    return visited, path

if __name__ == "__main__":
    graph = {
        '5': (0, [(0, '3'),(0,'7')]),
        '3': (0, [(0, '2'),(0,'4')]),
        '7': (0, [(0, '8')]),
        '2': (0, []),
        '4': (0, [(0, '8')]),
        '8': (0, [])
    }
    print(iterative(graph, "5", ["8"]))
