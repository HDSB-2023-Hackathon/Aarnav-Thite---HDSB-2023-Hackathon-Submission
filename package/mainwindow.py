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
    
    widget = QWidget()
    self.setCentralWidget(widget)
    gridLayout = QGridLayout(widget)
    titles = flashcardList.keys()

    self.deck = QGroupBox("Decks")
    self.deckVBox = QVBoxLayout()
    self.deckVBox.setAlignment(Qt.AlignTop)
    self.deck.setLayout(self.deckVBox)
    
    if len(flashcardList) == 0:
      self.deckVBox.addWidget(self.text)
    else:
      i = 0
      for item in titles:
        grid = QGridLayout()
        editButton = QPushButton("Edit")
        testButton = QPushButton("Test")
        label = QLabel(item)
        label.setStyleSheet("font-weight: bold")
        grid.addWidget(label, i, 0, 1, 2, Qt.AlignTop)
        grid.addWidget(editButton, i, 2, Qt.AlignTop)
        grid.addWidget(testButton, i, 3, Qt.AlignTop)
        self.deckVBox.addLayout(grid)
        print(self.deck)
        i += 1

    gridLayout.addWidget(self.deck, 0, 0)
    gridLayout.addWidget(self.button, 1, 0)
    self.setLayout(gridLayout)
    self.button.clicked.connect(self.openFlashcards)

  def openFlashcards(self):
    self.flashcards = Flashcards()
    self.flashcards.resize(300, 100)
    self.flashcards.show()