#!/usr/bin/env python3

import sys
import json
import os
from pathlib import Path

from bs4 import BeautifulSoup

from PyQt6.QtCore import QTranslator, QLocale, QLibraryInfo, QCoreApplication, Qt
from PyQt6.QtGui import QAction, QDragEnterEvent, QDropEvent, QIcon
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
    QMessageBox,
    QToolBar,
)

# Shorthand used throughout the file for translations
def tr(text, disambiguation=None):
    return QCoreApplication.translate("HtmlFixerApp", text, disambiguation)


# ============================================================
# APPLICATION ICON
# ============================================================
#
# The icon is loaded from assets/html-blogger-post-fixes.svg,
# located next to this script. The path is resolved with
# Path(__file__).parent so it works on Linux, Windows and macOS
# regardless of the working directory.
#
# Requirements for Qt to render SVG:
#   Linux with PyQt6 installed via apt:  sudo apt install python3-pyqt6.qtsvg
#     (libqt6svg6 is installed automatically as a dependency)
#   Linux with PyQt6 installed via pip:  nothing extra, SVG support is included
#   Windows / macOS with pip:            nothing extra, SVG support is included

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

APP_NAME = "HtmlFixerPyQt6"
CONFIG_FILE_NAME = "config.json"

# Add more recognised language labels for Markdown code blocks
# converted to HTML here. Examples:
#   "ruby", "javascript", "typescript", "go", "rust", etc.
MARKDOWN_CODE_LABELS = {
    "bash",
    "sh",
    "shell",
    "cmd",
    "bat",
    "batch",
    "powershell",
    "ps1",
    "console",
    "terminal",
    "python",
}

DEFAULT_CONFIG = {
    "table_font_size": "90%"
}


# ============================================================
# PATHS AND CONFIGURATION
# ============================================================

def get_config_dir():
    """
    Return the application configuration folder.
    Windows: AppData/Roaming
    Linux / macOS: ~/.config
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
    """
    Load the JSON configuration file.
    Falls back to defaults if the file does not exist or is corrupted.
    """
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
    """Save configuration as JSON."""
    config_path = get_config_path()
    with config_path.open("w", encoding="utf-8") as f:
        json.dump(config, f, indent=4, ensure_ascii=False)


# ============================================================
# HTML PROCESSING FUNCTIONS
# ============================================================

def improve_inline_code(html):
    """Style simple inline <code> elements."""
    soup = BeautifulSoup(html, "html.parser")
    for code in soup.find_all("code"):
        if not code.find_parent("pre"):
            code["style"] = (
                "background: #f5f5f5; "
                "border: 1px solid #d0d0d0; "
                "border-radius: 3px; "
                "padding: 1px 4px; "
                "font-family: 'Ubuntu Mono', Consolas, monospace; font-weight: bold; "
                "color: #c7254e; "
                "font-size: 90%; "
            )
    return str(soup)


def is_tagged_code_block(pre):
    """
    Return True if the <pre> element corresponds to a Markdown code block
    with a recognised language label (sourceCode, language-bash, bash, etc.).
    """
    classes_pre = set(pre.get("class", []))
    code = pre.find("code")
    classes_code = set(code.get("class", [])) if code else set()
    all_classes = classes_pre | classes_code

    if "sourceCode" in all_classes:
        return True

    for label in MARKDOWN_CODE_LABELS:
        if label in all_classes:
            return True
        if f"language-{label}" in all_classes:
            return True

    return False


def improve_code_boxes(html):
    """
    Style Markdown code blocks that have a language label.
    Adds a dark terminal-style box with a top bar and a Copy button.
    """
    soup = BeautifulSoup(html, "html.parser")

    for pre in soup.find_all("pre"):
        if not is_tagged_code_block(pre):
            continue

        container = soup.new_tag("div", style=(
            "margin: 15px 0; "
            "border-radius: 6px; "
            "overflow: hidden; "
            "box-shadow: 0 4px 8px rgba(0,0,0,0.2);"
        ))
        pre.wrap(container)

        pre["style"] = (
            "background: #1e1e1e; "
            "color: #f0f0f0; "
            "font-family: 'Ubuntu Mono', 'Courier New', monospace; "
            "font-weight: bold; "
            "font-size: 14px; "
            "line-height: 1.5; "
            "margin: 0; "
            "padding: 12px 20px; "
            "border-left: 4px solid #3aa655; "
            "overflow: auto; "
            "max-height: 500px; "
        )

        terminal_bar = soup.new_tag("div", style=(
            "background: #3a3a3a; "
            "height: 28px; "
            "display: flex; "
            "align-items: center; "
            "padding: 0 15px; "
            "border-bottom: 1px solid #2a2a2a; "
        ))

        for color in ["#FAD510", "#0066CC", "#CE1126"]:
            dot = soup.new_tag("span", style=(
                f"background: {color}; "
                "width: 12px; height: 12px; "
                "border-radius: 50%; margin-right: 8px; "
            ))
            terminal_bar.append(dot)

        copy_btn = soup.new_tag("button", attrs={
            "type": "button",
            "class": "code-copy-btn",
            "title": "Copy code",
            "aria-label": "Copy code",
            "style": (
                "margin-left:auto;"
                "background:rgba(255,255,255,0.10);"
                "border:1px solid rgba(255,255,255,0.18);"
                "color:#fff;"
                "border-radius:6px;"
                "padding:3px 10px;"
                "font-size:12px;"
                "font-weight:700;"
                "cursor:pointer;"
                "line-height:1;"
            )
        })
        copy_btn.string = "Copy"
        terminal_bar.append(copy_btn)

        container.insert(0, terminal_bar)

        for code in pre.find_all("code"):
            code["style"] = "color: inherit; font-family: inherit;"

    return str(soup)


def improve_tables(html, font_percentage):
    """Style HTML tables with alternating rows and horizontal scroll."""
    soup = BeautifulSoup(html, "html.parser")

    for table in soup.find_all("table"):
        table_style = (
            "border-collapse: collapse; "
            "width: 100%; "
            "background-color: #ffffff; "
            "table-layout: auto; "
        )
        if font_percentage:
            table_style += f"font-size: {font_percentage}; "
        table["style"] = table_style

        for i, row in enumerate(table.find_all("tr")):
            if i == 0:
                row["style"] = (
                    "background-color: #ececec; "
                    "color: #1f2d3d; "
                    "font-weight: bold;"
                )
            elif i % 2 == 1:
                row["style"] = "background-color: #ffffff;"
            else:
                row["style"] = "background-color: #f5f5f5;"

        for th in table.find_all("th"):
            th["style"] = (
                "border: 1px solid #cfcfcf; "
                "padding: 14px 16px; "
                "text-align: left; "
                "vertical-align: top; "
                "white-space: normal; "
                "overflow-wrap: break-word; "
                "word-break: normal; "
                "max-width: 220px;"
            )

        for td in table.find_all("td"):
            td["style"] = (
                "border: 1px solid #cfcfcf; "
                "padding: 14px 16px; "
                "text-align: left; "
                "vertical-align: top; "
                "white-space: normal; "
                "overflow-wrap: break-word; "
                "word-break: normal; "
                "line-height: 1.55; "
                "max-width: 220px;"
            )

        wrapper = soup.new_tag("div", attrs={
            "class": "table-code-box",
            "style": (
                "margin: 18px 0; "
                "background: #f8f8f8; "
                "border: 1px solid #d8d8d8; "
                "border-radius: 6px; "
                "overflow-x: auto; "
                "overflow-y: hidden; "
                "-webkit-overflow-scrolling: touch;"
            )
        })
        table.insert_before(wrapper)
        wrapper.append(table.extract())

    return str(soup)


def improve_simple_code_blocks(html):
    """
    Style plain <pre><code> blocks that have no recognised language label.
    Uses the CSS class simple-code-box so Blogger does not strip the style
    when editing in visual mode.
    """
    soup = BeautifulSoup(html, "html.parser")

    for pre in soup.find_all("pre"):
        if is_tagged_code_block(pre):
            continue

        if pre.code and not pre.get("class"):
            pre["class"] = pre.get("class", []) + ["simple-code-box"]
            pre["style"] = (
                "background-color: #f8f8f8; "
                "border: 1px solid #d0d0d0; "
                "border-left: 6px solid #d44950; "
                "line-height: 1.5; "
                "margin: 10px 0; "
                "overflow-x: auto; "
                "padding: 10px; "
                "border-radius: 4px; "
            )

            span_outer = soup.new_tag("span", style=(
                "color: #000000; "
                "font-family: 'Ubuntu Mono', Consolas, monospace; "
                "font-size: 15px; "
                "white-space: pre; "
            ))
            span_outer.string = pre.code.get_text()
            pre.clear()
            pre.append(span_outer)

    return str(soup)


# ============================================================
# DROP ZONE WIDGET
# ============================================================

class DropZoneWidget(QFrame):
    """
    Visual drop zone widget.
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
        self.setMinimumHeight(130)

        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.setSpacing(6)

        self.lbl_drag = QLabel(tr("Drag and drop files"))
        self.lbl_drag.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.lbl_drag.setStyleSheet(
            "font-size: 15px; font-weight: bold; color: #222; border: none;"
        )

        self.lbl_or = QLabel(tr("or"))
        self.lbl_or.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.lbl_or.setStyleSheet("font-size: 13px; color: #666; border: none;")

        self.btn_upload = QPushButton(tr("⬆  Upload"))
        self.btn_upload.setFixedSize(130, 36)
        self.btn_upload.setCursor(Qt.CursorShape.PointingHandCursor)
        self.btn_upload.setStyleSheet("""
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
        self.btn_upload.clicked.connect(on_upload_clicked)

        layout.addWidget(self.lbl_drag)
        layout.addWidget(self.lbl_or)
        layout.addWidget(self.btn_upload, alignment=Qt.AlignmentFlag.AlignCenter)
        self.setLayout(layout)


# ============================================================
# MAIN WINDOW
# ============================================================

class HtmlFixerApp(QMainWindow):
    def __init__(self):
        super().__init__()

        self.app_translator = QTranslator()
        self.qt_translator = QTranslator()
        self._load_app_translation()
        self._load_qt_translation()

        self.config = load_config()

        self.setWindowTitle(tr("HTML Blogger Fixer"))
        self.setWindowIcon(create_app_icon())
        self.resize(520, 310)
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
        Load the application .qm translation file from translations/
        based on the system locale.

        The locale is determined in this order:
          1. LANGUAGE environment variable (e.g. LANGUAGE=fr python3 ...)
          2. System locale from QLocale

        File naming convention:
            translations/html_blogger_fixer_es.qm      (Spanish)
            translations/html_blogger_fixer_pt_BR.qm   (Portuguese Brazil)
            translations/html_blogger_fixer_en.qm      (English — optional base)

        Falls back silently to the built-in English strings if no file
        is found for the current locale.
        """
        # Allow overriding the locale from the terminal for testing:
        #   LANGUAGE=fr python3 html_blogger_fixer_gui.py
        env_lang = os.environ.get("LANGUAGE", "").strip()

        if env_lang:
            # Normalise: "pt_BR" stays as-is, "fr" stays as-is
            locale_name = env_lang.replace("-", "_")
            locale_short = locale_name.split("_")[0]
        else:
            locale_name = QLocale.system().name()    # e.g. es_EC
            locale_short = locale_name.split("_")[0] # e.g. es

        translations_dir = Path(__file__).parent / "translations"

        candidates = [
            translations_dir / f"html_blogger_fixer_{locale_name}.qm",
            translations_dir / f"html_blogger_fixer_{locale_short}.qm",
        ]

        for path in candidates:
            if path.exists() and self.app_translator.load(str(path)):
                QApplication.installTranslator(self.app_translator)
                print(f"App translation loaded: {path.name}")
                return

        print(f"No app translation found for locale '{locale_name}', using English.")

    def _load_qt_translation(self):
        """
        Load Qt's own built-in translations (file dialogs, buttons, etc.)
        so they appear in the system language.
        Requires qt6-translations-l10n installed on Linux.
        """
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
            "<b>HTML Blogger Fixer PyQt6</b><br><br>"
            "<b>" + tr("Developer") + ":</b> Washington Indacochea Delgado<br>"
            "<b>" + tr("Email") + ":</b> linuxfrontier@proton.me<br>"
            "<b>" + tr("Website") + ":</b> "
            "<a href='https://github.com/wachin/html-fix-blogger-post'>"
            "https://github.com/wachin/html-fix-blogger-post</a><br><br>"
            "<b>" + tr("Technologies used") + ":</b><br>"
            "- Python 3<br>"
            "- PyQt6<br>"
            "- BeautifulSoup4<br>"
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

        self.label_font = QLabel(
            tr("Table font size (e.g. 90%, 100%, etc.):")
        )
        layout.addWidget(self.label_font)

        self.entry_font = QLineEdit()
        self.entry_font.setText(self.config.get("table_font_size", "90%"))
        layout.addWidget(self.entry_font)

        # Drop zone
        self.drop_zone = DropZoneWidget(on_upload_clicked=self.open_file_dialog)
        layout.addWidget(self.drop_zone)

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
    # Font size helpers
    # ----------------------------------------------------------

    def normalize_font_size(self, text):
        """Append % if the user typed a bare number like 90."""
        text = text.strip()
        if text and not text.endswith("%"):
            text += "%"
        return text

    def save_font_preference(self):
        value = self.normalize_font_size(self.entry_font.text())
        self.entry_font.setText(value)
        self.config["table_font_size"] = value
        save_config(self.config)

    # ----------------------------------------------------------
    # File opening
    # ----------------------------------------------------------

    def open_file_dialog(self):
        self.save_font_preference()

        # Use the native OS file dialog so shortcuts like Ctrl+F work.
        # On Linux launch via html_blogger_fixer_gui.sh to get the GTK dialog.
        file_path, _ = QFileDialog.getOpenFileName(
            self,
            tr("Select HTML file"),
            "",
            tr("HTML files (*.html *.htm)"),
            options=QFileDialog.Option(0),
        )
        if not file_path:
            return
        self._process_path(file_path)

    # ----------------------------------------------------------
    # Core processing
    # ----------------------------------------------------------

    def _process_path(self, filepath):
        """
        Process the given HTML file and save the result.
        Called both from the file dialog and from drag-and-drop.
        """
        self.save_font_preference()
        font_size = self.config.get("table_font_size", "90%")

        try:
            input_path = Path(filepath)

            with input_path.open("r", encoding="utf-8") as f:
                html = f.read()

            html = improve_inline_code(html)
            html = improve_code_boxes(html)
            html = improve_tables(html, font_size)
            html = improve_simple_code_blocks(html)

            output_path = input_path.with_name(f"{input_path.stem}-fix.html")

            with output_path.open("w", encoding="utf-8") as f:
                f.write(html)

            self.result_label.setText(
                tr("File saved to:") + f"\n{output_path}"
            )

            QMessageBox.information(
                self,
                tr("Done"),
                tr("File saved successfully to:") + f"\n{output_path}",
            )

        except Exception as e:
            QMessageBox.critical(
                self,
                tr("Error"),
                tr("An error occurred while processing the file:") + f"\n{e}",
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
        """Validate and process a file received via drag-and-drop."""
        if not os.path.exists(file_path):
            QMessageBox.warning(
                self,
                tr("File not found"),
                tr("The file does not exist:") + f"\n{file_path}",
            )
            return

        if not file_path.lower().endswith((".html", ".htm")):
            QMessageBox.warning(
                self,
                tr("Invalid file type"),
                tr("Only HTML files (.html or .htm) are accepted.") + f"\n{file_path}",
            )
            return

        self._process_path(file_path)


# ============================================================
# ENTRY POINT
# ============================================================

def main():
    # The native GTK file dialog (with Ctrl+F support) requires
    # QT_QPA_PLATFORMTHEME=gtk3 to be set BEFORE the process starts.
    # On Linux, use the provided launcher: html_blogger_fixer_gui.sh
    # On Windows and macOS the native dialog works automatically.
    app = QApplication(sys.argv)
    app.setWindowIcon(create_app_icon())
    window = HtmlFixerApp()
    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
