from enum import Enum
class BlockType(Enum):
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    ULIST = "unordered_list"
    OLIST = "ordered_list"


def markdown_to_blocks(markdown):
    split_blocks = markdown.split("\n\n")
    clean_blocks = []
    for block in split_blocks:
        stripped_block = block.strip()
        if stripped_block != "":
            clean_blocks.append(stripped_block)

    return clean_blocks

def block_to_block_type(block):
    block_type = BlockType.PARAGRAPH
    if block[:2] == "# ":
        block_type = BlockType.HEADING
    if block[:3] == block[-3:] == "```":
        block_type = BlockType.CODE
    if block[:1] == ">":
        for slice in block.split("\n"):
            if slice[:1] != ">":
                return block_type
        block_type = BlockType.QUOTE
    
    if block[:2] == "- ":
        for slice in block.split("\n"):
            if slice[:2] != "- ":
                return block_type
        block_type = BlockType.ULIST
    
    if block[:3] == "1. ":
        index = 1
        for slice in block.split("\n"):
            if slice[:3] != f"{index}. ":
                return block_type
            index += 1
        block_type = BlockType.OLIST
        

    return block_type


