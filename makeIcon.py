import fileinput
import os
import sys
import time
from sys import version_info
import PIL
from PIL import Image
import json
from pprint import pprint
from shutil import copyfile
import logging

class makeIcon():
    def __ini__():
        logging.basicConfig(filename='makeIcon.log', level=logging.INFO)
    
    def aiToPNG(self, root, file):
        filename = os.path.join(root, file)
        fileext = os.path.splitext(file)[1]
        fileN = os.path.splitext(file)[0]
        
        didRename = False
        
        if len(fileN.split(" ")) > 1:
            fileN = self.convertToString(fileN.split(" "), "_")
            os.rename(os.path.join(root,file), os.path.join(root,fileN+fileext))
            didRename = True
        
        #print(filename, fileN, fileext)
        logging.info()
        os.system("gs -dNOPAUSE -dBATCH -sDEVICE=pngalpha -r300 -sOutputFile="+os.path.join(root, fileN+".png")+" "+os.path.join(root, fileN+fileext)+ "> log.txt")

        if didRename == True: # if did rename, undo the actions
            fileN = self.convertToString(fileN.split("_"), " ")
            os.rename(os.path.join(root,file), os.path.join(root,fileN+fileext))

    def readJSON(self):
        with open('IconSizes.json') as data_file:
            return json.load(data_file)

    def convertToString(self, a, s):
        la = len(a)
        b = a[0:la] #copy list (like slice() in JavaScript)
        for i in xrange(0, la): #iterate
            b[i] = str(b[i]) #convert each to string
        return s.join(b) #return all string

    def isInt(self, s):
        try:
            int(s)
            return True
        except ValueError:
            return False

    def progress(self, count, total, suffix=''):
        bar_len = 60
        filled_len = int(round(bar_len * count / float(total)))
        
        percents = round(100.0 * count / float(total), 1)
        bar = '=' * filled_len + '-' * (bar_len - filled_len)
        
        sys.stdout.write('[%s] %s%s ...%s\r' % (bar, percents, '%', suffix))
        sys.stdout.flush()  # As suggested by Rom Ruben


    def handleFile(self, root, file, output, width, height):
        if width != height:
            #print("NOT A SQUARE!")
        
        #print("Resizing")
        #print("WRITING: "+output.split("/")[len(output.split("/"))-1])
        input = os.path.join(root, file)
        
        self.resize(input, output, width, height)
    


    def makeIcon(self, root, file, overwrite=True):
        data = self.readJSON()
        for platform, pValue in data.iteritems(): #iOS, Android, WatchKit, iMessage
            #print("PLATFORM: "+platform)
            for out, oValue in pValue.iteritems(): # Each Folder
                #Folder or file
                #print("OUTPUT: "+out)
                
                fileext = out.split(".")
                
                print(fileext)
                
                if len(fileext) > 1 and fileext[1] == "png":
                    #output file here
                    width = oValue["width"]
                    height = oValue["height"]
                    
                    input = os.path.join(root, file)
                    output = "output/"+platform+"/"+out
                    
                    #print(input, output)
                    
                    #Make sure the output folder exists
                    if not os.path.exists("output"):
                        print("Creating output directory")
                        os.makedirs("output")
                    
                    # Make sure the sub folder exists
                    if not os.path.exists("output/"+platform):
                        print("Creating "+platform+" directory")
                        os.makedirs("output/"+platform)
                    
                    self.handleFile(root, file, output, width, height)
                else:
                    for item, iValue in oValue.iteritems(): # Each File
                        print("ITEM: "+item)
                        
                        width = iValue["width"]
                        height = iValue["height"]
                        
                        input = os.path.join(root, file)
                        output = "output/"+platform+"/"+out+"/"+item
                        
                        if not os.path.exists("output"):
                            print("Creating output directory")
                            os.makedirs("output")
                        
                        # Make sure the sub folder exists
                        if not os.path.exists("output/"+platform):
                            print("Creating "+platform+" directory")
                            os.makedirs("output/"+platform)
                        
                        if not os.path.exists("output/"+platform+"/"+out):
                            print("Creating "+out+" directory")
                            os.makedirs("output/"+platform+"/"+out)
                        
                        self.handleFile(root, file, output, width, height)

            if platform == "iOS" or platform == "WatchKit":
                # Copy the bundle resources over
                copyfile("Resources/"+platform+".json", "output/"+platform+"/AppIcon.appiconset/Contents.json")


    def resize(self, source, dest, width, height=0):
        img = Image.open(source)
        
        #wpercent = width / float(img.size[0])
        #if height != width:
        #hsize = int(height / float(img.size[1]))
        #else:
        #hsize = int((float(img.size[1]) * float(wpercent)))
        
        assert(width > 0)
        assert(height > 0)
        # We already know the new size, so just set it to that.
        img = img.resize((width, height), PIL.Image.ANTIALIAS)
        img.save(dest)
            
    def createImages(self, isTest=False):
        py3 = version_info[0] > 2
        overwrite = True
        over = ""

        print("\n\t Icon Creator by Matthew Paletta\n")


        while not os.path.exists("images"):
            print("Creating images folder...")
            os.makedirs("images")
            print("It seems there was no images directory here.  We just created one for you!  Drag any images you would like to use in that folder, then restart the program.")
            if isTest:
                # Copy test file into directory
                from shutil import copyfile
                copyfile("tests/sampleImage.png", "images/sampleImage.png")
                copyfile("tests/sampleImage.ai", "images/sampleImage.ai")
            
            else:
                exit()

        #continue from while loop
        print("Input folder found")


        if not os.path.exists("output"):
            print("Creating output folder...")
            os.makedirs("output")

        print("Output folder found\n")


        if isTest:
            overwrite = True
        else:
            if py3:
                #print("Using Python 3.X")
                over = input("Should overwrite previous? [y/N] ")
                if over == 'y' or over == 'Y':
                    overwrite = True
                else:
                    overwrite = False
            else:
                #print("Using Python 2.X")
                over = raw_input("Should overwrite previous? [y/N] ")
                if over == 'y' or over == 'Y':
                    overwrite = True
                else:
                    overwrite = False

        total = 0
        i = 0

        for root, subFolders, files in os.walk("images"):
            for file in files:
                total += 1

        for root, subFolders, files in os.walk("images"):
            for file in files:
                #progress(i, total, "Reading: "+file)
                i += 1
                
                if (file.endswith('.png') or file.endswith('.jpg')) and os.path.islink(os.path.join(root, file)) == False:
                    
                    self.makeIcon(root, file, overwrite)
                if (file.endswith('.ai') or file.endswith('.psd')) and os.path.islink(os.path.join(root, file)) == False:
                    self.aiToPNG(root, file)
                    filename = os.path.splitext(file)[0]
                    self.makeIcon(root, filename+".png", overwrite)

                    os.remove(os.path.join(root, filename+".png"))

            if os.path.exists("log.txt"):
                os.remove("log.txt")
            #progress(total, total)
        print("\n")

if __name__ == "__main__":
    icon = makeIcon()
    icon.createImages()
