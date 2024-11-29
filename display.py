from PySide6.QtWidgets import QLineEdit
from PySide6.QtCore import Qt,Signal
from variables import BIG_FONT_SIZE,TEXT_MARGIN,MiNIMUM_WIDTH
from utils import IsEmpty,IsNumOrDot

class Display(QLineEdit):
    eqPressed = Signal()
    delPressed = Signal()
    clearPressed = Signal()
    inputPressed = Signal(str)
    operatorPressed = Signal(str)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.configStyle()

    def configStyle(self):
        self.setStyleSheet(f'font-size: {BIG_FONT_SIZE}px')
        self.setMinimumHeight(BIG_FONT_SIZE * 2)
        self.setMinimumWidth(MiNIMUM_WIDTH)
        self.setAlignment(Qt.AlignmentFlag.AlignRight)
        self.setTextMargins(*[TEXT_MARGIN for _ in range(4)])

    def keyPressEvent(self, event):
        text = event.text().strip()
        key = event.key()
        KEYS = Qt.Key

        isEnter = key in [KEYS.Key_Enter,KEYS.Key_Return,KEYS.Key_Equal]
        isDelete = key in [KEYS.Key_Delete,KEYS.Key_Backspace]
        isEsc = key in [KEYS.Key_Escape,KEYS.Key_C]
        IsOperator = key in [
            KEYS.Key_Plus,KEYS.Key_Minus,KEYS.Key_Asterisk,KEYS.Key_Slash,
            KEYS.Key_P
        ]

        if isEnter:
            self.eqPressed.emit()
            return event.ignore()
        elif isDelete or text == '⌫':
            self.delPressed.emit()
            return event.ignore()
        elif isEsc:
            self.clearPressed.emit()
            return event.ignore()
        elif IsOperator:
            if text.lower() == 'p':
                text = '^'
            if text.lower() == '/':
                text = '÷'
            if text.lower() == '*':
                text = '×'
            self.operatorPressed.emit(text)
            return event.ignore()
        
        if IsEmpty(text):
            return event.ignore()

        if IsNumOrDot(text):
            self.inputPressed.emit(text)
            return event.accept()
