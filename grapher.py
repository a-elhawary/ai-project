import sys

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
        self.move(x, y)
        self.setContentsMargins(0,0,0,0)
        self.setStyleSheet("""
            color:#000; 
            border:1px solid black;
            padding:25px;
            margin:0;
            border-radius:25px;
        """)
        layout = QVBoxLayout()
        label = QLabel(self.name)
        label.resize(50,50)
        layout.addWidget(label)
        self.setLayout(layout)

    def unSelect(self):
        self.isSelected = False
        i = 0
        for node in selectedNodes:
            if node == self:
                selectedNodes.pop(i)
            i+=1
        self.setStyleSheet("""
            color:#000; 
            border:1px solid black;
            padding:25px;
            margin:0;
            border-radius:25px;
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
                self.setStyleSheet("""
                    color:#000; 
                    border:1px solid green;
                    padding:25px;
                    margin:0;
                    border-radius:25px;
                """)
                if len(selectedNodes) == 2:
                    self.myParent.showCreateEdgeButton()
        self.update()

    def mouseDoubleClickEvent(self, event):
        for i in reversed(range(len(edges))):
            edge = edges[i]
            if self == edge[0] or self == edge[1]:
                self.myParent.removeEdgeFromGraph(edge[0], edge[1])
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
        temp = list(self.graph[parent.name])
        temp[1] += [successor.name]
        self.graph[parent.name] = tuple(temp)
        temp = list(self.graph[successor.name])
        temp[1] += [parent.name]
        self.graph[successor.name] = tuple(temp)
        self.update()
        if parent is not None:
            parent.update()

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
        self.algoComb.addItems(["Depth First", "Breadth First", "Uniform Cost", "Greedy", "A*"])
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
        print(self.graphWindow.getGraph())
        print(self.algoComb.currentText())

def main():
    app = QApplication(sys.argv)
    myApp = myApplication()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()