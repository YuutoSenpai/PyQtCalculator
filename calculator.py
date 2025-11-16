import os
import sys

# ŘEŠENÍ PROBLÉMU S QT PLUGINS - musí být na úplném začátku!
os.environ['QT_QPA_PLATFORM_PLUGIN_PATH'] = os.path.join(
    os.path.dirname(__file__), '.venv', 'Lib', 'site-packages', 'PyQt5', 'Qt5', 'plugins'
)

import math
from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout,
                             QHBoxLayout, QGridLayout, QLineEdit, QPushButton,
                             QListWidget, QLabel, QMessageBox)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont


class Calculator(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()
        self.history = []
        self.current_input = ""
        self.reset_on_next_input = False
        self.degrees_mode = True  # True = stupně, False = radiány

    def initUI(self):
        self.setWindowTitle('🎯 PyQt Kalkulačka')
        self.setFixedSize(500, 650)
        self.setStyleSheet("""
            QMainWindow {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                    stop:0 #2c3e50, stop:1 #34495e);
            }
            QLineEdit {
                background: #ecf0f1;
                border: 2px solid #bdc3c7;
                border-radius: 10px;
                padding: 10px;
                font-size: 18px;
                color: #2c3e50;
            }
            QPushButton {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #3498db, stop:1 #2980b9);
                border: none;
                border-radius: 8px;
                color: white;
                font-weight: bold;
                min-height: 40px;
            }
            QPushButton:hover {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #5dade2, stop:1 #3498db);
            }
            QPushButton:pressed {
                background: #2471a3;
            }
            QPushButton#equals {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #27ae60, stop:1 #229954);
            }
            QPushButton#advanced {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #e74c3c, stop:1 #c0392b);
            }
            QListWidget {
                background: #ecf0f1;
                border: 2px solid #bdc3c7;
                border-radius: 10px;
                padding: 5px;
                font-size: 12px;
                color: #2c3e50;
            }
            QLabel {
                color: #ecf0f1;
                font-weight: bold;
            }

            /* STYLY PRO ERROR DIALOGY */
            QMessageBox {
                background: #ecf0f1;
            }
            QMessageBox QLabel {
                color: #2c3e50;
                font-weight: normal;
                font-size: 14px;
            }
            QMessageBox QPushButton {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #3498db, stop:1 #2980b9);
                color: white;
                padding: 8px 15px;
                border-radius: 5px;
                font-weight: bold;
            }
            QMessageBox QPushButton:hover {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #5dade2, stop:1 #3498db);
            }
        """)

        # Hlavní widget a layout
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout(central_widget)
        main_layout.setSpacing(10)
        main_layout.setContentsMargins(15, 15, 15, 15)

        # Režim kalkulačky (stupně/radiány)
        mode_layout = QHBoxLayout()
        self.mode_label = QLabel("🌡️ Režim: Stupně")
        self.mode_label.setAlignment(Qt.AlignRight)
        self.mode_label.setStyleSheet("font-size: 14px; color: #f39c12;")
        mode_layout.addWidget(self.mode_label)
        main_layout.addLayout(mode_layout)

        # Display pro zadávání
        self.display = QLineEdit()
        self.display.setFont(QFont('Arial', 20, QFont.Bold))
        self.display.setAlignment(Qt.AlignRight)
        self.display.setReadOnly(False)
        self.display.setPlaceholderText("Zadejte výraz...")
        self.display.textChanged.connect(self.on_display_changed)
        main_layout.addWidget(self.display)

        # Tlačítka pro základní operace
        basic_buttons_layout = QGridLayout()
        basic_buttons_layout.setSpacing(8)
        basic_buttons_layout.setContentsMargins(0, 10, 0, 10)

        # Číselná tlačítka a základní operace
        buttons = [
            ('7', 0, 0), ('8', 0, 1), ('9', 0, 2), ('/', 0, 3),
            ('4', 1, 0), ('5', 1, 1), ('6', 1, 2), ('*', 1, 3),
            ('1', 2, 0), ('2', 2, 1), ('3', 2, 2), ('-', 2, 3),
            ('0', 3, 0), ('.', 3, 1), ('=', 3, 2), ('+', 3, 3),
            ('C', 4, 0), ('(', 4, 1), (')', 4, 2), ('DEL', 4, 3)
        ]

        for text, row, col in buttons:
            button = QPushButton(text)
            button.setFont(QFont('Arial', 14, QFont.Bold))
            button.clicked.connect(self.on_button_click)

            # Speciální styl pro =
            if text == '=':
                button.setObjectName('equals')
            elif text in ['C', 'DEL']:
                button.setStyleSheet("""
                    QPushButton {
                        background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                            stop:0 #e74c3c, stop:1 #c0392b);
                    }
                """)

            basic_buttons_layout.addWidget(button, row, col)

        main_layout.addLayout(basic_buttons_layout)

        # Pokročilé funkce
        advanced_label = QLabel("🎛️ Pokročilé funkce")
        advanced_label.setStyleSheet("color: #f39c12; font-weight: bold; font-size: 14px;")
        main_layout.addWidget(advanced_label)

        advanced_buttons_layout = QGridLayout()
        advanced_buttons_layout.setSpacing(6)

        advanced_buttons = [
            ('sin', 0, 0), ('cos', 0, 1), ('tan', 0, 2),
            ('log', 1, 0), ('e^x', 1, 1), ('%', 1, 2),
            ('π', 2, 0), ('Deg/Rad', 2, 1)
        ]

        for text, row, col in advanced_buttons:
            button = QPushButton(text)
            button.setFont(QFont('Arial', 11, QFont.Bold))
            button.clicked.connect(self.on_advanced_button_click)
            button.setObjectName('advanced')
            advanced_buttons_layout.addWidget(button, row, col)

        main_layout.addLayout(advanced_buttons_layout)

        # Historie výpočtů
        history_label = QLabel("📜 Historie výpočtů:")
        history_label.setStyleSheet("color: #f39c12; font-weight: bold; font-size: 14px; margin-top: 10px;")
        main_layout.addWidget(history_label)

        self.history_list = QListWidget()
        self.history_list.setMaximumHeight(120)
        self.history_list.itemDoubleClicked.connect(self.on_history_item_double_click)
        main_layout.addWidget(self.history_list)

    def on_display_changed(self):
        """Ošetření vstupu z klávesnice"""
        text = self.display.text()

        # Ošetření více desetinných teček v jednom čísle
        parts = text.split()
        for part in parts:
            if part.count('.') > 1:
                # Najdi poslední tečku a odstran ji
                cleaned = part.rsplit('.', 1)[0] + part.rsplit('.', 1)[1]
                text = text.replace(part, cleaned)
                self.display.setText(text)
                self.display.setCursorPosition(len(text))
                break

    def on_button_click(self):
        button = self.sender()
        text = button.text()

        if self.reset_on_next_input and text not in ['+', '-', '*', '/']:
            self.display.clear()
            self.reset_on_next_input = False

        if text == '=':
            self.calculate()
        elif text == 'C':
            self.display.clear()
        elif text == 'DEL':
            current_text = self.display.text()
            self.display.setText(current_text[:-1])
        else:
            current_text = self.display.text()
            self.display.setText(current_text + text)

    def on_advanced_button_click(self):
        button = self.sender()
        text = button.text()
        current_text = self.display.text()

        if self.reset_on_next_input:
            self.display.clear()
            self.reset_on_next_input = False

        if text == 'sin':
            try:
                value = self.evaluate_expression(current_text)
                if self.degrees_mode:
                    value = math.radians(value)
                result = math.sin(value)
                # Zaokrouhlení na 10 desetinných míst pro lepší zobrazení
                result_rounded = round(result, 10)
                self.add_to_history(f"sin({current_text}) = {result_rounded}")
                self.display.setText(str(result_rounded))
                self.reset_on_next_input = True
            except Exception as e:
                self.show_error("Chyba ve výpočtu sin")

        elif text == 'cos':
            try:
                value = self.evaluate_expression(current_text)
                if self.degrees_mode:
                    value = math.radians(value)
                result = math.cos(value)
                result_rounded = round(result, 10)
                self.add_to_history(f"cos({current_text}) = {result_rounded}")
                self.display.setText(str(result_rounded))
                self.reset_on_next_input = True
            except Exception as e:
                self.show_error("Chyba ve výpočtu cos")

        elif text == 'tan':
            try:
                value = self.evaluate_expression(current_text)
                if self.degrees_mode:
                    value = math.radians(value)
                result = math.tan(value)
                result_rounded = round(result, 10)
                self.add_to_history(f"tan({current_text}) = {result_rounded}")
                self.display.setText(str(result_rounded))
                self.reset_on_next_input = True
            except Exception as e:
                self.show_error("Chyba ve výpočtu tan")

        elif text == 'log':
            try:
                value = self.evaluate_expression(current_text)
                if value <= 0:
                    self.show_error("Logaritmus lze počítat pouze z kladných čísel")
                    return
                result = math.log10(value)
                result_rounded = round(result, 10)
                self.add_to_history(f"log({current_text}) = {result_rounded}")
                self.display.setText(str(result_rounded))
                self.reset_on_next_input = True
            except Exception as e:
                self.show_error("Chyba ve výpočtu logaritmu")

        elif text == 'e^x':
            try:
                value = self.evaluate_expression(current_text)
                result = math.exp(value)
                result_rounded = round(result, 10)
                self.add_to_history(f"e^({current_text}) = {result_rounded}")
                self.display.setText(str(result_rounded))
                self.reset_on_next_input = True
            except Exception as e:
                self.show_error("Chyba ve výpočtu exponenciály")

        elif text == '%':
            try:
                if not current_text:
                    return

                value = self.evaluate_expression(current_text)
                result = value / 100
                result_rounded = round(result, 10)

                if any(op in current_text for op in ['+', '-', '*', '/']):
                    self.add_to_history(f"({current_text})% = {result_rounded}")
                else:
                    self.add_to_history(f"{current_text}% = {result_rounded}")

                self.display.setText(str(result_rounded))
                self.reset_on_next_input = True

            except Exception as e:
                self.show_error("Chyba ve výpočtu procent")

        elif text == 'π':
            if current_text and not current_text[-1] in ['+', '-', '*', '/', '(']:
                self.display.setText(current_text + '*' + str(math.pi))
            else:
                self.display.setText(current_text + str(math.pi))

        elif text == 'Deg/Rad':
            self.degrees_mode = not self.degrees_mode
            self.mode_label.setText("Režim: Stupně" if self.degrees_mode else "Režim: Radiány")

    def evaluate_expression(self, expression):
        """Bezpečné vyhodnocení matematického výrazu"""
        try:
            # Bezpečné vyhodnocení - povolujeme pouze matematické operace
            allowed_chars = set('0123456789.+-*/() ')
            if not all(c in allowed_chars for c in expression):
                raise ValueError("Neplatné znaky ve výrazu")

            # Nahrazení implicitního násobení např. 2(3+4) za 2*(3+4)
            expression = self.add_multiplication_operators(expression)

            # Vyhodnocení s prioritou operací
            result = self.evaluate_with_parentheses(expression)
            return float(result)
        except Exception as e:
            raise ValueError(f"Chyba ve výrazu: {str(e)}")

    def add_multiplication_operators(self, expression):
        """Přidá operátory násobení tam, kde chybí (např. 2(3) -> 2*(3))"""
        result = []
        for i in range(len(expression)):
            result.append(expression[i])
            if i < len(expression) - 1:
                current = expression[i]
                next_char = expression[i + 1]
                if (current.isdigit() and next_char == '(') or (current == ')' and next_char.isdigit()):
                    result.append('*')
        return ''.join(result)

    def evaluate_with_parentheses(self, expression):
        """Vyhodnocení výrazu s podporou závorek"""

        def evaluate_simple(expr):
            """Vyhodnocení výrazu bez závorek"""
            # Rozdělení na čísla a operátory
            import re
            tokens = re.findall(r'[+\-*/]|\d+\.?\d*', expr)

            if not tokens:
                return 0

            # První fáze: násobení a dělení
            i = 1
            while i < len(tokens):
                if tokens[i] == '*':
                    result = float(tokens[i - 1]) * float(tokens[i + 1])
                    tokens[i - 1:i + 2] = [str(result)]
                elif tokens[i] == '/':
                    if float(tokens[i + 1]) == 0:
                        raise ZeroDivisionError("Dělení nulou")
                    result = float(tokens[i - 1]) / float(tokens[i + 1])
                    tokens[i - 1:i + 2] = [str(result)]
                else:
                    i += 2

            # Druhá fáze: sčítání a odčítání
            result = float(tokens[0])
            i = 1
            while i < len(tokens):
                if tokens[i] == '+':
                    result += float(tokens[i + 1])
                elif tokens[i] == '-':
                    result -= float(tokens[i + 1])
                i += 2

            return result

        # Zpracování závorek
        while '(' in expression:
            start = expression.rfind('(')
            end = expression.find(')', start)
            if end == -1:
                raise ValueError("Chybějící uzavírací závorka")

            sub_expr = expression[start + 1:end]
            sub_result = evaluate_simple(sub_expr)
            expression = expression[:start] + str(sub_result) + expression[end + 1:]

        return evaluate_simple(expression)

    def calculate(self):
        try:
            expression = self.display.text()
            if not expression:
                return

            result = self.evaluate_expression(expression)

            # Přidání do historie
            self.add_to_history(f"{expression} = {result}")

            # Zobrazení výsledku
            self.display.setText(str(result))
            self.reset_on_next_input = True

        except ZeroDivisionError:
            self.show_error("Dělení nulou není povoleno")
            self.display.clear()
            self.reset_on_next_input = False
        except Exception as e:
            error_msg = str(e)
            # Zjednodušení chybové zprávy
            if "Dělení nulou" in error_msg:
                self.show_error("Dělení nulou není povoleno")
            elif "Neplatné znaky" in error_msg:
                self.show_error("Výraz obsahuje neplatné znaky")
            elif "Chybějící uzavírací závorka" in error_msg:
                self.show_error("Chybějící uzavírací závorka")
            else:
                self.show_error("Chyba ve výrazu")
            self.display.clear()
            self.reset_on_next_input = False

    def add_to_history(self, item):
        """Přidá položku do historie s lepším formátováním"""
        # Zaokrouhlit čísla v historii na rozumný počet desetinných míst
        if '=' in item:
            parts = item.split('=')
            expression = parts[0].strip()
            result_str = parts[1].strip()

            try:
                result_num = float(result_str)
                # Pokud je číslo celé, zobrazit bez desetinných míst
                if result_num == int(result_num):
                    formatted_result = str(int(result_num))
                else:
                    # Zaokrouhlit na 6 desetinných míst
                    formatted_result = f"{result_num:.6f}".rstrip('0').rstrip('.')

                formatted_item = f"{expression} = {formatted_result}"
                self.history.append(formatted_item)
                self.history_list.addItem(formatted_item)
            except:
                # Pokud se nepodaří převést na číslo, použít původní formát
                self.history.append(item)
                self.history_list.addItem(item)
        else:
            self.history.append(item)
            self.history_list.addItem(item)

        # Udržuj historii na rozumné velikosti
        if len(self.history) > 50:
            self.history.pop(0)
            self.history_list.takeItem(0)

    def on_history_item_double_click(self, item):
        """Přenese vybranou položku z historie do displaye"""
        text = item.text()
        # Pokud obsahuje '=', vezme část za rovnítkem (výsledek)
        if '=' in text:
            result = text.split('=')[1].strip()
            self.display.setText(result)
        else:
            self.display.setText(text)

    def show_error(self, message):
        """Zobrazí chybovou zprávu"""
        QMessageBox.warning(self, "Chyba", message)
        self.display.clear()
        self.reset_on_next_input = False


def main():
    app = QApplication(sys.argv)
    calculator = Calculator()
    calculator.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()