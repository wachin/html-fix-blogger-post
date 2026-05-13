#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
CLI HTML Blogger Fixer

Versión de línea de comandos equivalente al procesamiento usado por
html_blogger_fixer.py, sin interfaz gráfica PyQt6.
"""

import argparse
import sys
import json
import os
from pathlib import Path
from bs4 import BeautifulSoup

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

    En Windows usa AppData/Roaming.
    En Linux usa ~/.config.
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

    Usa una clase CSS llamada simple-code-box para que Blogger no destruya
    tan fácilmente el estilo al editar en Vista de redacción.
    """
    soup = BeautifulSoup(html, 'html.parser')

    for pre in soup.find_all('pre'):
        if es_pre_de_codigo_con_etiqueta(pre):
            continue

        if pre.code and not pre.get('class'):
            pre['class'] = pre.get('class', []) + ['simple-code-box']

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
                "font-size: 15px; "
                "white-space: pre; "
            ))

            code = pre.code
            span_outer.string = code.get_text()

            pre.clear()
            pre.append(span_outer)

    return str(soup)



# ============================================================
# FUNCIONES CLI
# ============================================================

def normalizar_porcentaje_fuente(texto):
    """
    Si el usuario escribe 90 en vez de 90%, lo corrige automáticamente.
    Respeta valores con unidades CSS como 1em, 14px, small, etc.
    """
    if texto is None:
        return DEFAULT_CONFIG["table_font_size"]

    texto = str(texto).strip()
    if not texto:
        return DEFAULT_CONFIG["table_font_size"]

    # Si es solo número, asumimos porcentaje.
    if texto.replace('.', '', 1).isdigit():
        texto += '%'

    return texto


def obtener_ruta_salida(input_file, output_file=None):
    """
    Si no se indica archivo de salida, crea uno con sufijo -fix.
    ejemplo: archivo.html -> archivo-fix.html
    """
    entrada = Path(input_file)

    if output_file:
        return Path(output_file)

    return entrada.with_name(f"{entrada.stem}-fix{entrada.suffix}")


def procesar_archivo(input_file, output_file=None, font=None, guardar_config=True):
    """
    Procesa el archivo HTML indicado:
    - Aplica mejoras en <code> inline
    - Aplica cajas de código tipo terminal a bloques reconocidos
    - Aplica mejoras a tablas
    - Aplica estilo simple-code-box a bloques <pre><code> simples
    """
    ruta_entrada = Path(input_file)

    if not ruta_entrada.exists():
        raise FileNotFoundError(f"No existe el archivo de entrada: {ruta_entrada}")

    if not ruta_entrada.is_file():
        raise IsADirectoryError(f"La ruta indicada no es un archivo: {ruta_entrada}")

    config = cargar_configuracion()
    porcentaje_fuente = normalizar_porcentaje_fuente(
        font if font is not None else config.get("table_font_size", "90%")
    )

    if guardar_config:
        config["table_font_size"] = porcentaje_fuente
        guardar_configuracion(config)

    ruta_salida = obtener_ruta_salida(ruta_entrada, output_file)

    with ruta_entrada.open('r', encoding='utf-8') as file:
        html = file.read()

    html = mejorar_elementos_code(html)
    html = mejorar_caja_codigo(html)
    html = mejorar_tablas(html, porcentaje_fuente)
    html = mejorar_bloques_code_simples(html)

    ruta_salida.parent.mkdir(parents=True, exist_ok=True)
    with ruta_salida.open('w', encoding='utf-8') as file:
        file.write(html)

    return ruta_salida, porcentaje_fuente


def crear_parser():
    parser = argparse.ArgumentParser(
        description="Mejora archivos HTML para publicaciones de Blogger.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Ejemplos:
  python3 cli_html_fixer.py entrada.html
  python3 cli_html_fixer.py entrada.html -o salida.html
  python3 cli_html_fixer.py entrada.html -f 90%
  python3 cli_html_fixer.py entrada.html --font 95 --output salida.html
  python3 cli_html_fixer.py --show-config

Notas:
  - Si no se indica salida, se crea archivo-fix.html.
  - Si el tamaño de fuente es solo número, ejemplo 90, se interpreta como 90%.
  - El tamaño de fuente queda guardado en el config.json de la aplicación.
        """
    )

    parser.add_argument(
        "input_file",
        nargs="?",
        help="Archivo HTML de entrada"
    )

    parser.add_argument(
        "-o", "--output",
        help="Archivo HTML de salida. Si no se indica, se usa el sufijo -fix."
    )

    parser.add_argument(
        "-f", "--font",
        help="Tamaño de fuente para tablas. Ejemplos: 90%, 95, 1em, 14px."
    )

    parser.add_argument(
        "--no-save-config",
        action="store_true",
        help="No guardar el tamaño de fuente usado en config.json."
    )

    parser.add_argument(
        "--show-config",
        action="store_true",
        help="Muestra la ruta del archivo de configuración y sale."
    )

    return parser


def main():
    parser = crear_parser()
    args = parser.parse_args()

    if args.show_config:
        print(f"Archivo de configuración: {obtener_ruta_config()}")
        print(f"Configuración actual: {cargar_configuracion()}")
        return 0

    if not args.input_file:
        parser.print_help()
        return 1

    try:
        salida, fuente = procesar_archivo(
            input_file=args.input_file,
            output_file=args.output,
            font=args.font,
            guardar_config=not args.no_save_config,
        )
        print(f"✔ Archivo generado: {salida}")
        print(f"✔ Tamaño de fuente de tablas usado: {fuente}")
        print(f"✔ Archivo de configuración: {obtener_ruta_config()}")
        return 0

    except Exception as e:
        print(f"❌ Error: {e}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
