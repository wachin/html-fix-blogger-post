# HTML Blogger Fixer (PyQt6)

![Python](https://img.shields.io/badge/Python-3.x-blue)
![PyQt6](https://img.shields.io/badge/PyQt6-GUI-green)
![License](https://img.shields.io/badge/license-MIT-lightgrey)
![Platform](https://img.shields.io/badge/platform-Linux%20%7C%20Windows-orange)

Herramienta gráfica en **PyQt6** para mejorar automáticamente archivos HTML, especialmente pensada para contenido generado para **Blogger**.

---

## Características

- Mejora visual de bloques `<code>` y `<pre>`
- Soporte para Markdown convertido a HTML:
  - `bash`
  - `cmd`
  - `powershell`
- Mejora automática de tablas
- Botón de copia en bloques de código
- Interfaz gráfica simple
- Configuración persistente (`config.json`)
- Traducción automática de diálogos Qt
- Compatible con Linux y Windows

---

## Captura

> (imagen)

---

## Instalación

### 1. Clonar repositorio

```bash
git clone https://github.com/wachin/html-fix-blogger-post.git
cd html-fix-blogger-post
````

### 2. Instalar dependencias

```bash
pip install pyqt6 beautifulsoup4
```

---

## Traducciones (IMPORTANTE)

Para que los diálogos de Qt (como abrir archivos) aparezcan en español u otro idioma:

### En Debian / MX Linux:

```bash
sudo apt install qt6-translations-l10n
```

### ¿Para qué sirve esto?

El paquete `qt6-translations-l10n` proporciona traducciones para:

* QFileDialog
* QMessageBox
* Menús internos de Qt

Sin esto, la interfaz puede aparecer en inglés.

---

## ▶️ Uso

```bash
python3 html_blogger_fixer_pyqt6.py
```

1. Selecciona el tamaño de fuente de tabla
2. Haz clic en **Seleccionar archivo HTML**
3. Se genera automáticamente un archivo:

```
archivo.html → archivo-fix.html
```

---

## ⚙Configuración

Se guarda automáticamente en:

* **Linux:** `~/.config/HtmlFixerPyQt6/config.json`
* **Windows:** `AppData/Roaming/HtmlFixerPyQt6/config.json`

Ejemplo:

```json
{
    "table_font_size": "90%"
}
```

---

## Detalles técnicos (para desarrolladores)

### Centrar la ventana al iniciar

Esto se hace con:

```python
def centrar_ventana(self):
    frame = self.frameGeometry()
    screen = QApplication.primaryScreen()
    centro = screen.availableGeometry().center()
    frame.moveCenter(centro)
    self.move(frame.topLeft())
```

Y se llama después de mostrar la ventana:

```python
ventana.show()
ventana.centrar_ventana()
```

---

### Agrandar ventana "Seleccionar archivo HTML"

Por defecto, `QFileDialog.getOpenFileName()` es pequeño.

Este proyecto usa una versión avanzada:

```python
dialogo = QFileDialog(self, "Seleccionar archivo HTML")
dialogo.resize(900, 600)
dialogo.setViewMode(QFileDialog.ViewMode.Detail)
```

---

### 🔧 Cómo hacer la ventana aún más grande

Solo cambia esta línea:

```python
dialogo.resize(900, 600)
```

Por ejemplo:

```python
dialogo.resize(1200, 800)
```

---

### Soporte para etiquetas Markdown

Puedes modificar fácilmente las etiquetas reconocidas aquí:

```python
MARKDOWN_CODE_LABELS = {
    "bash",
    "cmd",
    "powershell",
}
```

Para añadir otra:

```python
"python",
"javascript",
```

esto es para la caja de código negra

---

### Sistema de traducción Qt

El código usa:

```python
self.translator = QTranslator()

translations_path = QLibraryInfo.path(
    QLibraryInfo.LibraryPath.TranslationsPath
)

self.translator.load("qtbase_es", translations_path)
QApplication.installTranslator(self.translator)
```

Esto permite que Qt use automáticamente el idioma del sistema.

---

## Autor

**Washington Indacochea Delgado**
📧 [linuxfrontier@proton.me](mailto:linuxfrontier@proton.me)
🌐 [https://github.com/wachin/html-fix-blogger-post](https://github.com/wachin/html-fix-blogger-post)

---

## 📄 Licencia

GPL 3

---


