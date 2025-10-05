class HTMLNode():

    def __init__(self, tag=None, value=None, children=None, props=None):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props

    def __repr__(self):
        return f"HTMLNode({self.tag}, {self.value}, children: {self.children}, {self.props})"

    def to_html(self):
        raise NotImplementedError("'.to_html' not implemented")

    def props_to_html(self):
        temp = ""
        if self.props != None:
            for element in self.props:
                temp +=f' {element}="{self.props[element]}"'
        return temp
       

class LeafNode(HTMLNode):

    def __init__(self,  tag, value, props=None):
        super(LeafNode, self).__init__(tag, value, None, props)

    def __repr__(self):
        return f"HTMLNode({self.tag}, {self.value}, {self.props})"

    def to_html(self):
        if self.value == None or self.value == "":
            raise ValueError("Leaf needs Value")
        if self.tag == None:
            return self.value
        else:
            output_string = f"<{self.tag}{self.props_to_html()}>{self.value}</{self.tag}>"
            return output_string

class ParentNode(HTMLNode):
    def __init__(self, tag, children, props=None):
        super(ParentNode,self).__init__(tag, None, children, props)

    def __repr__(self):
        return f"HTMLNode({self.tag}, children: {self.children}, {self.props})"

    def to_html(self):
        if self.tag == None or self.tag == "":
            raise ValueError("Parent needs Tag")
        if self.children == None or self.children == "":
            raise ValueError("Parent needs Child")
        
        recursive_output = ""
        for child in self.children:
           recursive_output += child.to_html()

        output_string = f"<{self.tag}{self.props_to_html()}>{recursive_output}</{self.tag}>"
        return output_string

