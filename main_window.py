from PySide6.QtWidgets import (QMainWindow,QVBoxLayout,QWidget)

class MainWindow(QMainWindow):
    def __init__(self, parent: QWidget | None = None, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)

        # Configurando um layout básico
        self.cw = QWidget()
        self.vLayout = QVBoxLayout()
        self.cw.setLayout(self.vLayout)
        self.setCentralWidget(self.cw)

        # Título da janela
        self.setWindowTitle('Calculator')

    def adjustFixedSize(self):
        # Ultima coisa a ser feita
        self.adjustSize()
        # logo apos a janela se ajustar com o tamanhos dos widgets
        # ela ficará fixa
        self.setFixedSize(self.width(),self.height())

    def addWidgetToVLayout(self, widget: QWidget):
        self.vLayout.addWidget(widget)