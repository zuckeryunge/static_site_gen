import unittest

from textnode import TextNode, TextType

class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", TextType.BOLD_TEXT)
        node2 = TextNode("This has a different Text now", TextType.BOLD_TEXT)
        node3 = TextNode("This is a text node", TextType.LINK_TEXT, "https://mymindbelike.ua/")

        self.assertEqual(node.url, None)
        self.assertNotEqual(node, node3)
        self.assertNotEqual(node, node2)
        self.assertEqual(node.text_type, node2.text_type)

if __name__ == "__main__":
    unittest.main()

