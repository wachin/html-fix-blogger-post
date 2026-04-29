#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
tag_markdown_cli.py

Versión CLI del script tag_markdown_gui.py.

Sirve para añadir una etiqueta de lenguaje a los bloques de código Markdown.
Por ejemplo, convierte:

```
sudo apt update
```

en:

```bash
sudo apt update
```

Autor original: Washington Indacochea Delgado
"""

import argparse
import re
import sys
from pathlib import Path


LANGUAGES = ["bash", "python", "html", "plaintext"]
DEFAULT_LANG = "bash"


def process_markdown(content: str, selected_lang: str, only_untagged: bool = True) -> str:
    """
    Procesa el contenido Markdown y añade una etiqueta de lenguaje a los bloques de código.

    Si only_untagged=True, solo modifica bloques sin etiqueta:

        ```
        código
        ```

    Si only_untagged=False, también reemplaza etiquetas existentes:

        ```python
        código
        ```

    por la etiqueta seleccionada.
    """
    if only_untagged:
        # Coincide solo con bloques que abren exactamente con ``` y luego salto de línea.
        pattern = r"```\s*\n([\s\S]*?)```"
    else:
        # Coincide con bloques con o sin etiqueta y reemplaza la etiqueta por selected_lang.
        pattern = r"```[^\n]*\n([\s\S]*?)```"

    def replace_block(match: re.Match) -> str:
        code_content = match.group(1).strip()
        return f"```{selected_lang}\n{code_content}\n```"

    return re.sub(pattern, replace_block, content)


def build_output_path(input_path: Path, output_arg: str | None) -> Path:
    """
    Crea la ruta de salida.
    Si el usuario no indica -o/--output, usa el sufijo -taged.md,
    conservando el comportamiento del script GUI original.
    """
    if output_arg:
        return Path(output_arg)

    return input_path.with_name(f"{input_path.stem}-taged{input_path.suffix}")


def read_text_file(path: Path) -> str:
    try:
        return path.read_text(encoding="utf-8")
    except UnicodeDecodeError:
        print(f"❌ Error: el archivo no parece estar en UTF-8: {path}", file=sys.stderr)
        sys.exit(1)
    except OSError as e:
        print(f"❌ Error al leer el archivo: {e}", file=sys.stderr)
        sys.exit(1)


def write_text_file(path: Path, content: str, overwrite: bool = False) -> None:
    if path.exists() and not overwrite:
        print(f"❌ El archivo de salida ya existe: {path}", file=sys.stderr)
        print("   Usa --overwrite para reemplazarlo.", file=sys.stderr)
        sys.exit(1)

    try:
        path.write_text(content, encoding="utf-8")
    except OSError as e:
        print(f"❌ Error al guardar el archivo: {e}", file=sys.stderr)
        sys.exit(1)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description=(
            "Añade etiquetas de lenguaje a bloques de código Markdown. "
            "Pensado para preparar archivos .md antes de convertirlos a HTML con Pandoc."
        ),
        epilog=(
            "Ejemplos:\n"
            "  python3 tag_markdown_cli.py entrada.md\n"
            "  python3 tag_markdown_cli.py entrada.md -l bash\n"
            "  python3 tag_markdown_cli.py entrada.md -l powershell -o salida.md\n"
            "  python3 tag_markdown_cli.py entrada.md --replace-existing --overwrite"
        ),
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )

    parser.add_argument(
        "input_file",
        help="Archivo Markdown de entrada (.md).",
    )

    parser.add_argument(
        "-o",
        "--output",
        help="Archivo Markdown de salida. Si no se indica, se crea archivo-taged.md.",
    )

    parser.add_argument(
        "-l",
        "--lang",
        default=DEFAULT_LANG,
        help=(
            f"Lenguaje que se añadirá a los bloques de código. "
            f"Por defecto: {DEFAULT_LANG}. Ejemplos: bash, python, html, plaintext, cmd, powershell."
        ),
    )

    parser.add_argument(
        "--replace-existing",
        action="store_true",
        help="Reemplaza también etiquetas existentes. Por defecto solo modifica bloques sin etiqueta.",
    )

    parser.add_argument(
        "--overwrite",
        action="store_true",
        help="Permite sobrescribir el archivo de salida si ya existe.",
    )

    parser.add_argument(
        "--list-languages",
        action="store_true",
        help="Muestra las etiquetas sugeridas y termina.",
    )

    return parser.parse_args()


def main() -> None:
    args = parse_args()

    if args.list_languages:
        print("Etiquetas sugeridas:")
        for lang in LANGUAGES:
            print(f"  - {lang}")
        print("También puedes usar otras, por ejemplo: cmd, powershell, javascript, css, etc.")
        return

    input_path = Path(args.input_file)

    if not input_path.exists():
        print(f"❌ Archivo no encontrado: {input_path}", file=sys.stderr)
        sys.exit(1)

    if input_path.suffix.lower() != ".md":
        print("❌ Entrada inválida: selecciona un archivo .md", file=sys.stderr)
        sys.exit(1)

    selected_lang = args.lang.strip()
    if not selected_lang:
        print("❌ La etiqueta de lenguaje no puede estar vacía.", file=sys.stderr)
        sys.exit(1)

    output_path = build_output_path(input_path, args.output)

    content = read_text_file(input_path)
    processed_content = process_markdown(
        content,
        selected_lang=selected_lang,
        only_untagged=not args.replace_existing,
    )

    write_text_file(output_path, processed_content, overwrite=args.overwrite)

    print(f"✔ Archivo generado: {output_path}")
    print(f"✔ Etiqueta aplicada: {selected_lang}")


if __name__ == "__main__":
    main()
