import json
from PySide6.QtWidgets import *
from PySide6.QtCore import Qt
from package.flashcards import Flashcards
from package.testcards import TestCards

flashcardList = {}

with open('flashcard.json', 'r') as f:
  flashcardList = json.load(f)

class MainWindow(QMainWindow):
  def __init__(self):
    super().__init__()

    self.button = QPushButton("Add flashcard set")
    self.text = QLabel("You don't have any flashcard sets added yet.",
                                  alignment=Qt.AlignCenter)
    self.grid = QGridLayout()
    widget = QWidget()
    self.setCentralWidget(widget)
    gridLayout = QGridLayout(widget)

    self.deck = QGroupBox("Decks")
    self.deckVBox = QVBoxLayout()
    self.deckVBox.setAlignment(Qt.AlignTop)
    self.deck.setLayout(self.deckVBox)
    self.flashcards = Flashcards("")

    self.empty = False
    if len(flashcardList) == 0:
      self.deckVBox.addWidget(self.text)
      self.empty = True
    else:
      self.seeAllDecks()

    gridLayout.addWidget(self.deck, 0, 0)
    gridLayout.addWidget(self.button, 1, 0)
    self.setLayout(gridLayout)
    self.button.clicked.connect(self.openFlashcards)
  def openFlashcards(self, title=""):
    print(title)
    self.flashcards = Flashcards(title)
    if title:
      self.flashcards.resize(800, 600)
    else:
      self.flashcards.resize(300, 100)
    self.flashcards.show()
    self.flashcards.updated.connect(self.reload)
    self.hide()

  def testFlashcards(self, title=""):
    print(title)
    self.testCards = TestCards(title)
    self.testCards.resize(800, 600)
    self.testCards.show()
    self.testCards.updated.connect(self.reload)
    self.hide()

  def reload(self):
    global flashcardList
    with open('flashcard.json', 'r') as f:
      flashcardList = json.load(f)

    self.seeAllDecks()
    self.show()
    
  def seeAllDecks(self):
    global flashcardList
    titles = list(flashcardList.keys())
    i = 0
    grid = QGridLayout()
    for item in titles:
      editButton = QPushButton("Edit")
      testButton = QPushButton("Test")
      label = QLabel(item)
      label.setStyleSheet("font-weight: bold")
      grid.addWidget(label, i, 0, 1, 2, Qt.AlignTop)
      grid.addWidget(editButton, i, 2, Qt.AlignTop)
      grid.addWidget(testButton, i, 3, Qt.AlignTop)
      editButton.clicked.connect(lambda c=None, a=i: self.openFlashcards(titles[a]))
      testButton.clicked.connect(lambda c=None, a=i: self.testFlashcards(titles[a]))
      i += 1
    
    print(i)
    if self.empty:
      self.deckVBox.removeWidget(self.text)
      self.text.deleteLater()
      self.empty = False
    
    self.deckVBox.removeItem(self.grid)
    self.grid = grid
    self.deckVBox.addLayout(grid)