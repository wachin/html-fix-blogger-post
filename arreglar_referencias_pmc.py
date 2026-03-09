import re
import sys
from pathlib import Path

from PyQt6.QtCore import Qt
from PyQt6.QtGui import QAction
from PyQt6.QtWidgets import (
    QApplication,
    QFileDialog,
    QHBoxLayout,
    QLabel,
    QMainWindow,
    QMessageBox,
    QPushButton,
    QPlainTextEdit,
    QSplitter,
    QStatusBar,
    QVBoxLayout,
    QWidget,
)


def fix_pmc_markdown(text: str) -> str:
    """
    Arregla markdown copiado desde referencias de artículos de PMC/PubMed Central.

    Cambios principales:
    - Convierte \[texto\] en [texto]
    - Elimina enlaces [PMC free article](/articles/...)
    - Une enlaces consecutivos tipo [DOI](...)[PubMed](...)[Google Scholar](...)
    - Limpia espacios sobrantes alrededor de enlaces finales
    """

    # Normalizar saltos de línea
    text = text.replace("\r\n", "\n").replace("\r", "\n")

    # 1) Des-escapar corchetes de markdown: \[ ... \] -> [ ... ]
    text = text.replace(r"\[", "[").replace(r"\]", "]")

    # 2) Eliminar enlaces "PMC free article"
    #    Ejemplo:
    #    [PMC free article](/articles/PMC9034083/)
    text = re.sub(
        r"\s*\[PMC free article\]\([^)]+\)",
        "",
        text,
        flags=re.IGNORECASE,
    )

    # 3) Quitar espacios entre enlaces consecutivos al final o en cualquier parte
    #    Ejemplo:
    #    [DOI](... ) [PubMed](... ) [Google Scholar](... )
    #    ->
    #    [DOI](...)[PubMed](...)[Google Scholar](...)
    #
    # Repetimos hasta que no haya más cambios.
    prev = None
    while prev != text:
        prev = text
        text = re.sub(r"\)\s+\[", r")[", text)

    # 4) Limpiar dobles espacios antes de los bloques de enlaces
    #    Ejemplo:
    #    "... doi: xxx.  [DOI](...)"
    #    -> "... doi: xxx. [DOI](...)"
    text = re.sub(r"\.\s{2,}\[", ". [", text)

    # 5) Quitar espacios al final de línea
    text = re.sub(r"[ \t]+$", "", text, flags=re.MULTILINE)

    # 6) Reducir exceso de líneas en blanco (máximo 2 seguidas)
    text = re.sub(r"\n{3,}", "\n\n", text)

    return text
    
def remove_empty_brackets(text: str) -> str:
    """
    Elimina todos los corchetes vacíos [] o con solo espacios dentro.
    """
    return re.sub(r"\[\s*\]", "", text)


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Arreglador Markdown PMC / PubMed Central")
        self.resize(1200, 700)

        self.current_input_file = None
        self.current_output_file = None

        self._build_ui()
        self._build_menu()

    def _build_ui(self):
        central = QWidget()
        self.setCentralWidget(central)

        main_layout = QVBoxLayout(central)

        title = QLabel(
            "Pega aquí el Markdown copiado desde referencias de PMC / PubMed Central y luego pulsa “Arreglar Markdown”."
        )
        title.setWordWrap(True)
        main_layout.addWidget(title)

        splitter = QSplitter(Qt.Orientation.Horizontal)

        # Panel izquierdo
        left_widget = QWidget()
        left_layout = QVBoxLayout(left_widget)
        left_label = QLabel("Entrada")
        self.input_edit = QPlainTextEdit()
        self.input_edit.setPlaceholderText(
            "Pega aquí el markdown original..."
        )
        left_layout.addWidget(left_label)
        left_layout.addWidget(self.input_edit)

        # Panel derecho
        right_widget = QWidget()
        right_layout = QVBoxLayout(right_widget)
        right_label = QLabel("Salida corregida")
        self.output_edit = QPlainTextEdit()
        self.output_edit.setPlaceholderText(
            "Aquí aparecerá el markdown corregido..."
        )
        right_layout.addWidget(right_label)
        right_layout.addWidget(self.output_edit)

        splitter.addWidget(left_widget)
        splitter.addWidget(right_widget)
        splitter.setSizes([600, 600])

        main_layout.addWidget(splitter)

        # Botones
        btn_layout = QHBoxLayout()

        self.btn_open = QPushButton("Abrir .md")
        self.btn_paste = QPushButton("Pegar en entrada")
        self.btn_fix = QPushButton("Arreglar Markdown")
        self.btn_copy = QPushButton("Copiar salida")
        self.btn_save = QPushButton("Guardar salida")
        self.btn_clear = QPushButton("Limpiar todo")
        self.btn_remove_empty = QPushButton("Eliminar [] vacíos")

        btn_layout.addWidget(self.btn_open)
        btn_layout.addWidget(self.btn_paste)
        btn_layout.addWidget(self.btn_fix)
        btn_layout.addWidget(self.btn_copy)
        btn_layout.addWidget(self.btn_save)
        btn_layout.addWidget(self.btn_clear)
        btn_layout.addWidget(self.btn_remove_empty)

        main_layout.addLayout(btn_layout)

        # Eventos
        self.btn_open.clicked.connect(self.open_file)
        self.btn_paste.clicked.connect(self.paste_input)
        self.btn_fix.clicked.connect(self.fix_text)
        self.btn_copy.clicked.connect(self.copy_output)
        self.btn_save.clicked.connect(self.save_output)
        self.btn_clear.clicked.connect(self.clear_all)
        self.btn_remove_empty.clicked.connect(self.remove_empty)

        # Barra de estado
        self.setStatusBar(QStatusBar())
        self.statusBar().showMessage("Listo")
        
    def _build_menu(self):
        menubar = self.menuBar()

        file_menu = menubar.addMenu("Archivo")
        tools_menu = menubar.addMenu("Herramientas")

        open_action = QAction("Abrir .md", self)
        open_action.triggered.connect(self.open_file)

        save_action = QAction("Guardar salida", self)
        save_action.triggered.connect(self.save_output)

        exit_action = QAction("Salir", self)
        exit_action.triggered.connect(self.close)

        paste_action = QAction("Pegar en entrada", self)
        paste_action.triggered.connect(self.paste_input)

        fix_action = QAction("Arreglar Markdown", self)
        fix_action.triggered.connect(self.fix_text)

        copy_action = QAction("Copiar salida", self)
        copy_action.triggered.connect(self.copy_output)

        clear_action = QAction("Limpiar todo", self)
        clear_action.triggered.connect(self.clear_all)

        file_menu.addAction(open_action)
        file_menu.addAction(save_action)
        file_menu.addSeparator()
        file_menu.addAction(exit_action)

        tools_menu.addAction(paste_action)
        tools_menu.addAction(fix_action)
        tools_menu.addAction(copy_action)
        tools_menu.addAction(clear_action)

    def open_file(self):
        file_path, _ = QFileDialog.getOpenFileName(
            self,
            "Abrir archivo Markdown",
            "",
            "Markdown (*.md);;Text files (*.txt);;Todos los archivos (*)",
        )
        if not file_path:
            return

        try:
            content = Path(file_path).read_text(encoding="utf-8")
            self.input_edit.setPlainText(content)
            self.current_input_file = file_path
            self.statusBar().showMessage(f"Archivo cargado: {file_path}")
        except UnicodeDecodeError:
            try:
                content = Path(file_path).read_text(encoding="latin-1")
                self.input_edit.setPlainText(content)
                self.current_input_file = file_path
                self.statusBar().showMessage(
                    f"Archivo cargado con codificación latin-1: {file_path}"
                )
            except Exception as e:
                QMessageBox.critical(self, "Error", f"No se pudo abrir el archivo:\n{e}")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"No se pudo abrir el archivo:\n{e}")

    def paste_input(self):
        clipboard = QApplication.clipboard()
        self.input_edit.setPlainText(clipboard.text())
        self.statusBar().showMessage("Texto pegado en la entrada")

    def fix_text(self):
        original = self.input_edit.toPlainText()
        if not original.strip():
            QMessageBox.information(self, "Aviso", "No hay texto en la entrada.")
            return

        fixed = fix_pmc_markdown(original)
        self.output_edit.setPlainText(fixed)

        in_len = len(original)
        out_len = len(fixed)
        self.statusBar().showMessage(
            f"Markdown arreglado. Caracteres: entrada={in_len}, salida={out_len}"
        )

    def copy_output(self):
        content = self.output_edit.toPlainText()
        if not content.strip():
            QMessageBox.information(self, "Aviso", "No hay texto corregido para copiar.")
            return

        QApplication.clipboard().setText(content)
        self.statusBar().showMessage("Salida copiada al portapapeles")

    def save_output(self):
        content = self.output_edit.toPlainText()
        if not content.strip():
            QMessageBox.information(self, "Aviso", "No hay salida para guardar.")
            return

        suggested_name = "referencias_arregladas.md"
        if self.current_input_file:
            p = Path(self.current_input_file)
            suggested_name = f"{p.stem}_arreglado.md"

        file_path, _ = QFileDialog.getSaveFileName(
            self,
            "Guardar salida",
            suggested_name,
            "Markdown (*.md);;Text files (*.txt);;Todos los archivos (*)",
        )
        if not file_path:
            return

        try:
            Path(file_path).write_text(content, encoding="utf-8")
            self.current_output_file = file_path
            self.statusBar().showMessage(f"Salida guardada en: {file_path}")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"No se pudo guardar el archivo:\n{e}")

    def clear_all(self):
        self.input_edit.clear()
        self.output_edit.clear()
        self.statusBar().showMessage("Campos limpiados")
        
    def remove_empty(self):
        text = self.output_edit.toPlainText()

        if not text.strip():
            QMessageBox.information(self, "Aviso", "No hay texto en la salida.")
            return

        cleaned = remove_empty_brackets(text)
        self.output_edit.setPlainText(cleaned)

        self.statusBar().showMessage("Corchetes vacíos eliminados")


def main():
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()