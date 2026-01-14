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