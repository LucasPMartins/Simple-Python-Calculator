from PySide6.QtWidgets import QPushButton, QGridLayout
from PySide6.QtCore import Slot
from variables import MEDIUM_FONT_SIZE
from utils import IsNumOrDot, IsValidNumber

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from display import Display
    from info import Info


class Button(QPushButton):
    def __init__(self,text: str,*args, **kwargs):
        super().__init__(text,*args, **kwargs)
        self.configStyle()

    def configStyle(self):
        font = self.font()
        # usar setStyleSheet sobrescreve outro setStyleSheet anterior
        # self.setStyleSheet(f'font-size: {SMALL_FONT_SIZE}px')
        font.setPixelSize(MEDIUM_FONT_SIZE)
        self.setFont(font)
        self.setMinimumSize(75, 75)

class ButtonsGrid(QGridLayout):
    def __init__(self, display:'Display',info:'Info',*args, **kwargs):
        super().__init__(*args, **kwargs)
        self._gridMask = [
            ['^', '÷', 'C', '⌫'],
            ['7', '8', '9', '×'],
            ['4', '5', '6', '-'],
            ['1', '2', '3', '+'],
            ['0',  '0', '.', '='],
        ]
        self.display = display
        self.info = info
        self._makeGrid()

    @property
    def equation(self):
        return self._equation
    @equation.setter
    def equation(self, value):
        self._equation = value
        self.info.setText(value)

    def _makeGrid(self):
        for i, row in enumerate(self._gridMask):
            j = 0
            while j < len(row):
                button_text = row[j]
                button = Button(button_text)
                if not IsNumOrDot(button_text):
                    button.setProperty('cssClass','specialButton')
                    font = button.font()
                    if button_text in 'C⌫':
                        font.setPixelSize(26)
                    if button_text in '÷-':
                        font.setPixelSize(30)
                    else:
                        font.setPixelSize(28)
                    font.setBold(True)
                    button.setFont(font)
                    self.addWidget(button, i, j)
                # Verifica se o próximo elemento existe e é igual ao atual
                if j + 1 < len(row) and row[j] == row[j + 1]:
                    # Botão ocupa duas colunas (columnSpan = 2)
                    self.addWidget(button, i, j, 1, 2)
                    j += 1  # Pula o próximo índice já que foi tratado
                # Botão padrão
                self.addWidget(button, i, j)
                buttonSlot = self._makeButtonDisplaySlot(
                    self._insertButtonTextToDisplay,
                    button,
                    )
                button.clicked.connect(buttonSlot)
                j += 1  # Incrementa para o próximo índice
                

    def _makeButtonDisplaySlot(self,func,*args,**kwargs):
        @Slot(bool)
        def realSlot(_):
            func(*args,**kwargs)
        return realSlot

    def _insertButtonTextToDisplay(self,button):
        button_text = button.text()
        newDisplayValue = self.display.text() + button_text

        if not IsValidNumber(newDisplayValue):
            return
            
        self.display.insert(button_text)