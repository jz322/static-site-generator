from textnode import *
import re
def split_nodes_delimiter(old_nodes, delimiter, text_type):
    nodes = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            nodes.append(node)
        else:
            char_list = node.text.split(delimiter)
            if len(char_list) % 2 == 0:
                raise Exception("Invalid delimeter")
            else:
                for i in range(0, len(char_list)):
                    if len(char_list[i]) == 0:
                        continue
                    elif i % 2 != 0:
                        new_node = TextNode(char_list[i], text_type)
                        nodes.append(new_node)
                    else:
                        new_node = TextNode(char_list[i], TextType.TEXT)
                        nodes.append(new_node)
    return nodes


def extract_markdown_images(text):
    image_regex = r"!\[([^\[\]]*)\]\(([^\(\)]*)\)"
    return re.findall(image_regex, text)

def extract_markdown_links(text):
    link_regex = r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)"
    return re.findall(link_regex, text)

def split_nodes_image(old_nodes):
    new_nodes = []

    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
        else:
            images = extract_markdown_images(node.text)
            if not images:
                new_nodes.append(node)
                continue
            text = node.text
            for alt, url in images:
                image_md = f"![{alt}]({url})"
                before, after = text.split(image_md, 1)
                if before:
                    new_nodes.append(TextNode(before, TextType.TEXT))

                new_nodes.append(TextNode(alt, TextType.IMAGE, url))
                
                text = after

            if text:
                new_nodes.append(TextNode(text, TextType.TEXT))

    return new_nodes

def split_nodes_link(old_nodes):
    new_nodes = []

    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
            continue

        links = extract_markdown_links(node.text)
        if not links:
            new_nodes.append(node)
            continue

        text = node.text

        for link_text, url in links:
            link_md = f"[{link_text}]({url})"
            before, after = text.split(link_md, 1)

            if before:
                new_nodes.append(TextNode(before, TextType.TEXT))

            new_nodes.append(TextNode(link_text, TextType.LINK, url))

            text = after

        if text:
            new_nodes.append(TextNode(text, TextType.TEXT))

    return new_nodes





def text_to_textnodes(text):
    nodes = [TextNode(text, TextType.TEXT)]

    nodes = split_nodes_image(nodes)
    nodes = split_nodes_link(nodes)
    nodes = split_nodes_delimiter(nodes, "**", TextType.BOLD)
    nodes = split_nodes_delimiter(nodes, "_", TextType.ITALIC)
    nodes = split_nodes_delimiter(nodes, "`", TextType.CODE)

    return nodes


        