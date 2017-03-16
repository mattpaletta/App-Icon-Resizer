import fileinput
import os
import sys
import time
from sys import version_info
import PIL
from PIL import Image
import json
from pprint import pprint

def aiToPNG(root, file):
    filename = os.path.join(root, file)
    fileext = os.path.splitext(file)[1]
    fileN = os.path.splitext(file)[0]
    
    didRename = False
    
    if len(fileN.split(" ")) > 1:
        fileN = convertToString(fileN.split(" "), "_")
        os.rename(os.path.join(root,file), os.path.join(root,fileN+fileext))
        didRename = True
    
    #print(filename, fileN, fileext)
    
    os.system("gs -dNOPAUSE -dBATCH -sDEVICE=pngalpha -r300 -sOutputFile="+os.path.join(root, fileN+".png")+" "+os.path.join(root, fileN+fileext)+ "> log.txt")

    if didRename == True: # if did rename, undo the actions
        fileN = convertToString(fileN.split("_"), " ")
        os.rename(os.path.join(root,file), os.path.join(root,fileN+fileext))

def readJSON():
    with open('IconSizes.json') as data_file:
        return json.load(data_file)

def convertToString(a, s):
    la = len(a)
    b = a[0:la] #copy list (like slice() in JavaScript)
    for i in xrange(0, la): #iterate
        b[i] = str(b[i]) #convert each to string
    return s.join(b) #return all string

def isInt(s):
    try:
        int(s)
        return True
    except ValueError:
        return False

def progress(count, total, suffix=''):
    bar_len = 60
    filled_len = int(round(bar_len * count / float(total)))
    
    percents = round(100.0 * count / float(total), 1)
    bar = '=' * filled_len + '-' * (bar_len - filled_len)
    
    sys.stdout.write('[%s] %s%s ...%s\r' % (bar, percents, '%', suffix))
    sys.stdout.flush()  # As suggested by Rom Ruben


def makeIcon(root, file, overwrite=True):
    data = readJSON()
    for platform, pValue in data.iteritems(): #iOS, Android, WatchKit, iMessage
        print(platform)
        for output, oValue in pValue.iteritems(): # Each Folder
            #Folder or file
            print(output)
            for item, iValue in oValue.iteritems(): # Each File
                print(item)

def resize(source, dest, width, height=0):
    img = Image.open(source)
    
    wpercent = width / float(img.size[0])
    if height > 0:
        hsize = int(height / float(img.size[1]))
    else:
        hsize = int((float(img.size[1]) * float(wpercent)))
        img = img.resize((width, hsize), PIL.Image.ANTIALIAS)

        img.save(dest)

py3 = version_info[0] > 2
overwrite = True
over = ""

print("\n\t Icon Creator by Matthew Paletta\n")


while not os.path.exists("images"):
    print("Creating images folder...")
    os.makedirs("images")
    _ = input("It seems there was no images directory here.  We just created one for you!  Drag any images you would like to use in that folder, then press enter to continue.")

#continue from while loop
print("Input folder found")


if not os.path.exists("output"):
    print("Creating output folder...")
    os.makedirs("output")

print("Output folder found\n")



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
        progress(i, total, "Reading: "+file)
        i += 1
        
        if (file.endswith('.png') or file.endswith('.jpg')) and os.path.islink(os.path.join(root, file)) == False:
            
            makeIcon(root, file, overwrite)
        if (file.endswith('.ai') or file.endswith('.psd')) and os.path.islink(os.path.join(root, file)) == False:
            aiToPNG(root, file)
            filename = os.path.splitext(file)[0]
            makeIcon(root, filename+".png", overwrite)

            os.remove(os.path.join(root, filename+".png"))

    if os.path.exists("log.txt"):
        os.remove("log.txt")
    progress(total, total)
print("\n")
