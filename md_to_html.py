import os
import re
from pathlib import Path

import markdown
import yaml

"""
Simple script to convert markdown files to html.

Usage:
python md_to_html.py <markdown_file> [output_directory]

Example:
python md_to_html.py posts/my-links.md
"""


def parse_frontmatter(content):
    # Match frontmatter between --- delimiters
    frontmatter_match = re.match(r"^---\s*\n(.*?)\n---\s*\n(.*)", content, re.DOTALL)

    if frontmatter_match:
        # Parse YAML frontmatter and remaining content
        try:
            metadata = yaml.safe_load(frontmatter_match.group(1))
            content = frontmatter_match.group(2)
        except yaml.YAMLError:
            # If YAML parsing fails, assume no frontmatter
            metadata = {}
    else:
        metadata = {}

    return metadata, content


def convert_markdown_to_html(markdown_file, output_dir=None):
    # Read the markdown file
    with open(markdown_file, "r", encoding="utf-8") as f:
        raw_content = f.read()

    # Parse frontmatter and content
    metadata, md_content = parse_frontmatter(raw_content)

    # Convert markdown to HTML
    html_content = markdown.markdown(md_content, extensions=["fenced_code", "tables"])

    # Get the output filename
    input_path = Path(markdown_file)
    if output_dir:
        output_path = Path(output_dir) / f"{input_path.stem}.html"
    else:
        output_path = input_path.with_suffix(".html")

    # Get title from frontmatter or filename
    title = metadata.get("title", input_path.stem.replace("-", " ").title())

    # Format date if provided
    date_html = ""
    if "date" in metadata:
        date_html = f"<date>{metadata['date']}</date>"

    # Create HTML template with your site's styling
    html_template = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Michael McAndrew | {title}</title>
    <link rel="stylesheet" href="../style.css">
</head>
<body>
    <h1><a href="../">Michael McAndrew</a></h1>
    {date_html}
    {html_content}
</body>
</html>
"""

    # Write the HTML file
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(html_template)

    print(f"Converted {markdown_file} to {output_path}")


if __name__ == "__main__":
    import sys

    if len(sys.argv) < 2:
        print("Usage: python md_to_html.py <markdown_file> [output_directory]")
        sys.exit(1)

    markdown_file = sys.argv[1]
    output_dir = sys.argv[2] if len(sys.argv) > 2 else None

    if not os.path.exists(markdown_file):
        print(f"Error: File {markdown_file} not found")
        sys.exit(1)

    if output_dir and not os.path.exists(output_dir):
        os.makedirs(output_dir)

    convert_markdown_to_html(markdown_file, output_dir)
    convert_markdown_to_html(markdown_file, output_dir)
