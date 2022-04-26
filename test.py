import sys

from PyQt5 import QtCore
from PyQt5.QtWidgets import QApplication
from PyQt5.QtWidgets import QLabel
from PyQt5.QtWidgets import QHBoxLayout
from PyQt5.QtWidgets import QWidget
from PyQt5.QtWidgets import QLineEdit
from PyQt5.QtGui import QPainter 
from PyQt5.QtGui import QPen

PAD=20

selectedNodes = []

class QtNode(QWidget):
    def __init__(self, x, y, parent=None):
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
        self.setParent(None)
        self.deleteLater()

class GraphWindow(QWidget):
    def __init__(self, parent=None):
        QWidget.__init__(self, parent)
        self.setContentsMargins(0,0,0,0)
        self.edges = []
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
        pen = QPen()
        pen.setWidth(3)
        painter.setPen(pen)
        for edge in self.edges:
            painter.drawLine(edge[0].x() + PAD, edge[0].y() + PAD,edge[1].x() + PAD, edge[1].y() + PAD )

    def mouseDoubleClickEvent(self, event):
        newNode = QtNode(event.pos().x(), event.pos().y(), self)
        newNode.show()

    def keyPressEvent(self,e):
        # pressed on e key
        if e.key() == 69 and len(selectedNodes) == 2:
            self.addEdge(selectedNodes[0], selectedNodes[1])

    def addEdge(self, parent, successor):
        self.edges.append([parent.pos(), successor.pos()])
        self.update()

def main():
    app = QApplication(sys.argv)
    window = GraphWindow()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()