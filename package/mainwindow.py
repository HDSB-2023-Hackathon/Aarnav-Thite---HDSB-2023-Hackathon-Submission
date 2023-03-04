from PySide6.QtWidgets import *
from PySide6.QtCore import Qt
from package.flashcards import FlashcardsTitle
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
    self.flashcards = FlashcardsTitle()
    self.flashcards.resize(300, 100)
    self.flashcards.show()