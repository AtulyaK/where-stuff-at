"""Application entry point for 'Where's My Stuff?'.

Initializes the PyQt6 application loop, loads the central stylesheet,
instantiates the MVVM architecture (MainController and MainWindow),
and handles any fatal runtime errors gracefully via central logging.
"""

import sys
import os
from typing import Optional

from PyQt6.QtWidgets import QApplication

from gui.main_window import MainWindow
from controllers.main_controller import MainController
from utils.logger import get_logger

logger = get_logger(__name__)


def load_stylesheet() -> str:
    """Loads the main QSS stylesheet for the application.

    Returns:
        The content of the style.qss file as a string. Returns an empty
        string if the file is not found.
    """
    style_path: str = os.path.join(os.path.dirname(__file__), "gui", "style.qss")
    if os.path.exists(style_path):
        try:
            with open(style_path, "r", encoding="utf-8") as f:
                return f.read()
        except OSError as e:
            logger.error(f"Failed to read stylesheet {style_path}: {e}")
            return ""
    else:
        logger.warning(f"Stylesheet not found at {style_path}.")
        return ""


def main() -> None:
    """The main entry point of the desktop application."""
    logger.info("Initializing 'Where's My Stuff?' application.")

    app = QApplication(sys.argv)
    app.setStyleSheet(load_stylesheet())

    # Initialize the Controller (Business Logic orchestrator)
    controller = MainController()

    # Initialize the View (passing the controller to bind signals if needed)
    window = MainWindow(controller)
    window.resize(1024, 768)
    window.show()

    # Trigger initial data load non-blockingly
    controller.load_initial_data()

    logger.info("Application loop started.")
    sys.exit(app.exec())


if __name__ == "__main__":
    # Catch any unhandled exceptions to ensure they are written to the log
    try:
        main()
    except Exception as e:
        logger.critical(f"Unhandled application exception: {e}", exc_info=True)
        sys.exit(1)
