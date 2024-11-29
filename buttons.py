from PySide6.QtWidgets import QPushButton, QGridLayout
from PySide6.QtCore import Slot
from variables import MEDIUM_FONT_SIZE
from utils import IsEmpty, IsNumOrDot, IsValidNumber

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
            ['N',  '0', '.', '='],
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
        self.display.eqPressed.connect(self._eq)
        self.display.delPressed.connect(self._backspace)
        self.display.clearPressed.connect(self._clear)
        self.display.inputPressed.connect(self._insertToDisplay)
        self.display.operatorPressed.connect(self._configOperator)

        for rowNumber, rowData in enumerate(self._gridMask):
            for colNumber, buttonText in enumerate(rowData):
                button = Button(buttonText)

                if not IsNumOrDot(buttonText) and not IsEmpty(buttonText):
                    button.setProperty('cssClass', 'specialButton')
                    self._configSpecialButton(button)

                self.addWidget(button, rowNumber, colNumber)
                slot = self._makeSlot(self._insertToDisplay, buttonText)
                self._connectButtonClicked(button, slot)

    def _connectButtonClicked(self,button,slot):
        button.clicked.connect(slot)

    def _configSpecialButton(self,button):
        text = button.text()
        if text == '⌫':
            self._connectButtonClicked(
                button, self._backspace)
        if text == 'N':
            self._connectButtonClicked(button,self._invertNumber)
        if text == 'C':
            # button.clicked.connect(self.display.clear)
            # slot = self._makeSlot(self.display.clear)
            self._connectButtonClicked(button,self._clear)
        if text in '+-÷×^':
            self._connectButtonClicked(
                button,
                self._makeSlot(self._configOperator, text)
                )
        if text == '=':
            self._connectButtonClicked(
                button, self._eq)

    @Slot()
    def _makeSlot(self,func,*args,**kwargs):
        @Slot(bool)
        def realSlot(_):
            func(*args,**kwargs)
        return realSlot

    @Slot()
    def _invertNumber(self):
        displayText = self.display.text()

        if not IsValidNumber(displayText):
            return
        
        newNumber = float(displayText)
        newNumber *= -1
        if newNumber.is_integer():
            newNumber = int(newNumber)
        self._left = newNumber
        self.display.setText(str(newNumber))
        self.display.setFocus()

    @Slot()
    def _insertToDisplay(self,text):
        newDisplayValue = self.display.text() + text
        # Verifica se o número digitado é válido
        if not IsValidNumber(newDisplayValue):
            return
        # Se o número atual é igual ao número da esquerda, quer dizer então que 
        # o número que está no display é o resultado de uma operação anterior, 
        # então limpa o display
        if IsValidNumber(self.display.text()) and float(self.display.text()) == self._left:
            # Se a equação termina com '=', então limpa a equação, 
            # pois o usuário quer fazer uma nova operação
            if self.equation.endswith('= '):
                self._left = None
                self.equation = ''
            self.display.clear()
        self.display.insert(text)
        self.display.setFocus()
    
    @Slot()
    def _clear (self):
        self._left = None
        self._right = None
        self._op = None
        self.equation = ''
        self.display.clear()
        self.display.setFocus()

    @Slot()
    def _configOperator(self, text):
        displayText = self.display.text()
        if not IsValidNumber(displayText) and self._left is None:
            self._showError('A valid number is necessary!')
            return
        self._op = text
        # Adiciona o operador na equação juntamente com o número da esquerda,
        # se ele for NONE
        if IsValidNumber(displayText) and self._left is None:
            self._left = float(displayText)
        self.equation = f'{self._left} {self._op}'
        self.display.setFocus()

    @Slot()
    def _eq(self):
        displayText = self.display.text()
        # Se o operador for None, então mostra um erro
        if self._op is None:
            self._showError('An operator is necessary!')
            return
        # Se o número da direita não for None e a equação termina com um operador,
        # quer dizer que o usuário quer realizar uma nova operação com o valor que 
        # está no display, para isso, o número da direita é setado como None e 
        # re-setado no if seguinte
        if self._right is not None and self.equation.endswith(('+','-','×','÷','^')):
            self._right = None
        # Se o número da direita for None, 
        # então ele é o número atual que está no display
        if IsValidNumber(displayText) and self._right is None:
            self._right = float(displayText)
        # Se a equação termina com '=' e o usuário usou EnterPressed, então o usuário 
        # que realizar a operação novamente com o resultado da última operação 
        # como o número da esquerda e o número da direita continua o mesmo
        if self.equation.endswith('= '):
            self._left = float(displayText)
        # Se a equação está vazia e o número atual é válido, quer dizer que o usuário
        # quer repetir a última operação com o mesmo número da direta com um novo
        # número da esquerda
        if self.equation == '' and IsValidNumber(displayText):
            self._left = float(displayText)
        
        self.equation = f'{self._left} {self._op} {self._right} = '

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
        self._left = float(f"{operation:.5f}".rstrip('0').rstrip('.'))
        self.display.setFocus()
    
    @Slot()
    def _backspace(self):
        self.display.backspace()
        self.display.setFocus()

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