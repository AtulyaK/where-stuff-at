# Agent Context & Notes: "Where's My Stuff?"

> **CRITICAL DIRECTIVE**: **BEFORE EVERY TASK**, you MUST read and cross-reference `instructions.md` located in the project root. Ensure all code strictly complies with the Google Python Style Guide, uses strict type hinting, implements centralized logging, and follows the MVC/MVVM non-blocking modular architecture.

## Goal
Build a pure PyQt6 desktop application replicating a modern web UI (Tailwind CSS, React component specs) provided by the user. The app will be an inventory manager.
The application needs to be packaged and installable on a device (macOS `.app`).

## Tech Stack & Architecture
- **Language**: Python 3
- **UI Framework**: `PyQt6` (Preferred over PySide6 unless blockers occur).
- **Styling Strategy**: Heavy reliance on `QSS` (Qt Style Sheets) to map Tailwind specs (`#22C55E` primary, muted grays, inter font-family).
- **Icons**: Need to look like Lucide. Using `qtawesome`.
- **Packaging**: `PyInstaller`. **DO NOT compile the application or run pyinstaller via commands yourself. The USER maintains responsibility for compiling and packaging.**
- **Strict Architecture**: MVVM/MVC, Google Style Guide, strict typing, and structured logging per `instructions.md`.

## Key Challenges to keep in mind:
1. **Responsive Grids**: PyQt layouts (`QGridLayout`, `QFlowLayout`) don't perfectly behave like CSS flex/grid out of the box. A custom FlowLayout might be needed for the item cards grid to wrap nicely on window resize.
2. **Modern Aesthetics**: Desktop GUIs tend to look dated. I must aggressively use QSS for border-radius, padding, border-colors, and subtle hover effects to achieve the requested "WOW" factor.
3. **Data Management**: I'll use simple in-memory python structures or SQLite optionally, mediated through strict Controllers.
4. **Cascading Dropdowns**: Need to cleanly reset children dropdowns when parents change.

## Workspace State
**Location**: `/Users/atulyakadur/Documents/Personal Code Work/where stuff at`

## Progress Log
- **Session 1**: Built v1 of the PyQt6 App mimicking Tailwind. Packaged into PyInstaller `.app`.
- **Session 2**: Integrating `instructions.md`. Planning massive refactor to align with Google Style, Typing, Logging, and MVVM structure.
- **Session 3**: Implemented UI enhancements (Dashboard Stock Panel Overlay, Add Items Styling, Locations Accordion).
  - **DB Requirement Note**: When implementing the actual database layer, each item must require a `low_supply_threshold` (or similar `status` column) to cleanly bifurcate "Low Supply" vs "Enough Supply" queries directly at the data layer instead of purely calculated on the UI.
