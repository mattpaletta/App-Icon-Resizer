import fileinput
import os
import sys
import time
from sys import version_info
import PIL
from PIL import Image


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

'''
    Updates the progress bar in the terminal window
    
    - requires: `count <= total`.
    - returns: NULL
    - parameters:
        - count: The current index out of the total
        - total: The total number of items to process
        - suffix: An optional parameter specifying any text at the end of the output
'''
def progress(count, total, suffix=''):
    bar_len = 60
    filled_len = int(round(bar_len * count / float(total)))
    
    percents = round(100.0 * count / float(total), 1)
    bar = '=' * filled_len + '-' * (bar_len - filled_len)
    
    sys.stdout.write('[%s] %s%s ...%s\r' % (bar, percents, '%', suffix))
    sys.stdout.flush()  # As suggested by Rom Ruben

'''
    Resizes and saves an image in a variety of sizes (1x, 2x, 3x)
    
    - requires: `width > 0`.
    - requires: `width >= (width of the original image) / 3`.
    - requires: 'height >= 0'.
    
    - returns: NULL
    - parameters:
        - root: The path to the folder
        - file: The input file, contained in the root folder
        - width: An optional parameter specifying the width of the output image
        - height: An optional parameter specifying the height of the image
    '''
def resize(root, file, width, height=0, overwrite=True):
    filename = os.path.join(root, file)

    path = root.split('/')
    if len(path) > 1: #contains sub directory
        if isInt(path[len(path)-1]):
            width = int(path[len(path)-1]) #set width to the name of the parent folder
    
    img = Image.open(filename)
    wpercent = width / float(img.size[0])
    if height > 0:
        hsize = int(height / float(img.size[1]))
    else:
        hsize = int((float(img.size[1]) * float(wpercent)))
    for i in range(3):
        iteration = i+1
        img = img.resize((width * iteration, hsize * iteration), PIL.Image.ANTIALIAS)

        fileext = os.path.splitext(file)[1]
        filename = os.path.splitext(file)[0]
        
        add = ""
        if len(path) > 1: #was in a sub folder, write into same subfolder
            if os.path.exists("output/"+convertToString(path[1:], "/")) == False:
                os.makedirs("output/"+convertToString(path[1:], "/"))
            if iteration == 1:
                while os.path.exists("output/"+convertToString(path[1:], "/")+"/"+filename+str(add)+fileext) and overwrite == False:
                    if add == "":
                        add = 1
                    else:
                        add+=1
                img.save("output/"+convertToString(path[1:], "/")+"/"+filename+str(add)+fileext)
            else:
                while os.path.exists("output/"+convertToString(path[1:], "/")+"/"+filename+str(add)+'@'+str(iteration)+'x'+fileext) and overwrite == False:
                    if add == "":
                        add = 1
                    else:
                        add+=1
                img.save("output/"+convertToString(path[1:], "/")+"/"+filename+str(add)+'@'+str(iteration)+'x'+fileext)
        else:
            if iteration == 1:
                while os.path.exists("output/"+filename+str(add)+fileext) and overwrite == False:
                    if add == "":
                        add = 1
                    else:
                        add+=1

                img.save("output/"+filename+str(add)+fileext)

            else:
                while os.path.exists("output/"+filename+str(add)+'@'+str(iteration)+'x'+fileext) and overwrite == False:
                    if add == "":
                        add = 1
                    else:
                        add+=1
                img.save("output/"+filename+str(add)+'@'+str(iteration)+'x'+fileext)

py3 = version_info[0] > 2
width = 0
height = 0
overwrite = True
over = ""

print("\n\tiOS Image Resizer by Matthew Paletta\n")


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
    width = input("Please enter the desired width of the image(s) (in pixels) ")
    height = input("Please enter the desired height of the image(s) [Or by 0 to constrain to proportions] (in pixels) ")
    over = input("Should overwrite previous? [y/N] ")
    if over == 'y' or over == 'Y':
        overwrite = True
    else:
        overwrite = False
else:
    #print("Using Python 2.X")
    width = raw_input("Please enter the desired width of the image(s) (in pixels) ")
    height = raw_input("Please enter the desired height of the image(s) [Or by 0 to constrain to proportions] (in pixels) ")
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
            
            resize(root, file, int(width), int(height), overwrite)
        if (file.endswith('.ai') or file.endswith('.psd')) and os.path.islink(os.path.join(root, file)) == False:
            aiToPNG(root, file)
            filename = os.path.splitext(file)[0]
            resize(root, filename+".png", int(width), int(height), overwrite)

            os.remove(os.path.join(root, filename+".png"))

    if os.path.exists("log.txt"):
        os.remove("log.txt")
    progress(total, total)
print("\n")
