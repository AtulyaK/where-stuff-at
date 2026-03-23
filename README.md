# Where's My Stuff? 📦

A beautiful, responsive desktop application for inventory management, built strictly with **PyQt6** while mirroring modern web design specifications (Tailwind CSS equivalents). 

This project strictly adheres to the **Google Python Style Guide**, utilizing strict type hints, centralized logging, and a robust **Model-View-ViewModel (MVVM)** architecture.

## 🚀 Getting Started

### Prerequisites

Ensure you have **Python 3.12+** installed on your machine.

### 1. Set Up the Virtual Environment

Create and activate a virtual environment to isolate the project dependencies:

```bash
# On macOS/Linux
python3 -m venv venv
source venv/bin/activate

# On Windows (Command Prompt)
venv\Scripts\activate.bat
```

### 2. Install Dependencies

Install the required PyQt6 components, custom icons (`qtawesome`), and packaging tools:

```bash
pip install -r requirements.txt
```

### 3. Run the Application (Development Mode)

To launch the desktop application, run the core entry point. All debugging and execution logs will automatically output to both your console and a rotating `app.log` file in the project root.

```bash
python app.py
```

### 4. Running Static Analysis

To ensure code health and maintain adherence to the `instructions.md` configurations, you can run the suite of linters and formatters:

```bash
# Auto-format the entire codebase (88 line-width limit)
black .

# Check for PEP 8 compliance and linting errors
flake8 .

# Verify strict static type hints
mypy .
```

### 5. Compiling the Application

When you are ready to distribute or run the application as a standalone executable (e.g., a macOS `.app` bundle), use `PyInstaller`:

```bash
pyinstaller --windowed --name "WhereIsMyStuff" app.py
```

The compiled application bundle will be generated inside the `dist/` directory.

---

*Note: The AI Agent (`Antigravity`) will maintain code architecture and handle programmatic scaling, but relies on you (the User) to deliberately trigger PyInstaller compilation steps.*

source venv/bin/activate
python app.py
