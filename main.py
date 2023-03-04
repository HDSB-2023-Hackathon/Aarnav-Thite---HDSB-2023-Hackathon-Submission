import sys
import random
from PySide6 import QtCore, QtWidgets, QtGui

class Flashcards(QtWidgets.QDialog):
  def __init__(self):
    super().__init__()

class MainWindow(QtWidgets.QMainWindow):
  def __init__(self):
    super().__init__()

    self.button = QtWidgets.QPushButton("Add flashcard set")
    self.text = QtWidgets.QLabel("You don't have any flashcard sets added yet.",
                                  alignment=QtCore.Qt.AlignCenter)
    
    widget = QtWidgets.QWidget()
    self.setCentralWidget(widget)
    gridLayout = QtWidgets.QGridLayout(widget)
    gridLayout.addWidget(self.text, 0, 0)
    gridLayout.addWidget(self.button, 1, 0)

    self.button.clicked.connect(self.openFlashcards)

  def openFlashcards(self):
    self.flashcards = Flashcards()
    self.flashcards.show()

if __name__ == "__main__":
  app = QtWidgets.QApplication([])

  window = MainWindow()
  window.resize(800, 600)
  window.show()

  sys.exit(app.exec())