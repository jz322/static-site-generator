from textnode import *

class HTMLNode():
    def __init__(self, tag=None, value=None, children=None, props=None):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props

    def to_html(self):
        raise NotImplementedError

    def props_to_html(self):
        string = ""
        if self.props is None or self.props == {}:
            return string
        for key in self.props:
            string += f' {key}="{self.props[key]}"'
        return string

    def __repr__(self):
        return f"HTMLNode({self.tag}, {self.value}, children: {self.children}, {self.props})"


class LeafNode(HTMLNode):
    def __init__(self, tag, value, props=None):
        super().__init__(tag, value, None, props)

    def to_html(self):
        string = ""
        if self.value == None:
            raise ValueError
        elif self.tag == None:
            string = str(self.value)
            return string
        
        if self.props is None or self.props == {}:
            string = f"<{self.tag}>{self.value}</{self.tag}>"
        else:
            html_prop = self.props_to_html()
            string = f'<{self.tag}{html_prop}>{self.value}</{self.tag}>'

        return string 


    def __repr__(self):
        return f"LeafNode({self.tag}, {self.value}, {self.props})"


class ParentNode(HTMLNode):
    def __init__(self, tag, children, props=None):
        super().__init__(tag, None, children, props)

    def to_html(self):
        if self.tag == None:
            raise ValueError("Need tag value")
        elif self.children == None or len(self.children) == 0 :
            raise ValueError("Missing Child Value")
        string = f"<{self.tag}{self.props_to_html()}>"
        for i in range(0, len(self.children)):
            string += self.children[i].to_html()
        string += f"</{self.tag}>"
        return string


def text_node_to_html_node(text_node):
    if text_node.text_type == TextType.TEXT:
        return LeafNode(None, text_node.text)
    elif text_node.text_type == TextType.BOLD:
        return LeafNode("b", text_node.text)
    elif text_node.text_type == TextType.ITALIC:
        return LeafNode("i", text_node.text)
    elif text_node.text_type == TextType.CODE:
        return LeafNode("code", text_node.text)
    elif text_node.text_type == TextType.LINK:
        return LeafNode("a", text_node.text, {"href": text_node.url})
    elif text_node.text_type == TextType.IMAGE:
        return LeafNode("img", "", {"src": text_node.url, "alt": text_node.text})
    else:
        raise Exception("Need correct text type")