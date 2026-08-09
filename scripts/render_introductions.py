#!/usr/bin/env python3
"""Render the repository's constrained Markdown introductions as HTML."""

from __future__ import annotations

import argparse
import html
import re
import unicodedata
from pathlib import Path
from typing import List, Sequence, Tuple


TOPIC_DIRECTORIES = (
    "01-Lists",
    "02-Tuple",
    "03-Dictionary",
    "04-Sets",
    "05-Strings",
    "06-Collections",
    "07-Itertools",
    "08-Lambda",
    "09-Exceptions",
    "10-Logging",
    "11-JSON",
    "12-RandomNumbers",
    "13-Decorators",
    "14-Generators",
    "15-Threading-vs-Multiprocessing",
    "16-Threading-in-Python",
    "17-Multiprocessing",
    "18-Function-Arguments",
    "19-The-Asterisk",
    "20-Copying",
    "21-Context-Manager",
    "Python-Tricks",
)

INLINE_PATTERN = re.compile(
    r"(?P<code>`[^`]+`)"
    r"|(?P<link>\[[^\]]+\]\([^)]+\))"
    r"|(?P<strong>\*\*[^*]+\*\*)"
)


def render_inline(source: str) -> str:
    """Render the inline subset used by these documents."""
    output: List[str] = []
    position = 0

    for match in INLINE_PATTERN.finditer(source):
        plain = source[position : match.start()].replace(r"\|", "|")
        output.append(html.escape(plain))

        token = match.group(0)
        if match.lastgroup == "code":
            code = token[1:-1].replace(r"\|", "|")
            output.append(f"<code>{html.escape(code)}</code>")
        elif match.lastgroup == "link":
            label, url = re.fullmatch(r"\[([^\]]+)\]\(([^)]+)\)", token).groups()
            output.append(
                f'<a href="{html.escape(url, quote=True)}">'
                f"{html.escape(label)}</a>"
            )
        else:
            output.append(f"<strong>{render_inline(token[2:-2])}</strong>")

        position = match.end()

    plain = source[position:].replace(r"\|", "|")
    output.append(html.escape(plain))
    return "".join(output)


def split_table_row(line: str) -> List[str]:
    """Split a Markdown table row while preserving escaped and code-span pipes."""
    value = line.strip()
    if value.startswith("|"):
        value = value[1:]
    if value.endswith("|") and not value.endswith(r"\|"):
        value = value[:-1]

    cells: List[str] = []
    current: List[str] = []
    in_code = False
    index = 0

    while index < len(value):
        character = value[index]
        if character == "`":
            in_code = not in_code
            current.append(character)
        elif character == "\\" and index + 1 < len(value) and value[index + 1] == "|":
            current.append(r"\|")
            index += 1
        elif character == "|" and not in_code:
            cells.append("".join(current).strip())
            current = []
        else:
            current.append(character)
        index += 1

    cells.append("".join(current).strip())
    return cells


def is_separator_row(line: str) -> bool:
    cells = split_table_row(line)
    return bool(cells) and all(re.fullmatch(r":?-{3,}:?", cell) for cell in cells)


def alignment_class(marker: str) -> str:
    if marker.startswith(":") and marker.endswith(":"):
        return "align-center"
    if marker.endswith(":"):
        return "align-right"
    return ""


def slugify(text: str) -> str:
    value = unicodedata.normalize("NFKC", text).strip().lower()
    value = re.sub(r"[`*_]", "", value)
    value = re.sub(r"[^\w\s-]", "", value, flags=re.UNICODE)
    value = re.sub(r"[-\s]+", "-", value).strip("-")
    return value or "section"


def is_block_start(lines: Sequence[str], index: int) -> bool:
    line = lines[index]
    if not line.strip():
        return True
    if line.startswith("```") or re.match(r"^#{1,6} ", line):
        return True
    if line.startswith("> ") or line.startswith("- "):
        return True
    if index + 1 < len(lines) and "|" in line and is_separator_row(lines[index + 1]):
        return True
    return False


def render_markdown(source: str) -> str:
    lines = source.splitlines()
    output: List[str] = []
    seen_slugs = {}
    index = 0

    while index < len(lines):
        line = lines[index]
        if not line.strip():
            index += 1
            continue

        if line.startswith("```"):
            language = line[3:].strip()
            code_lines: List[str] = []
            index += 1
            while index < len(lines) and not lines[index].startswith("```"):
                code_lines.append(lines[index])
                index += 1
            if index >= len(lines):
                raise ValueError("Unclosed fenced code block")
            language_class = (
                f' class="language-{html.escape(language, quote=True)}"'
                if language
                else ""
            )
            code = html.escape("\n".join(code_lines))
            output.append(f"<pre><code{language_class}>{code}</code></pre>")
            index += 1
            continue

        heading = re.match(r"^(#{1,6}) (.+)$", line)
        if heading:
            level = len(heading.group(1))
            title = heading.group(2)
            base_slug = slugify(title)
            count = seen_slugs.get(base_slug, 0)
            seen_slugs[base_slug] = count + 1
            slug = base_slug if count == 0 else f"{base_slug}-{count}"

            if level == 2 and title == "目录":
                output.append(f'<nav class="toc" aria-labelledby="{slug}">')
                output.append(f'<h2 id="{slug}">{render_inline(title)}</h2>')
                index += 1
                while index < len(lines) and not lines[index].strip():
                    index += 1
                if index >= len(lines) or not lines[index].startswith("- "):
                    raise ValueError("The table of contents must be followed by a list")
                items: List[str] = []
                while index < len(lines) and lines[index].startswith("- "):
                    items.append(lines[index][2:].strip())
                    index += 1
                output.append("<ul>")
                output.extend(f"<li>{render_inline(item)}</li>" for item in items)
                output.append("</ul></nav>")
                continue

            output.append(
                f'<h{level} id="{slug}">{render_inline(title)}</h{level}>'
            )
            index += 1
            continue

        if line.startswith("> "):
            quote_lines: List[str] = []
            while index < len(lines) and lines[index].startswith("> "):
                quote_lines.append(lines[index][2:].strip())
                index += 1
            output.append(
                f"<blockquote><p>{render_inline(' '.join(quote_lines))}</p></blockquote>"
            )
            continue

        if index + 1 < len(lines) and "|" in line and is_separator_row(lines[index + 1]):
            headers = split_table_row(line)
            markers = split_table_row(lines[index + 1])
            if len(headers) != len(markers):
                raise ValueError(f"Malformed table near line {index + 1}")
            alignments = [alignment_class(marker) for marker in markers]
            index += 2
            rows: List[List[str]] = []
            while index < len(lines) and lines[index].strip().startswith("|"):
                row = split_table_row(lines[index])
                if len(row) != len(headers):
                    raise ValueError(f"Malformed table row near line {index + 1}")
                rows.append(row)
                index += 1

            output.append('<div class="table-wrap"><table>')
            output.append("<thead><tr>")
            for cell, alignment in zip(headers, alignments):
                class_attribute = f' class="{alignment}"' if alignment else ""
                output.append(
                    f"<th{class_attribute}>{render_inline(cell)}</th>"
                )
            output.append("</tr></thead><tbody>")
            for row in rows:
                output.append("<tr>")
                for cell, alignment in zip(row, alignments):
                    class_attribute = f' class="{alignment}"' if alignment else ""
                    output.append(
                        f"<td{class_attribute}>{render_inline(cell)}</td>"
                    )
                output.append("</tr>")
            output.append("</tbody></table></div>")
            continue

        if line.startswith("- "):
            items: List[str] = []
            while index < len(lines) and lines[index].startswith("- "):
                items.append(lines[index][2:].strip())
                index += 1
            output.append("<ul>")
            output.extend(f"<li>{render_inline(item)}</li>" for item in items)
            output.append("</ul>")
            continue

        paragraph_lines = [line.strip()]
        index += 1
        while index < len(lines) and not is_block_start(lines, index):
            paragraph_lines.append(lines[index].strip())
            index += 1
        output.append(f"<p>{render_inline(' '.join(paragraph_lines))}</p>")

    return "\n".join(output)


def extract_metadata(source: str) -> Tuple[str, str]:
    title_match = re.search(r"^# (.+)$", source, re.MULTILINE)
    if not title_match:
        raise ValueError("Document must contain one level-one title")
    quote_match = re.search(r"^> (.+)$", source, re.MULTILINE)
    title = re.sub(r"[`*_]", "", title_match.group(1))
    description = re.sub(r"[`*_]", "", quote_match.group(1)) if quote_match else title
    return title, description


def render_page(source: str) -> str:
    title, description = extract_metadata(source)
    body = render_markdown(source)
    return f"""<!doctype html>
<html lang="zh-CN">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <meta name="description" content="{html.escape(description, quote=True)}">
  <meta name="generator" content="scripts/render_introductions.py">
  <title>{html.escape(title)}</title>
  <link rel="stylesheet" href="../assets/docs.css">
</head>
<body>
  <main>
{body}
  </main>
</body>
</html>
"""


def render_all(root: Path, check: bool) -> int:
    failures = 0
    for directory in TOPIC_DIRECTORIES:
        markdown_path = root / directory / "introduction.md"
        html_path = root / directory / "introduction.html"
        if not markdown_path.is_file():
            raise FileNotFoundError(markdown_path)

        rendered = render_page(markdown_path.read_text(encoding="utf-8"))
        if check:
            if not html_path.is_file() or html_path.read_text(encoding="utf-8") != rendered:
                print(f"out of date: {html_path.relative_to(root)}")
                failures += 1
        else:
            html_path.write_text(rendered, encoding="utf-8")
            print(f"rendered: {html_path.relative_to(root)}")
    return failures


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--check",
        action="store_true",
        help="report HTML files that do not match their Markdown source",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    root = Path(__file__).resolve().parents[1]
    return render_all(root, check=args.check)


if __name__ == "__main__":
    raise SystemExit(main())
