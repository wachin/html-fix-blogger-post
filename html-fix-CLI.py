import argparse
from bs4 import BeautifulSoup

def mejorar_caja_codigo(html):
    """Mejora la apariencia de la caja de código en el HTML."""
    soup = BeautifulSoup(html, 'html.parser')
    
    for pre in soup.find_all('pre', class_='sourceCode'):
        pre['style'] = "background: rgb(231, 232, 233); border-color: rgb(214, 73, 55); " \
                      "border-style: solid; border-width: 1px 1px 1px 20px; font-family: 'Ubuntu Mono', Courier, monospace; " \
                      "font-size: medium; line-height: 22.4px; margin: 10px; max-height: 500px; min-height: 16px; " \
                      "overflow: auto; padding: 28px 10px 10px 20px; z-index: 10000;"
    return str(soup)

def mejorar_tablas(html):
    """Mejora la apariencia de las tablas en el HTML."""
    soup = BeautifulSoup(html, 'html.parser')
    
    for table in soup.find_all('table'):
        table['style'] = "border-collapse: collapse; width: 100%;"
        
        for i, row in enumerate(table.find_all('tr')):
            if i == 0:
                row['style'] = "background-color: #eaecf0ff;"
            elif i % 2 == 1:
                row['style'] = "background-color: #ffffffff;"
            else:
                row['style'] = "background-color: #eff0ffff;"
        
        for th in table.find_all('th'):
            th['style'] = "border: 1px solid black; padding: 8px; text-align: left;"
        
        for td in table.find_all('td'):
            td['style'] = "border: 1px solid black; padding: 8px; text-align: left;"
        
        # Envolver en un bloque desplazable
        wrapper = soup.new_tag('pre', **{
            "class": "table-code-box",
            "style": "background-color: #f9f9f9; padding: 10px; border: 1px solid #ddd; overflow-x: auto;"
        })
        table.insert_before(wrapper)
        wrapper.append(table.extract())
    
    return str(soup)

def procesar_archivo(filepath):
    """Procesa el archivo HTML y genera la versión mejorada."""
    with open(filepath, 'r', encoding='utf-8') as file:
        html = file.read()
    
    html = mejorar_caja_codigo(html)
    html = mejorar_tablas(html)
    
    output_filepath = filepath.replace(".html", "-fix.html")
    with open(output_filepath, 'w', encoding='utf-8') as file:
        file.write(html)
    
    print(f"Archivo guardado en: {output_filepath}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Mejorador de HTML para cajas de código y tablas.")
    parser.add_argument("archivo", help="Ruta del archivo HTML a procesar.")
    args = parser.parse_args()
    
    procesar_archivo(args.archivo)
