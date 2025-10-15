from enum import Enum
import re
from htmlnode import LeafNode, ParentNode

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
    if block.startswith("# ", "## ", "### ", "#### ", "##### ", "###### "):
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



def which_heading(string):
    heading = re.findall("^(#+) ", string)
    h_hierarchy = heading.count("#")
    if 1 < h_hierarchy > 6:
        raise Exception("Not a Heading")
    return h_hierarchy

def strip_quote(quote):
    pass



def strip_ulist(ulist):
    pass



def strip_olist(olist):
    pass



def strip_markdown_from_block(block, block_type):
    if block_type == "heading":
        return block.strip("# ")
    if block_type == "code":
        return block.strip("` ")



def get_inline_text_nodes(text):
    return ["write me!"]



def markdown_to_html_node(markdown):
    html_node_list = []
    split_to_blocks = markdown_to_blocks(markdown)

    # get blocks into nodes and put them into a list
    for block in split_to_blocks:
        block_type = block_to_block_type(block)
        
        if block_type == "paragraph":
            pass

        if block_type == "heading":
            tag = f"h{which_heading(block)}"
            value = strip_markdown_from_block(block, block_type)
            text_inline_nodes = get_inline_text_nodes(value)
            heading_node = ParentNode(tag, text_inline_nodes)
            html_node_list.extend(text_inline_nodes)
            html_node_list.append(heading_node)

        if block_type == "code":
            value = strip_markdown_from_block(block, block_type)
            code_node = LeafNode("code", value)
            pre_node = ParentNode("pre", code_node)
            html_node_list.extend([code_node, pre_node])
            
        if block_type == "quote":
            pass
        
        if block_type == "unordered_list":
            pass

        if block_type == "ordered_list":
            pass



    # set blocks_node_list as master-div-children
    master_node = ParentNode("div", None, html_node_list)
    # return master_node
    return master_node

