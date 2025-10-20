from enum import Enum
import re
from htmlnode import LeafNode, ParentNode
from textnode import text_node_to_html_node
from inline_markdown import text_to_textnodes

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
    if block.startswith(("# ", "## ", "### ", "#### ", "##### ", "###### ")):
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
    h_hierarchy = len(*heading)
    if 1 < h_hierarchy > 6:
        raise Exception("Not a Heading")
    return h_hierarchy



def get_tag(block, block_type):

    if block_type == "paragraph":
        return "p"

    if block_type == "heading":
        return f"h{which_heading(block)}"

    if block_type == "code":
        return "pre"

    if block_type == "quote":
        return "blockquote"

    if block_type == "unordered_list":
        return "ul"

    if block_type == "ordered_list":
        return "ol"



def strip_markdown_from_block(block, block_type):

    if block_type == "paragraph":
        return block.replace("\n", " ")

    if block_type == "heading":
        block = block.replace("\n", " ")
        return block.strip("# ")

    if block_type == "code":
        return block[4:-3]

    if block_type == "quote":
        lines = []
        for line in block.split("\n"):
            if line != "":
                lines.append(line[1:])
        block = "".join(lines)
        return block.strip()

    if block_type == "unordered_list":
        lines = []
        for line in block.split("\n"):
            if line != "":
                lines.append(line[2:])
        return lines

    if block_type == "ordered_list":
        lines = []
        for line in block.split("\n"):
            if line != "":
                lines.append(line[3:])
        return lines

        

def get_inline_html_nodes(list_with_strings):

    if type(list_with_strings) != list:
        # converting one line of text into text_nodes
        textnode_line = text_to_textnodes(list_with_strings)

        htmlnode_line = []
        # converting the text_nodes into hmtl_nodes and packing in a line
        for node in textnode_line:
            htmlnode_line.append(text_node_to_html_node(node))

        return htmlnode_line

    else:
        # handling multiline node_blocks
        lines_to_nodes_list = []
        # unpacking the block into lines, converting the lines into text_nodes
        for line in list_with_strings:
            textnode_line = text_to_textnodes(line)
            lines_to_nodes_list.append(textnode_line)

        htmlnode_line_list = []
        # unpacking the list of list of text_nodes
        for node_line in lines_to_nodes_list:
            htmlnode_line = []
            # convert each line of text_nodes into their html_node equivalent
            for node in node_line:
                htmlnode_line.append(text_node_to_html_node(node))
            # collection the html_node_lines into a node_block again 
            htmlnode_line_list.append(htmlnode_line)

        return htmlnode_line_list



def markdown_to_html_node(markdown):
    html_node_list = []
    split_to_blocks = markdown_to_blocks(markdown)

    # get blocks into nodes and put them into a list
    for block in split_to_blocks:

        block_type = block_to_block_type(block).value
        child_nodes = []
        tag = get_tag(block, block_type)
        clean_content= strip_markdown_from_block(block, block_type)
        
        if block_type == "paragraph":
            # get all the inline html nodes
            child_nodes = get_inline_html_nodes(clean_content)

        if block_type == "heading":
            # get all the inline html nodes
            child_nodes = get_inline_html_nodes(clean_content)

        if block_type == "code":
            child_nodes = [LeafNode("code", clean_content)]

        if block_type == "quote":
            # get all the inline html nodes
            child_nodes = get_inline_html_nodes(clean_content)
        
        if block_type == "unordered_list" or block_type == "ordered_list":
            # get all the inline html nodes
            grandchild_nodes = get_inline_html_nodes(clean_content)
            # create the parent node (the block) for them
            for line_list in grandchild_nodes:
                child_nodes.append(ParentNode("li", line_list))

        block_node = ParentNode(tag, child_nodes)
        html_node_list.append(block_node)

    # set blocks_node_list as master-div-children
    master_node = ParentNode("div", html_node_list)
    # return master_node
    return master_node

