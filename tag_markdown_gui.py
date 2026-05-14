#!/usr/bin/env python3
"""
Tag Markdown GUI - PyQt6

Automatically adds a language tag to untagged Markdown code blocks.

When you convert a web page to Markdown with services like
https://urltomarkdown.com/, code blocks often look like this:

    ```
    sudo apt update
    ```

For Pandoc to preserve the language when converting to HTML, each block
needs a tag:

    ```bash
    sudo apt update
    ```

This program adds that tag automatically to every block that lacks one.

Author: Washington Indacochea Delgado
Email:  linuxfrontier@proton.me
"""

import sys
import re
import json
import os
from pathlib import Path

from PyQt6.QtCore import (
    QTranslator, QLocale, QLibraryInfo, QCoreApplication, Qt,
)
from PyQt6.QtGui import QDragEnterEvent, QDropEvent, QIcon
from PyQt6.QtWidgets import (
    QApplication,
    QMainWindow,
    QWidget,
    QLabel,
    QLineEdit,
    QPushButton,
    QFileDialog,
    QVBoxLayout,
    QHBoxLayout,
    QFrame,
    QComboBox,
    QMessageBox,
    QToolBar,
)


# Shorthand for translations — context name matches the main class
def tr(text, disambiguation=None):
    return QCoreApplication.translate("TagMarkdownApp", text, disambiguation)


# ============================================================
# APPLICATION ICON
# ============================================================
#
# Loaded from assets/html-blogger-post-fixes.svg next to this script.
# Path(__file__).parent makes it work regardless of the working directory.
#
# Requirements for Qt to render SVG:
#   Linux (apt):  sudo apt install python3-pyqt6.qtsvg
#   Linux (pip) / Windows / macOS:  nothing extra needed

def create_app_icon():
    """
    Load the SVG icon from assets/ relative to this script.
    Returns an empty QIcon (no error) if the file is not found.
    """
    icon_path = Path(__file__).parent / "assets" / "html-blogger-post-fixes.svg"
    if icon_path.exists():
        return QIcon(str(icon_path))
    return QIcon()


# ============================================================
# GENERAL CONFIGURATION
# ============================================================

APP_NAME = "TagMarkdownPyQt6"
CONFIG_FILE_NAME = "config.json"

# Language tags available in the combo box.
# Add more here if needed, e.g. "javascript", "yaml", "xml", etc.
LANGUAGES = [
    "bash",
    "sh",
    "shell",
    "python",
    "html",
    "css",
    "javascript",
    "json",
    "cmd",
    "powershell",
    "plaintext",
]

DEFAULT_CONFIG = {
    "last_language": "bash",
    "last_directory": "",
}


# ============================================================
# PATHS AND CONFIGURATION
# ============================================================

def get_config_dir():
    """
    Return the application configuration folder.
    Windows:        AppData/Roaming/TagMarkdownPyQt6
    Linux / macOS:  ~/.config/TagMarkdownPyQt6
    """
    if sys.platform.startswith("win"):
        appdata = os.environ.get("APPDATA")
        if appdata:
            config_dir = Path(appdata) / APP_NAME
        else:
            config_dir = Path.home() / "AppData" / "Roaming" / APP_NAME
    else:
        config_dir = Path.home() / ".config" / APP_NAME

    config_dir.mkdir(parents=True, exist_ok=True)
    return config_dir


def get_config_path():
    return get_config_dir() / CONFIG_FILE_NAME


def load_config():
    config_path = get_config_path()
    if not config_path.exists():
        save_config(DEFAULT_CONFIG)
        return DEFAULT_CONFIG.copy()
    try:
        with config_path.open("r", encoding="utf-8") as f:
            data = json.load(f)
        config = DEFAULT_CONFIG.copy()
        config.update(data)
        return config
    except Exception:
        save_config(DEFAULT_CONFIG)
        return DEFAULT_CONFIG.copy()


def save_config(config):
    config_path = get_config_path()
    with config_path.open("w", encoding="utf-8") as f:
        json.dump(config, f, indent=4, ensure_ascii=False)


# ============================================================
# MARKDOWN PROCESSING
# ============================================================

def process_markdown(content, selected_lang):
    """
    Add a language tag to untagged Markdown code blocks.

    Converts:
        ```
        sudo apt update
        ```

    Into:
        ```bash
        sudo apt update
        ```

    Blocks that already have a tag are left untouched.
    """
    pattern = r"```[ \t]*\n([\s\S]*?)```"

    def replace_block(match):
        code_content = match.group(1).strip("\n")
        return f"```{selected_lang}\n{code_content}\n```"

    return re.sub(pattern, replace_block, content)


def build_output_path(input_path):
    """Return the output path with a -taged suffix."""
    p = Path(input_path)
    return p.with_name(f"{p.stem}-taged{p.suffix}")


# ============================================================
# DROP ZONE WIDGET
# ============================================================

class DropZoneWidget(QFrame):
    """
    Visual drop zone.
    Does not capture drop events itself — the main window handles them.
    """
    def __init__(self, on_upload_clicked, parent=None):
        super().__init__(parent)
        self.setAcceptDrops(False)
        self._build_ui(on_upload_clicked)

    def _build_ui(self, on_upload_clicked):
        self.setObjectName("dropZone")
        self.setStyleSheet("""
            QFrame#dropZone {
                border: 2px dashed #b0b8c1;
                border-radius: 10px;
                background-color: #fafafa;
            }
        """)
        self.setMinimumHeight(110)

        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.setSpacing(6)

        self.lbl_drag = QLabel(tr("Drag and drop .md file"))
        self.lbl_drag.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.lbl_drag.setStyleSheet(
            "font-size: 14px; font-weight: bold; color: #222; border: none;"
        )

        self.lbl_or = QLabel(tr("or"))
        self.lbl_or.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.lbl_or.setStyleSheet("font-size: 13px; color: #666; border: none;")

        self.btn_browse = QPushButton(tr("⬆  Browse .md file"))
        self.btn_browse.setMinimumWidth(180)
        self.btn_browse.setFixedHeight(36)
        self.btn_browse.setCursor(Qt.CursorShape.PointingHandCursor)
        self.btn_browse.setStyleSheet("""
            QPushButton {
                background: qlineargradient(
                    x1:0, y1:0, x2:1, y2:0,
                    stop:0 #2bbfa4, stop:1 #1a9e87
                );
                color: white;
                border: none;
                border-radius: 18px;
                font-size: 13px;
                font-weight: bold;
                padding: 0 16px;
            }
            QPushButton:hover {
                background: qlineargradient(
                    x1:0, y1:0, x2:1, y2:0,
                    stop:0 #25a890, stop:1 #158a74
                );
            }
            QPushButton:pressed {
                background: #117a63;
            }
        """)
        self.btn_browse.clicked.connect(on_upload_clicked)

        layout.addWidget(self.lbl_drag)
        layout.addWidget(self.lbl_or)
        layout.addWidget(self.btn_browse, alignment=Qt.AlignmentFlag.AlignCenter)
        self.setLayout(layout)


# ============================================================
# MAIN WINDOW
# ============================================================

class TagMarkdownApp(QMainWindow):
    def __init__(self):
        super().__init__()

        self.app_translator = QTranslator()
        self.qt_translator = QTranslator()
        self._load_app_translation()
        self._load_qt_translation()

        self.config = load_config()

        self.setWindowTitle(tr("Markdown Code Block Tagger"))
        self.setWindowIcon(create_app_icon())
        self.resize(620, 320)
        self.setAcceptDrops(True)

        self.init_ui()
        self.center_window()

    def center_window(self):
        """Center the main window on the screen."""
        frame = self.frameGeometry()
        screen = QApplication.primaryScreen()
        center = screen.availableGeometry().center()
        frame.moveCenter(center)
        self.move(frame.topLeft())

    # ----------------------------------------------------------
    # Translation loaders
    # ----------------------------------------------------------

    def _load_app_translation(self):
        """
        Load the application .qm translation file from translations/.

        Locale priority:
          1. LANGUAGE environment variable  (e.g. LANGUAGE=fr python3 ...)
          2. System locale from QLocale

        File naming:
            translations/tag_markdown_es.qm
            translations/tag_markdown_pt_BR.qm
        """
        env_lang = os.environ.get("LANGUAGE", "").strip()

        if env_lang:
            locale_name = env_lang.replace("-", "_")
            locale_short = locale_name.split("_")[0]
        else:
            locale_name = QLocale.system().name()
            locale_short = locale_name.split("_")[0]

        translations_dir = Path(__file__).parent / "translations"

        candidates = [
            translations_dir / f"tag_markdown_{locale_name}.qm",
            translations_dir / f"tag_markdown_{locale_short}.qm",
        ]

        for path in candidates:
            if path.exists() and self.app_translator.load(str(path)):
                QApplication.installTranslator(self.app_translator)
                print(f"App translation loaded: {path.name}")
                return

        print(f"No app translation found for locale '{locale_name}', using English.")

    def _load_qt_translation(self):
        """Load Qt's built-in translations (file dialogs, buttons, etc.)."""
        translations_path = QLibraryInfo.path(
            QLibraryInfo.LibraryPath.TranslationsPath
        )
        locale_name = QLocale.system().name()
        locale_short = locale_name.split("_")[0]

        for name in [f"qtbase_{locale_name}", f"qtbase_{locale_short}"]:
            if self.qt_translator.load(name, translations_path):
                QApplication.installTranslator(self.qt_translator)
                print(f"Qt translation loaded: {name}")
                return

        print("No Qt translation found.")

    # ----------------------------------------------------------
    # About dialog
    # ----------------------------------------------------------

    def show_about(self):
        text = (
            "<b>Tag Markdown GUI - PyQt6</b><br><br>"
            "<b>" + tr("Developer") + ":</b> Washington Indacochea Delgado<br>"
            "<b>" + tr("Email") + ":</b> linuxfrontier@proton.me<br>"
            "<b>" + tr("Website") + ":</b> "
            "<a href='https://github.com/wachin/html-fix-blogger-post'>"
            "https://github.com/wachin/html-fix-blogger-post</a><br><br>"
            "<b>" + tr("Function") + ":</b><br>"
            + tr("Adds tags like <code>bash</code>, <code>python</code>, "
                 "<code>cmd</code> or <code>powershell</code> to untagged "
                 "Markdown code blocks.") + "<br><br>"
            "<b>" + tr("Technologies used") + ":</b><br>"
            "- Python 3<br>"
            "- PyQt6<br>"
            "- " + tr("Regular expressions") + "<br>"
            "- JSON<br>"
        )
        msg = QMessageBox(self)
        msg.setWindowTitle(tr("About"))
        msg.setTextFormat(msg.textFormat().RichText)
        msg.setText(text)
        msg.setStandardButtons(QMessageBox.StandardButton.Ok)
        msg.exec()

    # ----------------------------------------------------------
    # UI setup
    # ----------------------------------------------------------

    def init_ui(self):
        # Toolbar
        self.toolbar = QToolBar(tr("Main toolbar"))
        self.toolbar.setMovable(False)
        self.toolbar.setFloatable(False)
        self.addToolBar(self.toolbar)

        self.btn_about = QPushButton(tr("About..."))
        self.btn_about.clicked.connect(self.show_about)
        self.toolbar.addWidget(self.btn_about)

        # Central widget
        central_widget = QWidget()
        layout = QVBoxLayout()
        layout.setSpacing(8)
        layout.setContentsMargins(14, 10, 14, 10)

        self.lbl_description = QLabel(
            tr("Select a Markdown file and choose the tag to add "
               "to code blocks that have no language.")
        )
        self.lbl_description.setWordWrap(True)
        layout.addWidget(self.lbl_description)

        # Drop zone (replaces the old browse button)
        self.drop_zone = DropZoneWidget(on_upload_clicked=self.open_file_dialog)
        layout.addWidget(self.drop_zone)

        # Selected file path (read-only display)
        self.entry_file = QLineEdit()
        self.entry_file.setPlaceholderText(tr("No file selected"))
        self.entry_file.setReadOnly(True)
        layout.addWidget(self.entry_file)

        # Language selector row
        lang_row = QHBoxLayout()
        self.lbl_tag = QLabel(tr("Tag:"))
        lang_row.addWidget(self.lbl_tag)

        self.combo_lang = QComboBox()
        self.combo_lang.addItems(LANGUAGES)
        last_lang = self.config.get("last_language", "bash")
        self.combo_lang.setCurrentText(
            last_lang if last_lang in LANGUAGES else "bash"
        )
        lang_row.addWidget(self.combo_lang)
        lang_row.addStretch()
        layout.addLayout(lang_row)

        # Process button
        self.btn_process = QPushButton(tr("Process"))
        self.btn_process.clicked.connect(self.process_file)
        layout.addWidget(self.btn_process)

        self.result_label = QLabel("")
        self.result_label.setWordWrap(True)
        layout.addWidget(self.result_label)

        self.config_label = QLabel(
            tr("Configuration file:") + f"\n{get_config_path()}"
        )
        self.config_label.setWordWrap(True)
        layout.addWidget(self.config_label)

        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)

    # ----------------------------------------------------------
    # File opening
    # ----------------------------------------------------------

    def open_file_dialog(self):
        """Open the native file dialog to pick a Markdown file."""
        last_dir = self.config.get("last_directory", "")

        file_path, _ = QFileDialog.getOpenFileName(
            self,
            tr("Select Markdown file"),
            last_dir if Path(last_dir).exists() else "",
            tr("Markdown files (*.md *.markdown)"),
            options=QFileDialog.Option(0),
        )
        if not file_path:
            return

        self._set_file(file_path)

    def _set_file(self, file_path):
        """Store the selected file path and update the display."""
        self.entry_file.setText(file_path)
        self.config["last_directory"] = str(Path(file_path).parent)
        save_config(self.config)

    # ----------------------------------------------------------
    # Core processing
    # ----------------------------------------------------------

    def process_file(self):
        """Tag untagged code blocks in the selected Markdown file."""
        file_path = self.entry_file.text().strip()
        selected_lang = self.combo_lang.currentText().strip()

        if not file_path:
            QMessageBox.warning(
                self,
                tr("No file selected"),
                tr("Please select a Markdown file first."),
            )
            return

        input_path = Path(file_path)

        if not input_path.exists() or input_path.suffix.lower() not in (".md", ".markdown"):
            QMessageBox.warning(
                self,
                tr("Invalid input"),
                tr("Please select a valid .md or .markdown file."),
            )
            return

        try:
            content = input_path.read_text(encoding="utf-8")
        except Exception as e:
            QMessageBox.critical(
                self,
                tr("Error"),
                tr("Could not read the file:") + f"\n{e}",
            )
            return

        processed = process_markdown(content, selected_lang)
        output_path = build_output_path(input_path)

        try:
            output_path.write_text(processed, encoding="utf-8")
        except Exception as e:
            QMessageBox.critical(
                self,
                tr("Error"),
                tr("Could not save the file:") + f"\n{e}",
            )
            return

        self.config["last_language"] = selected_lang
        self.config["last_directory"] = str(input_path.parent)
        save_config(self.config)

        self.result_label.setText(tr("File saved as:") + f"\n{output_path}")

        QMessageBox.information(
            self,
            tr("Done"),
            tr("File saved successfully as:") + f"\n{output_path}",
        )

    # ----------------------------------------------------------
    # Drag and drop
    # ----------------------------------------------------------

    def dragEnterEvent(self, event: QDragEnterEvent):
        if event.mimeData().hasUrls():
            event.acceptProposedAction()
        else:
            event.ignore()

    def dragMoveEvent(self, event):
        if event.mimeData().hasUrls():
            event.acceptProposedAction()
        else:
            event.ignore()

    def dropEvent(self, event: QDropEvent):
        if event.mimeData().hasUrls():
            file_path = event.mimeData().urls()[0].toLocalFile()
            self.open_dropped_file(file_path)
            event.acceptProposedAction()
        else:
            event.ignore()

    def open_dropped_file(self, file_path):
        """Validate and load a file received via drag-and-drop."""
        if not os.path.exists(file_path):
            QMessageBox.warning(
                self,
                tr("File not found"),
                tr("The file does not exist:") + f"\n{file_path}",
            )
            return

        if Path(file_path).suffix.lower() not in (".md", ".markdown"):
            QMessageBox.warning(
                self,
                tr("Invalid file type"),
                tr("Only Markdown files (.md or .markdown) are accepted.")
                + f"\n{file_path}",
            )
            return

        self._set_file(file_path)


# ============================================================
# ENTRY POINT
# ============================================================

def main():
    # The native GTK file dialog (with Ctrl+F support) requires
    # QT_QPA_PLATFORMTHEME=gtk3 to be set BEFORE the process starts.
    # On Linux, use the provided launcher: tag_markdown_gui.sh
    # On Windows and macOS the native dialog works automatically.
    app = QApplication(sys.argv)
    app.setWindowIcon(create_app_icon())
    window = TagMarkdownApp()
    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
