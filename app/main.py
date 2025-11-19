from PyQt6.QtWidgets import QApplication, QMainWindow
from ui import HomeWindow, set_style

# You need one (and only one) QApplication instance per application.
# Pass in sys.argv to allow command line arguments for your app.
# If you know you won't use command line arguments QApplication([]) works too.
app = QApplication([])

# set style sheet function
set_style(app)
# Create a Qt widget, which will be our window.
window = HomeWindow()
# IMPORTANT!!!!! Windows are hidden by default.
window.show()

# Start the event loop.
app.exec()


# Your application won't reach here until you exit and the event
# loop has stopped.