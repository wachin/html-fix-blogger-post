
# Blogger HTML Fixer + Botón Copiar

Este proyecto tiene dos partes:

1. **gui_html_fixer.py**
2. **Script en la plantilla de Blogger para el botón "Copiar"**

El script de Python prepara el HTML exportado para Blogger y crea cajas de código con un botón **Copiar**.

La plantilla del blog contiene un pequeño script JavaScript que permite copiar el contenido del bloque de código al portapapeles.

---

# Flujo de trabajo

1. Escribes tu tutorial en Markdown.
2. Lo conviertes a HTML.
3. Pasas el HTML por `gui_html_fixer.py`.
4. El script mejora los bloques `<code>` y `<pre>`.
5. El HTML resultante se pega en Blogger.
6. El botón **Copiar** funciona gracias al script instalado en la plantilla.

---

# Estructura que genera gui_html_fixer.py

El script genera algo como esto:

```html
<div class="code-container">
  <div class="code-bar">
    <button class="code-copy-btn">Copiar</button>
  </div>

  <pre class="sourceCode">
    <code>sudo apt update</code>
  </pre>
</div>
```

El botón **Copiar** necesita encontrar el `<pre>` que contiene el código.

---

# Script que debe ir en la plantilla de Blogger

Este script debe colocarse **antes de `</body>`** en la plantilla del blog.

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

    setTimeout(function () {
      btn.textContent = old;
    }, 1200);

  });

})();
//]]>
</script>
```

---

# Problema común

Una versión anterior del script usaba:

```javascript
btn.closest("div").querySelector("pre")
```

Eso falla porque el botón está dentro de una **barra superior** y el `<pre>` está en otro nivel.

La versión actual sube al contenedor correcto y luego busca el `<pre>`.

---

# Resultado

El botón **Copiar**:

- copia el código al portapapeles
- cambia temporalmente a **¡Copiado!**
- vuelve a **Copiar** después de 1.2 segundos

---

# Compatibilidad

Funciona en:

- Blogger
- Chrome
- Edge
- Firefox
- navegadores modernos

Incluye fallback para navegadores antiguos sin `navigator.clipboard`.
