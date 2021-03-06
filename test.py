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
        for root, value1 in expectedOutput.items():
            assert(os.path.exists("output/"+root))
            for size, value2 in value1.items():
                assert(os.path.exists("output/"+root+"/"+size))
                for fileName, value3 in value2.items():
                    # Verify the file exists
                    if fileName != "width" and fileName != "height":
                        assert(os.path.exists("output/"+root+"/"+size+"/"+fileName))
                        img = Image.open("output/"+root+"/"+size+"/"+fileName)
                        # Check the image is the correct size
                        assert(img.size[0] == value3["width"])
                        assert(img.size[1] == value3["height"])
                    else:
                        img = Image.open("output/"+root+"/"+size)
                        # Check the image is the correct size
                        assert(img.size[0] == value3 or img.size[1] == value3)

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
        for root, value1 in expectedOutput.items():
            assert(os.path.exists("output/"+root))
            for size, value2 in value1.items():
                assert(os.path.exists("output/"+root+"/"+size))
                for fileName, value3 in value2.items():
                    # Verify the file exists
                    if fileName != "width" and fileName != "height":
                        assert(os.path.exists("output/"+root+"/"+size+"/"+fileName))
                        img = Image.open("output/"+root+"/"+size+"/"+fileName)
                        # Check the image is the correct size
                        assert(img.size[0] == value3["width"])
                        assert(img.size[1] == value3["height"])
                    else:
                        img = Image.open("output/"+root+"/"+size)
                        # Check the image is the correct size
                        print(img.size, value3, "output/"+root+"/"+size)
                        assert(img.size[0] == value3 or img.size[1] == value3)

unittest.main()
