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
from PyQt5.QtWidgets import QLineEdit
from PyQt5.QtGui import QPainter 
from PyQt5.QtGui import QPen
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
        startButton = QPushButton("Start")
        startButton.setStyleSheet("""
            background-color:#23292e; 
            border-radius:2px;
            padding:10px 15px;
            margin:0;
        """)
        startButton.clicked.connect(self.start)
        hLayout.addWidget(startButton)
        topBar.setLayout(hLayout)
        vLayout.addWidget(topBar,1)
        vLayout.addWidget(self.graphWindow,10)
        self.setLayout(vLayout)
        self.show()

    def start(self):
        graph = self.graphWindow.getGraph()
        algo = self.algoComb.currentText()
        if len(selectedNodes) != 1:
            #TODO:error msg to usr
            return  
        goal = []
        for key in graph:
            if graph[key][0] == 0:
                goal += [key]
        if len(goal) == 0:
            #TODO:error msg to usr
            return
        if algo == "Depth First":
            print(dfs(graph, selectedNodes[0].name, goal))
        elif algo == "Breadth First":
            print(bfs(graph, selectedNodes[0].name, goal))
        elif algo == "Uniform Cost":
            print(ucs(graph, selectedNodes[0].name, goal))
        elif algo == "Greedy":
            print(greedy(graph, selectedNodes[0].name, goal))
        elif algo == "A*":
            print(a_star(graph, selectedNodes[0].name, goal))
        elif algo == "Iterative":
            print(iterative(graph, selectedNodes[0].name, goal))

def main():
    app = QApplication(sys.argv)
    myApp = myApplication()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()