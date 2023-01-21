from __future__ import annotations
import sys

from typing import Optional
from operator import add, sub, mul, truediv

from PySide6.QtWidgets import QApplication, QMainWindow
from PySide6.QtGui import QFontDatabase
from typing import Union, Optional
from calculation import Ui_MainWindow

operators = {
    '+': add,
    '-': sub,
    '*': mul,
    '/': truediv,
}

default_font_size = 16
default_entry_font_size = 40

error_div_zerro = "ZeroDivisionError"
error_underfined = "Result is underfined!"

class Calculator(QMainWindow):
    def __init__(self):
        super(Calculator, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.entry_max_len = self.ui.le_entry.maxLength()

        #digit
        self.ui.btn_0.clicked.connect(self.add_digit)
        self.ui.btn_1.clicked.connect(self.add_digit)
        self.ui.btn_2.clicked.connect(self.add_digit)
        self.ui.btn_3.clicked.connect(self.add_digit)
        self.ui.btn_4.clicked.connect(self.add_digit)
        self.ui.btn_5.clicked.connect(self.add_digit)
        self.ui.btn_6.clicked.connect(self.add_digit)
        self.ui.btn_7.clicked.connect(self.add_digit)
        self.ui.btn_8.clicked.connect(self.add_digit)
        self.ui.btn_9.clicked.connect(self.add_digit)

        #action
        self.ui.btn_clear.clicked.connect(self.clear_all)
        self.ui.btn_del.clicked.connect(self.clear_entry)
        self.ui.btn_dot.clicked.connect(self.add_dot)
        self.ui.btn_neg.clicked.connect(self.negative)
        self.ui.btn_backspace.clicked.connect(self.backspace)

        #math
        self.ui.btn_enter.clicked.connect(self.calculation)
        self.ui.btn_plus.clicked.connect(self.math_operation)
        self.ui.btn_sub.clicked.connect(self.math_operation)
        self.ui.btn_multy.clicked.connect(self.math_operation)
        self.ui.btn_div.clicked.connect(self.math_operation)

    def adjust_entry_font_size(self) -> None:
        font_size = default_entry_font_size
        while self.get_entry_text_width() > self.ui.le_entry.width() - 15:
            font_size -= 1
            self.ui.le_entry.setStyleSheet('font-size: ' + str(font_size) + 'pt; border: none;')

        font_size = 1
        while self.get_entry_text_width() < self.ui.le_entry.width() - 60:
            font_size += 1
            if font_size > default_entry_font_size:
                break
            self.ui.le_entry.setStyleSheet('font-size: ' + str(font_size) + 'pt; border: none;')

    def adjust_temp_font_size(self) -> None:
        font_size = default_font_size
        while self.get_temp_text_width() > self.ui.lbl_temp.width() - 10:
            font_size -= 1
            self.ui.lbl_temp.setStyleSheet(
                'font-size: ' + str(font_size) + 'pt; color: #808080;')
        font_size = 1
        while self.get_temp_text_width() < self.ui.lbl_temp.width() - 60:
            font_size += 1
            if font_size > default_font_size:
                break
            self.ui.lbl_temp.setStyleSheet('font-size: ' + str(font_size) + 'pt; color: #808080;')
    def add_digit(self):
        self.remove_error()
        self.clear_temp()
        btn = self.sender()
        digit_buttons = ('btn_0', 'btn_1', 'btn_2', 'btn_3', 'btn_4',
                         'btn_5', 'btn_6', 'btn_7', 'btn_8', 'btn_9')
        if btn.objectName() in digit_buttons:
            if self.ui.le_entry.text() == '0':
                self.ui.le_entry.setText(btn.text())
            else:
                self.ui.le_entry.setText(self.ui.le_entry.text() + btn.text())
        self.adjust_entry_font_size()

    def add_dot(self) -> None:
        self.clear_temp()
        if '.' not in self.ui.le_entry.text():
            self.ui.le_entry.setText(self.ui.le_entry.text() + '.')
            self.adjust_entry_font_size()

    def clear_all(self) -> None:
        self.remove_error()
        self.ui.le_entry.setText('0')
        self.ui.lbl_temp.clear()
        self.adjust_temp_font_size()

    def clear_entry(self) -> None:
        self.remove_error()
        self.ui.le_entry.setText('0')
        self.adjust_entry_font_size()

    def backspace(self) -> None:
        self.remove_error()
        self.clear_temp()
        entry = self.ui.le_entry.text()

        if len(entry) != 1:
            if len(entry) == 2 and '-' in entry:
                self.ui.le_entry.setText('0')
            else:
                self.ui.le_entry.setText(entry[:-1])
        else:
            self.ui.le_entry.setText('0')
        self.adjust_entry_font_size()

    def negative (self):
        self.clear_temp()
        entry =  self.ui.le_entry.text()
        if entry != '0' and '-' not in entry:
            entry = '-' + entry
        else:
            entry = entry[1:]

        if len(entry) == self.entry_max_len + 1 and '-' in entry:
            self.ui.le_entry.setMaxLength(self.entry_max_len + 1)
        else:
            self.ui.le_entry.setMaxLength(self.entry_max_len)
        self.ui.le_entry.setText(entry)
        self.adjust_entry_font_size()

    def clear_temp(self) -> None:
        if self.get_math_sign() == '=':
            self.ui.lbl_temp.clear()
            self.adjust_temp_font_size()

    @staticmethod
    def rem_zeroes(num: str) -> str:
        n = str(float(num))
        return n[:-2] if n[-2:] == '.0' else n

    def add_temp(self) -> None:
        btn = self.sender()
        entry = self.rem_zeroes(self.ui.le_entry.text())
        if not self.ui.lbl_temp.text() or self.get_math_sign() == '=':
            self.ui.lbl_temp.setText(entry  + f' {btn.text()} ')
            self.adjust_temp_font_size()
            self.ui.le_entry.setText('0')
            self.adjust_entry_font_size()

    def get_entry_num(self) -> int | float:
        entry = self.ui.le_entry.text().strip('.')
        return  float(entry) if '.' in entry else int(entry)

    def get_temp_num(self) -> int | float | None:
        if self.ui.lbl_temp.text():
            temp = self.ui.lbl_temp.text().strip('.').split()[0]
            return float(temp) if '.' in temp else int(temp)

    def get_math_sign (self) -> Optional[str]:
        if self.ui.lbl_temp.text():
            return self.ui.lbl_temp.text().strip('.').split()[-1]

    def get_entry_text_width(self) -> int:
        return self.ui.le_entry.fontMetrics().boundingRect(self.ui.le_entry.text()).width()

    def get_temp_text_width(self) -> int:
        return self.ui.lbl_temp.fontMetrics().boundingRect(self.ui.lbl_temp.text()).width()

    #operations
    def calculation(self) -> str:
        entry = self.ui.le_entry.text()
        temp = self.ui.lbl_temp.text()
        if temp:
            try:
                result = self.rem_zeroes(
                    str(operators[self.get_math_sign()](self.get_temp_num(), self.get_entry_num()))
                )
                self.ui.lbl_temp.setText(temp + self.rem_zeroes(entry) + ' =')
                self.adjust_temp_font_size()
                self.ui.le_entry.setText(result)
                self.adjust_entry_font_size()
                return result
            except KeyError:
                pass
            except ZeroDivisionError:
                if self.get_temp_num() == 0:
                    self.show_error(error_underfined)
                else:
                    self.show_error(error_div_zerro)

    def math_operation(self) -> None:
        btn = self.sender()
        temp = self.ui.lbl_temp.text()
        if not temp:
            self.add_temp()
        elif self.get_math_sign() != btn.text():
            if self.get_math_sign() == '=':
                self.add_temp()
            else:
                self.ui.lbl_temp.setText(temp[:-2] + f'{btn.text()}')
        else:
            self.ui.lbl_temp.setText(self.calculation() + f' {btn.text}')

        self.adjust_temp_font_size()

    def show_error(self, text: str) -> None:
        self.ui.le_entry.setMaxLength(len(text))
        self.ui.le_entry.setText(text)
        self.adjust_entry_font_size()
        self.lock_buttons(True)

    def remove_error(self) -> None:
        if self.ui.le_entry.text() in (error_underfined, error_div_zerro):
            self.ui.le_entry.setMaxLength(self.entry_max_len)
            self.ui.le_entry.setText('0')
            self.lock_buttons(False)

    def lock_buttons(self, flag: bool) -> None:
        self.ui.btn_plus.setDisabled(flag)
        self.ui.btn_sub.setDisabled(flag)
        self.ui.btn_div.setDisabled(flag)
        self.ui.btn_multy.setDisabled(flag)
        self.ui.btn_neg.setDisabled(flag)
        self.ui.btn_dot.setDisabled(flag)
        self.ui.btn_enter.setDisabled(flag)

        color = 'color: #808080;' if flag else 'color: white;'
        self.change_buttons_color(color)

    def change_buttons_color(self, css_color: str) -> None:
        self.ui.btn_plus.setStyleSheet(css_color)
        self.ui.btn_sub.setStyleSheet(css_color)
        self.ui.btn_div.setStyleSheet(css_color)
        self.ui.btn_multy.setStyleSheet(css_color)
        self.ui.btn_neg.setStyleSheet(css_color)
        self.ui.btn_dot.setStyleSheet(css_color)
        self.ui.btn_enter.setStyleSheet(css_color)

    def resizeEvent(self, event) -> None:
        self.adjust_entry_font_size()
        self.adjust_temp_font_size()


if __name__ == "__main__":
    app = QApplication(sys.argv)

    window = Calculator()
    window.show()

    sys.exit(app.exec())

