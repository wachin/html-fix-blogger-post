import sys
import json
from pathlib import Path

from bs4 import BeautifulSoup

from PyQt6.QtCore import QTranslator, QLocale, QLibraryInfo, QStandardPaths, QSize
from PyQt6.QtGui import QAction
from PyQt6.QtWidgets import (
    QApplication,
    QMainWindow,
    QWidget,
    QLabel,
    QLineEdit,
    QPushButton,
    QFileDialog,
    QVBoxLayout,
    QMessageBox,
    QToolBar,
)


# ============================================================
# CONFIGURACIÓN GENERAL FÁCIL DE EDITAR
# ============================================================

APP_NAME = "HtmlFixerPyQt6"
CONFIG_FILE_NAME = "config.json"

# Aquí puedes añadir fácilmente más etiquetas reconocidas
# para bloques de código tipo Markdown convertidos a HTML.
#
# Ejemplos:
#   "bash"
#   "sh"
#   "shell"
#   "cmd"
#   "powershell"
#   "python"
#
# Si luego quieres añadir otra, solo agrégala aquí:
#   "ruby", "javascript", etc.
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
# RUTAS Y CONFIGURACIÓN
# ============================================================

def obtener_directorio_config():
    """
    Devuelve la carpeta de configuración de la app.

    En Windows normalmente será AppData/Roaming.
    En Linux será la carpeta de configuración del usuario.
    """
    base_dir = QStandardPaths.writableLocation(
        QStandardPaths.StandardLocation.AppConfigLocation
    )

    if not base_dir:
        # Respaldo simple por si algo fallara
        base_dir = str(Path.home() / f".{APP_NAME.lower()}")

    config_dir = Path(base_dir)
    config_dir.mkdir(parents=True, exist_ok=True)
    return config_dir


def obtener_ruta_config():
    return obtener_directorio_config() / CONFIG_FILE_NAME


def cargar_configuracion():
    """
    Carga el archivo de configuración JSON.
    Si no existe o está dañado, usa valores por defecto.
    """
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
        # Si el archivo está corrupto, restauramos valores por defecto
        guardar_configuracion(DEFAULT_CONFIG)
        return DEFAULT_CONFIG.copy()


def guardar_configuracion(config):
    """
    Guarda la configuración en formato JSON.
    """
    config_path = obtener_ruta_config()
    with config_path.open("w", encoding="utf-8") as f:
        json.dump(config, f, indent=4, ensure_ascii=False)


# ============================================================
# FUNCIONES DE PROCESAMIENTO HTML
# ============================================================

def mejorar_elementos_code(html):
    """
    Mejora la apariencia de los elementos <code> simples.
    Aplica un estilo similar al de código pero más simple que los bloques <pre>.
    """
    soup = BeautifulSoup(html, 'html.parser')

    for code in soup.find_all('code'):
        if not code.find_parent('pre'):
            code['style'] = (
                "background: #f5f5f5; "
                "border: 1px solid #d0d0d0; "
                "border-radius: 3px; "
                "padding: 1px 4px; "
                "font-family: 'Ubuntu Mono', Consolas, monospace; font-weight: bold; "
                "color: #c7254e; "
                "font-size: 90%; "
            )
    return str(soup)


def es_pre_de_codigo_con_etiqueta(pre):
    """
    Determina si un <pre> parece corresponder a una caja de código Markdown
    con alguna de las etiquetas definidas en MARKDOWN_CODE_LABELS.

    Busca clases como:
      - sourceCode
      - language-bash
      - language-cmd
      - language-powershell
      - bash
      - cmd
      - powershell

    También revisa el <code> interno, por si la clase viene allí.
    """
    clases_pre = set(pre.get("class", []))

    code = pre.find("code")
    clases_code = set(code.get("class", [])) if code else set()

    todas = clases_pre | clases_code

    # Caso clásico de pandoc / resaltado
    if "sourceCode" in todas:
        return True

    # Reconocer language-bash, language-cmd, language-powershell, etc.
    for etiqueta in MARKDOWN_CODE_LABELS:
        if etiqueta in todas:
            return True
        if f"language-{etiqueta}" in todas:
            return True

    return False


def mejorar_caja_codigo(html):
    """
    Mejora la apariencia de cajas de código estilo Markdown.
    Reconoce:
    - pre.sourceCode
    - bloques con clases como language-bash, language-cmd, language-powershell
    - y etiquetas simples añadidas en MARKDOWN_CODE_LABELS
    """
    soup = BeautifulSoup(html, 'html.parser')

    for pre in soup.find_all('pre'):
        if not es_pre_de_codigo_con_etiqueta(pre):
            continue

        container = soup.new_tag('div', style=(
            "margin: 15px 0; "
            "border-radius: 6px; "
            "overflow: hidden; "
            "box-shadow: 0 4px 8px rgba(0,0,0,0.2);"
        ))
        pre.wrap(container)

        pre['style'] = (
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

        terminal_bar = soup.new_tag('div', style=(
            "background: #3a3a3a; "
            "height: 28px; "
            "display: flex; "
            "align-items: center; "
            "padding: 0 15px; "
            "border-bottom: 1px solid #2a2a2a; "
        ))

        for color in ['#FAD510', '#0066CC', '#CE1126']:
            dot = soup.new_tag('span', style=(
                f"background: {color}; "
                "width: 12px; "
                "height: 12px; "
                "border-radius: 50%; "
                "margin-right: 8px; "
            ))
            terminal_bar.append(dot)

        copy_btn = soup.new_tag('button', attrs={
            "type": "button",
            "class": "code-copy-btn",
            "title": "Copiar código",
            "aria-label": "Copiar código",
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
        copy_btn.string = "Copiar"
        terminal_bar.append(copy_btn)

        container.insert(0, terminal_bar)

        for code in pre.find_all('code'):
            code['style'] = "color: inherit; font-family: inherit;"

    return str(soup)


def mejorar_tablas(html, porcentaje_fuente):
    """Mejora la apariencia de las tablas en el HTML con scroll horizontal."""
    soup = BeautifulSoup(html, 'html.parser')

    for table in soup.find_all('table'):
        estilo_tabla = (
            "border-collapse: collapse; "
            "width: 100%; "
            "background-color: #ffffff; "
            "table-layout: auto; "
        )

        if porcentaje_fuente:
            estilo_tabla += f"font-size: {porcentaje_fuente}; "

        table['style'] = estilo_tabla

        for i, row in enumerate(table.find_all('tr')):
            if i == 0:
                row['style'] = (
                    "background-color: #ececec; "
                    "color: #1f2d3d; "
                    "font-weight: bold;"
                )
            elif i % 2 == 1:
                row['style'] = "background-color: #ffffff;"
            else:
                row['style'] = "background-color: #f5f5f5;"

        for th in table.find_all('th'):
            th['style'] = (
                "border: 1px solid #cfcfcf; "
                "padding: 14px 16px; "
                "text-align: left; "
                "vertical-align: top; "
                "white-space: normal; "
                "overflow-wrap: break-word; "
                "word-break: normal; "
                "max-width: 220px;"
            )

        for td in table.find_all('td'):
            td['style'] = (
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

        wrapper = soup.new_tag(
            'div',
            attrs={
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
            }
        )

        table.insert_before(wrapper)
        wrapper.append(table.extract())

    return str(soup)


def mejorar_bloques_code_simples(html):
    """
    Mejora la apariencia de los bloques <pre><code> simples que no tienen
    etiqueta reconocible ni clase sourceCode.
    """
    soup = BeautifulSoup(html, 'html.parser')

    for pre in soup.find_all('pre'):
        if es_pre_de_codigo_con_etiqueta(pre):
            continue

        if pre.code and not pre.get('class'):
            div = soup.new_tag('div')
            pre.wrap(div)

            pre['style'] = (
                "background-color: #f8f8f8; "
                "border: 1px solid #d0d0d0; "
                "border-left: 6px solid #d44950; "
                "line-height: 1.5; "
                "margin: 10px 0; "
                "overflow-x: auto; "
                "padding: 10px; "
                "border-radius: 4px; "
            )

            span_outer = soup.new_tag('span', style=(
                "color: #000000; "
                "font-family: 'Ubuntu Mono', Consolas, monospace; "
            ))

            span_inner = soup.new_tag('span', style=(
                "font-size: 15px; "
                "white-space: pre; "
            ))

            code = pre.code
            span_inner.string = code.get_text()

            span_outer.append(span_inner)
            pre.clear()
            pre.append(span_outer)

    return str(soup)


# ============================================================
# INTERFAZ
# ============================================================

class HtmlFixerApp(QMainWindow):
    def __init__(self):
        super().__init__()

        self.translator = QTranslator()
        self.cargar_traducciones_qt()

        self.config = cargar_configuracion()

        self.setWindowTitle("Mejorador de HTML")
        self.resize(520, 260)

        self.init_ui()
        self.centrar_ventana()

    def centrar_ventana(self):
        """
        Centra la ventana principal en la pantalla.
        """
        frame = self.frameGeometry()
        screen = QApplication.primaryScreen()
        centro_pantalla = screen.availableGeometry().center()
        frame.moveCenter(centro_pantalla)
        self.move(frame.topLeft())

    def mostrar_acerca_de(self):
        texto = (
            "<b>HTML Blogger Fixer PyQt6</b><br><br>"
            "<b>Desarrollador:</b> Washington Indacochea Delgado<br>"
            "<b>Correo:</b> linuxfrontier@proton.me<br>"
            "<b>Página web:</b> "
            "<a href='https://github.com/wachin/html-fix-blogger-post'>"
            "https://github.com/wachin/html-fix-blogger-post</a><br><br>"
            "<b>Tecnología usada:</b><br>"
            "- Python 3<br>"
            "- PyQt6<br>"
            "- BeautifulSoup4<br>"
            "- JSON para configuración<br>"
        )

        msg = QMessageBox(self)
        msg.setWindowTitle("Acerca de...")
        msg.setTextFormat(msg.textFormat().RichText)
        msg.setText(texto)
        msg.setStandardButtons(QMessageBox.StandardButton.Ok)
        msg.exec()

    def cargar_traducciones_qt(self):
        """
        Carga las traducciones de Qt para que los diálogos del sistema Qt
        aparezcan en el idioma configurado, siempre que esté instalado
        qt6-translations-l10n.
        """
        translations_path = QLibraryInfo.path(
            QLibraryInfo.LibraryPath.TranslationsPath
        )

        locale_name = QLocale.system().name()          # ej: es_EC
        locale_short = locale_name.split("_")[0]      # ej: es

        candidatos = [
            f"qtbase_{locale_name}",
            f"qtbase_{locale_short}",
        ]

        cargado = False
        for nombre in candidatos:
            if self.translator.load(nombre, translations_path):
                QApplication.installTranslator(self.translator)
                print(f"Traducción cargada correctamente: {nombre}")
                cargado = True
                break

        if not cargado:
            print("No se pudo cargar la traducción de Qt.")
            print(f"Ruta de traducciones: {translations_path}")

    def init_ui(self):
        # Barra superior debajo de la barra de título
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

        self.label_fuente = QLabel(
            "Elije el tamaño de la fuente de la tabla (ej: 90%, 100%, etc):"
        )
        layout.addWidget(self.label_fuente)

        self.entry_fuente = QLineEdit()
        self.entry_fuente.setText(self.config.get("table_font_size", "90%"))
        layout.addWidget(self.entry_fuente)

        self.boton_procesar = QPushButton("Seleccionar archivo HTML")
        self.boton_procesar.clicked.connect(self.procesar_archivo)
        layout.addWidget(self.boton_procesar)

        self.resultado_label = QLabel("")
        self.resultado_label.setWordWrap(True)
        layout.addWidget(self.resultado_label)

        self.info_config_label = QLabel(
            f"Archivo de configuración:\n{obtener_ruta_config()}"
        )
        self.info_config_label.setWordWrap(True)
        layout.addWidget(self.info_config_label)

        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)

    def normalizar_porcentaje_fuente(self, texto):
        """
        Si el usuario escribe 90 en vez de 90%, lo corrige automáticamente.
        """
        texto = texto.strip()
        if texto and not texto.endswith('%'):
            texto += '%'
        return texto

    def guardar_preferencia_fuente(self):
        valor = self.normalizar_porcentaje_fuente(self.entry_fuente.text())
        self.entry_fuente.setText(valor)
        self.config["table_font_size"] = valor
        guardar_configuracion(self.config)

    def procesar_archivo(self):
        self.guardar_preferencia_fuente()
        porcentaje_fuente = self.config.get("table_font_size", "90%")

        dialogo = QFileDialog(self, "Seleccionar archivo HTML")
        dialogo.setFileMode(QFileDialog.FileMode.ExistingFile)
        dialogo.setNameFilter("Archivos HTML (*.html *.htm)")
        dialogo.resize(900, 600)  # aquí controlas el tamaño
        dialogo.setViewMode(QFileDialog.ViewMode.Detail)

        if not dialogo.exec():
            return

        archivos = dialogo.selectedFiles()
        if not archivos:
            return

        filepath = archivos[0]

        try:
            ruta_entrada = Path(filepath)

            with ruta_entrada.open('r', encoding='utf-8') as file:
                html = file.read()

            html = mejorar_elementos_code(html)
            html = mejorar_caja_codigo(html)
            html = mejorar_tablas(html, porcentaje_fuente)
            html = mejorar_bloques_code_simples(html)

            ruta_salida = ruta_entrada.with_name(f"{ruta_entrada.stem}-fix.html")

            with ruta_salida.open('w', encoding='utf-8') as file:
                file.write(html)

            self.resultado_label.setText(f"Archivo guardado en:\n{ruta_salida}")

            QMessageBox.information(
                self,
                "Proceso completado",
                f"Archivo guardado correctamente en:\n{ruta_salida}"
            )

        except Exception as e:
            QMessageBox.critical(
                self,
                "Error",
                f"Ocurrió un error al procesar el archivo:\n{e}"
            )

def main():
    app = QApplication(sys.argv)
    ventana = HtmlFixerApp()
    ventana.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
