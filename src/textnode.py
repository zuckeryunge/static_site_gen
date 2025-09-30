from enum import Enum

class TextType(Enum):
    PLAIN_TEXT = "text"
    BOLD_TEXT = "bold"
    CODE_TEXT = "code"
    LINK_TEXT = "link"
    IMAGE_EMBED = "image"

