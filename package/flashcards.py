from PySide6.QtCore import Qt
from PySide6.QtWidgets import *

class FlashcardsTitle(QMainWindow):
  def __init__(self):
    super().__init__()

    self.titleLabel = QLabel("Title: ")
    self.title = QLineEdit()
    self.titleSubmit = QPushButton("Next")

    widget = QWidget()
    self.setCentralWidget(widget)
    gridLayout = QGridLayout(widget)
    gridLayout.addWidget(self.titleLabel, 0, 0)
    gridLayout.addWidget(self.title, 0, 1)
    gridLayout.addWidget(self.titleSubmit, 1, 0, 1, 2, Qt.AlignCenter)

    self.titleSubmit.clicked.connect(self.acceptTitle)

  def acceptTitle(self):
    title = self.title.text()
    if not title:
      self.title.setStyleSheet("border: 1px solid red")
    else:
      self.title.setStyleSheet("")
      print(title)