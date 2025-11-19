import os


def set_style(app):
    current_directory = os.path.dirname(os.path.abspath(__file__))
    with open(f"{current_directory}/style.qss", "r") as f:
        STYLESHEET = f.read()
    app.setStyleSheet(STYLESHEET)