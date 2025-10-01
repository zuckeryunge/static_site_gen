from enum import Enum

class TextType(Enum):
    PLAIN_TEXT = "text"
    BOLD_TEXT = "bold"
    CODE_TEXT = "code"
    LINK_TEXT = "link"
    IMAGE_EMBED = "image"


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
