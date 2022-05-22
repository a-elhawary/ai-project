import sys

# GUI Imports
from PyQt5 import QtCore
from PyQt5.QtWidgets import QApplication
from PyQt5.QtWidgets import QLabel
from PyQt5.QtWidgets import QComboBox
from PyQt5.QtWidgets import QPushButton
from PyQt5.QtWidgets import QHBoxLayout
from PyQt5.QtWidgets import QVBoxLayout
from PyQt5.QtWidgets import QWidget
from PyQt5.QtWidgets import QMessageBox
from PyQt5.QtWidgets import QLineEdit
from PyQt5.QtGui import QPainter 
from PyQt5.QtGui import QPen
from PyQt5.QtGui import QBrush
from PyQt5.QtGui import QColor

# Algorithm imports
from a_star import a_star
from greedy import greedy
from iterative import iterative
from ufc import ucs
from uninformed import dfs,bfs

PAD=20

selectedNodes = []
edges = []
nodeCount=0

class QtNode(QWidget):
    def __init__(self, x, y, parent=None):
        QWidget.__init__(self, parent)
        global nodeCount
        nodeCount+=1
        self.color = None
        self.name = str(nodeCount)
        self.heuristic=None
        self.myParent = parent
        self.isSelected = False
        self.setGeometry(x,y,120,120)
        self.setContentsMargins(0,0,0,0)
        self.node = QWidget(self)
        self.node.setObjectName("node")
        self.node.setGeometry(0,0,120,120)
        self.node.setStyleSheet("""
            QWidget#node{
                border:1px solid black;
                border-radius:60px;
            } 
            QWidget{
                background-color:#f7f7f7;
                color:#000;
            }
        """)
        self.node.setContentsMargins(10,10,10,10)
        vLayout = QVBoxLayout()
        label = QLabel(self.name)
        label.setStyleSheet("""
            margin-left:28px; 
        """)
        vLayout.addWidget(label)
        inputRow = QWidget()
        hLayout = QHBoxLayout()
        hLayout.addWidget(QLabel("h= "))
        self.heuristicInput= QLineEdit()
        self.heuristicInput.textChanged.connect(self.setHeuristic)
        hLayout.addWidget(self.heuristicInput)
        inputRow.setLayout(hLayout)
        vLayout.addWidget(inputRow)
        self.node.setLayout(vLayout)

    def setHeuristic(self, event):
        value = self.heuristicInput.text()
        if len(value) == 0:
            return 
        if not (value[-1] >= "0" and value[-1] <= "9"):
            self.heuristicInput.backspace()
            return
        self.myParent.changeHeuristic(self.name, int(value))

    def unSelect(self):
        self.isSelected = False
        i = 0
        for node in selectedNodes:
            if node == self:
                selectedNodes.pop(i)
            i+=1
        self.node.setStyleSheet("""
            QWidget#node{
                border:1px solid black;
                border-radius:60px;
            } 
            QWidget{
                background-color:#f7f7f7;
                color:#000;
            }
        """)
        if len(selectedNodes) < 2:
            self.myParent.hideCreateEdgeButton()

    def changeColor(self,color):
        borderColor = ""
        if self.isSelected:
            borderColor = "green"
        else:
            borderColor = "black"
        self.node.setStyleSheet(f"""
            QWidget#node{{
                border:1px solid {borderColor};
                border-radius:60px;
            }} 
            QWidget{{
                background-color:#{color};
                color:#000;
            }}
        """)

    def mousePressEvent(self, event):
        if self.isSelected:
            self.unSelect()
        else:
            if len(selectedNodes) < 2:
                self.isSelected = True
                selectedNodes.append(self)
                self.node.setStyleSheet("""
                    QWidget#node{
                        border:1px solid green;
                        border-radius:60px;
                    } 
                    QWidget{
                        background-color:#f7f7f7;
                        color:#000;
                    }
                """)
                if len(selectedNodes) == 2:
                    self.myParent.showCreateEdgeButton()
        self.update()

    def mouseDoubleClickEvent(self, event):
        for i in reversed(range(len(edges))):
            edge = edges[i]
            if self == edge[0] or self == edge[1]:
                self.myParent.removeEdgeFromGraph(edge[0], edge[1])
                if len(edge) > 2:
                    edge[2].setParent(None)
                    edge[2].deleteLater()
                edges.pop(i)
        for i in reversed(range(len(selectedNodes))):
            if selectedNodes[i] == self:
                selectedNodes.pop(i)
        self.setParent(None)
        self.myParent.removeNodeFromGraph(self)
        self.myParent.update()
    

class GraphWindow(QWidget):
    def __init__(self, parent=None):
        QWidget.__init__(self, parent)
        self.isUndirected = True
        self.nodes = []
        self.movingNode = None
        self.graph = {}
        self.setContentsMargins(0,0,0,0)
        self.setStyleSheet("""
            background-color:#fff; 
            margin:0
        """)
        self.createEdge = QPushButton(self)
        self.createEdge.clicked.connect(self.onCreateEdgeClick)
        self.createEdge.move(10, 10)
        self.createEdge.setText("Create Edge")
        self.createEdge.setStyleSheet("""
            border:none; 
            background-color:#23292e; 
            color:#fff;
            padding:10px 15px;
            border-radius:4px;
        """)
        self.createEdge.hide()

    def onCreateEdgeClick(self):
        self.addEdge(selectedNodes[0], selectedNodes[1])
        selectedNodes[0].unSelect()
        selectedNodes[0].unSelect()
    
    def hideCreateEdgeButton(self):
        self.createEdge.hide()
    
    def showCreateEdgeButton(self):
        self.createEdge.show()
    
    def changeNodeColor(self, nodeName, color):
        for node in self.nodes:
            if node.name == nodeName:
                node.changeColor(color)
            
    def resetNodesColor(self):
        for node in self.nodes:
            node.changeColor("f7f7f7")
        
    def paintEvent(self, e):
        for edge in edges:
            if len(edge) >= 3:
                xMid = (edge[0].pos().x() + edge[1].pos().x())/ 2
                yMid = (edge[0].pos().y() + edge[1].pos().y())/ 2
                edge[2].move(int(xMid), int(yMid))
        painter = QPainter()
        painter.begin(self)
        painter.eraseRect(e.rect())
        pen = QPen()
        pen.setWidth(1)
        painter.setPen(pen)
        for edge in edges:
            painter.drawLine(edge[0].pos().x() + PAD, edge[0].pos().y() + PAD,edge[1].pos().x() + PAD, edge[1].pos().y() + PAD )
            if not self.isUndirected:
                x = edge[1].pos().x()
                y = edge[1].pos().y()
                painter.setBrush(QBrush(QtCore.Qt.black, QtCore.Qt.SolidPattern))
                painter.drawEllipse(x + 10, y + 10, 10, 10)
    
    def mouseMoveEvent(self, event):
        if self.movingNode == None:
            for node in self.nodes:
                if abs(node.pos().x() - event.pos().x()) < 50 and abs(node.pos().y() - event.pos().y()) < 50:
                    self.movingNode = node
                    break
        else:
            self.movingNode.move(event.pos().x(), event.pos().y())
            self.movingNode.update()
            self.update()
        
    def mouseReleaseEvent(self, event):
        self.movingNode = None

    def mouseDoubleClickEvent(self, event):
        newNode = QtNode(event.pos().x(), event.pos().y(), self)
        newNode.show()
        self.graph[newNode.name] = (newNode.heuristic, [])
        self.nodes.append(newNode)

    def addEdge(self, parent, successor):
        edges.append([parent, successor])
        self.createEdgeLabel(edges[-1])
        temp = list(self.graph[parent.name])
        temp[1] += [(0, successor.name)]
        self.graph[parent.name] = tuple(temp)
        if self.isUndirected:
            temp = list(self.graph[successor.name])
            temp[1] += [(0, parent.name)]
            self.graph[successor.name] = tuple(temp)
        self.update()
        if parent is not None:
            parent.update()
    
    def createEdgeLabel(self, edge):
        xMid = (edge[0].pos().x() + edge[1].pos().x())/ 2
        yMid = (edge[0].pos().y() + edge[1].pos().y())/ 2
        edgeEdit = QLineEdit(self)
        edgeEdit.setStyleSheet("""
            color:#000;
            border:1px solid #222;
            border-radius:4px;
            width:40px;
        """)
        edgeEdit.move(int(xMid), int(yMid))
        edgeEdit.textChanged.connect(lambda event: self.updateCost(event, edge))
        edgeEdit.show()
        edge.append(edgeEdit)
    
    def updateCost(self, event, edge):
        if event == "":
            event = '0'
        nxt = self.graph[edge[0].name][1]
        for i in range(len(nxt)):
            node = nxt[i]
            if node[1] == edge[1].name:
                x = list(node)
                x[0] = int(event)
                nxt[i] = tuple(x)
                break
        x = list(self.graph[edge[0].name])
        x[1] = nxt
        self.graph[edge[0].name] = tuple(x)
        nxt = list(self.graph[edge[1].name][1])
        for i in range(len(nxt)):
            node = nxt[i]
            if node[1] == edge[0].name:
                x = list(node)
                x[0] = int(event)
                nxt[i] = tuple(x)
                break
        x = list(self.graph[edge[1].name])
        x[1] = nxt
        self.graph[edge[1].name] = tuple(x)

    def changeHeuristic(self, node, heuristic):
        x = list(self.graph[node])
        x[0] = heuristic
        self.graph[node] = tuple(x)

    def getGraph(self):
        return self.graph

    def setDirection(self, isUndirected):
        self.isUndirected = isUndirected
        for edge in edges:
            if isUndirected:
                temp = list(self.graph[edge[1].name])
                parentGraph = self.graph[edge[0].name][1]
                newCost = 0
                for pEdge in parentGraph:
                    if pEdge[1] == edge[1].name:
                        newCost = pEdge[0]
                        break
                temp[1] += [(newCost, edge[0].name)]
                self.graph[edge[1].name] = tuple(temp)
            else:
                temp = list(self.graph[edge[1].name])
                for i in reversed(range(len(temp[1]))):
                    node = temp[1][i]
                    if node[1] == edge[0].name:
                        temp[1].pop(i)
                self.graph[edge[1].name] = tuple(temp)
        self.update()

    def removeEdgeFromGraph(self, parent, succesor):
        x = list(self.graph[parent.name])
        for i in range(len(x[1])):
            if x[1][i] == succesor.name:
                x[1].pop(i)
                break
        self.graph[parent.name] = tuple(x)
        x = list(self.graph[succesor.name])
        for i in range(len(x[1])):
            if x[1][i] == parent.name:
                x[1].pop(i)
                break
        self.graph[succesor.name] = tuple(x)
    
    def removeNodeFromGraph(self,node):
        del self.graph[node.name]

class myApplication(QWidget):
    def __init__(self, parent=None):
        QWidget.__init__(self,parent)
        self.iterativeCount = 0
        self.stepCount = 0
        self.visited = []
        self.path = []
        self.errorBox = QMessageBox()
        self.errorBox.setIcon(QMessageBox.Critical)
        self.graphWindow = GraphWindow()
        self.setGeometry(100,100,1080,720)
        self.setContentsMargins(0,0,0,0)
        self.setStyleSheet("""
            margin:0;
            padding:0;
        """)
        vLayout = QVBoxLayout()
        topBar = QWidget()
        topBar.setContentsMargins(0,0,0,0)
        topBar.setStyleSheet("""
            background-color: #7f99b0;
            color:#fff;
            margin:0;
        """)
        hLayout = QHBoxLayout() 
        hLayout.addWidget(QLabel("AI - Search"), 1)
        self.algoComb = QComboBox()
        self.algoComb.addItems(["Depth First", "Breadth First", "Uniform Cost", "Greedy", "A*", "Iterative"])
        self.algoComb.setStyleSheet("""
            background-color:#fff;
            color:#000;
            border:none;
        """)
        hLayout.addWidget(self.algoComb)
        self.startButton = QPushButton("Start")
        self.startButton.setStyleSheet("""
            background-color:#23292e; 
            border-radius:2px;
            padding:10px 15px;
            margin:0;
        """)
        self.startButton.clicked.connect(self.start)
        self.stepButton = QPushButton("Step")
        self.stepButton.setStyleSheet("""
            background-color:#23292e; 
            border-radius:2px;
            padding:10px 15px;
            margin:0;
        """)
        self.stepButton.hide()
        self.stepButton.clicked.connect(self.step)
        self.directionButton = QPushButton("Undirected")
        self.directionButton.setStyleSheet("""
            background-color:#23292e; 
            border-radius:2px;
            padding:10px 15px;
            margin:0;
        """)
        self.directionButton.clicked.connect(self.toggleDirection)
        hLayout.addWidget(self.directionButton)
        hLayout.addWidget(self.stepButton)
        hLayout.addWidget(self.startButton)
        topBar.setLayout(hLayout)
        vLayout.addWidget(topBar,1)
        vLayout.addWidget(self.graphWindow,10)
        self.setLayout(vLayout)
        self.show()
    
    def stop(self):
        self.visited = []
        self.graphWindow.resetNodesColor()
        self.stepButton.hide()
        self.startButton.clicked.connect(self.start)
        self.startButton.setText("Start")
        self.stepCount = 0
        self.iterativeCount = 0

    def start(self):
        graph = self.graphWindow.getGraph()
        algo = self.algoComb.currentText()
        if len(selectedNodes) != 1:
            self.errorBox.setText("<html>Must Select exactly one starting node before running algorithm<br/><br/> Select a node by clicking on it<html>")
            self.errorBox.exec_()
            return  
        goal = []
        for key in graph:
            if graph[key][0] == 0:
                goal += [key]
        if len(goal) == 0:
            self.errorBox.setText("<html>Must Select at least one goal node before running algorithm<br/><br/> Select a goal node by setting it's heuristic to 0<html>")
            self.errorBox.exec_()
            return
        self.stepButton.show()
        if algo == "Depth First":
            self.visited, self.path = dfs(graph, selectedNodes[0].name, goal)
        elif algo == "Breadth First":
            self.visited, self.path = bfs(graph, selectedNodes[0].name, goal)
        elif algo == "Uniform Cost":
            self.visited, self.path = ucs(graph, selectedNodes[0].name, goal)
        elif algo == "Greedy":
            self.visited, self.path = greedy(graph, selectedNodes[0].name, goal)
        elif algo == "A*":
            self.visited, self.path = a_star(graph, selectedNodes[0].name, goal)
        elif algo == "Iterative":
            self.visited, self.path = iterative(graph, selectedNodes[0].name, goal)
        self.startButton.clicked.connect(self.stop)
        self.startButton.setText("Stop")
        
    def step(self):
        if(self.algoComb.currentText() == "Iterative"):
            if(self.iterativeCount >= len(self.visited)):
                for node in self.path:
                    self.graphWindow.changeNodeColor(node,"b32434")
                return
            if(self.stepCount >= len(self.visited[self.iterativeCount])):
                self.stepCount = 0
                self.iterativeCount+=1
                if(self.iterativeCount < len(self.visited)):
                    self.graphWindow.resetNodesColor()
                return 
            nodeName = self.visited[self.iterativeCount][self.stepCount]
            visitedFringe = self.visited[self.iterativeCount][0:self.stepCount]
        else:
            if(self.stepCount >= len(self.visited)):
                for node in self.path:
                    self.graphWindow.changeNodeColor(node,"b32434")
                return 
            nodeName = self.visited[self.stepCount]
            visitedFringe = self.visited[0:self.stepCount]
        graph = self.graphWindow.getGraph()
        fringeTuple = graph[nodeName][1]
        for node in fringeTuple:
            if node[1] not in visitedFringe:
                self.graphWindow.changeNodeColor(node[1], "ebeba4")
        self.graphWindow.changeNodeColor(nodeName, "89b579")
        self.stepCount+=1
 
    def toggleDirection(self):
        if self.directionButton.text() == "Undirected":
            self.graphWindow.setDirection(False)
            self.directionButton.setText("Directed")
        else:
            self.graphWindow.setDirection(True)
            self.directionButton.setText("Undirected")

def main():
    app = QApplication(sys.argv)
    myApp = myApplication()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()