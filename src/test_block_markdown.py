import unittest
from block_markdown import  block_to_block_type, markdown_to_blocks, markdown_to_html_node



class TestMarkdownToBlocks(unittest.TestCase):

    def test_strip_all_whitespace(self):
        md = """
This is **bolded** paragraph

This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line

- This is a list
- with items
"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This is **bolded** paragraph",
                "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
                "- This is a list\n- with items",
            ],
        )

class TestBlockTypeAsserter(unittest.TestCase):

    def test_block_to_block_types(self):
        many_blocks = [
            "this is just paragraph",
            "# heading",
            "```code\ncode\nmore code```",
            """>quote this
>qoute that
>quote anything you like""",
            "- check me out\n- nananana\n- yeah",
            "1. you should\n2. brush your\n3. dirty feet",
        ]
        blocktype_list = []
        for block in many_blocks:
            blocktype = block_to_block_type(block)
            blocktype_list.append(blocktype.value)
        
        self.assertEqual(
                blocktype_list,
                [
                    "paragraph",
                    "heading",
                    "code",
                    "quote",
                    "unordered_list",
                    "ordered_list",
                ]
            )

class TestMarkdownToHtml(unittest.TestCase):

    def test_md_file_to_html_nodes(self):
        input_md = """
This is **bolded** paragraph
text in a p
tag here

This is another paragraph with _italic_ text and `code` here

"""
        node = markdown_to_html_node(input_md)

        html = node.to_html()
        self.assertEqual(
            html,
            "<div><p>This is <b>bolded</b> paragraph text in a p tag here</p><p>This is another paragraph with <i>italic</i> text and <code>code</code> here</p></div>",
        )

if __name__ == "__main__":
    unittest.main()

