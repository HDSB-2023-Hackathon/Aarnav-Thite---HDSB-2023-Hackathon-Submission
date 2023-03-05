from PySide6.QtCore import *
from PySide6.QtWidgets import *
import json
global_title = ""
class Flashcards(QMainWindow):
  def __init__(self):
    super().__init__()

    self.central_widget = QStackedWidget()
    self.setCentralWidget(self.central_widget)

    self.titleScreen = FlashcardsTitle()
    self.addScreen = FlashcardsAdd()

    self.central_widget.addWidget(self.titleScreen)
    self.central_widget.setCurrentWidget(self.titleScreen)

    self.setWindowTitle("Create Flashcard Set")
    self.titleScreen.clicked.connect(lambda t: self.changeToAdd(t))
    self.addScreen.done.connect(self.cobalt)

  def changeToAdd(self, title):
    global global_title
    self.setWindowTitle(title)
    self.central_widget.addWidget(self.addScreen)
    self.central_widget.setCurrentWidget(self.addScreen)
    self.resize(800, 600)
    global_title = title
  def cobalt(self):
    self.hide()

class FlashcardsTitle(QWidget):
  clicked = Signal(str)

  def __init__(self):
    super().__init__()

    widget = QWidget()

    self.titleLabel = QLabel("Title: ")
    self.title = QLineEdit()
    self.titleSubmit = QPushButton("Create")
  
    gridLayout = QGridLayout(widget)
    gridLayout.addWidget(self.titleLabel, 0, 0)
    gridLayout.addWidget(self.title, 0, 1)
    gridLayout.addWidget(self.titleSubmit, 1, 0, 1, 2, Qt.AlignCenter)
  
    self.setLayout(gridLayout)
  
    self.titleSubmit.clicked.connect(self.acceptTitle)
    self.title.returnPressed.connect(self.acceptTitle)

  def acceptTitle(self):
    with open('flashcard.json', 'r') as f:
      flashcardList = json.load(f)
    title = self.title.text()
    if title in flashcardList:
      temp = self.checkDuplicates(title, 1, flashcardList)
      print(temp)
      flashcardList[temp] = []
    else:
      flashcardList[title] = []
    with open('flashcard.json','w') as f:
      json.dump(flashcardList, f)
    if not title:
      self.title.setStyleSheet("border: 1px solid red")
    else:
      self.title.setStyleSheet("")
      self.clicked.emit(title)
  def checkDuplicates(self, name,number,  dict):
    if f"{name}({number})" not in dict:
      return f"{name}({number})"
    else:
      self.checkDuplicates(self, name, number+1, dict)



class FlashcardsAdd(QWidget):
  cards = [("", "")]
  done = Signal()
  def __init__(self):
    super().__init__()

    widget = QWidget()

    self.deck = QGroupBox("Deck")
    self.deckVBox = QVBoxLayout()
    self.deck.setLayout(self.deckVBox)

    self.selector = QListWidget()
    self.selector.addItem(QListWidgetItem("New Flashcard"))
    self.selector.setCurrentRow(0)
    self.addButton = QPushButton("Add")
    self.removeButton = QPushButton("Remove")
  
    self.deckVBox.addWidget(self.selector)
    self.deckVBox.addWidget(self.addButton)
    self.deckVBox.addWidget(self.removeButton)

    self.card = QGroupBox("Card")
    self.cardVBox = QVBoxLayout()
    self.card.setLayout(self.cardVBox)

    self.questionEdit = QTextEdit()
    self.answerEdit = QTextEdit()
    self.questionLabel = QLabel("Question")
    self.answerLabel = QLabel("Answer")
    self.doneButton = QPushButton("Done")

    self.questionEdit.setPlaceholderText("Jake Park is more commonly known as:")
    self.answerEdit.setPlaceholderText("Lake")

    self.cardVBox.addWidget(self.questionLabel)
    self.cardVBox.addWidget(self.questionEdit)
    self.cardVBox.addWidget(self.answerLabel)
    self.cardVBox.addWidget(self.answerEdit)
    self.cardVBox.addWidget(self.doneButton)

    gridLayout = QGridLayout(widget)
    gridLayout.addWidget(self.deck, 0, 0, 5, 1, Qt.AlignLeft)
    gridLayout.addWidget(self.card, 0, 1, 5, 3)
    self.setLayout(gridLayout)

    self.addButton.clicked.connect(self.addCard)
    self.removeButton.clicked.connect(self.removeCard)
    self.questionEdit.textChanged.connect(self.updateTitle)
    self.questionEdit.textChanged.connect(self.updateCards)
    self.answerEdit.textChanged.connect(self.updateCards)
    self.selector.itemPressed.connect(self.updateQA)
    self.doneButton.clicked.connect(self.addToArray)
  def addCard(self):
    self.selector.addItem(QListWidgetItem("New Flashcard"))
    self.cards.append(("", ""))
    self.selector.setCurrentRow(self.selector.count() - 1)
    self.questionEdit.setText("")
    self.answerEdit.setText("")
    


  def removeCard(self):
    it = self.selector.takeItem(self.selector.currentRow())
    del it
    self.cards.pop(self.selector.currentRow())

  def updateTitle(self):
    text = self.questionEdit.toPlainText()
    if text:
      self.selector.currentItem().setText(text.replace("\n", " "))
    else:
      self.selector.currentItem().setText("New Flashcard")

  def updateCards(self):
    self.cards[self.selector.currentRow()] = (self.questionEdit.toPlainText(), self.answerEdit.toPlainText())
    print(self.cards)

  def updateQA(self):
    row = self.selector.currentRow()
    card = self.cards[row]
    self.questionEdit.setText(card[0])
    self.answerEdit.setText(card[1])

  def addToArray(self):
    global global_title
    with open('flashcard.json', 'r') as f:
      flashcardList = json.load(f)
    title = global_title
    for item in self.cards:
      flashcardList[title].append([item[0], item[1], 1])
    with open('flashcard.json','w') as f:
      json.dump(flashcardList, f)
    global_title = ""
    self.done.emit()