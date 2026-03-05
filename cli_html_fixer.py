#!/usr/bin/env python3
import sys
import os
from bs4 import BeautifulSoup

# -----------------------------
# Estilo para <code> inline
# -----------------------------
def mejorar_elementos_code(html):
    soup = BeautifulSoup(html, 'html.parser')
    for code in soup.find_all('code'):
        if not code.find_parent('pre'):
            code['style'] = (
                "background:#f5f5f5;"
                "border:1px solid #d0d0d0;"
                "border-radius:3px;"
                "padding:1px 4px;"
                "font-family:'Ubuntu Mono',Consolas,monospace;"
                "color:#c7254e;"
                "font-size:90%;"
            )
    return str(soup)

# -----------------------------
# Caja negra tipo terminal 🇪🇨
# -----------------------------
def mejorar_caja_codigo(html):
    soup = BeautifulSoup(html, 'html.parser')

    for pre in soup.find_all('pre', class_='sourceCode'):
        container = soup.new_tag('div', style=(
            "margin:15px 0;"
            "border-radius:6px;"
            "overflow:hidden;"
            "box-shadow:0 4px 8px rgba(0,0,0,0.2);"
        ))
        pre.wrap(container)

        pre['style'] = (
            "background:#1e1e1e;"
            "color:#f0f0f0;"
            "font-family:'Ubuntu Mono','Courier New',monospace;"
            "font-weight:bold;"
            "font-size:14px;"
            "line-height:1.5;"
            "margin:0;"
            "padding:12px 20px;"
            "border-left:4px solid #3aa655;"
            "overflow:auto;"
            "max-height:500px;"
        )

        bar = soup.new_tag('div', style=(
            "background:#3a3a3a;"
            "height:28px;"
            "display:flex;"
            "align-items:center;"
            "padding:0 15px;"
            "border-bottom:1px solid #2a2a2a;"
        ))

        for color in ['#FAD510', '#0066CC', '#CE1126']:
            dot = soup.new_tag('span', style=(
                f"background:{color};"
                "width:12px;"
                "height:12px;"
                "border-radius:50%;"
                "margin-right:8px;"
            ))
            bar.append(dot)

        container.insert(0, bar)

        for code in pre.find_all('code'):
            code['style'] = "color:inherit;font-family:inherit;"

    return str(soup)

# -----------------------------
# Tablas
# -----------------------------
def mejorar_tablas(html, porcentaje):
    soup = BeautifulSoup(html, 'html.parser')

    for table in soup.find_all('table'):
        table['style'] = (
            "border-collapse:collapse;"
            "width:100%;"
            f"font-size:{porcentaje};"
        )

        for i, row in enumerate(table.find_all('tr')):
            if i == 0:
                row['style'] = "background:black;color:white;font-weight:bold;"
            elif i % 2 == 0:
                row['style'] = "background:#e6e6e6;"
            else:
                row['style'] = "background:#ffffff;"

        for td in table.find_all(['td','th']):
            td['style'] = "border:1px solid black;padding:8px;text-align:left;"

    return str(soup)

# -----------------------------
# Bloques <pre><code> simples
# -----------------------------
def mejorar_bloques_code_simples(html):
    soup = BeautifulSoup(html, 'html.parser')

    for pre in soup.find_all('pre'):
        if pre.code and not pre.get('class'):
            wrapper = soup.new_tag('div')
            pre.wrap(wrapper)

            pre['style'] = (
                "background:#f8f8f8;"
                "border:1px solid #d0d0d0;"
                "border-left:3px solid #d44950;"
                "padding:10px;"
                "border-radius:4px;"
                "line-height:1.5;"
            )

            span = soup.new_tag('span', style=(
                "color:#222;"
                "font-family:'Ubuntu Mono','Courier New',monospace;"
                "font-size:15px;"
                "white-space:pre-wrap;"
            ))

            span.string = pre.get_text()
            pre.clear()
            pre.append(span)

    return str(soup)

# -----------------------------
# Procesador
# -----------------------------
def procesar_archivo(input_file, output_file, font):
    with open(input_file, 'r', encoding='utf-8') as f:
        html = f.read()

    html = mejorar_elementos_code(html)
    html = mejorar_caja_codigo(html)
    html = mejorar_tablas(html, font)
    html = mejorar_bloques_code_simples(html)

    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(html)

    print("✔ Archivo generado:", output_file)

# -----------------------------
# Ayuda
# -----------------------------
def mostrar_ayuda():
    print("""
Uso:
  python3 cli_html_fixer_pro.py [opciones] archivo.html

Opciones:
  -o, --output   Archivo de salida
  -f, --font     Tamaño de fuente de tablas (ej: 90%, 1em)
  -h, --help     Mostrar esta ayuda

Ejemplos:
  python3 cli_html_fixer_pro.py entrada.html
  python3 cli_html_fixer_pro.py -o salida.html -f 95% entrada.html
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
        if arg in ('-o','--output'):
            output_file = sys.argv[i+1]
            i += 2
        elif arg in ('-f','--font'):
            font = sys.argv[i+1]
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
