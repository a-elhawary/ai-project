import sys

from PyQt5 import QtCore
from PyQt5.QtWidgets import QApplication
from PyQt5.QtWidgets import QLabel
from PyQt5.QtWidgets import QHBoxLayout
from PyQt5.QtWidgets import QWidget
from PyQt5.QtWidgets import QLineEdit
from PyQt5.QtGui import QPainter 
from PyQt5.QtGui import QPen
from PyQt5.QtGui import QColor

PAD=20

selectedNodes = []
edges = []

class QtNode(QWidget):
    def __init__(self, x, y, parent=None):
        self.myParent = parent
        self.isSelected = False
        QWidget.__init__(self, parent)
        self.move(x, y)
        self.setContentsMargins(0,0,0,0)
        self.setStyleSheet("""
            color:#000; 
            border:1px solid black;
            padding:25px;
            margin:0;
            border-radius:25px;
        """)
        layout = QHBoxLayout()
        label = QLabel("test")
        label.resize(50,50)
        layout.addWidget(label)
        self.setLayout(layout)
    
    def mousePressEvent(self, event):
        if self.isSelected:
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
        self.update()

    def mouseDoubleClickEvent(self, event):
        for i in reversed(range(len(edges))):
            edge = edges[i]
            if self == edge[0] or self == edge[1]:
                edges.pop(i)
        self.setParent(None)
        self.myParent.update()

class GraphWindow(QWidget):
    def __init__(self, parent=None):
        QWidget.__init__(self, parent)
        self.setContentsMargins(0,0,0,0)
        self.WIDTH = 1080
        self.HEIGHT = 720
        self.setStyleSheet("""
            background-color:#fff; 
        """)
        self.setGeometry(100, 100, self.WIDTH, self.HEIGHT)
        self.show()

    def paintEvent(self, e):
        painter = QPainter()
        painter.begin(self)
        painter.eraseRect(e.rect())
        pen = QPen()
        pen.setWidth(3)
        painter.setPen(pen)
        for edge in edges:
            painter.drawLine(edge[0].pos().x() + PAD, edge[0].pos().y() + PAD,edge[1].pos().x() + PAD, edge[1].pos().y() + PAD )

    def mouseDoubleClickEvent(self, event):
        newNode = QtNode(event.pos().x(), event.pos().y(), self)
        newNode.show()

    def keyPressEvent(self,e):
        # pressed on e key
        if e.key() == 69 and len(selectedNodes) == 2:
            self.addEdge(selectedNodes[0], selectedNodes[1])

    def addEdge(self, parent, successor):
        edges.append([parent, successor])
        self.update()

def main():
    app = QApplication(sys.argv)
    window = GraphWindow()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()