from PyQt5.QtWidgets import QApplication

from utilities.essential_main_menu_window import MainMenuOfEssential

import sys
import os

import logging

logging.basicConfig(
    level=logging.ERROR, 
    format="%(levelname)s on %(asctime)s in %(filename)s; %(message)s", 
    datefmt="%d/%m/%Y, %I:%M:%S %p"
)


def main():
    os.system("cls")

    application = QApplication(sys.argv)

    window_to_be_shown_first = MainMenuOfEssential()
    window_to_be_shown_first.show()

    sys.exit(application.exec())

if __name__ == "__main__":
    main()
