from PySide6.QtCore import *
from PySide6.QtWidgets import *

class TestCards(QWidget):
  def __init__(self, title):
    super().__init__()

    self.central_widget = QStackedWidget()
    self.setCentralWidget(self.central_widget)

    self.setWindowTitle("testing")