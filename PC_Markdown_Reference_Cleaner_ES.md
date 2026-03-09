# PMC Markdown Reference Cleaner

Herramienta gráfica en **Python + PyQt6** para limpiar automáticamente referencias copiadas desde **PubMed Central (PMC)**.

Cuando se copian referencias desde la página de PMC:

[https://pmc.ncbi.nlm.nih.gov/](https://pmc.ncbi.nlm.nih.gov/)

el Markdown generado suele contener problemas como:

* corchetes escapados `\[ \]`
* enlaces innecesarios como `[PMC free article]`
* espacios entre enlaces
* corchetes vacíos `[]`

Este programa limpia automáticamente el texto para que quede listo para usar en **Markdown**, **blogs**, **documentación técnica** o **artículos científicos**.

---

# Características

El programa corrige automáticamente:

* `\[texto\]` → `[texto]`
* elimina enlaces `[PMC free article]`
* une enlaces finales:

```
[DOI](...)[PubMed](...)[Google Scholar](...)
```

* elimina corchetes vacíos `[]`
* permite:

✔ pegar texto
✔ corregir Markdown
✔ copiar resultado
✔ guardar como `.md`

---

# Ejemplo

### Entrada

```
- 2.Hou K., Wu Z.-X., Chen X.-Y., Wang J.-Q., Zhang D., Xiao C., Zhu D., Koya J.B., Wei L., Li J., et al. Microbiota in health and diseases. Signal Transduct. Target. Ther. 2022;7:135. doi: 10.1038/s41392-022-00974-4. \[[DOI](https://doi.org/10.1038/s41392-022-00974-4)\] \[[PMC free article](/articles/PMC9034083/)\] \[[PubMed](https://pubmed.ncbi.nlm.nih.gov/35461318/)\] \[[Google Scholar](https://scholar.google.com/...)\]
```

### Salida

```
- 2.Hou K., Wu Z.-X., Chen X.-Y., Wang J.-Q., Zhang D., Xiao C., Zhu D., Koya J.B., Wei L., Li J., et al. Microbiota in health and diseases. Signal Transduct. Target. Ther. 2022;7:135. doi: 10.1038/s41392-022-00974-4. [DOI](https://doi.org/10.1038/s41392-022-00974-4)[PubMed](https://pubmed.ncbi.nlm.nih.gov/35461318/)[Google Scholar](https://scholar.google.com/...)
```

---

# Requisitos

* Python **3.9 o superior**
* PyQt6

---

# Instalación

## Windows

1. Instalar Python

Descargar desde:

[https://www.python.org/downloads/](https://www.python.org/downloads/)

Durante la instalación **activar la opción**:

```
Add Python to PATH
```

2. Instalar PyQt6

Abrir **CMD** o **PowerShell**:

```
pip install PyQt6
```

3. Ejecutar el programa

```
python arreglar_referencias_pmc.py
```

---

## Linux

La mayoría de distribuciones ya incluyen Python.

Verificar:

```
python3 --version
```

Instalar PyQt6:

```
pip install PyQt6
```

Ejecutar:

```
python3 arreglar_referencias_pmc.py
```

---

## macOS

1. Verificar Python:

```
python3 --version
```

Si no está instalado:

```
brew install python
```

2. Instalar PyQt6

```
pip3 install PyQt6
```

3. Ejecutar

```
python3 arreglar_referencias_pmc.py
```

---

# Uso

1. Copiar referencias desde **PubMed Central**
2. Pegarlas en el panel izquierdo
3. Pulsar:

```
Arreglar Markdown
```

Opcional:

```
Eliminar [] vacíos
```

4. Copiar o guardar el resultado.

---

# Flujo de trabajo recomendado

1️⃣ Abrir artículo en:

[https://pmc.ncbi.nlm.nih.gov/](https://pmc.ncbi.nlm.nih.gov/)

2️⃣ Ir a **References**

3️⃣ Usar una extensión como:

**Copiloto de Selección**

[https://microsoftedge.microsoft.com/addons/detail/copiloto-de-selección/ignppgbmdpkamckbgakeofhlbnonpopn](https://microsoftedge.microsoft.com/addons/detail/copiloto-de-selección/ignppgbmdpkamckbgakeofhlbnonpopn)

4️⃣ Copiar referencias en Markdown.

5️⃣ Pegarlas en el programa y limpiarlas.

---

# Licencia

MIT License

---

# Autor

Herramienta creada para limpiar referencias Markdown provenientes de **PubMed Central (PMC)**.

---
