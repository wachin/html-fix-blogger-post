#!/usr/bin/env python3
import sys
import os
from bs4 import BeautifulSoup

def mejorar_elementos_code(html):
    """Mejora la apariencia de los elementos <code> simples"""
    soup = BeautifulSoup(html, 'html.parser')
    
    for code in soup.find_all('code'):
        if not code.find_parent('pre'):
            code['style'] = (
                "background: #f5f5f5; "
                "border: 1px solid #d0d0d0; "
                "border-radius: 3px; "
                "padding: 1px 4px; "
                "font-family: 'Ubuntu', Console, monospace; "
                "color: #c7254e; "
                "font-size: 90%;"
            )
    return str(soup)

def mejorar_caja_codigo(html):
    """Mejora la apariencia de las cajas de código <pre class='sourceCode'>"""
    soup = BeautifulSoup(html, 'html.parser')
    
    for pre in soup.find_all('pre', class_='sourceCode'):
        pre['style'] = (
            "background: rgb(231, 232, 233); "
            "border-color: rgb(214, 73, 55); "
            "border-style: solid; "
            "border-width: 1px 1px 1px 20px; "
            "font-family: 'Ubuntu Mono', Console, monospace; "
            "font-size: medium; line-height: 22.4px; "
            "margin: 10px; max-height: 500px; overflow: auto; "
            "padding: 28px 10px 10px 20px; z-index: 10000;"
        )
    return str(soup)

def mejorar_tablas(html, porcentaje_fuente="80%"):
    """Mejora la apariencia de las tablas HTML"""
    soup = BeautifulSoup(html, 'html.parser')
    
    for table in soup.find_all('table'):
        estilo_base = (
            "border-collapse: collapse; width: 100%; table-layout: auto; "
            "white-space: normal; word-break: normal; overflow-wrap: break-word; "
            f"border: 1px solid #333333; font-size: {porcentaje_fuente};"
        )
        table['style'] = estilo_base

        for i, row in enumerate(table.find_all('tr')):
            if i == 0:
                row['style'] = "background-color: #fcebea;"
            elif i % 2 == 1:
                row['style'] = "background-color: #ffffff;"
            else:
                row['style'] = "background-color: #f9f9f9;"

        for th in table.find_all('th'):
            th['style'] = (
                "border: 1px solid #333333; padding: 8px; text-align: left; "
                "white-space: normal; word-break: normal; overflow-wrap: break-word;"
            )

        for td in table.find_all('td'):
            td['style'] = (
                "border: 1px solid #333333; padding: 8px; text-align: left; "
                "white-space: normal; word-break: normal; overflow-wrap: break-word;"
            )

        wrapper = soup.new_tag('div', **{
            "style": "width: 100%; overflow-x: auto; margin-bottom: 1em;"
        })
        table.insert_before(wrapper)
        wrapper.append(table.extract())
    
    return str(soup)

def procesar_archivo(input_file, output_file=None, font_size="80%"):
    """Procesa el archivo HTML y guarda el resultado"""
    try:
        with open(input_file, 'r', encoding='utf-8') as file:
            html = file.read()
    except Exception as e:
        print(f"Error al leer el archivo: {e}")
        return False

    html = mejorar_elementos_code(html)
    html = mejorar_caja_codigo(html)
    html = mejorar_tablas(html, font_size)

    if not output_file:
        base, ext = os.path.splitext(input_file)
        output_file = f"{base}-fix{ext}"

    try:
        with open(output_file, 'w', encoding='utf-8') as file:
            file.write(html)
        print(f"Archivo procesado guardado como: {output_file}")
        return True
    except Exception as e:
        print(f"Error al guardar el archivo: {e}")
        return False

def mostrar_ayuda():
    """Muestra mensaje de ayuda"""
    print("\nUso: python3 cli_html_fixer.py [opciones] archivo.html")
    print("\nOpciones:")
    print("  -o, --output FILE    Especifica el archivo de salida")
    print("  -f, --font SIZE      Tamaño de fuente para tablas (ej: 90%, 1em)")
    print("  -h, --help           Muestra este mensaje de ayuda")
    print("\nEjemplos:")
    print("  python3 cli_html_fixer.py entrada.html")
    print("  python3 cli_html_fixer.py -o salida.html -f 90% entrada.html")

def main():
    if len(sys.argv) < 2 or '-h' in sys.argv or '--help' in sys.argv:
        mostrar_ayuda()
        return

    input_file = None
    output_file = None
    font_size = "80%"

    # Procesar argumentos
    i = 1
    while i < len(sys.argv):
        arg = sys.argv[i]
        if arg in ['-o', '--output']:
            output_file = sys.argv[i+1]
            i += 2
        elif arg in ['-f', '--font']:
            font_size = sys.argv[i+1]
            if not font_size.endswith(('%', 'em', 'px')):
                font_size += '%'
            i += 2
        elif not arg.startswith('-'):
            input_file = arg
            i += 1
        else:
            i += 1

    if not input_file:
        print("Error: Debes especificar un archivo de entrada")
        mostrar_ayuda()
        return

    if not os.path.exists(input_file):
        print(f"Error: El archivo '{input_file}' no existe")
        return

    procesar_archivo(input_file, output_file, font_size)

if __name__ == "__main__":
    main()
