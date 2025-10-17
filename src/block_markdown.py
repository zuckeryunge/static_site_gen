from enum import Enum
import re
from htmlnode import LeafNode, ParentNode
from textnode import TextNode, text_node_to_html_node
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
    h_hierarchy = heading.count("#")
    if 1 < h_hierarchy > 6:
        raise Exception("Not a Heading")
    return h_hierarchy



def strip_markdown_from_block(block, block_type):
    if block_type == "code":
        return block.strip("\n` ")
    if block_type == "heading":
        block = block.replace("\n", " ")
        return block.strip("# ")
    if block_type == "quote":
        block = block.replace("\n>", " ")
        return block.strip(">")
    if block_type == "unordered_list":
        block = block.split("\n")
        clean_lines = [] 
        for line in block:
            clean_lines.append(line[2:])
        return clean_lines
    if block_type == "ordered_list":
        block = block.split("\n")
        clean_lines = []
        for line in block:
            clean_lines.append(line[3:])
        return clean_lines

        

def get_inline_html_nodes(list_with_strings):
    lines_to_nodes_list = []
    for line in list_with_strings:
        textnode_line = []
        textnode_line.extend(text_to_textnodes(line))
        lines_to_nodes_list.append(textnode_line)

    htmlnode_line_list = []
    for node_line in lines_to_nodes_list:
        htmlnode_line = []
        for node in node_line:
            htmlnode_line.append(text_node_to_html_node(node))
        htmlnode_line_list.append(htmlnode_line)

    return htmlnode_line_list



def markdown_to_html_node(markdown):
    html_node_list = []
    split_to_blocks = markdown_to_blocks(markdown)

    # get blocks into nodes and put them into a list
    for block in split_to_blocks:
        block_type = block_to_block_type(block).value

        if block_type == "code":
            value = strip_markdown_from_block(block, block_type)
            code_node = LeafNode("code", value)
            pre_node = ParentNode("pre", [code_node])
            html_node_list.append(pre_node)

        if block_type == "paragraph":
            tag = "p"
            block = block.replace("\n", " ")
            # get all the inline html nodes
            html_inline_nodes = get_inline_html_nodes([block])
            # create the parent node (the block) for them
            paragraph_node = ParentNode(tag, *html_inline_nodes)
            # add all to the main node list
            html_node_list.append(paragraph_node)

        if block_type == "heading":
            tag = f"h{which_heading(block)}"
            print(tag)
            clean_content = strip_markdown_from_block(block, block_type)
            # get all the inline html nodes
            html_inline_nodes = get_inline_html_nodes([clean_content])
            # create the parent node (the block) for them
            heading_node = ParentNode(tag, *html_inline_nodes)
            # add all to the main node list
            html_node_list.append(heading_node)

                    
        if block_type == "quote":
            tag = "blockquote"
            clean_content = strip_markdown_from_block(block, block_type)
            # get all the inline html nodes
            html_inline_nodes = get_inline_html_nodes([clean_content])
            # create the parent node (the block) for them
            quote_node = ParentNode(tag, *html_inline_nodes)
            # add all to the main node list
            html_node_list.append(quote_node)
        
        if block_type == "unordered_list":
            tag = "ul"
            clean_content = strip_markdown_from_block(block, block_type)
            # get all the inline html nodes
            html_inline_nodes = get_inline_html_nodes(clean_content)
            # create the parent node (the block) for them
            li_nodes = []
            for list_item in html_inline_nodes:
                li_nodes.append(ParentNode("li", list_item))

            ul_node = ParentNode(tag, li_nodes)
            # add all to the main node list
            html_node_list.append(ul_node)


        if block_type == "ordered_list":
            tag = "ol"
            clean_content = strip_markdown_from_block(block, block_type)
            # get all the inline html nodes
            html_inline_nodes = get_inline_html_nodes(clean_content)
            # create the parent node (the block) for them
            li_nodes = []
            for list_item in html_inline_nodes:
                li_nodes.append(ParentNode("li", list_item))

            ol_node = ParentNode(tag, li_nodes)
            # add all to the main node list
            html_node_list.append(ol_node)



    # set blocks_node_list as master-div-children
    master_node = ParentNode("div", html_node_list)
    # return master_node
    return master_node

