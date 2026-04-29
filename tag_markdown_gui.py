#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Tag Markdown GUI - PyQt6

Cuando transformas una página web a Markdown con servicios como
https://urltomarkdown.com/, muchas veces los bloques de código quedan así:

```
sudo apt update
```

Para que luego Pandoc conserve correctamente el lenguaje al convertir a HTML,
conviene que el bloque tenga una etiqueta:

```bash
sudo apt update
```

Este programa añade automáticamente una etiqueta a los bloques de código
Markdown que NO tienen lenguaje.

Copyright: Washington Indacochea Delgado
Correo: linuxfrontier@proton.me
"""

import sys
import re
import json
import os
from pathlib import Path

from PyQt6.QtCore import QTranslator, QLocale, QLibraryInfo
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
    QComboBox,
    QMessageBox,
    QToolBar,
)


# ============================================================
# CONFIGURACIÓN GENERAL
# ============================================================

APP_NAME = "TagMarkdownPyQt6"
CONFIG_FILE_NAME = "config.json"

# Etiquetas disponibles para añadir a los bloques Markdown sin lenguaje.
# Puedes agregar más si lo necesitas, por ejemplo:
# "javascript", "css", "json", "xml", "yaml", "ini", etc.
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
# CONFIGURACIÓN EN APPDATA / .config
# ============================================================

def obtener_directorio_config():
    """
    Devuelve la carpeta de configuración de la app.

    En Windows usa:
        AppData/Roaming/TagMarkdownPyQt6

    En Linux usa:
        ~/.config/TagMarkdownPyQt6
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


def obtener_ruta_config():
    return obtener_directorio_config() / CONFIG_FILE_NAME


def cargar_configuracion():
    config_path = obtener_ruta_config()

    if not config_path.exists():
        guardar_configuracion(DEFAULT_CONFIG)
        return DEFAULT_CONFIG.copy()

    try:
        with config_path.open("r", encoding="utf-8") as f:
            data = json.load(f)

        config = DEFAULT_CONFIG.copy()
        config.update(data)
        return config

    except Exception:
        guardar_configuracion(DEFAULT_CONFIG)
        return DEFAULT_CONFIG.copy()


def guardar_configuracion(config):
    config_path = obtener_ruta_config()
    with config_path.open("w", encoding="utf-8") as f:
        json.dump(config, f, indent=4, ensure_ascii=False)


# ============================================================
# PROCESAMIENTO MARKDOWN
# ============================================================

def process_markdown(content, selected_lang):
    """
    Añade una etiqueta de lenguaje a bloques de código Markdown sin etiqueta.

    Convierte esto:

        ```
        sudo apt update
        ```

    En esto:

        ```bash
        sudo apt update
        ```

    Importante:
    - Solo modifica bloques sin lenguaje.
    - No toca bloques que ya tienen etiqueta, por ejemplo:
      ```python
      print("Hola")
      ```
    """

    # Este patrón busca bloques que empiezan exactamente con ```
    # seguido de espacios opcionales y salto de línea.
    # Es decir, bloques SIN lenguaje.
    pattern = r"```[ \t]*\n([\s\S]*?)```"

    def replace_block(match):
        code_content = match.group(1).strip("\n")
        return f"```{selected_lang}\n{code_content}\n```"

    return re.sub(pattern, replace_block, content)


def generar_ruta_salida(input_path):
    """
    Genera archivo de salida con sufijo -taged.md
    respetando el nombre original.
    """
    ruta = Path(input_path)
    return ruta.with_name(f"{ruta.stem}-taged{ruta.suffix}")


# ============================================================
# INTERFAZ PYQT6
# ============================================================

class TagMarkdownApp(QMainWindow):
    def __init__(self):
        super().__init__()

        self.translator = QTranslator()
        self.cargar_traducciones_qt()

        self.config = cargar_configuracion()

        self.setWindowTitle("Etiquetador de Bloques de Código Markdown")
        self.resize(620, 260)

        self.init_ui()
        self.centrar_ventana()

    def cargar_traducciones_qt(self):
        """
        Carga traducciones de Qt si están disponibles.

        En Debian/MX Linux se recomienda instalar:
            sudo apt install qt6-translations-l10n

        Esto ayuda a que diálogos como QFileDialog aparezcan en español.
        """
        translations_path = QLibraryInfo.path(
            QLibraryInfo.LibraryPath.TranslationsPath
        )

        locale_name = QLocale.system().name()      # ej: es_EC
        locale_short = locale_name.split("_")[0]  # ej: es

        candidatos = [
            f"qtbase_{locale_name}",
            f"qtbase_{locale_short}",
        ]

        for nombre in candidatos:
            if self.translator.load(nombre, translations_path):
                QApplication.installTranslator(self.translator)
                print(f"Traducción Qt cargada: {nombre}")
                return

        print("No se pudo cargar traducción Qt.")
        print(f"Ruta de traducciones: {translations_path}")

    def centrar_ventana(self):
        """
        Centra la ventana principal en la pantalla.
        """
        frame = self.frameGeometry()
        screen = QApplication.primaryScreen()
        centro_pantalla = screen.availableGeometry().center()
        frame.moveCenter(centro_pantalla)
        self.move(frame.topLeft())

    def init_ui(self):
        # Barra superior
        self.toolbar = QToolBar("Barra principal")
        self.toolbar.setMovable(False)
        self.toolbar.setFloatable(False)
        self.addToolBar(self.toolbar)

        self.boton_acerca_de = QPushButton("Acerca de...")
        self.boton_acerca_de.clicked.connect(self.mostrar_acerca_de)
        self.toolbar.addWidget(self.boton_acerca_de)

        # Widget central
        central_widget = QWidget()
        layout = QVBoxLayout()

        descripcion = QLabel(
            "Selecciona un archivo Markdown y elige la etiqueta que se añadirá "
            "a los bloques de código que no tengan lenguaje."
        )
        descripcion.setWordWrap(True)
        layout.addWidget(descripcion)

        # Ruta del archivo
        fila_archivo = QHBoxLayout()

        self.entry_file = QLineEdit()
        self.entry_file.setPlaceholderText("Selecciona un archivo .md")
        fila_archivo.addWidget(self.entry_file)

        self.btn_browse = QPushButton("Buscar archivo .md")
        self.btn_browse.clicked.connect(self.open_file)
        fila_archivo.addWidget(self.btn_browse)

        layout.addLayout(fila_archivo)

        # Selector de lenguaje
        fila_lenguaje = QHBoxLayout()

        label_lang = QLabel("Etiqueta:")
        fila_lenguaje.addWidget(label_lang)

        self.combo_lang = QComboBox()
        self.combo_lang.addItems(LANGUAGES)

        last_lang = self.config.get("last_language", "bash")
        if last_lang in LANGUAGES:
            self.combo_lang.setCurrentText(last_lang)
        else:
            self.combo_lang.setCurrentText("bash")

        fila_lenguaje.addWidget(self.combo_lang)
        layout.addLayout(fila_lenguaje)

        # Botón procesar
        self.btn_process = QPushButton("Procesar")
        self.btn_process.clicked.connect(self.process_file)
        layout.addWidget(self.btn_process)

        self.resultado_label = QLabel("")
        self.resultado_label.setWordWrap(True)
        layout.addWidget(self.resultado_label)

        self.config_label = QLabel(f"Configuración:\n{obtener_ruta_config()}")
        self.config_label.setWordWrap(True)
        layout.addWidget(self.config_label)

        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)

    def mostrar_acerca_de(self):
        texto = (
            "<b>Tag Markdown GUI - PyQt6</b><br><br>"
            "<b>Desarrollador:</b> Washington Indacochea Delgado<br>"
            "<b>Correo:</b> linuxfrontier@proton.me<br><br>"
            "<b>Función:</b><br>"
            "Añade etiquetas como <code>bash</code>, <code>python</code>, "
            "<code>cmd</code> o <code>powershell</code> a bloques de código "
            "Markdown sin lenguaje.<br><br>"
            "<b>Tecnología usada:</b><br>"
            "- Python 3<br>"
            "- PyQt6<br>"
            "- Expresiones regulares<br>"
            "- JSON para configuración<br>"
        )

        msg = QMessageBox(self)
        msg.setWindowTitle("Acerca de...")
        msg.setTextFormat(msg.textFormat().RichText)
        msg.setText(texto)
        msg.setStandardButtons(QMessageBox.StandardButton.Ok)
        msg.exec()

    def open_file(self):
        last_directory = self.config.get("last_directory", "")

        dialogo = QFileDialog(self, "Seleccionar archivo Markdown")
        dialogo.setFileMode(QFileDialog.FileMode.ExistingFile)
        dialogo.setNameFilter("Archivos Markdown (*.md *.markdown)")
        dialogo.resize(900, 600)
        dialogo.setViewMode(QFileDialog.ViewMode.Detail)

        if last_directory and Path(last_directory).exists():
            dialogo.setDirectory(last_directory)

        if not dialogo.exec():
            return

        archivos = dialogo.selectedFiles()
        if not archivos:
            return

        file_path = archivos[0]
        self.entry_file.setText(file_path)

        self.config["last_directory"] = str(Path(file_path).parent)
        guardar_configuracion(self.config)

    def process_file(self):
        file_path = self.entry_file.text().strip()
        selected_lang = self.combo_lang.currentText().strip()

        if not file_path:
            QMessageBox.warning(
                self,
                "Entrada inválida",
                "Por favor selecciona un archivo Markdown."
            )
            return

        ruta_entrada = Path(file_path)

        if not ruta_entrada.exists() or ruta_entrada.suffix.lower() not in [".md", ".markdown"]:
            QMessageBox.warning(
                self,
                "Entrada inválida",
                "Por favor selecciona un archivo .md o .markdown válido."
            )
            return

        try:
            content = ruta_entrada.read_text(encoding="utf-8")
        except Exception as e:
            QMessageBox.critical(
                self,
                "Error",
                f"No se pudo leer el archivo:\n{e}"
            )
            return

        processed_content = process_markdown(content, selected_lang)
        output_path = generar_ruta_salida(ruta_entrada)

        try:
            output_path.write_text(processed_content, encoding="utf-8")
        except Exception as e:
            QMessageBox.critical(
                self,
                "Error",
                f"No se pudo guardar el archivo:\n{e}"
            )
            return

        self.config["last_language"] = selected_lang
        self.config["last_directory"] = str(ruta_entrada.parent)
        guardar_configuracion(self.config)

        self.resultado_label.setText(f"Archivo guardado como:\n{output_path}")

        QMessageBox.information(
            self,
            "Éxito",
            f"Archivo guardado como:\n{output_path}"
        )


def main():
    app = QApplication(sys.argv)
    ventana = TagMarkdownApp()
    ventana.show()
    ventana.centrar_ventana()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
