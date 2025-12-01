import re

import keyword

import logging

from PyQt5.QtGui import QFont, QColor
from PyQt5.QtCore import QObject

from PyQt5.Qsci import QsciLexerCustom

from utilities.settings.essential_settings import DEBUGGING_MODE

import pkgutil
import builtins

logging.basicConfig(
    level=logging.DEBUG, 
    format="%(levelname)s on %(asctime)s in %(filename)s; %(message)s", 
    datefmt="%d/%m/%Y, %I:%M:%S %p"
)


class PythonLexer(QsciLexerCustom):
    def __init__(self, parent: QObject | None = ...) -> None:
        super(PythonLexer, self).__init__(parent)

        self.setDefaultColor(QColor("#000000"))
        self.setDefaultPaper(QColor("#f91d1c1c"))
        self.setDefaultFont(QFont("Consolas", 14))

        self.REGULAR_STYLE_ID = 0
        self.KEYWORD_STYLE_ID = 1
        self.FUNCTION_STYLE_ID = 2
        self.COMMENT_STYLE_ID = 3
        self.OPERATOR_STYLE_ID = 4
        self.BRACKETS_STYLE_ID = 5
        self.MODULE_STYLE_ID = 6

        self.ARITHMETIC_OPERATORS = ["+", "-", "*", "/", "//", "**", "%", "="]
        self.BITWISE_OPERATORS = ["&", "|", "^", "~", "<<", ">>"]
        self.CONDITIONAL_OPERATORS = ["==", "!=", "<=", ">="]

        self.BRACKETS = ["(", ")", "{", "}", "[", "]"]

        self.ALL_OPERATIONS = self.ARITHMETIC_OPERATORS \
        + self.CONDITIONAL_OPERATORS \
        + self.BITWISE_OPERATORS

        self.MODULES_INSTALLED_ON_COMPUTER = [module.name for module in pkgutil.iter_modules()]

        self.BUILT_IN_FUNCTIONS = dir(builtins)

        self.setColor(QColor("#FFFFFF"), self.REGULAR_STYLE_ID)
        self.setColor(QColor("#0000FF"), self.KEYWORD_STYLE_ID)
        self.setColor(QColor("#FF0000"), self.FUNCTION_STYLE_ID)
        self.setColor(QColor("#00FF00"), self.COMMENT_STYLE_ID)
        self.setColor(QColor("#FF8000"), self.OPERATOR_STYLE_ID)
        self.setColor(QColor("#FF00FF"), self.BRACKETS_STYLE_ID)
        self.setColor(QColor("#FFBF00"), self.MODULE_STYLE_ID)

        self.setFont(QFont("Consolas", 14, weight=QFont.Bold), self.REGULAR_STYLE_ID)
        self.setFont(QFont("Consolas", 14, weight=QFont.Bold), self.KEYWORD_STYLE_ID)
        self.setFont(QFont("Consolas", 14, weight=QFont.Bold), self.COMMENT_STYLE_ID)
        self.setFont(QFont("Consolas", 14, weight=QFont.Bold), self.FUNCTION_STYLE_ID)
        self.setFont(QFont("Consolas", 14, weight=QFont.Bold), self.OPERATOR_STYLE_ID)
        self.setFont(QFont("Consolas", 14, weight=QFont.Bold), self.BRACKETS_STYLE_ID)
        self.setFont(QFont("Consolas", 14, weight=QFont.Bold), self.MODULE_STYLE_ID)

    def console_debug(self, message):
        if DEBUGGING_MODE:
            logging.debug(message)

    def description(self, style: int) -> str:
        if style == self.REGULAR_STYLE_ID:
            return "regular_style"
        elif style == self.KEYWORD_STYLE_ID:
            return "keyword_style"
        elif style == self.FUNCTION_STYLE_ID:
            return "function_style"
        elif style == self.COMMENT_STYLE_ID:
            return "comment_style"
        elif style == self.OPERATOR_STYLE_ID:
            return "operator_style"
        elif style == self.BRACKETS_STYLE_ID:
            return "brackets_style"
        elif style == self.MODULE_STYLE_ID:
            return "module_style"
        else:
            return ""

    def styleText(self, start: int, end: int) -> None:
        self.startStyling(start)

        # ! CHANGE IF ORIGINAL VARIABLE [code_editor.py] WAS CHANGED.
        text = self.parent().document.text()[start:end]

        regex_statement_for_syntax_highlighting = re.compile(r"\s+|\w+|\W")

        # TODO Add regex statements for other statements.
        # regex_statement_for_strings = re.compile("\".*\"")
        # regex_statement_for_type_strings = re.compile(".+?\".*\"")

        # regex_statement_for_functions = re.compile(r"def \w+\(\)")
        # regex_statement_for_comments = re.compile(r"#.+")
        # regex_statement_for_decorators = re.compile(r"@\w+")

        tokens_for_syntax_highlighting = [
            (token, len(bytearray(token, "utf-8"))) \
            for token in regex_statement_for_syntax_highlighting.findall(text)
        ]

        for token in tokens_for_syntax_highlighting:
            if token[0] in list(keyword.kwlist):
                self.setStyling(token[1], self.KEYWORD_STYLE_ID)
            elif token[0] in self.ALL_OPERATIONS:
                self.setStyling(token[1], self.OPERATOR_STYLE_ID)
            elif token[0] in self.BRACKETS:
                self.setStyling(token[1], self.BRACKETS_STYLE_ID)
            elif token[0] in self.MODULES_INSTALLED_ON_COMPUTER:
                self.setStyling(token[1], self.MODULE_STYLE_ID)
            elif token[0] in self.BUILT_IN_FUNCTIONS:
                self.setStyling(token[1], self.FUNCTION_STYLE_ID)
            elif re.search(r"#.+", token[0]):
                self.setStyling(token[1], self.COMMENT_STYLE_ID)
            else:
                self.setStyling(token[1], self.REGULAR_STYLE_ID)

        self.assertion_check_for_syntax_highlighting(text, tokens_for_syntax_highlighting)

    def assertion_check_for_syntax_highlighting(self, text, tokens_for_syntax_highlighting):
        length_of_byte_array_of_text = len(bytearray(text, encoding="utf-8"))

        sum_of_tokens = 0

        for token in tokens_for_syntax_highlighting:
            sum_of_tokens += token[1]

        print(
            f"Assertion: {length_of_byte_array_of_text == sum_of_tokens} ({length_of_byte_array_of_text} == {sum_of_tokens})"
        )
