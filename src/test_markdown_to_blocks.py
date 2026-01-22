import unittest

from textnode import TextNode, TextType
from markdown_to_blocks import *
from markdown_to_html_node import *

class TestSplitNode(unittest.TestCase):
    def test_markdown_to_blocks(self):
        md = """
This is **bolded** paragraph

This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line

- This is a list
- with items
"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This is **bolded** paragraph",
                "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
                "- This is a list\n- with items",
            ],
        )



    def test_heading_levels(self):
        self.assertEqual(
            block_to_block_type("# Heading"),
            BlockType.HEADING
        )
        self.assertEqual(
            block_to_block_type("###### Small heading"),
            BlockType.HEADING
        )

    def test_invalid_heading(self):
        self.assertEqual(
            block_to_block_type("####### Too many hashes"),
            BlockType.PARAGRAPH
        )
        self.assertEqual(
            block_to_block_type("#No space"),
            BlockType.PARAGRAPH
        )

    def test_code_block(self):
        block = "```\nprint('hello')\n```"
        self.assertEqual(
            block_to_block_type(block),
            BlockType.CODE
        )

    def test_invalid_code_block(self):
        block = "```\nprint('hello')"
        self.assertEqual(
            block_to_block_type(block),
            BlockType.PARAGRAPH
        )
    def test_quote_block(self):
        block = "> quote line one\n> quote line two"
        self.assertEqual(
            block_to_block_type(block),
            BlockType.QUOTE
        )

    def test_invalid_quote_block(self):
        block = "> valid quote\nnot quoted"
        self.assertEqual(
            block_to_block_type(block),
            BlockType.PARAGRAPH
        )

    def test_single_paragraph(self):
        md = "Just plain text"
        node = markdown_to_html_node(md)
        self.assertEqual(
            node.to_html(),
            "<div><p>Just plain text</p></div>"
        )

    def test_multiple_paragraphs(self):
        md = """
This is paragraph one

This is paragraph two
"""
        node = markdown_to_html_node(md)
        self.assertEqual(
            node.to_html(),
            "<div><p>This is paragraph one</p><p>This is paragraph two</p></div>"
        )

    def test_inline_markdown(self):
        md = "This is **bold**, _italic_, and `code`"
        node = markdown_to_html_node(md)
        self.assertEqual(
            node.to_html(),
            "<div><p>This is <b>bold</b>, <i>italic</i>, and <code>code</code></p></div>"
        )

    def test_links_and_images(self):
        md = "A [link](https://boot.dev) and ![img](img.png)"
        node = markdown_to_html_node(md)
        self.assertEqual(
            node.to_html(),
            '<div><p>A <a href="https://boot.dev">link</a> and <img src="img.png" alt="img"></p></div>'
        )

    def test_heading(self):
        md = "# Heading text"
        node = markdown_to_html_node(md)
        self.assertEqual(
            node.to_html(),
            "<div><h1>Heading text</h1></div>"
        )

    def test_blockquote(self):
        md = """
> Quote line one
> Quote line two
"""
        node = markdown_to_html_node(md)
        self.assertEqual(
            node.to_html(),
            "<div><blockquote>Quote line one Quote line two</blockquote></div>"
        )

    def test_unordered_list(self):
        md = """
- item one
- item two
- item three
"""
        node = markdown_to_html_node(md)
        self.assertEqual(
            node.to_html(),
            "<div><ul><li>item one</li><li>item two</li><li>item three</li></ul></div>"
        )

    def test_ordered_list(self):
        md = """
1. first
2. second
3. third
"""
        node = markdown_to_html_node(md)
        self.assertEqual(
            node.to_html(),
            "<div><ol><li>first</li><li>second</li><li>third</li></ol></div>"
        )