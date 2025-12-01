"""The document window, powered by `PyQt5` and `Qsci`."""

from PyQt5.QtWidgets import (
    QWidget, QApplication, QMessageBox, 
    QFileDialog, QAction, QVBoxLayout, 
    QMenu, QMenuBar, QFontDialog, QPushButton, QInputDialog, 
    QLineEdit, QColorDialog
)
from PyQt5.QtGui import QFont, QIcon, QKeySequence, QColor, QPixmap
from PyQt5.QtCore import pyqtSlot, Qt, QDir
from PyQt5.Qsci import QsciScintilla, QsciAPIs

from utilities.settings.essential_settings import DEBUGGING_MODE

from utilities.lexers.lexer_ide import PythonLexer

from pathlib import Path

import logging

import sys
import subprocess
import threading

import builtins
import keyword

import inspect
import pkgutil

logging.basicConfig(
    level=logging.DEBUG, 
    format="%(levelname)s on %(asctime)s in %(filename)s; %(message)s", 
    datefmt="%d/%m/%Y, %I:%M:%S %p"
)


class EssentialIDE(QWidget):
    """
    The document window. \\
    Inherits `PyQt5.QtWidgets.QWidget`.
    """
    def __init__(self, window_title) -> None:
        """
        The initialization function of the 
        `utilities.document.Document` class.

        It creates the window due to the inheritance of the 
        `PyQt5.QtWidgets.QWidget` class.
        """
        super(EssentialIDE, self).__init__()

        self.WINDOW_X: int = 200
        self.WINDOW_Y: int = 200

        self.WINDOW_WIDTH: int = 1080
        self.WINDOW_HEIGHT: int = 720

        self.name_of_document = window_title

        self.title: str = f"PySee | \"{self.name_of_document}\""

        self.FONT_FAMILY: str = "Consolas"
        self.font_size: int = 14

        self._font = QFont(self.FONT_FAMILY, self.font_size)

        self.setGeometry(self.WINDOW_X, self.WINDOW_Y, self.WINDOW_WIDTH, self.WINDOW_HEIGHT)
        self.setWindowTitle(self.title)
        self.setWindowIcon(QIcon(r"assets\icons\pysee_icon.ico"))

        self.clipboard = QApplication.clipboard()

        self.start_UI()

        self.showMaximized()

    def closeEvent(self, event):
        """Calls close event. Built-in method from QWidget."""

        self.console_debug("CONFIRMING EXIT...")

        self.exit_confirmation_message_box = QMessageBox.question(
            self, "Exit Conformation", "Exit application?", 
            QMessageBox.Yes | QMessageBox.No, QMessageBox.No
        )

        if self.exit_confirmation_message_box == QMessageBox.Yes:
            self.console_debug("EXIT CONFIRMED")

            event.accept()
            sys.exit(0)
        else:
            self.console_debug("USER DOES NOT WANT TO EXIT")
            event.ignore()

    def create_edit_menu_as_context_menu(self):
        """Creates right-click edit menu."""

        self.edit_menu_as_context_menu = QMenu("Edit")

    def mousePressEvent(self, event):
        """
        Calls is mouse was left clicked. 
        Built-in method from QWidget.
        """

        if event.button() == Qt.RightButton:
            self.create_edit_menu_as_context_menu()

    def console_debug(self, message):
        """
        Debugs message to terminal if 
        `utilities.settings.consts.DEBUGGING_MODE` is set to True
        """

        if DEBUGGING_MODE: 
            logging.debug(message)

    @pyqtSlot()
    def exit_application(self):
        """
        Exits the application when called, 
        uses `PyQt5.QtCore.pyqtSlot()` decorator.
        """

        self.console_debug("EXITING APP.")

        self.exit_confirmation_message_box = QMessageBox.question(
            self, "Exit Conformation", "Exit application?", 
            QMessageBox.Yes | QMessageBox.No, QMessageBox.No
        )

        if self.exit_confirmation_message_box == QMessageBox.Yes:
            sys.exit(0)

    @pyqtSlot()
    def new_application(self):
        """
        Creates a new application when called, 
        uses `PyQt5.QtCore.pyqtSlot()` decorator.
        """

        self.console_debug("CREATING NEW APP.")

        self.new_document_window = EssentialIDE("EEIIDoc")
        self.new_document_window.show()

    @pyqtSlot()
    def copy(self):
        """
        Copies selected text on the document when called, 
        uses `PyQt5.QtCore.pyqtSlot()` decorator.
        """

        self.console_debug("TEXT COPIED.")

        self.clipboard.clear()
        self.clipboard.setText(self.document.text())

    @pyqtSlot()
    def paste(self):
        """
        Pastes text on clipboard to the document when called, 
        uses `PyQt5.QtCore.pyqtSlot()` decorator.
        """

        self.console_debug("TEXT PASTE.")

        self.document.setText(self.document.text() + self.clipboard.text())

    @pyqtSlot()
    def save(self):
        """
        Saves text on document to given file when called, 
        uses `PyQt5.QtCore.pyqtSlot()` decorator.
        """

        # FIXME When saved, doubles the lines in saved file.

        save_dialog_options = QFileDialog.Options()
        save_dialog_options |= QFileDialog.DontUseNativeDialog

        file_name, _ = QFileDialog.getSaveFileName(
            self, "Save Document", "", 
            "All Files (*);;Python Files (.py)", 
            options=save_dialog_options
        )

        if file_name: 
            self.console_debug(f"FILE {file_name} SAVED")

            with open(file_name, "w") as file:
                file.writelines(self.document.text())

                self.console_debug(self.document.text())

            self.file_has_been_saved = True
            self.name_of_saved_file = file_name

    @pyqtSlot()
    def load(self):
        """
        Loads given file to the application when called, 
        uses `PyQt5.QtCore.pyqtSlot()` decorator.
        """

        load_dialog_options = QFileDialog.Options()
        load_dialog_options |= QFileDialog.DontUseNativeDialog

        file_name, _ = QFileDialog.getOpenFileName(
            self, "Load Document", "", 
            "All Files (*);;Python Files (.py)", 
            options=load_dialog_options
        )

        if file_name: 
            self.console_debug(f"FILE {file_name} LOADED")

            with open(file_name, "r") as file:
                to_be_on_document = "".join(map(str, file.readlines()))

                self.document.setText(to_be_on_document)

            self.file_has_been_saved = True

            self.name_of_saved_file = file_name

        self.document.setFont(QFont(self.FONT_FAMILY, 16))

    # FIXME Fix theme changing.

    @pyqtSlot()
    def add_dark_theme_for_code_editor(self):
        if not self.dark_theme_is_on:
            self.console_debug("ADDING DARK THEME...")

            self.lexer.setDefaultColor(QColor("#000000"))
            self.lexer.setDefaultPaper(QColor("#f91d1c1c"))

            self.dark_theme_is_on = True

    @pyqtSlot()
    def add_light_theme_for_code_editor(self):
        if self.dark_theme_is_on:
            self.console_debug("ADDING LIGHT THEME...")

            self.lexer.setColor(QColor("#000000"), self.lexer.REGULAR_STYLE_ID)
            self.lexer.setDefaultPaper(QColor("#FFFFFF"))

            self.dark_theme_is_on = False

    @pyqtSlot()
    def set_font_for_document(self):
        """
        Uses `PyQt.QtWidgets.QFontDialog` to set the font of the document, 
        uses `PyQt5.QtCore.pyqtSlot()` decorator.
        """

        font, confirm = QFontDialog.getFont()

        if confirm:
            self.document.setFont(font)

    @pyqtSlot()
    def rename_while_in_document(self):
        """
        The `PyQt.QtWidgets.QInputDialog` 
        sets the name of the document while in the document when called, 
        uses `PyQt5.QtCore.pyqtSlot()` decorator.
        """

        new_name_of_document, confirm = QInputDialog().getText(
            self, "Rename Document", "New Name for Document", 
            QLineEdit.Normal, QDir().home().dirName()
        )

        if new_name_of_document and confirm:
            self.title = f"DOCESSENTIAL | Document \"{new_name_of_document}\""
            self.setWindowTitle(self.title)

    @pyqtSlot()
    def set_text_color_of_document(self):
        """
        Loads given file to the application when called, 
        uses `PyQt5.QtCore.pyqtSlot()` decorator.
        """

        self.text_color = QColorDialog().getColor()

        self.document.setTextColor(self.text_color)

    @pyqtSlot()
    def run_code_and_wait(self):
        self.code_running_process = self.start_code_running_process()

        if self.code_running_process != 1:
            self.thread_to_wait_until_user_presses_any_key = threading.Thread(target=lambda: input())
            self.thread_to_wait_until_user_presses_any_key.start()

            self.code_running_process.wait()

        self.file_has_not_been_saved_dialog = QMessageBox.information(
            self, "File has not been saved", "User has not saved file.", QMessageBox.Ok
        )

    @pyqtSlot()
    def set_file_has_been_saved_variable_to_false(self):
        self.file_has_been_saved = False

    def start_UI(self):
        """Makes the user interface (UI)."""

        self.file_has_been_saved = False

        self.style_sheet_path = Path(r"utilities\settings\stylesheets\code_editor_style.qss")
        self.setStyleSheet(self.style_sheet_path.read_text())

        self.set_up_code_editor()

        self.add_document_menu_bar_to_document()
        
        self.define_menu_item_actions()

        self.add_file_menu_to_document()
        self.add_edit_menu_to_document()
        self.add_themes_menu_to_document()

        self.add_menu_items_to_menu_bar()

        self.add_change_font_button_to_document()
        #// self.add_change_text_color_button_to_document()

        self.create_edit_menu_as_context_menu()

    def add_document_menu_bar_to_document(self):
        """
        Uses `PyQt5.QtWidgets.QMenuBar` and `PyQt5.QtWidgets.QVBoxLayout` 
        to create the menu bar
        for saving, loading, etc.
        """

        self.document_menu_bar = QMenuBar(self)

        self.widget_layout = QVBoxLayout()
        self.setLayout(self.widget_layout)
        
        self.widget_layout.setMenuBar(self.document_menu_bar)

    def add_change_text_color_button_to_document(self):
        """
        Uses `PyQt5.QtWidgets.QPushButton` and `PyQt5.QtWidgets.QFont` 
        to add a button that when clicked, 
        changes the text's color for optional styling.
        """

        self.text_color_change_button = QPushButton(self)

        self.text_color_change_button.setText("Change Text Color")
        self.text_color_change_button.setFont(QFont(self.FONT_FAMILY, 16))

        self.text_color_change_button.move(300, 38)

        self.text_color_change_button.adjustSize()

        self.text_color_change_button.clicked.connect(self.set_text_color_of_document)

    def add_change_font_button_to_document(self):
        """
        Uses `PyQt5.QtWidgets.QPushButton` and `PyQt5.QtWidgets.QFont` 
        to add a button that when clicked, 
        changes the text's font for optional styling.
        """

        self.change_font_button = QPushButton(self)

        self.change_font_button.setFont(QFont(self.FONT_FAMILY, 16))
        self.change_font_button.setText("Choose/Change Font")

        self.change_font_button.adjustSize()

        self.change_font_button.move(0, 38)

        self.change_font_button.clicked.connect(self.set_font_for_document)

    def add_menu_items_to_menu_bar(self):
        """
        Adds menu items to `utilities.document.Document.file_menu` 
        for functionality.
        """

        self.document_menu_bar.addMenu(self.file_menu)
        self.document_menu_bar.addMenu(self.edit_menu)
        # self.document_menu_bar.addMenu(self.theme_menu)

    def define_menu_item_actions(self):
        """Defines `PyQt5.QtWidgets.QAction`s for functionality."""

        self.new_action = QAction("New", self)
        self.close_action = QAction("Exit", self)
        self.save_action = QAction("Save", self)
        self.load_action = QAction("Load", self)
        self.rename_action = QAction("Rename", self)

        self.change_to_dark_theme_action = QAction("Dark Theme", self)
        self.change_to_light_theme_action = QAction("Light Theme", self)

        # self.switch_to_coding_mode_action = QAction("Document Mode", self)
        # self.run_code = QAction("Run Code", self)

        self.new_action.triggered.connect(self.new_application)
        self.new_action.setShortcut(QKeySequence("Ctrl+N"))

        self.close_action.triggered.connect(self.exit_application)

        self.save_action.triggered.connect(self.save)
        self.save_action.setShortcut(QKeySequence("Ctrl+S"))

        self.load_action.triggered.connect(self.load)
        self.load_action.setShortcut(QKeySequence("Ctrl+D"))

        self.rename_action.triggered.connect(self.rename_while_in_document)
        self.rename_action.setShortcut(QKeySequence("Ctrl+R"))

        self.change_to_dark_theme_action.triggered.connect(self.add_dark_theme_for_code_editor)

        self.change_to_light_theme_action.triggered.connect(self.add_light_theme_for_code_editor)

        # self.switch_to_coding_mode_action.triggered.connect(self.switch_coding_to_document_mode)
        # self.switch_to_coding_mode_action.setShortcut(QKeySequence("Ctrl+Alt+S"))

        # self.run_code.triggered.connect(self.run_code_and_wait)

    def get_all_modules_in_users_computer(self):
        pip_freeze_subprocess = subprocess.Popen(
            ["pip", "freeze"], shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE
        )

        output, error = pip_freeze_subprocess.communicate()

        return output.decode().split() if not error else error.decode()

    def add_file_menu_to_document(self):
        """
        Creates `utilities.document.Document.file_menu` 
        and binds aforementioned actions to the menu.
        """

        self.file_menu = QMenu("File")

        self.file_menu.addAction(self.new_action)
        self.file_menu.addAction(self.rename_action)
        self.file_menu.addSeparator()
        self.file_menu.addAction(self.save_action)
        self.file_menu.addAction(self.load_action)
        self.file_menu.addSeparator()
        self.file_menu.addAction(self.close_action)

    def add_edit_menu_to_document(self):
        """
        Creates `utilities.document.Document.edit_menu` 
        and binds aforementioned actions to the menu.
        """

        self.edit_menu = QMenu("Edit")

        # self.edit_menu.addAction(self.switch_to_coding_mode_action)
        # self.edit_menu.addAction(self.run_code)

    def add_themes_menu_to_document(self):
        self.theme_menu = QMenu("Themes")

        self.dark_theme_is_on = True

        self.theme_menu.addAction(self.change_to_dark_theme_action)
        self.theme_menu.addAction(self.change_to_light_theme_action)

    def get_parameters_from_function(self, function_to_get_parameters_from):
        return inspect.signature(function_to_get_parameters_from)
    
    def convert_string_to_function(self, string_to_convert_to_function):
        return eval(string_to_convert_to_function)

    def set_up_code_editor(self):
        self.TAB_WIDTH = 4

        self.document = QsciScintilla(self)

        self.document.setFixedSize(1917, 1008)
        self.document.move(10, 75)

        self.lexer = PythonLexer(self)

        self.function_autocompletion_image = QPixmap(r"assets\images\function_type_for_code_editor.png")
        self.document.registerImage(1, self.function_autocompletion_image)

        self.module_autocompletion_image = QPixmap(r"assets\images\module_type_for_code_editor.png")
        self.document.registerImage(2, self.module_autocompletion_image)

        self.keyword_autocompletion_image = QPixmap(r"assets\images\keyword_type_for_code_editor.png")
        self.document.registerImage(3, self.keyword_autocompletion_image)

        self.modules_installed_on_computer = [module.name for module in pkgutil.iter_modules()]

        self.api = QsciAPIs(self.lexer)
        self.built_in_functions = dir(builtins) + list(keyword.kwlist)

        for built_in_function in self.built_in_functions:
            if keyword.iskeyword(built_in_function):
                self.api.add(f"{built_in_function}?3")
            else:
                self.api.add(built_in_function)

        for module in self.modules_installed_on_computer:
            self.api.add(f"{module}?2")

        self.api.prepare()

        self.document.setLexer(self.lexer)
        self.document.setFont(self._font)
        self.document.setUtf8(True)

        self.document.setIndentationsUseTabs(True)
        self.document.setIndentationGuides(True)
        self.document.setTabWidth(self.TAB_WIDTH)

        self.document.setMarginType(1, QsciScintilla.NumberMargin)
        self.document.setMarginWidth(1, 100)
        self.document.setMarginsFont(self._font)

        self.document.setAutoCompletionCaseSensitivity(False)
        self.document.setAutoCompletionReplaceWord(False)
        self.document.setAutoCompletionSource(QsciScintilla.AcsAll)
        self.document.setAutoCompletionThreshold(1)

        self.document.setCallTipsStyle(QsciScintilla.CallTipsContext)
        self.document.setCallTipsVisible(0)
        self.document.setCallTipsPosition(QsciScintilla.CallTipsBelowText)
        self.document.setCallTipsHighlightColor(QColor("#0000FF"))
