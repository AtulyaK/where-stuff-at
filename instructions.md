Here is a comprehensive `Instructions.md` file you can provide to your AI agent to ensure it builds a maintainable, well-structured, and robust Python desktop application.

This guide enforces the Google Python Style Guide, strict modularity, and best practices for desktop application architecture.

---

# `Instructions.md`: Python Desktop App Development Guidelines

> **Primary Objective:** Develop a production-ready Python desktop application prioritizing modularity, readability, and the Google Python Style Guide. The codebase must be highly maintainable and strictly separate the user interface from the underlying business logic.

## 1. Code Style and Conventions

* **Adhere to PEP 8 & Google Style:** Follow the Google Python Style Guide for all naming conventions, code layout, and formatting.
* **Type Hinting:** Use strict type hints (`typing` module) for all function arguments, return types, and class attributes.
* **Docstrings:** Use Google-style docstrings for every module, class, and function. Include `Args:`, `Returns:`, and `Raises:` sections where applicable.
* **Line Length:** Limit all lines to a maximum of 88 characters (standard Black formatter length).
* **Linting & Formatting:** Code must be compatible with standard linting and formatting tools (e.g., `flake8`, `black`, `mypy`).

## 2. Architecture and Modularity

* **Separation of Concerns:** Strictly enforce a Model-View-Controller (MVC) or Model-View-ViewModel (MVVM) architecture. The GUI code must never contain business logic, database queries, or heavy computations.
* **Modular Directory Structure:** Organize the project into focused, modular directories. Do not dump all scripts into the root folder.
* *Example Structure:*
* `/core/` or `/models/` (Business logic, data processing)
* `/gui/` or `/views/` (Window layouts, widgets, UI components)
* `/controllers/` (Connecting the UI to the business logic)
* `/utils/` (Helper functions, logging configuration)
* `/assets/` (Images, icons, styles)




* **Single Responsibility Principle:** Each class and function should have one specific, well-defined job.

## 3. Desktop Application Specifics

* **Non-Blocking UI:** Never run heavy computations, network requests, or long I/O operations on the main GUI thread. Use threading (`threading`, `QThread`, etc.) or asynchronous programming (`asyncio`) to keep the interface responsive.
* **State Management:** Maintain a clear and predictable application state. The UI should dynamically update to reflect changes in the underlying model without requiring hard refreshes.
* **Cross-Platform Compatibility:** Ensure file paths use `pathlib` or `os.path` to guarantee the app works seamlessly across Windows, macOS, and Linux.

## 4. Error Handling and Logging

* **No Silent Failures:** Do not use bare `except:` blocks. Catch specific exceptions and handle them gracefully.
* **Centralized Logging:** Implement the built-in `logging` module instead of `print()` statements. Log to both a rotating file and the console, utilizing appropriate severity levels (`DEBUG`, `INFO`, `WARNING`, `ERROR`, `CRITICAL`).
* **User-Facing Errors:** When an error occurs, present a clean, user-friendly error dialog in the GUI rather than crashing the application.

## 5. Dependency and Environment Management

* **Virtual Environments:** Assume the project will run in an isolated virtual environment (`venv` or `conda`).
* **Explicit Dependencies:** Maintain a strict `requirements.txt` or `pyproject.toml` file. Pin library versions to prevent future breaking changes (e.g., `PyQt6==6.5.0`).

---

Would you like me to tailor this file to include specific instructions for a particular GUI framework you plan on using, such as PyQt, CustomTkinter, or Kivy?