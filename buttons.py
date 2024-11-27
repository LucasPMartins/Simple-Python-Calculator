from PySide6.QtWidgets import QPushButton, QGridLayout
from PySide6.QtCore import Slot
from variables import MEDIUM_FONT_SIZE
from utils import IsNumOrDot, IsValidNumber

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from display import Display
    from main_window import MainWindow
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
    def __init__(self, display:'Display',info:'Info',window:'MainWindow',*args, **kwargs):
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
        self.window = window
        self._equation = ''
        self._left = None
        self._right = None
        self._op = None
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
                    self._configSpecialButton(button)
                    font = button.font()
                    if button_text in 'C⌫':
                        font.setPixelSize(26)
                    if button_text in '÷-':
                        font.setPixelSize(30)
                    else:
                        font.setPixelSize(28)
                    font.setBold(True)
                    button.setFont(font)
                # Verifica se o próximo elemento existe e é igual ao atual
                if j + 1 < len(row) and row[j] == row[j + 1]:
                    # Botão ocupa duas colunas (columnSpan = 2)
                    self.addWidget(button, i, j, 1, 2)
                    j += 1  # Pula o próximo índice já que foi tratado
                # Botão padrão
                self.addWidget(button, i, j)
                slot = self._makeSlot(self._insertButtonTextToDisplay,button)
                self._connectButtonClicked(button,slot)
                j += 1  # Incrementa para o próximo índice
                
    def _connectButtonClicked(self,button,slot):
        button.clicked.connect(slot)

    def _configSpecialButton(self,button):
        text = button.text()
        if text in '⌫':
            self._connectButtonClicked(
                button, self.display.backspace)
        if text == 'C':
            # button.clicked.connect(self.display.clear)
            # slot = self._makeSlot(self.display.clear)
            self._connectButtonClicked(button,self._clear)
        if text in '+-÷×^':
            self._connectButtonClicked(
                button,
                self._makeSlot(self._operatorClicked, button)
                )
        if text in '=':
            self._connectButtonClicked(
                button, self._eq)
        

    def _makeSlot(self,func,*args,**kwargs):
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

    def _clear (self):
        self._left = None
        self._right = None
        self._op = None
        self.equation = ''
        self.display.clear()

    def _operatorClicked(self, button):
        buttonText = button.text() # operadores
        displayText = self.display.text() # número da esquerda (_left)
        self.display.clear() # limpa o display

        if not IsValidNumber(displayText) and self._left is None:
            self._showError('A valid number is necessary!')
            return

        if self._left is None:
            self._left = float(displayText)

        self._op = buttonText
        self.equation = f'{self._left} {self._op}'
    
    def _eq(self):
        displayText = self.display.text()

        if not IsValidNumber(displayText):
            self._showError('A valid number is necessary!')
            return
        if self._left == None:
            self._showError('The left number and the operator is missing!')
            return

        self._right = float(displayText)
        self.equation = f'{self._left} {self._op} {self._right}'

        operation = 0.0
        if self._op == '+':
            operation = self._left + self._right
        elif self._op == '-':
            operation = self._left - self._right
        elif self._op == '÷':
            try:
                operation = self._left / self._right
            except ZeroDivisionError:
                self._showError('Error: Zero division error')
        elif self._op == '×':
            operation = self._left * self._right
        elif self._op == '^':
            try:
                operation = self._left ** self._right
            except OverflowError:
                self._showError('Error: Overflow Error')
        self.display.clear()
        self.display.insert(f"{operation:.5f}".rstrip('0').rstrip('.'))
        self._left = operation

    def _showError(self,text):
        msgBox = self.window.makeMsgBox()
        msgBox.setText(text)
        msgBox.setIcon(msgBox.Icon.Critical)
        msgBox.exec()
        # msgBox.setStandardButtons(
        #     msgBox.StandardButton.Ok |
        #     msgBox.StandardButton.Cancel
        # )
        # result = msgBox.exec()
        # if result == msgBox.StandardButton.Ok:
        #     print('User clicked in OK')
        # elif result == msgBox.StandardButton.Cancel:
        #     print('User clicked in Cancel')