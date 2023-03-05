from PySide6.QtCore import *
from PySide6.QtWidgets import *
import json
import functools
import random

class TestCards(QMainWindow):
  def __init__(self, title):
    super().__init__()

    self.central_widget = QStackedWidget()
    self.setCentralWidget(self.central_widget)
    self.practiceScreen = PracticeScreen(title)
    # self.practice = Practice()

    self.setWindowTitle(f"Practice {title}")
    self.central_widget.addWidget(self.practiceScreen)
  
    self.central_widget.setCurrentWidget(self.practiceScreen)
    self.practiceScreen.clicked.connect(lambda x, y: self.startPractice(x, y))
  
  def startPractice(self, title, toDo):
    self.setWindowTitle(f"Practicing {title}...")
    self.practice = Practice(title, toDo)
    self.practice.complete.connect(self.complete)
    self.central_widget.addWidget(self.practice)
    self.central_widget.setCurrentWidget(self.practice)
  
  def complete(self):
    self.hide()

class PracticeScreen(QWidget):
  clicked = Signal(str, list)

  def __init__(self, title):
    super().__init__()

    with open('flashcard.json', 'r') as f:
      flashcardList = json.load(f)
    cards: list[dict] = flashcardList[title]["cards"]
    widget = QWidget()
    gridLayout = QGridLayout(widget)

    self.practiced = functools.reduce(lambda x, y: x + y, list(map(lambda x: int(x["practiced"]), cards)))
    self.practicedLabel = QLabel(f"You have practiced {self.practiced} cards today.", alignment=Qt.AlignCenter)
    self.practicedLabel.setStyleSheet("font-size: 20px; font-weight: bold")
    self.toDo = list(filter(lambda x: not x["practiced"], cards))
    if len(self.toDo):
      self.practiceButton = QPushButton("Practice")
      self.practiceButton.clicked.connect(lambda c=None, t=title, a=self.toDo: self.clicked.emit(t, a))
      gridLayout.addWidget(self.practiceButton, 1, 0)

    gridLayout.addWidget(self.practicedLabel, 0, 0)

    self.setLayout(gridLayout)


class Practice(QWidget):
  complete = Signal()
  def __init__(self, title, toDo):
    super().__init__()

    with open('flashcard.json', 'r') as f:
      self.flashcardList = json.load(f)

    self.cards = toDo
    self.title = title
    self.i = 0
    random.shuffle(self.cards)

    self.card = QGroupBox("Card")
    self.cardVBox = QVBoxLayout()
    self.card.setLayout(self.cardVBox)

    self.question = QLabel("")
    self.answer = QLabel("")
    self.showAnswer = QPushButton("Show Answer")
    self.right = QPushButton("I got that right!")
    self.wrong = QPushButton("I got that wrong...")

    self.cardVBox.addWidget(self.question)
    self.cardVBox.addWidget(self.answer)
    self.questionVBox = QVBoxLayout()

    self.questionVBox.addWidget(self.card, 3)
    self.questionVBox.addWidget(self.right, alignment=Qt.AlignmentFlag.AlignBottom)
    self.questionVBox.addWidget(self.wrong, alignment=Qt.AlignmentFlag.AlignBottom)
    self.nextQ()
    self.setLayout(self.questionVBox)

    self.showAnswer.clicked.connect(self.revealAnswer)

  def nextQ(self):
    if self.i >= len(self.cards):
      self.flashcardList[self.title]["cards"] = self.cards
      self.flashcardList[self.title]["days"] += 1
      with open('flashcard.json', 'w') as f:
        json.dump(self.flashcardList, f)
      self.complete.emit()
      return
    self.cardVBox.removeWidget(self.question)
    self.cardVBox.removeWidget(self.answer)
    self.questionVBox.removeWidget(self.right)
    self.questionVBox.removeWidget(self.wrong)

    self.right.deleteLater()
    self.wrong.deleteLater()
    self.question.deleteLater()
    self.answer.deleteLater()
  
    self.right = QPushButton("I got that right!")
    self.wrong = QPushButton("I got that wrong...")
    self.right.clicked.connect(self.handleRight)
    self.wrong.clicked.connect(self.handleWrong)

    self.questionVBox.removeWidget(self.card)
    self.question = QLabel(self.cards[self.i]["question"], alignment=Qt.AlignmentFlag.AlignCenter)
    # self.answer = QLabel("")
    self.question.setStyleSheet("font-size: 20px;")
    
    self.cardVBox.addWidget(self.question)
    
    self.questionVBox.addWidget(self.card, 3)
    self.questionVBox.addWidget(self.showAnswer, alignment=Qt.AlignmentFlag.AlignBottom)
  
  def revealAnswer(self):
    self.questionVBox.removeWidget(self.card)
    self.questionVBox.removeWidget(self.showAnswer)
    self.answer = QLabel(self.cards[self.i]["answer"], alignment=Qt.AlignmentFlag.AlignCenter)
    self.answer.setStyleSheet("font-size: 30px; font-weight: bold")
    self.cardVBox.addWidget(self.answer)
    
    self.questionVBox.addWidget(self.card, 3)
    self.questionVBox.addWidget(self.right, alignment=Qt.AlignmentFlag.AlignBottom)
    self.questionVBox.addWidget(self.wrong, alignment=Qt.AlignmentFlag.AlignBottom)

  def handleRight(self):
    self.cards[self.i]["level"] += 1
    self.cards[self.i]["practiced"] = True
    print('right')
    self.i += 1
    self.nextQ()

  def handleWrong(self):
    self.cards[self.i]["level"] = 1
    self.cards[self.i]["practiced"] = True
    print('wrong')
    self.i += 1
    self.nextQ()
