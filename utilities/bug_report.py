"""The main menu window, powered by `PyQt5`."""

from PyQt5.QtWidgets import QMessageBox, QLineEdit, QPushButton, QWidget, QTextEdit

from PyQt5.QtGui import QFont, QIcon
from PyQt5.QtCore import pyqtSlot

from utilities.settings.essential_settings import DEBUGGING_MODE

from pathlib import Path

import logging

import sys

from datetime import datetime

from discord_webhook import DiscordWebhook, DiscordEmbed

logging.basicConfig(
    level=logging.DEBUG, 
    format="%(levelname)s on %(asctime)s in %(filename)s; %(message)s", 
    datefmt="%d/%m/%Y, %I:%M:%S %p"
)


class BugReport(QWidget):
    """
    The main menu window.

    Inherits `PyQt5.QtWidgets.QMainWindow`.
    """
    def __init__(self) -> None:
        """
        The initialization function of the 
        `utilities.main_menu.MainMenu` class.

        It creates the window due to the inheritance of the 
        `PyQt5.QtWidgets.QMainWindow` class.
        """
        super(BugReport, self).__init__()

        self.WINDOW_X: int = 200
        self.WINDOW_Y: int = 200

        self.WINDOW_WIDTH: int = 1080//2
        self.WINDOW_HEIGHT: int = 720//2

        self.TITLE: str = "DOCESSENTIAL"

        self.FONT_FAMILY: str = "Segoe UI"

        self.setGeometry(self.WINDOW_X, self.WINDOW_Y, self.WINDOW_WIDTH, self.WINDOW_HEIGHT)
        self.setWindowTitle(self.TITLE)
        self.setWindowIcon(QIcon(r"assets\doce_logo.png"))

        self.start_UI()

        self.showMaximized()

    def closeEvent(self, event):
        """Calls close event. Built-in method from QWidget."""

        self.console_debug("EXITING APP.")

        self.exit_confirmation_message_box = QMessageBox.question(
            self, "Exit Conformation", "Exit application?", 
            QMessageBox.Yes | QMessageBox.No, QMessageBox.No
        )

        if self.exit_confirmation_message_box == QMessageBox.Yes:
            event.accept()
            sys.exit(0)
        else:
            event.ignore()

    @pyqtSlot()
    def send_bug_report_to_discord_webhook(self):
        self.webhook_url = "[REDACTED]"  # DISCORD WEBHOOK REDACTED FOR PRIVACY PURPOSES (11/30/2025).

        self.webhook = DiscordWebhook(url=self.webhook_url)

        self.time_as_of_sending_bug_report = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        self.embed_to_be_sent_to_discord_server = DiscordEmbed(
            title="Bug Report", 
            description="New bug report for `PySee Beta v2024.0.1`", 
            color="ff0000"
        )

        self.embed_to_be_sent_to_discord_server.set_footer(
            text=f"Time Sent: {self.time_as_of_sending_bug_report}"
        )

        self.embed_to_be_sent_to_discord_server.add_embed_field(
            name="Bug", value=self.bug_text_box.text() + "\n"
        )
        self.embed_to_be_sent_to_discord_server.add_embed_field(
            name="Description", value=self.description_text_box.toPlainText()
        )

        self.webhook.add_embed(self.embed_to_be_sent_to_discord_server)

        self.response = self.webhook.execute()

        self.destroy()
        sys.exit(0)

    def console_debug(self, message):
        """
        Debugs message to terminal if 
        `utilities.settings.consts.DEBUGGING_MODE` is set to True
        """

        if DEBUGGING_MODE: 
            logging.debug(message)

    def create_bug_text_box(self):
        self.bug_text_box = QLineEdit(self)

        self.bug_text_box.setPlaceholderText("Bug...")

        self.bug_text_box.setFont(QFont(self.FONT_FAMILY, 20))
        self.bug_text_box.adjustSize()

        self.bug_text_box.move(200, 200)

    def create_description_text_box(self):
        self.description_text_box = QTextEdit(self)

        self.description_text_box.setPlaceholderText("Description...")

        self.description_text_box.setFont(QFont(self.FONT_FAMILY, 20))
        self.description_text_box.adjustSize()

        self.description_text_box.move(200, 400)

        self.description_text_box.setFixedSize(500, 250)

    def add_send_bug_report_button(self):
        """Adds `create_document_button: QPushButton` to `BugReport`."""

        self.send_report_bug_button = QPushButton(self)

        self.send_report_bug_button.setFont(QFont(self.FONT_FAMILY, 20))
        self.send_report_bug_button.setText("Send")

        self.send_report_bug_button.adjustSize()

        self.send_report_bug_button.clicked.connect(self.send_bug_report_to_discord_webhook)

        self.send_report_bug_button.move(200, 800)

    def start_UI(self) -> None:
        """Makes the user interface (UI)."""

        self.document_window = None

        self.style_sheet_path = Path(r"utilities\settings\stylesheets\main_menu_style.qss")
        self.setStyleSheet(self.style_sheet_path.read_text())

        self.create_bug_text_box()
        self.create_description_text_box()

        self.add_send_bug_report_button()
