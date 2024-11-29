import sys

from main_window import MainWindow
from info import Info
from display import Display
from PySide6.QtGui import QIcon
from PySide6.QtWidgets import QApplication
from variables import WINDOW_LOGO_PATH
from styles import setupTheme
from buttons import ButtonsGrid

if __name__ == '__main__':
    # Cria a aplicação
    app = QApplication(sys.argv)
    setupTheme(app)
    window = MainWindow()

    # Define o ícone
    icon = QIcon(str(WINDOW_LOGO_PATH))
    window.setWindowIcon(icon)
    app.setWindowIcon(icon)
    
    # Info: Label que mostra a equação
    info = Info('')
    # Adiciona o info ao layout vertical
    window.addWidgetToVLayout(info)

    # Display: QLineEdit que mostra o resultado
    display = Display()
    # Adiciona o display ao layout vertical
    window.addWidgetToVLayout(display)

    # GRID: Grid de botões
    buttonsGrid = ButtonsGrid(display,info,window)
    # Adiciona o grid ao layout vertical
    window.vLayout.addLayout(buttonsGrid)

    # Executa tudo
    window.adjustFixedSize()
    window.show()
    app.exec()