import tkinter as tk
from tkinter import filedialog
from bs4 import BeautifulSoup


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



def mejorar_caja_codigo(html):
    """
    Caja de codigo negra, con botones con el color de la bandera del Ecuador
    Mejora la apariencia de las cajas de código <pre class="sourceCode">.
    Versión ajustada sin separación entre la barra y el contenido.
    """
    soup = BeautifulSoup(html, 'html.parser')

    for pre in soup.find_all('pre', class_='sourceCode'):
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
    """
    Mejora la apariencia de las tablas en el HTML.

    CAMBIO IMPORTANTE:
    Las tablas ya NO se envuelven en <pre>, porque eso produce HTML inválido
    (<pre><table>...</table></pre>) y puede romper el renderizado en Blogger.
    Ahora se envuelven en <div>, que sí es válido para contener tablas.

    Además, si el HTML ya venía dañado de una ejecución anterior, también repara
    cualquier <pre class="table-code-box"> que contenga una tabla.
    """
    soup = BeautifulSoup(html, 'html.parser')

    # Reparar salidas antiguas rotas: <pre class="table-code-box"><table>...</table></pre>
    for pre in soup.find_all('pre', class_='table-code-box'):
        if pre.find('table'):
            div = soup.new_tag('div', attrs={
                "class": "table-code-box",
                "style": pre.get('style', "background-color: #f9f9f9; padding: 10px; border: 1px solid #ddd; overflow-x: auto;")
            })
            pre.insert_before(div)
            for child in list(pre.contents):
                div.append(child.extract())
            pre.decompose()

    for table in soup.find_all('table'):
        estilo_base = "border-collapse: collapse; width: 100%;"

        if porcentaje_fuente:
            estilo_base += f" font-size: {porcentaje_fuente};"

        table['style'] = estilo_base

        for i, row in enumerate(table.find_all('tr')):
            if i == 0:
                row['style'] = (
                    "background-color: black; "
                    "color: white; "
                    "font-weight: bold; "
                    "padding: 8px; "
                )
            elif i % 2 == 1:
                row['style'] = "background-color: #ffffffff;"
            else:
                row['style'] = "background-color: #e6e6e6;"

        for th in table.find_all('th'):
            th['style'] = "border: 1px solid black; padding: 8px; text-align: left;"

        for td in table.find_all('td'):
            td['style'] = "border: 1px solid black; padding: 8px; text-align: left;"

        parent = table.parent
        if not (parent and parent.name == 'div' and 'table-code-box' in (parent.get('class') or [])):
            wrapper = soup.new_tag('div', attrs={
                "class": "table-code-box",
                "style": "background-color: #f9f9f9; padding: 10px; border: 1px solid #ddd; overflow-x: auto;"
            })
            table.insert_before(wrapper)
            wrapper.append(table.extract())

    return str(soup)



def mejorar_bloques_code_simples(html):
    """
    Mejora la apariencia de los bloques <pre><code> simples que no tienen clase sourceCode.
    No toca bloques especiales como table-code-box.
    """
    soup = BeautifulSoup(html, 'html.parser')

    for pre in soup.find_all('pre'):
        # Solo procesamos <pre> simples sin clase que contengan <code>
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



def procesar_archivo(entry_fuente):
    """
    Procesa el archivo HTML seleccionado:
    - Aplica mejoras en cajas de código, elementos code y tablas
    - Guarda el resultado en un archivo con sufijo '-fix.html'
    """
    porcentaje_fuente = entry_fuente.get().strip()
    if porcentaje_fuente and not porcentaje_fuente.endswith('%'):
        porcentaje_fuente += '%'

    filepath = filedialog.askopenfilename(filetypes=[("Archivos HTML", "*.html")])
    if not filepath:
        return

    with open(filepath, 'r', encoding='utf-8') as file:
        html = file.read()

    html = mejorar_elementos_code(html)
    html = mejorar_caja_codigo(html)
    html = mejorar_tablas(html, porcentaje_fuente)
    html = mejorar_bloques_code_simples(html)

    output_filepath = filepath.replace(".html", "-fix.html")
    with open(output_filepath, 'w', encoding='utf-8') as file:
        file.write(html)

    resultado_label.config(text=f"Archivo guardado en: {output_filepath}")



def crear_gui():
    """
    Crea la interfaz gráfica:
    - Entrada para tamaño de fuente
    - Botón para seleccionar archivo
    - Etiqueta para mostrar resultado
    """
    root = tk.Tk()
    root.title("Mejorador de HTML")
    root.geometry("460x250")

    label_fuente = tk.Label(root, text="Elije el tamaño de la fuente de la tabla (ej: 90%, 100%, etc):")
    label_fuente.pack(pady=5)

    entry_fuente = tk.Entry(root)
    entry_fuente.insert(0, "90%")
    entry_fuente.pack(pady=5)

    boton_procesar = tk.Button(root, text="Seleccionar archivo HTML", command=lambda: procesar_archivo(entry_fuente))
    boton_procesar.pack(pady=20)

    global resultado_label
    resultado_label = tk.Label(root, text="")
    resultado_label.pack(pady=10)

    root.mainloop()


if __name__ == "__main__":
    crear_gui()
