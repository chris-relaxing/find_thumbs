#-------------------------------------------------------------------------------
# Name:         find_thumbs.py
# Purpose:      Point this script at a folder that has zip files and it will search each zip file
#               for Thumbs.db files. If Thumbs.db files are found, a find_thumbs.txt file will be created in the searched folder
#               and it will contain the counts and locations of Thumbs.db files that were found inside each zip. If no Thumbs.db
#               files are found, then no output file will be created.
# Author:       Christopher Nielsen
#
# Created:          09/18/2013
# Last updated:     10/08/2013
# Copyright:        (c) Chris Nielsen 2013

#-------------------------------------------------------------------------------


import zipfile
import os
from Tkinter import *
import sys
import tkMessageBox
import tkFileDialog


#-----------------------------------------------------------------------------
class pathDialog(Frame):

    ##Initiate parent frame
    def __init__(self, parent):
        Frame.__init__(self, parent)
        self.parent = parent
        self.parent.title("Find Thumbs.db in .zip files")
        self.pack(fill=BOTH, expand=1)
        self.centerWindow()
        self.initUI()

    ##Main menu Interface
    ## This is not needed if the script has only one function
    def initUI(self):

        def loadDir(entry):
            folder = tkFileDialog.askdirectory()
            entry.set(folder)

        def printSelectedDirs(visual_contents_folder):
            global SelectedPath
            global path
            global zip_folder
            global writepath

            SelectedPath = ""
            SelectedPath = str(visual_contents_folder.get())
            path = SelectedPath
            zip_folder = SelectedPath
            writepath = zip_folder+'\\'+"find_thumbs.txt"

            if not path:
                ThrowError("Error: No path has been selected.", "", "Error")
                sys.exit()

            legitfolder = os.path.isdir(zip_folder)

            if legitfolder:
                print "writepath is", writepath
                print "The selected path is:", zip_folder

            else:
                ThrowError("Error: Not a valid path.", zip_folder, "Error")
                sys.exit()


        def multCommands(visual_contents_folder):
            printSelectedDirs(visual_contents_folder)
            if path:
                self.parent.destroy() # This is what destroys the main window

        self.title = 'Find Thumbs.db in .zip files'
        Label(self, text = 'Path to folder containing zips to be searched:').grid(row = 0, column = 0, pady=0)

        visual_contents_folder = StringVar()
        Entry(self, width=100,textvariable = visual_contents_folder).grid(row = 1, column =0, columnspan = 1, pady=0)
        Button(self, text = "Browse", command = lambda: loadDir(visual_contents_folder), width = 10).grid(row = 1, column = 1, pady=0)

        Button(self, text = '  Search .zip files  ', command = lambda: multCommands(visual_contents_folder)).grid(row = 5, column = 0, pady=20)

    ##Main menu should appear in middle of screen
    def centerWindow(self):
        w = 750
        h = 100

        sw = self.parent.winfo_screenwidth()
        sh = self.parent.winfo_screenheight()

        x = (sw - w)/2
        y = (sh - h)/2
        self.parent.geometry('%dx%d+%d+%d' % (w,h, x, y))


    def loadtemplate(self,entry):
        filename = tkFileDialog.askopenfilename()
        entry.set(filename)


#-----------------------------------------------------------------------------

def listZip():

    try:
        i = 0
        for (path, dirs, files) in os.walk(zip_folder):
            i += 1
            if i >= 4:
                break

        zipfound = 0
        for e in files:
            if ".zip" in e:
                zipfound = 1
            else:
                pass
        if zipfound == 0:
            print "\nError. No zip files can be found at this path:", zip_folder
            ThrowError("Error. No zip files can be found at this path:", zip_folder, "Error")
            sys.exit()
        else:
            for e in files:
                if ".zip" in e:
                    current_zip = zip_folder+"\\"+e
                    print "\nSearching", current_zip, "..."
                    z = zipfile.ZipFile(current_zip, "r")
                    found_count = 0
                    for filename in z.namelist( ):
                        if "Thumbs.db" in filename:
                            piece = current_zip+"-->"+filename
                            print 'File:', piece
                            found_count +=1
                    print  "# of Thumbs.db found in this zip:", found_count

            if found_count != 0:

                writer = open(writepath, "w")
                writer.write("The selected path is: %s\n\n" % (zip_folder))
                for e in files:
                    if ".zip" in e:
                        current_zip = zip_folder+"\\"+e
                        writer.write("\nSearching %s\n" % (current_zip))

                        z = zipfile.ZipFile(current_zip, "r")
                        found_count = 0
                        for filename in z.namelist( ):
                            if "Thumbs.db" in filename:
                                piece = current_zip+"-->"+filename
                                writer.write("File: %s\n" % (piece))
                                found_count +=1
                                #bytes = z.read(filename)
                                #print 'has', len(bytes), 'bytes'
                        #print  "# of Thumbs.db found in this zip:", found_count
                        writer.write("# of Thumbs.db found in this zip: %s\n\n" % (found_count))
                ThrowError("Process completed. The output can be found here:", writepath, "Process Complete")
            else:
                ThrowError("Search completed. No Thumbs.db files found.", "Zip files are clean.", "Process Complete")

    except:
        sys.exit()


#-----------------------------------------------------------------------------
def ThrowError(message, path, title):
    root = Tk()
    #root.title("Error")
    root.title(title)

    w = 750
    h = 200

    sw = root.winfo_screenwidth()
    sh = root.winfo_screenheight()

    x = (sw - w)/2
    y = (sh - h)/2
    root.geometry('%dx%d+%d+%d' % (w,h, x, y))

    m = message
    m += '\n'
    m += path
    w = Label(root, text=m, width=120, height=10)
    w.pack()
    b = Button(root, text="OK", command=root.destroy, width=10)
    b.pack()
    mainloop()

#-----------------------------------------------------------------------------
def main():
    root = Tk()
    Tk.wantobjects = 0
    app = pathDialog(root)
    root.mainloop()
    listZip()



if __name__ == '__main__':
    main()
