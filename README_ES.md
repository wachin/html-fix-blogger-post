# Blogger HTML Fixer — Cajas de código, Tablas y Botón Copiar

[![Python](https://img.shields.io/badge/Python-3.x-blue.svg)](https://www.python.org/)
[![Platform](https://img.shields.io/badge/Platform-Linux%20%7C%20Windows%20%7C%20macOS%20%7C%20Termux-informational.svg)](#)
[![GUI](https://img.shields.io/badge/GUI-PyQt6-41CD52.svg)](https://riverbankcomputing.com/software/pyqt/)
[![HTML Parser](https://img.shields.io/badge/Parser-BeautifulSoup4-success.svg)](https://www.crummy.com/software/BeautifulSoup/)

> 🇬🇧 Prefer to read this in English? See [README.md](README.md)

Herramienta para mejorar archivos HTML generados por Pandoc antes de publicarlos en Blogger. Corrige la apariencia de cajas de código, tablas y elementos `<code>` en línea. Incluye también una herramienta para limpiar referencias bibliográficas copiadas desde PubMed Central.

---

## Scripts incluidos

| Script | Tipo | Función |
|---|---|---|
| `html_blogger_fixer_gui.py` | GUI (PyQt6) | Aplica el fix al HTML con interfaz gráfica |
| `html_blogger_fixer_cli.py` | CLI | Aplica el fix al HTML desde la terminal |
| `tag_markdown_gui.py` | GUI (PyQt6) | Etiqueta bloques de código en archivos `.md` |
| `tag_markdown_cli.py` | CLI | Etiqueta bloques de código desde la terminal |
| `arreglar_referencias_pmc.py` | GUI (PyQt6) | Limpia referencias copiadas desde PMC / PubMed Central |

---

## Flujo de trabajo completo

```
Markdown
   ↓
(opcional) tag_markdown_gui.py / tag_markdown_cli.py
   → añade etiquetas a bloques de código sin lenguaje
   ↓
pandoc archivo.md -o archivo.html
   ↓
html_blogger_fixer_gui.py / html_blogger_fixer_cli.py
   → mejora cajas de código, tablas y código en línea
   ↓
archivo-fix.html
   ↓
Pegar en Blogger (editor HTML)
   ↓
JS en la plantilla habilita el botón "Copiar"
```

---

## Obtener el programa

```bash
git clone https://github.com/wachin/html-fix-blogger-post
```

O descarga el ZIP desde el botón verde de GitHub y descomprímelo.

---

## Instalación

### Linux — Debian, Ubuntu and derivatives

```bash
sudo apt update
sudo apt install python3-bs4 python3-pyqt6 qt6-translations-l10n qt6-gtk-platformtheme python3-pyqt6.qtsvg qttools5-dev-tools pandoc git
```

- `python3-bs4` — BeautifulSoup4 for HTML manipulation
- `python3-pyqt6` — PyQt6 for the GUI versions
- `qt6-translations-l10n` — Qt translations (dialogs in the system language)
- `qt6-gtk-platformtheme` — native OS file dialog with `Ctrl+F` support
- `python3-pyqt6.qtsvg` — renders the SVG application icon
- `qttools5-dev-tools` — provides `lrelease` to compile `.ts` translation files to `.qm`
- `pandoc` — converts Markdown to HTML

Packages available at:
- [packages.debian.org/python3-bs4](https://packages.debian.org/python3-bs4) (since bullseye)
- [packages.ubuntu.com/python3-bs4](https://packages.ubuntu.com/python3-bs4)

### Android — Termux

```bash
pkg install git pandoc python3
python -m pip install bs4 PyQt6
```

Guía para instalar git en Termux: [github.com/wachin/Instalar-git-en-Android-con-Termux](https://github.com/wachin/Instalar-git-en-Android-con-Termux)

### Windows

1. Descarga Python desde [python.org/downloads](https://www.python.org/downloads/) y activa **Add Python to PATH** durante la instalación.

2. Verifica la instalación abriendo PowerShell:

```powershell
python --version
```

3. Instala las dependencias:

```powershell
python -m pip install beautifulsoup4 PyQt6
```

4. Instala Pandoc desde [pandoc.org/installing](https://pandoc.org/installing.html) si lo necesitas para convertir Markdown a HTML.

### macOS

1. Verifica si Python está instalado:

```bash
python3 --version
```

Si no está instalado, instálalo con Homebrew:

```bash
brew install python
```

Si no tienes Homebrew, instálalo desde [brew.sh](https://brew.sh/).

2. Instala las dependencias:

```bash
pip3 install beautifulsoup4 PyQt6
```

3. Instala Pandoc si lo necesitas:

```bash
brew install pandoc
```

---

## Ejecutar los scripts

### Linux y macOS

```bash
python3 html_blogger_fixer_gui.py
python3 html_blogger_fixer_cli.py archivo.html
python3 tag_markdown_gui.py
python3 tag_markdown_cli.py archivo.md
python3 arreglar_referencias_pmc.py
```

### Windows

```powershell
python html_blogger_fixer_gui.py
python html_blogger_fixer_cli.py archivo.html
python tag_markdown_gui.py
python tag_markdown_cli.py archivo.md
python arreglar_referencias_pmc.py
```

---

## Translations (i18n)

The GUI programs use Qt Linguist `.ts` / `.qm` files for internationalization. The translation files live in the `translations/` folder.

The application automatically loads the translation matching the system locale. If no translation is found it falls back to English.

### Available translations

| File | Language |
|---|---|
| `translations/html_blogger_fixer_en.ts` / `.qm` | English (base) |
| `translations/html_blogger_fixer_es.ts` / `.qm` | Spanish |

### Compiling translations after editing a `.ts` file

```bash
lrelease translations/html_blogger_fixer_es.ts -qm translations/html_blogger_fixer_es.qm
```

On Linux `lrelease` is provided by the `qttools5-dev-tools` package:

```bash
sudo apt install qttools5-dev-tools
```

On Windows and macOS it is included with the Qt installation or available via `pip install PyQt6-tools`.

### Adding a new language

1. Copy `translations/html_blogger_fixer_en.ts` to `translations/html_blogger_fixer_XX.ts`  
   (where `XX` is the locale code, e.g. `fr`, `de`, `pt_BR`)
2. Open the file in **Qt Linguist** or any text editor and fill in the `<translation>` tags
3. Compile it:

```bash
lrelease translations/html_blogger_fixer_XX.ts -qm translations/html_blogger_fixer_XX.qm
```

The program will pick it up automatically on a system with that locale.

---

## Paso previo: convertir Markdown a HTML con Pandoc

```bash
pandoc archivo.md -o archivo.html
```

Para que Pandoc genere cajas de código con estilo, cada bloque debe tener su etiqueta de lenguaje:

~~~markdown
```bash
sudo apt update
```
~~~

~~~markdown
```python
print("Hola, mundo!")
```
~~~

~~~markdown
```plaintext
ejemplo de texto en una caja de código
```
~~~

Si tus bloques no tienen etiqueta, usa primero `tag_markdown_gui.py` o `tag_markdown_cli.py` (ver más abajo).

---

# 1. html_blogger_fixer_gui.py — Versión gráfica

Ejecuta el script:

```bash
python3 html_blogger_fixer_gui.py
```

Se abrirá la interfaz gráfica. Desde allí puedes:

- Elegir el tamaño de fuente para las tablas (ej: `90%`)
- Arrastrar y soltar un archivo `.html` sobre la ventana, o hacer clic en **Upload** para buscarlo
- El archivo corregido se guarda automáticamente como `archivo-fix.html` en la misma carpeta

La configuración (tamaño de fuente) se guarda en:

- Linux: `~/.config/HtmlFixerPyQt6/config.json`
- Windows: `AppData\Roaming\HtmlFixerPyQt6\config.json`
- macOS: `~/.config/HtmlFixerPyQt6/config.json`

### Cambiar el tamaño de la ventana

El tamaño inicial de la ventana se controla con esta línea en `html_blogger_fixer_gui.py`:

```python
self.resize(520, 310)
```

El primer número es el **ancho** y el segundo es el **alto**, ambos en píxeles.

Ejemplos:

```python
# Ventana más pequeña
self.resize(420, 280)

# Ventana más grande
self.resize(650, 400)

# Ventana ancha para pantallas grandes
self.resize(800, 420)
```

---

# 2. html_blogger_fixer_cli.py — Versión de terminal

Ideal para Linux, macOS, Termux o automatización.

## Uso básico

```bash
python3 html_blogger_fixer_cli.py archivo.html
```

Genera `archivo-fix.html` en la misma carpeta.

## Opciones

```
python3 html_blogger_fixer_cli.py [opciones] archivo.html

  -o, --output        Archivo de salida (por defecto: archivo-fix.html)
  -f, --font          Tamaño de fuente para tablas (ej: 90%, 1em, 14px)
  --no-save-config    No guardar el tamaño de fuente en config.json
  --show-config       Muestra la ruta y contenido del archivo de configuración
```

## Ejemplos

```bash
# Procesar con opciones por defecto
python3 html_blogger_fixer_cli.py entrada.html

# Especificar archivo de salida y tamaño de fuente
python3 html_blogger_fixer_cli.py entrada.html -o salida.html -f 90%

# Ver configuración guardada
python3 html_blogger_fixer_cli.py --show-config
```

---

# 3. tag_markdown_gui.py — Etiquetar bloques de código (versión gráfica)

Cuando conviertes una página web a Markdown con [urltomarkdown.com](https://urltomarkdown.com/), los bloques de código quedan sin etiqueta:

~~~markdown
```
sudo apt update
```
~~~

Pandoc necesita la etiqueta para generar una caja de código con estilo. Este script la añade automáticamente.

## Uso

```bash
python3 tag_markdown_gui.py
```

1. Haz clic en **Buscar archivo .md** y selecciona tu archivo Markdown
2. Elige la etiqueta que se aplicará a los bloques sin lenguaje:
   `bash`, `sh`, `shell`, `python`, `html`, `css`, `javascript`, `json`, `cmd`, `powershell`, `plaintext`
3. Haz clic en **Procesar**

El programa genera `archivo-taged.md` con todos los bloques sin etiqueta corregidos. Los bloques que ya tenían etiqueta no se modifican.

La configuración (última etiqueta usada, última carpeta) se guarda en:

- Linux / macOS: `~/.config/TagMarkdownPyQt6/config.json`
- Windows: `AppData\Roaming\TagMarkdownPyQt6\config.json`

---

# 4. tag_markdown_cli.py — Etiquetar bloques de código (versión terminal)

Ideal para macOS, Termux, servidores o scripts automatizados.

## Uso básico

```bash
python3 tag_markdown_cli.py archivo.md
```

Genera `archivo-taged.md` con etiqueta `bash` por defecto.

## Opciones

```
python3 tag_markdown_cli.py [opciones] archivo.md

  -l, --lang           Etiqueta a aplicar (por defecto: bash)
  -o, --output         Archivo de salida (por defecto: archivo-taged.md)
  --replace-existing   Reemplaza también etiquetas existentes
  --overwrite          Sobrescribe el archivo de salida si ya existe
  --list-languages     Muestra las etiquetas sugeridas
```

## Ejemplos

```bash
# Etiquetar con bash (por defecto)
python3 tag_markdown_cli.py archivo.md

# Elegir etiqueta
python3 tag_markdown_cli.py archivo.md -l python
python3 tag_markdown_cli.py archivo.md -l powershell
python3 tag_markdown_cli.py archivo.md -l cmd

# Especificar archivo de salida
python3 tag_markdown_cli.py archivo.md -l bash -o salida.md

# Ver etiquetas disponibles
python3 tag_markdown_cli.py --list-languages
```

---

# 5. arreglar_referencias_pmc.py — Limpiar referencias de PMC / PubMed Central

Cuando copias referencias bibliográficas desde artículos de [PubMed Central](https://pmc.ncbi.nlm.nih.gov/), el Markdown resultante suele tener problemas:

- Corchetes escapados: `\[texto\]` en lugar de `[texto]`
- Enlaces `[PMC free article](...)` que no aportan información útil
- Espacios entre enlaces consecutivos: `[DOI](...) [PubMed](...) [Google Scholar](...)`
- Dobles espacios antes de bloques de enlaces
- Corchetes vacíos `[]`

Este script los corrige automáticamente.

## Ejemplo

**Entrada** (copiado desde PMC):

```
Hou K., et al. Microbiota in health and diseases. 2022;7:135.
doi: 10.1038/s41392-022-00974-4.
\[[DOI](https://doi.org/10.1038/s41392-022-00974-4)\]
\[[PMC free article](/articles/PMC9034083/)\]
\[[PubMed](https://pubmed.ncbi.nlm.nih.gov/35461318/)\]
\[[Google Scholar](https://scholar.google.com/...)\]
```

**Salida** (limpia):

```
Hou K., et al. Microbiota in health and diseases. 2022;7:135.
doi: 10.1038/s41392-022-00974-4.
[DOI](https://doi.org/10.1038/s41392-022-00974-4)[PubMed](https://pubmed.ncbi.nlm.nih.gov/35461318/)[Google Scholar](https://scholar.google.com/...)
```

## Uso

**Linux / macOS:**

```bash
python3 arreglar_referencias_pmc.py
```

**Windows:**

```powershell
python arreglar_referencias_pmc.py
```

Se abre una ventana con dos paneles (entrada / salida) y los siguientes botones:

|         Botón          |                   Función                   |
| ---------------------- | ------------------------------------------- |
| **Abrir .md**          | Carga un archivo Markdown                   |
| **Pegar en entrada**   | Pega el portapapeles en el panel de entrada |
| **Arreglar Markdown**  | Aplica todas las correcciones               |
| **Copiar salida**      | Copia el resultado al portapapeles          |
| **Guardar salida**     | Guarda el resultado como archivo `.md`      |
| **Eliminar [] vacíos** | Elimina corchetes vacíos `[]` del resultado |
| **Limpiar todo**       | Limpia ambos paneles                        |

### Flujo de trabajo recomendado para referencias PMC

1. Abre el artículo en [pmc.ncbi.nlm.nih.gov](https://pmc.ncbi.nlm.nih.gov/)
2. Ve a la sección **References**
3. Copia las referencias en Markdown (puedes usar una extensión de navegador como [Copiloto de Selección](https://microsoftedge.microsoft.com/addons/detail/copiloto-de-selección/ignppgbmdpkamckbgakeofhlbnonpopn) para Edge)
4. Pega el texto en el panel izquierdo del programa
5. Haz clic en **Arreglar Markdown**
6. Opcionalmente haz clic en **Eliminar [] vacíos**
7. Copia o guarda el resultado

---

# Flujo completo: Página web → Blogger

Este es el flujo para convertir páginas web en artículos técnicos con código bien formateado:

1. Convertir la página web a Markdown con [urltomarkdown.com](https://urltomarkdown.com/)

2. Etiquetar los bloques de código:

```bash
python3 tag_markdown_cli.py archivo.md
```

3. Convertir a HTML con Pandoc:

```bash
pandoc archivo-taged.md -o archivo.html
```

4. Aplicar el HTML Fixer:

```bash
python3 html_blogger_fixer_cli.py archivo.html
```

5. Abrir `archivo-fix.html`, copiar su contenido y pegarlo en Blogger en el editor HTML.

---

# Qué hace el HTML Fixer

## Cajas de código con etiqueta (`mejorar_caja_codigo`)

Los bloques Markdown con etiqueta, como:

~~~markdown
```bash
sudo apt install kate
```
~~~

Pandoc los convierte en:

```html
<div class="sourceCode"><pre class="sourceCode bash"><code>...</code></pre></div>
```

El script los transforma en una caja negra tipo terminal con:

- Barra superior oscura con tres puntos de color (amarillo, azul, rojo)
- Botón **Copiar** en la esquina derecha de la barra
- Fondo `#1e1e1e`, fuente monoespaciada, borde izquierdo verde

![](vx_images/caja-de-codigo-sourceCode.png)

## Cajas de código sin etiqueta (`mejorar_bloques_code_simples`)

Los bloques sin etiqueta que Pandoc convierte en `<pre><code>` simples reciben un estilo claro con borde izquierdo rojo:

![](vx_images/caja-de-codigo-code.png)

## Elementos `<code>` en línea (`mejorar_elementos_code`)

El código en línea dentro del texto, como `` `sudo apt update` ``, recibe:

- Fondo gris claro (`#f5f5f5`)
- Borde sutil (`#d0d0d0`)
- Fuente monoespaciada
- Color de texto rojizo (`#c7254e`)

## Tablas (`mejorar_tablas`)

Las tablas reciben:

- Encabezado con fondo gris claro y texto oscuro en negrita
- Filas alternas (blanco / gris claro)
- Bordes grises (`#cfcfcf`)
- Contenedor con scroll horizontal para pantallas pequeñas

### Tablas más compactas (opcional)

Para tablas más densas, como en artículos científicos, edita en `mejorar_tablas()`:

```python
# Compacto (recomendado para blog)
padding: 6px 12px;
line-height: 1.2;

# Muy compacto (para impresión o documentos densos)
padding: 4px 10px;
line-height: 1.1;
```

---

# Solución para el borde rojo en Blogger

Blogger puede eliminar el `border-left` de las cajas simples al editar en Vista de redacción. Para evitarlo, añade este CSS en tu tema:

**Tema → Personalizar → Avanzado → Añadir CSS**

```css
.post-body pre.simple-code-box,
pre.simple-code-box,
.simple-code-box {
  background-color: #f8f8f8 !important;
  border: 1px solid #d0d0d0 !important;
  border-left: 1px solid #d44950 !important;
  /* box-shadow reemplaza border-left cuando Blogger lo elimina */
  box-shadow: inset 6px 0 0 #d44950 !important;
  line-height: 1.5 !important;
  margin: 10px 0 !important;
  overflow-x: auto !important;
  padding: 10px 10px 10px 14px !important;
  border-radius: 4px !important;
}

.post-body pre.simple-code-box span,
pre.simple-code-box span,
.simple-code-box span {
  color: #000000 !important;
  font-family: 'Ubuntu Mono', Consolas, monospace !important;
  font-size: 15px !important;
  white-space: pre !important;
}
```

El `box-shadow` es la solución real: Blogger respeta `box-shadow` aunque elimine `border-left`.

---

# Botón "Copiar" en Blogger

El HTML Fixer añade un botón **Copiar** en cada caja de código con etiqueta. Para que funcione en Blogger, añade este JavaScript en tu tema **antes de `</body>`**:

**Tema → Mi tema → Editar HTML**

```html
<script>
//<![CDATA[
(function () {
  function getCodeText(pre) {
    const code = pre.querySelector("code");
    return (code ? code.innerText : pre.innerText).replace(/\n$/, "");
  }

  async function copyText(text) {
    if (navigator.clipboard && window.isSecureContext) {
      await navigator.clipboard.writeText(text);
      return true;
    }
    const ta = document.createElement("textarea");
    ta.value = text;
    ta.setAttribute("readonly", "");
    ta.style.position = "fixed";
    ta.style.top = "-9999px";
    document.body.appendChild(ta);
    ta.select();
    ta.setSelectionRange(0, ta.value.length);
    let ok = false;
    try {
      ok = document.execCommand("copy");
    } finally {
      document.body.removeChild(ta);
    }
    return ok;
  }

  document.addEventListener("click", async function (ev) {
    const btn = ev.target.closest(".code-copy-btn");
    if (!btn) return;
    const bar = btn.parentElement;
    const container = bar ? bar.parentElement : null;
    const pre = container ? container.querySelector("pre.sourceCode, pre") : null;
    if (!pre) return;
    const text = getCodeText(pre);
    const old = btn.textContent;
    try {
      const ok = await copyText(text);
      btn.textContent = ok ? "¡Copiado!" : "Error";
    } catch (e) {
      btn.textContent = "Error";
    }
    setTimeout(function () { btn.textContent = old; }, 1200);
  });
})();
//]]>
</script>
```

Al hacer clic en **Copiar**, el botón cambia a **¡Copiado!** durante 1.2 segundos. Incluye fallback para navegadores sin `navigator.clipboard`.

---

# Etiquetas de código reconocidas

El HTML Fixer reconoce estas etiquetas para aplicar el estilo de caja negra tipo terminal:

```python
MARKDOWN_CODE_LABELS = {
    "bash", "sh", "shell",
    "cmd", "bat", "batch",
    "powershell", "ps1",
    "console", "terminal",
    "python",
}
```

Para añadir más, edita esa variable en `html_blogger_fixer_gui.py` o `html_blogger_fixer_cli.py`.

---

## Autor

**Washington Indacochea Delgado**  
Correo: linuxfrontier@proton.me  
Repositorio: [github.com/wachin/html-fix-blogger-post](https://github.com/wachin/html-fix-blogger-post)

## Licencia

GPL 3
