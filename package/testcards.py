from PySide6.QtCore import *
from PySide6.QtWidgets import *
import json
import functools

class TestCards(QMainWindow):
  def __init__(self, title):
    super().__init__()

    self.central_widget = QStackedWidget()
    self.setCentralWidget(self.central_widget)
    self.practiceScreen = PracticeScreen(title)
    self.practice = Practice(title)

    self.setWindowTitle(f"Practice {title}")
    self.central_widget.addWidget(self.practiceScreen)
    self.central_widget.addWidget(self.practice)
  
    self.central_widget.setCurrentWidget(self.practiceScreen)
    self.practiceScreen.clicked.connect(lambda x: self.startPractice(x))
  
  def startPractice(self, title):
    self.setWindowTitle(f"Practicing {title}...")
    self.central_widget.setCurrentWidget(self.practice)

class PracticeScreen(QWidget):
  clicked = Signal(str)

  def __init__(self, title):
    super().__init__()

    with open('flashcard.json', 'r') as f:
      flashcardList = json.load(f)
    cards: list[dict] = flashcardList[title]
    widget = QWidget()
    gridLayout = QGridLayout(widget)

    self.practiced = functools.reduce(lambda x, y: x + y, list(map(lambda x: int(x["practiced"]), cards)))
    self.practicedLabel = QLabel(f"You have practiced {self.practiced} cards today.", alignment=Qt.AlignCenter)
    self.practicedLabel.setStyleSheet("font-size: 20px; font-weight: bold")
    self.practiceButton = QPushButton("Practice")

    gridLayout.addWidget(self.practicedLabel, 0, 0)
    gridLayout.addWidget(self.practiceButton, 1, 0)

    self.setLayout(gridLayout)
    self.practiceButton.clicked.connect(lambda c=None, t=title: self.clicked.emit(t))


class Practice(QWidget):
  def __init__(self, title):
    super().__init__()

    print(title)