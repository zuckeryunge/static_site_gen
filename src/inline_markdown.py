from textnode import TextType, TextNode
import re

def split_nodes_delimiter(old_nodes, delimiter, text_type):
    output = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            output.append(node)

        else:
            if node.text.count(delimiter)%2 != 0:
                print(f"delimiter_count: {node.text.count(delimiter)}")
                print(node.text)
                raise Exception(f"could not resolve .split('{delimiter}'). Insufficent delimiter count.")

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

def extract_markdown_images(text):
    found_images = re.findall(r"!\[([^\[\]]*)\]\(([^\(\)]*)\)", text)
    return found_images


def extract_markdown_links(text):
    found_links = re.findall(r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)", text)
    return found_links

def split_nodes_image(old_nodes):
    total_split = []
    for old_node in old_nodes:
        if old_node.text_type == TextType.TEXT:
            old_text = old_node.text
            extr_images = extract_markdown_images(old_text)
            if extr_images == []:
                total_split.append(old_node)
            else:
                split_node = []
                for image in extr_images:
                    image_alt = image[0]
                    image_link = image[1]
                    new_text = old_text.split(f"![{image_alt}]({image_link})",1)
                    old_text = new_text[1]
                    if new_text[0] != "":
                        split_node.append(TextNode(new_text[0], TextType.TEXT))
                    split_node.append(TextNode(image_alt, TextType.IMAGE, image_link))
                if old_text != "":
                    split_node.append(TextNode(old_text, TextType.TEXT))
                total_split.extend(split_node)
        else:
            total_split.append(old_node)

    return total_split


def split_nodes_link(old_nodes):
    total_split = []
    for old_node in old_nodes:
        if old_node.text_type == TextType.TEXT:
            old_text = old_node.text
            extr_links = extract_markdown_links(old_text)
            if extr_links == []:
                total_split.append(old_node)
            else:
                split_node = []
                for link in extr_links:
                    link_text = link[0]
                    link_url = link[1]
                    new_text = old_text.split(f"[{link_text}]({link_url})",1)
                    old_text = new_text[1]
                    if new_text[0] != "":
                        split_node.append(TextNode(new_text[0], TextType.TEXT))
                    split_node.append(TextNode(link_text, TextType.LINK, link_url))
                if old_text != "":
                    split_node.append(TextNode(old_text, TextType.TEXT))
                total_split.extend(split_node)
        else:
            total_split.append(old_node)

    return total_split


def text_to_textnodes(text):
    result_node_list = [TextNode(text, TextType.TEXT)]
    result_node_list = split_nodes_delimiter(result_node_list, "**", TextType.BOLD)
    result_node_list = split_nodes_delimiter(result_node_list, "_", TextType.ITALIC)
    result_node_list = split_nodes_delimiter(result_node_list, "`", TextType.CODE)
    result_node_list = split_nodes_image(result_node_list)
    result_node_list = split_nodes_link(result_node_list)
    return result_node_list
