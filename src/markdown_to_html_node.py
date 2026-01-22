from htmlnode import *
from textnode import *
from markdown_to_blocks import *

def text_to_children(text):
    text_nodes = text_to_textnodes(text)
    return [text_node_to_html_node(node) for node in text_nodes]


def markdown_to_html_node(markdown):
    blocks = markdown_to_blocks(markdown)
    children = []

    for block in blocks:
        block_type = block_to_block_type(block)

        if block_type == BlockType.PARAGRAPH:
            text = " ".join(line.strip() for line in block.split("\n"))
            inline_nodes = text_to_children(text)
            children.append(ParentNode("p", inline_nodes))

        elif block_type == BlockType.HEADING:
            level = len(block.split(" ")[0]) 
            text = block[level + 1 :]
            inline_nodes = text_to_children(text)
            children.append(ParentNode(f"h{level}", inline_nodes))

        elif block_type == BlockType.CODE:
            code_text = block[4:-3]
            text_node = TextNode(code_text, TextType.TEXT)
            code_html = text_node_to_html_node(text_node)
            code_node = ParentNode("code", [code_html])
            children.append(ParentNode("pre", [code_node]))

        elif block_type == BlockType.QUOTE:
            text = " ".join(
                line.lstrip("> ").strip()
                for line in block.split("\n")
            )
            inline_nodes = text_to_children(text)
            children.append(ParentNode("blockquote", inline_nodes))

        elif block_type == BlockType.UNORDERED_LIST:
            items = []
            for line in block.split("\n"):
                text = line[2:]
                inline_nodes = text_to_children(text)
                items.append(ParentNode("li", inline_nodes))
            children.append(ParentNode("ul", items))

        elif block_type == BlockType.ORDERED_LIST:
            items = []
            for line in block.split("\n"):
                text = line.split(". ", 1)[1]
                inline_nodes = text_to_children(text)
                items.append(ParentNode("li", inline_nodes))
            children.append(ParentNode("ol", items))

        else:
            raise ValueError("Unknown block type")

    return ParentNode("div", children)

