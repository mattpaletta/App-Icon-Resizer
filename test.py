import unittest
from makeIcon import makeIcon
import json
from PIL import Image

class MyTest(unittest.TestCase):
    
    def test_PNG(self):
        # Copy test file into directory
        import os
        from shutil import copyfile
        if not os.path.exists("images"):
            os.makedirs("images")
        copyfile("tests/Blue.ai", "images/BlueAI.ai")
        icon = makeIcon()
        icon.createImages(True)
        with open('IconSizes.json') as data_file:
            expectedOutput = json.load(data_file)
        
        # Check every level of the directory structure
        for root, value1 in expectedOutput.iteritems():
            assert(os.path.exists("output/"+root))
            for size, value2 in value1.iteritems():
                assert(os.path.exists("output/"+root+"/"+size))
                for fileName, value3 in value2.iteritems():
                    # Verify the file exists
                    assert(os.path.exists("output/"+root+"/"+size+"/"+fileName))
                    img = Image.open("output/"+root+"/"+size+"/"+fileName)
                    # Check the image is the correct size
                    assert(img.size[0] == value3["width"])
                    assert(img.size[1] == value3["height"])
    
    def test_AI(self):
        import os
        from shutil import copyfile
        if not os.path.exists("images"):
            os.makedirs("images")
        copyfile("tests/Blue.ai", "images/BlueAI.ai")
        icon = makeIcon()
        icon.createImages(True)
        with open('IconSizes.json') as data_file:
            expectedOutput = json.load(data_file)
        # Check every level of the directory structure
        for root, value1 in expectedOutput.iteritems():
            assert(os.path.exists("output/"+root))
            for size, value2 in value1.iteritems():
                assert(os.path.exists("output/"+root+"/"+size))
                for fileName, value3 in value2.iteritems():
                    # Verify the file exists
                    assert(os.path.exists("output/"+root+"/"+size+"/"+fileName))
                    img = Image.open("output/"+root+"/"+size+"/"+fileName)
                    # Check the image is the correct size
                    assert(img.size[0] == value3["width"])
                    assert(img.size[1] == value3["height"])

unittest.main()
