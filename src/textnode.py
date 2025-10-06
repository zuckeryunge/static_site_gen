from enum import Enum
from htmlnode import LeafNode


class TextType(Enum):
    TEXT = "text"
    BOLD = "bold"
    ITALIC = "italic"
    CODE = "code"
    LINK = "link"
    IMAGE = "image"


class TextNode():

    def __init__(self, text, text_type, url=None):
        self.text = text
        self.text_type = TextType(text_type) 
        self.url = url

    def __eq__(self, other):
        if self.text_type == other.text_type:
            if self.url == other.url:
                if self.text == other.text:
                    return True
        return False

    def __repr__(self):
        return f"TextNode({self.text}, {self.text_type.value}, {self.url})"



def split_nodes_delimiter(old_nodes, delimiter, text_type):
    output = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            output.append(node)

        else:
            if node.text.count(delimiter)%2 != 0:
                raise Exception("could not resolve .split(). Insufficent delimiter count.")

            else:
                odd = True
                for text in node.text.split(delimiter):
                    if text != "":
                        if odd == True:
                            output.append(TextNode(text, TextType.TEXT))
                        else:
                            output.append(TextNode(text, text_type))
                    odd = not odd
    
    return output


def text_node_to_html_node(text_node):
    if text_node.text_type == TextType.TEXT:
        return LeafNode(None, text_node.text)
    if text_node.text_type == TextType.BOLD:
        return LeafNode("b", text_node.text)
    if text_node.text_type == TextType.ITALIC:
        return LeafNode("i", text_node.text)
    if text_node.text_type == TextType.CODE:
        return LeafNode("code", text_node.text)
    if text_node.text_type == TextType.LINK:
        return LeafNode("a", text_node.text, {"href":text_node.url})
    if text_node.text_type == TextType.IMAGE:
        return LeafNode("img", "", {"src":text_node.url,"alt":text_node.text})
    raise Exception(f"Wrong TextType: {text_node.text_type}")

