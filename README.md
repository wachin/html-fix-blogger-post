# El porqué de este script

Estoy usando markdown para escribir mis tutoriales y luego el archivo .md resultante lo convierto a html y lo pego en una entrada de Blogger, pero como las cajas de código tienen una vista no muy bien aceptable y como además las tablas convertidas no tienen los bordes de colores, pues este script sirve para aplicar un fix al archivo html dado por pandoc y que quede bonito

# Tutorial de Instalación y Uso de HTML Fixer en Debian

Este tutorial explica cómo instalar las dependencias necesarias y cómo utilizar el script en sus versiones de línea de comandos (CLI) y con interfaz gráfica (GUI) en Debian 12.

---

## 1. Instalación de Dependencias

Antes de ejecutar el script, necesitas instalar algunas dependencias necesarias. Para ello, abre una terminal y ejecuta los siguientes comandos:

```sh
sudo apt update
sudo apt install python3-bs4 python3-tk pandoc git
```

- `python3-bs4`: Instala BeautifulSoup4 para manipulación de HTML.
- `python3-tk`: Instala Tkinter para la versión con GUI.
- `pandoc`: Convierte archivos Markdown a HTML.

---

## 2. Uso de HTML Fixer

Puedes utilizar HTML Fixer en dos formas:

### **2.1. Usar la versión CLI (Línea de Comandos)**

#### **Paso 1: Convertir el archivo Markdown a HTML**
Si tienes un archivo Markdown (`archivo.md`), conviértelo a HTML con:

```sh
pandoc archivo.md -o archivo.html
```
---

### 2 Aplicar el Fix al HTML con la versión GUI (Interfaz Gráfica)

1. Ejecuta el script GUI con:

   ```sh
   python3 tkinter_html_fixer.py
   ```

2. Se abrirá una ventana donde podrás seleccionar el archivo `.html` generado con `pandoc`.
3. Una vez procesado, se guardará automáticamente como `archivo-fix.html`.
4. El programa mostrará la ubicación del archivo generado.

### 3 Aplicar el Fix al HTML desde la terminal de Linux
Si deseas usar la terminal de Linux ejecuta el script CLI con:

```sh
python3 cli_html_fixer.py archivo.html
```

### 4 Aplicar el Fix al HTML desde la terminal de Termux en Android
Si estás en un celular con Andorid y [estás usando Termux](https://github.com/wachin/Instalar-git-en-Android-con-Termux) puedes instalar allí git y las dependencias:

```
pkg install git pandoc python3
```

y luego instalar el paquete beautifulsoup4 con el comando: 

```sh
python -m pip install bs4
```

 y convertir el .md a html ejecutando el script CLI con:

```sh
python3 cli_html_fixer.py archivo.html
```

Esto generará un archivo `archivo-fix.html` con las mejoras aplicadas.

---

## 3. Notas Finales
- Cuando vaya a convertir un markdown que tiene cajas de comandos de terminal asegúrese que tiene la etiqueta de cada codigo pues sino no se convierte la caja, ejemplo deben estar así:

~~~
```bash
sudo apt update
```
~~~

o si es algún código en python:

~~~
```python
print("Hola, mundo!")
```
~~~

y si es sólo texto

~~~
```plaintext
ejemplo de texto en una caja de código
```
~~~

y así sucesivamente siempre debe ir una etiqueta en el código de la caja

- Puedes usar cualquier editor de texto para escribir en Markdown, claro que debes saber Markdown.
- `pandoc` permite muchas opciones adicionales para mejorar la conversión de Markdown a HTML, puedes averiguar en internet algún arreglo que necesites
- Asegúrate de que el script esté en el mismo directorio donde ejecutas los comandos o proporciona la ruta completa.

Esta es la forma en la que convierto markdowna html para algunas de mis entradas en Blogger. 🚀

# Para hacer al revés y pasar una pagina web a markdown
Un buen sitio online que convierte html a markdown es:

[https://urltomarkdown.com/](https://urltomarkdown.com/)

me gusta porque en las cajas de código las convierte así:

```
```
ejemplo de codigo
```
```
y así es como yo necesito que estén para poderlas convertir con pandoc a html, pero les hace falta algo, la etiqueta, entonces el siguiente es un script con GUI que usa Tkinter que he hecho para eso

Las caracteristicas del **script en Python con GUI usando `tkinter`** son:

✅ Script visual (GUI)  
✅ Tiene un botón para buscar el archivo `.md`  
✅ Muestra una lista desplegable (combobox) para elegir el lenguaje (tag), con **bash por defecto** además de otros
✅ Tiene un botón “Procesar” que aplica el tag elegido a **todos los bloques de código del archivo**  
✅ Guarda el archivo con el sufijo `-taged.md`

---

El siguiente es el script funcionando en Debian 12:

```python
import tkinter as tk
from tkinter import filedialog, ttk, messagebox
import re

# Etiquetas disponibles
LANGUAGES = ["bash", "python", "html", "plaintext"]

def process_markdown(content, selected_lang):
    # Reemplazar todos los bloques de código sin etiqueta por ```lang...
    pattern = r"```(?:\n|.*\n)([\s\S]*?)```"

    def replace_block(match):
        code_content = match.group(1).strip()
        return f"```{selected_lang}\n{code_content}\n```"

    new_content = re.sub(pattern, replace_block, content)
    return new_content

def open_file():
    file_path = filedialog.askopenfilename(filetypes=[("Markdown files", "*.md")])
    if not file_path:
        return
    entry_file.delete(0, tk.END)
    entry_file.insert(0, file_path)

def process_file():
    file_path = entry_file.get()
    selected_lang = combo_lang.get()

    if not file_path or not file_path.endswith(".md"):
        messagebox.showwarning("Entrada inválida", "Por favor selecciona un archivo .md válido.")
        return

    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
    except Exception as e:
        messagebox.showerror("Error", f"No se pudo leer el archivo:\n{e}")
        return

    processed_content = process_markdown(content, selected_lang)

    output_path = file_path.replace(".md", "-taged.md")

    try:
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(processed_content)
        messagebox.showinfo("Éxito", f"Archivo guardado como:\n{output_path}")
    except Exception as e:
        messagebox.showerror("Error", f"No se pudo guardar el archivo:\n{e}")

# Crear la ventana principal
root = tk.Tk()
root.title("Etiquetador de Bloques de Código Markdown")
root.geometry("500x200")
root.resizable(False, False)

# Campo para mostrar la ruta del archivo
entry_file = tk.Entry(root, width=40)
entry_file.pack(pady=20)

# Botón para buscar archivo
btn_browse = tk.Button(root, text="Buscar Archivo .md", command=open_file)
btn_browse.pack()

# Combobox para elegir el lenguaje
combo_lang = ttk.Combobox(root, values=LANGUAGES, state="readonly")
combo_lang.set("bash")
combo_lang.pack(pady=10)

# Botón para procesar
btn_process = tk.Button(root, text="Procesar", command=process_file)
btn_process.pack()

# Iniciar interfaz
root.mainloop()
```

---

## Cómo usarlo:

1. Este script `tag_markdown_gui.py`
2. Ejecútalo desde terminal:

```bash
python3 tag_markdown_gui.py
```

3. Usa la interfaz:
   - Haz clic en **"Buscar Archivo .md"**
   - Selecciona tu archivo `.md`
   - Elige el lenguaje (por defecto es `bash`)
   - Haz clic en **"Procesar"**

Se generará un nuevo archivo con el nombre: `archivo-taged.md`


Dios les bendiga



