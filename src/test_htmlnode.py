import unittest

from htmlnode import *


class TestHTMLNode(unittest.TestCase):
    def test_values(self):
        node = HTMLNode("p", "hello")

        self.assertEqual(node.tag, "p")
        self.assertEqual(node.value, "hello")
        self.assertEqual(node.children, None)
        self.assertEqual(node.props, None)

        
   

if __name__ == "__main__":
    unittest.main()
