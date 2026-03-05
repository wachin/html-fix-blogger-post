# El porqué de este script

Estoy usando markdown para escribir mis tutoriales y luego el archivo .md resultante lo convierto a html y lo pego en una entrada de Blogger, pero como:
- Las cajas de código tienen una vista no muy bien aceptable
- Las tablas convertidas no tienen los bordes de colores
- Los elementos `<code>` simples se ven como texto normal

Este script sirve para aplicar un fix al archivo html dado por pandoc y que quede bonito.

# Tutorial de Instalación y Uso de HTML Fixer en Debian

Este tutorial explica cómo instalar las dependencias necesarias y cómo utilizar el script en sus versiones de línea de comandos (CLI) y con interfaz gráfica (GUI) en Debian 12.

---

## Instalación de Dependencias

Antes de ejecutar el script, necesitas instalar algunas dependencias necesarias. Para ello, abre una terminal y ejecuta los siguientes comandos:

```sh
sudo apt update
sudo apt install python3-bs4 python3-tk pandoc git
```

- `python3-bs4`: Instala BeautifulSoup4 para manipulación de HTML.
- `python3-tk`: Instala Tkinter para la versión con GUI.
- `pandoc`: Convierte archivos Markdown a HTML.

---

## Previo al uso, ti tenías el archivo en markdown conviertelo a html con pandoc

Con mucha frecuencia primero edito mi entrada para Blogger en mardown en mi editor preferido [VNote](https://facilitarelsoftwarelibre.blogspot.com/2025/05/como-descargar-vnote-editor-de-markdown-y-hacerlo-funcionar-en-linux-debian-mx-ubuntu-mint-con-manual.html)
 
Si tienes un archivo Markdown (`archivo.md`), conviértelo a HTML con:

```sh
pandoc archivo.md -o archivo.html
```

###  Consejo para aplicar el fix a archivos markdown que no tienen etiquetas en las cajas de código
Cuando vaya a convertir un markdown que tiene cajas de comandos de terminal asegúrese que tiene la etiqueta de cada código pues sino no se convierte la caja, ejemplo deben estar así:

~~~markdown
```bash
sudo apt update
```
~~~

o si es algún código en python:

~~~markdown
```python
print("Hola, mundo!")
```
~~~

y si es sólo texto:

~~~markdown
```plaintext
ejemplo de texto en una caja de código
```
~~~


## Uso de HTML Fixer

Puedes utilizar HTML Fixer en dos formas:

### 1. Aplicar el Fix al HTML con la versión GUI (Interfaz Gráfica)

1. Ejecuta el script GUI con:

```sh
python3 gui_html_fixer.py
```

2. Se abrirá una ventana donde podrás:
   - Especificar el tamaño de fuente para las tablas (por defecto 80%)
   - Seleccionar el archivo `.html` generado con `pandoc`
   
3. El script aplicará automáticamente:
   - Estilos profesionales a bloques de código `<pre class="sourceCode">`
   - Mejoras visuales a todas las tablas
   - Formato especial a elementos `<code>` simples
   - Diseño responsive para todos los elementos

4. Se guardará automáticamente como `archivo-fix.html`.
5. El programa mostrará la ubicación del archivo generado.

### Caracteristicas de lo que hace el script

El script realiza las siguientes mejoras visuales:

#### **Para bloques de código (`<pre class="sourceCode">`)**
- Fondo gris claro con borde lateral rojo
- Fuente monoespaciada
- Máximo de altura con scroll
- Padding y márgenes adecuados

#### **Para elementos `<code>` simples**
Para código en línea dentro del texto en archivos markdown, ejemplo:

~~~markdown
`sudo apt update`
~~~

ese se convertirá a `<code>` en html, y se aplicará lo siguiente:

- Fondo gris muy claro (#f5f5f5)
- Borde sutil (#d0d0d0)
- Fuente monoespaciada
- Color de texto rojizo (#c7254e)
- Pequeño padding y bordes redondeados


#### **Para tablas**
- Encabezado con fondo rojo claro (#fcebea)
- Filas alternas (blanco/gris suave)
- Bordes oscuros (#333333)
- Texto que se ajusta automáticamente
- Contenedor responsive con scroll horizontal


### **2.5. Aplicar el Fix al HTML desde la terminal de Linux o de Termux en Android**

**Para Linux **todo lo que necesita el programa ya está instalado


**Para Termux** en Android necesitas lo siguiente si estás en un celular con Android:  [https://github.com/wachin/Instalar-git-en-Android-con-Termux](https://github.com/wachin/Instalar-git-en-Android-con-Termux) y luego instala las siguientes dependencias:

```sh
pkg install git pandoc python3
```

y luego instalar el paquete beautifulsoup4 con el comando: 

```sh
python -m pip install bs4
```

#### **Modo de uso**:

Coloca el archvio `cli_html_fixer.py` donde esté el archivo al que deseas aplicar el fix. Las especificaciones para hacerlo funcionar son las siguientes:

```bash
python3 cli_html_fixer.py [opciones] archivo.html
```

   **Opciones disponibles**:
   - `-o` o `--output`: Especifica el archivo de salida
   - `-f` o `--font`: Tamaño de fuente para tablas (ej: 90%, 1em)
   - `-h` o `--help`: Muestra ayuda

 **Ejemplos**:
   
Procesar archivo.html y guardar como archivo-fix.html

```bash
python3 cli_html_fixer.py archivo.html
```

Especificar archivo de salida y tamaño de fuente:
   
```
python3 cli_html_fixer.py -o salida.html -f 90% archivo.html
```

### Características de esta versión CLI:
- **Ligera**: Optimizada para Termux/Android
- **Opciones configurables**: Tamaño de fuente y archivo de salida
- **Manejo de errores**: Informa problemas claramente
- **Conserva todas las mejoras**: Bloques de código, elementos `<code>` y tablas
- **Retrocompatible**: Funciona igual que la versión GUI pero desde terminal

El script generará un nuevo archivo con el sufijo `-fix.html` (a menos que especifiques otro nombre con `-o`) con todas las mejoras visuales aplicadas.
   

### **Recomendaciones adicionales**
- Puedes usar cualquier editor de texto para escribir en Markdown.
- `pandoc` permite muchas opciones adicionales para mejorar la conversión de Markdown a HTML.
- Asegúrate de que el script esté en el mismo directorio donde ejecutas los comandos o proporciona la ruta completa.
- Para elementos `<code>`, el script no modifica aquellos que ya están dentro de bloques `<pre>` para evitar duplicar estilos.

Esta es la forma en la que convierto markdown a html para algunas de mis entradas en Blogger. 🚀

---

# Para hacer al revés y pasar una página web a markdown
Un buen sitio online que convierte html a markdown es:

[https://urltomarkdown.com/](https://urltomarkdown.com/)

Me gusta porque en las cajas de código las convierte así:

~~~
```
ejemplo de codigo
```
~~~

y así es como yo necesito que estén para poderlas convertir con pandoc a html, pero les hace falta algo, la etiqueta, entonces el siguiente es un script con GUI que usa Tkinter que he hecho para eso.

## Script para etiquetar bloques de código en Markdown

Las caracteristicas del **script en Python con GUI usando `tkinter`** son:

✅ Script visual (GUI)  
✅ Tiene un botón para buscar el archivo `.md`  
✅ Muestra una lista desplegable (combobox) para elegir el lenguaje (tag), con **bash por defecto** además de otros  
✅ Tiene un botón "Procesar" que aplica el tag elegido a **todos los bloques de código del archivo**  
✅ Guarda el archivo con el sufijo `-taged.md`

### Cómo usarlo:

1. Ejecuta el script `tag_markdown_gui.py` desde terminal:

```bash
python3 tag_markdown_gui.py
```

2. Usa la interfaz:
   - Haz clic en **"Buscar Archivo .md"**
   - Selecciona tu archivo `.md`
   - Elige el lenguaje (por defecto es `bash`)
   - Haz clic en **"Procesar"**

Se generará un nuevo archivo con el nombre: `archivo-taged.md`


Dios les bendiga
