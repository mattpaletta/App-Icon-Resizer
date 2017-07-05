import unittest
from makeIcon import makeIcon

class MyTest(unittest.TestCase):
    
    def test_PNG(self):
        # Copy test file into directory
        from shutil import copyfile
        copyfile("tests/Blue.png", "images/BluePNG.png")
        icon = makeIcon()
        icon.createImages(True)
        assert(1==1)
    
    def test_AI(self):
        from shutil import copyfile
        copyfile("tests/Blue.ai", "images/BlueAI.ai")
        icon = makeIcon()
        icon.createImages(True)

unittest.main()
