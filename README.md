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

Dios les bendiga



