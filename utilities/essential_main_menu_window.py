from PyQt5.QtWidgets import (
    QMainWindow, QMessageBox, QLineEdit, QPushButton, QInputDialog, 
    QLabel
)

from PyQt5.QtGui import QFont, QIcon, QPixmap
from PyQt5.QtCore import pyqtSlot

from utilities.ide import EssentialIDE

from utilities.settings.essential_settings import DEBUGGING_MODE

from pathlib import Path

import logging

import sys

logging.basicConfig(
    level=logging.DEBUG, 
    format="%(levelname)s on %(asctime)s in %(filename)s; %(message)s", 
    datefmt="%d/%m/%Y, %I:%M:%S %p"
)


class MainMenuOfEssential(QMainWindow):
    def __init__(self) -> None:
        """
        The initialization function of the 
        `utilities.main_menu.MainMenu` class.

        It creates the window due to the inheritance of the 
        `PyQt5.QtWidgets.QMainWindow` class.
        """
        super(MainMenuOfEssential, self).__init__()

        self.WINDOW_X: int = 200
        self.WINDOW_Y: int = 200

        self.WINDOW_WIDTH: int = 1080
        self.WINDOW_HEIGHT: int = 720

        self.TITLE: str = "EEI | PySee"

        self.FONT_FAMILY: str = "Segoe UI"

        self.setGeometry(self.WINDOW_X, self.WINDOW_Y, self.WINDOW_WIDTH, self.WINDOW_HEIGHT)
        self.setWindowTitle(self.TITLE)
        self.setWindowIcon(QIcon(r"assets\icons\pysee_icon.ico"))

        self.start_UI()

        self.showMaximized()

    def console_debug(self, message):
        """
        Debugs message to terminal if 
        `utilities.settings.consts.DEBUGGING_MODE` is set to True
        """

        if DEBUGGING_MODE: 
            logging.debug(message)

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

    @pyqtSlot()
    def create_file_slot_action(self):
        self.ide_window = None

        self.file_name, confirm = QInputDialog().getText(
            self, "Create File", "Insert Python file name: ", 
            QLineEdit.Normal, "pysee_file.py"
        )

        if self.ide_window is None and self.file_name and confirm:
            self.ide_window = EssentialIDE(self.file_name)

            self.destroy()
            self.ide_window.show()

    def add_create_file_button_to_essential_main_menu_window(self):
        self.file_button_in_essential_main_menu_window = QPushButton(self)

        self.file_button_in_essential_main_menu_window_font = QFont(self.FONT_FAMILY, 20)
        self.file_button_in_essential_main_menu_window_text = "New Python File"

        self.file_button_in_essential_main_menu_window.setFont(
            self.file_button_in_essential_main_menu_window_font
        )
        self.file_button_in_essential_main_menu_window.setText(
            self.file_button_in_essential_main_menu_window_text
        )

        self.file_button_in_essential_main_menu_window.adjustSize()

        self.file_button_in_essential_main_menu_window.clicked.connect(
            self.create_file_slot_action
        )

        self.file_button_in_essential_main_menu_window.move(
            (3*self.WINDOW_WIDTH)//4 - 290//4, 245
        )

    def start_UI(self):
        self.style_sheet_for_main_menu = Path(
            r"utilities\settings\stylesheets\main_menu_style.qss"
        )

        self.style_for_main_menu = self.style_sheet_for_main_menu.read_text()
        self.setStyleSheet(self.style_for_main_menu)

        self.add_create_file_button_to_essential_main_menu_window()
