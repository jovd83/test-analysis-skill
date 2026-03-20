import argparse
import html
import os
import re
import sys

TITLE_RE = re.compile(r"^#\s+(.+)$")
INLINE_CODE_RE = re.compile(r"`([^`]+)`")
BOLD_RE = re.compile(r"\*\*([^*]+)\*\*")
LINK_RE = re.compile(r"\[([^\]]+)\]\(([^)]+)\)")
ORDERED_RE = re.compile(r"^\d+\.\s+")


def render_inline(text: str) -> str:
    escaped = html.escape(text)
    escaped = LINK_RE.sub(r'<a href="\2">\1</a>', escaped)
    escaped = INLINE_CODE_RE.sub(r"<code>\1</code>", escaped)
    escaped = BOLD_RE.sub(r"<strong>\1</strong>", escaped)
    return escaped


def is_table_separator(line: str) -> bool:
    stripped = line.replace("|", "").replace(":", "").replace("-", "").strip()
    return stripped == ""


def render_table(lines: list[str]) -> str:
    rows = []
    for line in lines:
        cells = [render_inline(cell.strip()) for cell in line.strip().strip("|").split("|")]
        rows.append(cells)
    header = rows[0]
    body = rows[2:]
    header_html = "".join(f"<th>{cell}</th>" for cell in header)
    body_html = []
    for row in body:
        body_html.append("<tr>" + "".join(f"<td>{cell}</td>" for cell in row) + "</tr>")
    return (
        "<table>"
        "<thead><tr>"
        f"{header_html}"
        "</tr></thead>"
        f"<tbody>{''.join(body_html)}</tbody>"
        "</table>"
    )


def markdown_to_html(text: str) -> str:
    lines = text.splitlines()
    blocks = []
    index = 0

    while index < len(lines):
        line = lines[index]
        stripped = line.strip()

        if not stripped:
            index += 1
            continue

        if stripped.startswith("```"):
            language = stripped[3:].strip()
            code_lines = []
            index += 1
            while index < len(lines) and not lines[index].strip().startswith("```"):
                code_lines.append(lines[index])
                index += 1
            index += 1
            class_attr = f' class="language-{html.escape(language)}"' if language else ""
            code = html.escape("\n".join(code_lines))
            blocks.append(f"<pre><code{class_attr}>{code}</code></pre>")
            continue

        if stripped.startswith("|") and index + 1 < len(lines) and is_table_separator(lines[index + 1]):
            table_lines = [lines[index], lines[index + 1]]
            index += 2
            while index < len(lines) and lines[index].strip().startswith("|"):
                table_lines.append(lines[index])
                index += 1
            blocks.append(render_table(table_lines))
            continue

        if stripped == "---":
            blocks.append("<hr>")
            index += 1
            continue

        if stripped.startswith("#"):
            level = len(stripped) - len(stripped.lstrip("#"))
            content = render_inline(stripped[level:].strip())
            blocks.append(f"<h{level}>{content}</h{level}>")
            index += 1
            continue

        if stripped.startswith(("- ", "* ")):
            items = []
            while index < len(lines) and lines[index].strip().startswith(("- ", "* ")):
                items.append(f"<li>{render_inline(lines[index].strip()[2:])}</li>")
                index += 1
            blocks.append("<ul>" + "".join(items) + "</ul>")
            continue

        if ORDERED_RE.match(stripped):
            items = []
            while index < len(lines) and ORDERED_RE.match(lines[index].strip()):
                item = ORDERED_RE.sub("", lines[index].strip(), count=1)
                items.append(f"<li>{render_inline(item)}</li>")
                index += 1
            blocks.append("<ol>" + "".join(items) + "</ol>")
            continue

        paragraph_lines = [stripped]
        index += 1
        while index < len(lines):
            lookahead = lines[index].strip()
            if not lookahead:
                break
            if lookahead.startswith(("```", "#", "- ", "* ", "|")) or lookahead == "---" or ORDERED_RE.match(lookahead):
                break
            paragraph_lines.append(lookahead)
            index += 1
        paragraph = " ".join(paragraph_lines)
        blocks.append(f"<p>{render_inline(paragraph)}</p>")

    return "\n".join(blocks)


def infer_title(text: str, fallback: str) -> str:
    for line in text.splitlines():
        match = TITLE_RE.match(line.strip())
        if match:
            return match.group(1).strip()
    return fallback


def build_document(body: str, title: str) -> str:
    return f"""<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <title>{html.escape(title)}</title>
    <style>
        :root {{
            color-scheme: light;
            --surface: #ffffff;
            --text: #1b2733;
            --line: #d5dde5;
            --accent: #0f5aa8;
            --code-bg: #f0f4f8;
        }}
        * {{ box-sizing: border-box; }}
        body {{
            margin: 0;
            background: linear-gradient(180deg, #eef3f8 0%, #f7f9fb 100%);
            color: var(--text);
            font-family: "Segoe UI", Tahoma, Geneva, Verdana, sans-serif;
            line-height: 1.6;
        }}
        main {{
            max-width: 960px;
            margin: 32px auto;
            padding: 40px 48px;
            background: var(--surface);
            border: 1px solid rgba(15, 90, 168, 0.08);
            border-radius: 18px;
            box-shadow: 0 12px 32px rgba(15, 37, 64, 0.08);
        }}
        h1, h2, h3, h4 {{
            color: var(--accent);
            line-height: 1.25;
            margin-top: 1.6em;
        }}
        h1 {{ margin-top: 0; font-size: 2.1rem; }}
        p {{ margin: 0 0 1rem; }}
        ul, ol {{ padding-left: 1.4rem; margin: 0 0 1rem; }}
        code {{
            background: var(--code-bg);
            border-radius: 6px;
            padding: 0.1rem 0.35rem;
            font-family: Consolas, "Courier New", monospace;
        }}
        pre {{
            background: #0f1720;
            color: #f2f6fb;
            padding: 16px;
            border-radius: 12px;
            overflow-x: auto;
        }}
        pre code {{
            background: transparent;
            color: inherit;
            padding: 0;
        }}
        table {{
            width: 100%;
            border-collapse: collapse;
            margin: 1rem 0 1.5rem;
            font-size: 0.96rem;
        }}
        th, td {{
            border: 1px solid var(--line);
            padding: 0.7rem 0.8rem;
            text-align: left;
            vertical-align: top;
        }}
        th {{
            background: #eef4fb;
            color: #143a66;
        }}
        tr:nth-child(even) td {{
            background: #fbfcfd;
        }}
        hr {{
            border: 0;
            border-top: 1px solid var(--line);
            margin: 2rem 0;
        }}
        a {{ color: var(--accent); }}
    </style>
</head>
<body>
<main>
{body}
</main>
</body>
</html>
"""


def export_html(md_path: str, out_path: str, title: str | None = None) -> None:
    with open(md_path, "r", encoding="utf-8") as handle:
        text = handle.read()

    html_body = markdown_to_html(text)
    document_title = title or infer_title(text, "Test Analysis Report")
    html_document = build_document(html_body, document_title)

    with open(out_path, "w", encoding="utf-8") as handle:
        handle.write(html_document)

    print(f"Exported {md_path} -> {out_path}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Export a Markdown report to styled HTML.")
    parser.add_argument("input", help="Input markdown file")
    parser.add_argument("--format", choices=["html"], default="html", help="Output format")
    parser.add_argument("--output", help="Optional output file path")
    parser.add_argument("--title", help="Optional HTML document title")

    args = parser.parse_args()

    if not os.path.exists(args.input):
        print(f"Error: {args.input} not found.")
        sys.exit(1)

    out_path = args.output
    if not out_path:
        out_path = os.path.splitext(args.input)[0] + ".html"

    if args.format == "html":
        export_html(args.input, out_path, title=args.title)
