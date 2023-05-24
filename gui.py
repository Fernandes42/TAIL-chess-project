import chess
import chess.svg
import sys


from PyQt5.QtSvg import QSvgWidget
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QMainWindow


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setGeometry(100, 100, 1100, 1100)

        self.widgetSvg = QSvgWidget(parent=self)
        self.widgetSvg.setGeometry(10, 10, 900, 900)

        self.chessboard = chess.Board()

        # button = QPushButton("Press Me!")
        # button.setCheckable(True)
        # button.clicked.connect(self.the_button_was_clicked)

        # # Set the central widget of the Window.
        # self.setCentralWidget(button)


        # Set the central widget of the Window.
        self.chessboardSvg = chess.svg.board(self.chessboard).encode("UTF-8")
        self.widgetSvg.load(self.chessboardSvg)

    def the_button_was_clicked(self):
        print("Clicked!")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    app.exec()