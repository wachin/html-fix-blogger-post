# El porqué de este script

Estoy usando markdown para escribir mis tutoriales y luego el archivo .md resultante con pandoc lo convierto a html y lo pego en una entrada de Blogger, pero como:

- Las cajas de código tienen una vista no muy bien aceptable
- Las tablas convertidas no tienen los bordes de colores
- Los elementos `<code>` simples se ven como texto normal

Este script sirve para aplicar un fix al archivo html dado por pandoc y que quede bonito.


Flujo de trabajo

```
Markdown
   ↓
Pandoc
   ↓
HTML
   ↓
gui_html_fixer.py (mejora cajas de código + botón copiar)
   ↓
Publicación en Blogger
   ↓
JS del tema habilita copiar al portapapeles
```

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

~~~
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

Coloca el archivo `cli_html_fixer_pro.py` en la misma carpeta donde esté el archivo HTML al que deseas aplicar el fix.

Las especificaciones para ejecutarlo son:

```bash
python3 cli_html_fixer_pro.py [opciones] archivo.html
````

### Opciones disponibles

* `-o` o `--output`: Especifica el archivo de salida
* `-f` o `--font`: Tamaño de fuente para tablas (ej: 90%, 1em)
* `-h` o `--help`: Muestra ayuda

### Ejemplos

Procesar `archivo.html` y guardar como `archivo-fix.html`:

```bash
python3 cli_html_fixer_pro.py archivo.html
```

Especificar archivo de salida y tamaño de fuente:

```bash
python3 cli_html_fixer_pro.py -o salida.html -f 90% archivo.html
```

---

### Características de esta versión CLI

* **Ligera**: Funciona perfectamente en Linux, Termux y Android
* **Opciones configurables**: Tamaño de fuente y archivo de salida
* **Manejo de errores**: Detecta archivos inválidos y muestra ayuda
* **Motor visual profesional**:

  * Cajas de código negras tipo terminal
  * Barra superior tricolor 🇪🇨
  * Bloques `<pre><code>` simples mejorados
  * Elementos `<code>` inline estilizados
  * Tablas formateadas automáticamente
* **Totalmente compatible con la versión GUI**
* **Ideal para flujos Markdown → HTML → GitHub Pages o Blogger**

El script generará un nuevo archivo con el sufijo `-fix.html` (a menos que especifiques otro nombre con `-o`) con todas las mejoras visuales aplicadas.


### **Recomendaciones adicionales**
- Puedes usar cualquier editor de texto para escribir en Markdown.
- `pandoc` permite muchas opciones adicionales para mejorar la conversión de Markdown a HTML.
- Asegúrate de que el script esté en el mismo directorio donde ejecutas los comandos o proporciona la ruta completa.
- Para elementos `<code>`, el script no modifica aquellos que ya están dentro de bloques `<pre>` para evitar duplicar estilos.

Esta es la forma en la que convierto markdown a html para algunas de mis entradas en Blogger. 🚀

---

## 🧩 Convertir páginas web a Markdown con cajas de código funcionales (Script para etiquetar bloques de código en Markdown)

Cuando convierto una página web a Markdown usando:

> [https://urltomarkdown.com/](https://urltomarkdown.com/)

las cajas de código se generan así:

~~~
```
sudo apt update
```
~~~

Eso **no es suficiente** para que Pandoc genere bloques `<pre class="sourceCode">`, que son los que luego nuestro **HTML Fixer** puede estilizar correctamente.

Para que el flujo funcione, cada caja debe tener un lenguaje:

~~~
```bash
sudo apt update
```
~~~

Sin esa etiqueta, Pandoc genera un `<pre><code>` simple y no una caja de código real.

---

# 🔧 Solución: etiquetar automáticamente las cajas de código

Para resolver esto he creado un script que toma un archivo `.md` y **añade automáticamente una etiqueta de lenguaje** (`bash`, `python`, `html` o `plaintext`) a **todas las cajas de código**.

Hay dos versiones:
- `tag_markdown_gui.py` (interfaz gráfica)
- `tag_markdown_cli.py` (línea de comandos)

Ambas hacen exactamente lo mismo.

---

# 🖥️ 1) Uso de `tag_markdown_gui.py` (versión gráfica)

Esta versión es ideal si prefieres trabajar de forma visual.

## Cómo usarlo

1. Ejecuta el script:

```bash
python3 tag_markdown_gui.py
```

**Nota**: En algunos Linux está un opción para ejecutar scripts python con clic derecho.

2. Se abrirá una ventana con:

   * Un botón **"Buscar Archivo .md"**
   * Un selector de lenguaje (por defecto `bash`)
   * Un botón **"Procesar"**

3. Haz clic en **"Buscar Archivo .md"** y selecciona tu archivo Markdown.

4. Elige el lenguaje que deseas aplicar a todas las cajas de código:

   * `bash` (comandos de terminal)
   * `python`
   * `html`
   * `plaintext` (texto simple)

5. Haz clic en **"Procesar"**.

El programa generará automáticamente:

```
archivo-taged.md
```

Este nuevo archivo ya tiene todas las cajas de código correctamente etiquetadas y listo para ser convertido por Pandoc.

---

# 🖥️ 2) Uso de `tag_markdown_cli.py` (versión de terminal)

Esta versión es ideal para automatizar el flujo o usar en Termux, servidores o scripts.

## Sintaxis

```bash
python3 tag_markdown_cli.py [opciones] archivo.md
```

# Opciones

* `-l` o `--lang` → Lenguaje a usar (`bash`, `python`, `html`, `plaintext`)
* `-o` o `--output` → Archivo de salida
* `-h` o `--help` → Muestra ayuda

## Ejemplos

Etiquetar todas las cajas como `bash`:

```bash
python3 tag_markdown_cli.py archivo.md
```

Usar Python:

```bash
python3 tag_markdown_cli.py -l python archivo.md
```

Elegir nombre de salida:

```bash
python3 tag_markdown_cli.py -l bash -o archivo-taged.md archivo.md
```

El resultado será un archivo:

```
archivo-taged.md
```

---

# 🚀 Flujo completo para Blogger

Este es el flujo profesional que uso para convertir páginas web en artículos técnicos con código bien formateado:

1. Convertir una página web a Markdown
   👉 [https://urltomarkdown.com/](https://urltomarkdown.com/)

2. Etiquetar las cajas de código:

```bash
python3 tag_markdown_cli.py archivo.md
```

(o usando `tag_markdown_gui.py`)

3. Convertir a HTML con Pandoc:

```bash
pandoc archivo-taged.md -o archivo.html
```

4. Aplicar el HTML Fixer:

```bash
python3 cli_html_fixer_pro.py archivo.html
```

5. Subir a Blogger el archivo final:

```
archivo-fix.html
```

---

## 🎯 Resultado final

Con este flujo obtienes:

* Cajas de código negras tipo terminal 🇪🇨
* Tablas con estilo
* Código inline resaltado
* HTML limpio y profesional para Blogger o GitHub Pages

Esto convierte cualquier página web común en un **artículo técnico de alta calidad** 🚀
