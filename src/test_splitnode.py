import unittest

from textnode import TextNode, TextType
from splitnode import *

class TestSplitNode(unittest.TestCase):
    def test_single_delimiter_pair(self):
        nodes = [TextNode("This is **bold** text", TextType.TEXT)]
        result = split_nodes_delimiter(nodes, "**", TextType.BOLD)

        assert result == [
            TextNode("This is ", TextType.TEXT),
            TextNode("bold", TextType.BOLD),
            TextNode(" text", TextType.TEXT),
        ]
    def test_multiple_delimiters(self):
        nodes = [TextNode("**bold** and **more**", TextType.TEXT)]
        result = split_nodes_delimiter(nodes, "**", TextType.BOLD)

        assert result == [
            TextNode("bold", TextType.BOLD),
            TextNode(" and ", TextType.TEXT),
            TextNode("more", TextType.BOLD),
        ]
    def test_extract_markdown_images(self):
        matches = extract_markdown_images(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)"
        )
        self.assertListEqual([("image", "https://i.imgur.com/zjjcJKZ.png")], matches)

    def test_split_images(self):
        node = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and another ", TextType.TEXT),
                TextNode(
                    "second image", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png"
                ),
            ],
            new_nodes,
        )

    def test_split_images_multiple_nodes(self):
        nodes = [
            TextNode("before ![img](url)", TextType.TEXT),
            TextNode("already bold", TextType.BOLD),
        ]

        result = split_nodes_image(nodes)

        assert result == [
            TextNode("before ", TextType.TEXT),
            TextNode("img", TextType.IMAGE, "url"),
            TextNode("already bold", TextType.BOLD),
        ]

    def test_no_images_or_links(self):
        node = TextNode("Just plain text", TextType.TEXT)

        self.assertListEqual(
            split_nodes_image([node]),
            [node]
        )

        self.assertListEqual(
            split_nodes_link([node]),
            [node]
        )

