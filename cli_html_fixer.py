#!/usr/bin/env python3
import sys
import os
from bs4 import BeautifulSoup

# -----------------------------
# Estilo para <code> inline
# -----------------------------
def mejorar_elementos_code(html):
    """
    Mejora la apariencia de los elementos <code> simples.
    Aplica un estilo similar al de código pero más simple que los bloques <pre>
    """
    soup = BeautifulSoup(html, 'html.parser')

    for code in soup.find_all('code'):
        # Si el elemento code no está dentro de un pre (para no duplicar estilos)
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

# -----------------------------
# Caja negra tipo terminal 🇪🇨
# -----------------------------
def mejorar_caja_codigo(html):
    """
    Caja de codigo negra, con botones con el color de la bandera del Ecuador
    Mejora la apariencia de las cajas de código <pre class="sourceCode">.
    Versión ajustada sin separación entre la barra y el contenido.
    """
    soup = BeautifulSoup(html, 'html.parser')

    for pre in soup.find_all('pre', class_='sourceCode'):
        # Primero creamos un contenedor para agrupar la barra y el contenido
        container = soup.new_tag('div', style=(
            "margin: 15px 0; "
            "border-radius: 6px; "
            "overflow: hidden; "
            "box-shadow: 0 4px 8px rgba(0,0,0,0.2);"
        ))
        pre.wrap(container)

        # Estilo mejorado para el pre (contenido del código)
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

        # Barra de terminal ajustada
        terminal_bar = soup.new_tag('div', style=(
            "background: #3a3a3a; "
            "height: 28px; "
            "display: flex; "
            "align-items: center; "
            "padding: 0 15px; "
            "border-bottom: 1px solid #2a2a2a; "
        ))

        # Puntos de la barra de terminal
        for color in ['#FAD510', '#0066CC', '#CE1126']:
            dot = soup.new_tag('span', style=(
                f"background: {color}; "
                "width: 12px; "
                "height: 12px; "
                "border-radius: 50%; "
                "margin-right: 8px; "
            ))
            terminal_bar.append(dot)

        # --- Botón "Copiar" ---
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

        # Insertamos la barra antes del pre dentro del contenedor
        container.insert(0, terminal_bar)

        # Ajustamos el código interno
        for code in pre.find_all('code'):
            code['style'] = "color: inherit; font-family: inherit;"

    return str(soup)

# -----------------------------
# Tablas
# -----------------------------
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

# -----------------------------
# Bloques <pre><code> simples
# -----------------------------
def mejorar_bloques_code_simples(html):
    """
    Mejora la apariencia de los bloques <pre><code> simples que no tienen clase sourceCode. Los que
    vienen de la conversión de bloques de códog markdown sin tag, ejemplo:
    ```
    sudo apt update
    ```
    Esta es la versión mejorada con mejor contraste y legibilidad.
    """
    soup = BeautifulSoup(html, 'html.parser')

    for pre in soup.find_all('pre'):
        # Solo procesamos los pre que contienen code directamente y no son de clase sourceCode
        if pre.code and not pre.get('class'):
            # Creamos el nuevo div contenedor
            div = soup.new_tag('div')
            pre.wrap(div)

            # Estilo mejorado para el pre
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

            # Creamos el span para el contenido con mejor contraste
            span_outer = soup.new_tag('span', style=(
                "color: #000000; "
                "font-family: 'Ubuntu Mono', Consolas, monospace; "
            ))

            span_inner = soup.new_tag('span', style=(
                "font-size: 15px; "
                "white-space: pre; "
            ))

            # Movemos el contenido del code al span interno
            code = pre.code
            span_inner.string = code.get_text()

            # Reconstruimos la estructura
            span_outer.append(span_inner)
            pre.clear()
            pre.append(span_outer)

    return str(soup)

# -----------------------------
# Procesador
# -----------------------------
def procesar_archivo(input_file, output_file, font):
    """
    Procesa el archivo HTML indicado:
    - Aplica mejoras en cajas de código, elementos code y tablas
    - Guarda el resultado en un archivo con sufijo '-fix.html' si no se indica otro
    """
    if font and not font.endswith('%') and not any(ch.isalpha() for ch in font):
        font += '%'

    with open(input_file, 'r', encoding='utf-8') as f:
        html = f.read()

    html = mejorar_elementos_code(html)
    html = mejorar_caja_codigo(html)
    html = mejorar_tablas(html, font)
    html = mejorar_bloques_code_simples(html)

    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(html)

    print(f"✔ Archivo generado: {output_file}")

# -----------------------------
# Ayuda
# -----------------------------
def mostrar_ayuda():
    print("""
Uso:
  python3 cli_html_fixer_corregido.py [opciones] archivo.html

Opciones:
  -o, --output   Archivo de salida
  -f, --font     Tamaño de fuente de tablas (ej: 90%, 1em)
  -h, --help     Mostrar esta ayuda

Ejemplos:
  python3 cli_html_fixer_corregido.py entrada.html
  python3 cli_html_fixer_corregido.py -o salida.html -f 95% entrada.html
""")

# -----------------------------
# Main
# -----------------------------
def main():
    if len(sys.argv) < 2 or '-h' in sys.argv or '--help' in sys.argv:
        mostrar_ayuda()
        return

    input_file = None
    output_file = None
    font = "80%"

    i = 1
    while i < len(sys.argv):
        arg = sys.argv[i]
        if arg in ('-o', '--output'):
            if i + 1 >= len(sys.argv):
                print("❌ Falta indicar el archivo de salida después de -o/--output")
                return
            output_file = sys.argv[i + 1]
            i += 2
        elif arg in ('-f', '--font'):
            if i + 1 >= len(sys.argv):
                print("❌ Falta indicar el tamaño de fuente después de -f/--font")
                return
            font = sys.argv[i + 1]
            i += 2
        else:
            input_file = arg
            i += 1

    if not input_file or not os.path.exists(input_file):
        print("❌ Archivo de entrada inválido")
        return

    if not output_file:
        base, ext = os.path.splitext(input_file)
        output_file = f"{base}-fix{ext}"

    procesar_archivo(input_file, output_file, font)

if __name__ == "__main__":
    main()
