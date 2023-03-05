import json
from PySide6.QtWidgets import *
from PySide6.QtCore import Qt
from package.flashcards import Flashcards

with open('flashcard.json', 'r') as f:
      flashcardList = json.load(f)

class MainWindow(QMainWindow):
  def __init__(self):
    super().__init__()

    self.button = QPushButton("Add flashcard set")
    self.text = QLabel("You don't have any flashcard sets added yet.",
                                  alignment=Qt.AlignCenter)
    
    self.selector = QListWidget()
    for item in flashcardList:
      self.selector.addItem(QListWidgetItem(item))
    self.selector.setCurrentRow(0)
    
    widget = QWidget()
    self.setCentralWidget(widget)
    gridLayout = QGridLayout(widget)

    if len(flashcardList) == 0:
      gridLayout.addWidget(self.text, 0, 0)
    else:
      gridLayout.addWidget(self.selector, 0, 0)

    gridLayout.addWidget(self.button, 1, 0)

    self.button.clicked.connect(self.openFlashcards)

  def openFlashcards(self):
    self.flashcards = Flashcards()
    self.flashcards.resize(300, 100)
    self.flashcards.show()