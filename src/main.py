from textnode import *
import os
import shutil
from htmlnode import *
from splitnode import *
from textnode import *
from markdown_to_blocks import *
from markdown_to_html_node import *

def copy_directory(src, dest):
    if os.path.exists(dest):
        print(f"Deleting existing directory: {dest}")
        shutil.rmtree(dest)

    os.makedirs(dest, exist_ok=True)

    for item in os.listdir(src):
        src_path = os.path.join(src, item)
        dest_path = os.path.join(dest, item)

        if os.path.isfile(src_path):
            print(f"Copying file: {src_path} → {dest_path}")
            shutil.copy2(src_path, dest_path) 
        elif os.path.isdir(src_path):
            print(f"Copying directory: {src_path} → {dest_path}")
            copy_directory(src_path, dest_path)

def extract_title(markdown):
    for line in markdown.splitlines():
        line = line.strip()
        if line.startswith("# "):  # single # followed by space
            return line[2:].strip()
    raise ValueError("No H1 header (#) found in markdown")

def generate_page(from_path, template_path, dest_path):
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")

    # Read markdown content
    with open(from_path, "r", encoding="utf-8") as f:
        md_content = f.read()

    # Read template
    with open(template_path, "r", encoding="utf-8") as f:
        template_content = f.read()

    # Convert markdown to HTML
    html_content = markdown_to_html_node(md_content).to_html()

    # Extract title
    title = extract_title(md_content)

    # Replace placeholders
    full_html = template_content.replace("{{ Title }}", title).replace("{{ Content }}", html_content)

    # Ensure destination directory exists
    os.makedirs(os.path.dirname(dest_path), exist_ok=True)

    # Write the final HTML
    with open(dest_path, "w", encoding="utf-8") as f:
        f.write(full_html)

    print(f"Page generated at {dest_path}")

def main():
    static_dir = "static"
    public_dir = "public"

    print(f"Copying all static files from '{static_dir}' → '{public_dir}'")
    copy_directory(static_dir, public_dir)
    print("Done copying static files.")

    content_md = "content/index.md"
    template_html = "template.html"
    dest_html = os.path.join(public_dir, "index.html")

    generate_page(content_md, template_html, dest_html)

if __name__ == "__main__":
    main()
