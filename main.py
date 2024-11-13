import sys

from main_window import MainWindow
from info import Info
from display import Display
from PySide6.QtGui import QIcon
from PySide6.QtWidgets import QApplication
from variables import WINDOW_LOGO_PATH
from styles import setupTheme
from buttons import Button

if __name__ == '__main__':
    # Cria a aplicação
    app = QApplication(sys.argv)
    setupTheme(app)
    window = MainWindow()

    # Define o ícone
    icon = QIcon(str(WINDOW_LOGO_PATH))
    window.setWindowIcon(icon)
    app.setWindowIcon(icon)
    # Faz o ícone aparecer na barra de tarefas do Win 11
    if sys.platform.startswith('win'):
        import ctypes
        ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(
            u'CompanyName.ProductName.SubProduct.VersionInformation')

    # Info
    info = Info('2.0 ^ 10.0 = 1024.0')
    window.addToVLayout(info)

    # Display
    display = Display()
    window.addToVLayout(display)

    # Button
    button = Button('Texto do Botão')
    window.addToVLayout(button)

    # Executa tudo
    window.adjustFixedSize()
    window.show()
    app.exec()