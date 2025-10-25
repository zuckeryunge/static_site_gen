import unittest
from generate_webpage import extract_title


class TestTitleExtraction(unittest.TestCase):

    def test_extract_title(self):

        md = """
osudfo asdoifjoiadjf asoifjoiadf
odsfisd # sodijfoi
## slkdfk ksdkv sdlnkvlk#
#fdkpmkpfd dfklfd
# this is heading
oaisdjoic
spmfpo spiodjsi
# this should be 
sodnv
"""

        heading = extract_title(md)
        self.assertEqual(heading, "this is heading")
