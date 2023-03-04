import sys
from PySide6.QtCore import *
from PySide6.QtWidgets import *
from PySide6.QtGui import *

class Flashcards(QMainWindow):
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

class MainWindow(QMainWindow):
  def __init__(self):
    super().__init__()

    self.button = QPushButton("Add flashcard set")
    self.text = QLabel("You don't have any flashcard sets added yet.",
                                  alignment=Qt.AlignCenter)
    
    widget = QWidget()
    self.setCentralWidget(widget)
    gridLayout = QGridLayout(widget)
    gridLayout.addWidget(self.text, 0, 0)
    gridLayout.addWidget(self.button, 1, 0)

    self.button.clicked.connect(self.openFlashcards)

  def openFlashcards(self):
    self.flashcards = Flashcards()
    self.flashcards.resize(300, 100)
    self.flashcards.show()

if __name__ == "__main__":
  app = QApplication([])

  window = MainWindow()
  window.resize(800, 600)
  window.show()

  sys.exit(app.exec())