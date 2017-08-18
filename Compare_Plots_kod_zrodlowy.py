from PIL import Image, ImageTk, ImageChops, ImageFile
from tkinter import Tk, BOTH, Text, INSERT, END, Listbox, ANCHOR
from tkinter import messagebox as mbox
from tkinter.ttk import Frame, Label, Style, Button, Entry
import os

class Window(Frame):

    def __init__(self):
        super().__init__()

        self.initUI()


    def initUI(self):
        """
        Function defines basic layout of whole program.
        """

        # Start instances atributes
        self.master.title("Image Compare")
        self.pack(fill=BOTH, expand=1)
        self.listOfPaths = []
        self.lenght = 0
        self.i = 0
        self.directory1 = "C:\\Plots1"
        self.directory2 = "C:\\Plots2"

        Style().configure("TFrame", background="#333")

        # Defining entrys, lables and text fields
        self.path1 = Entry(self, width=50)
        self.path1.place(x=10, y=10)

        self.path2 = Entry(self, width=50)
        self.path2.place(x=10, y=35)

        self.startFromEntry = Entry(self, width=5)
        self.startFromEntry.place(x=550, y=10)

        self.plot1PathText = Text(self, height=3, width=75)
        self.plot1PathText.place(x=620, y=670)

        self.plot2PathText = Text(self, height=3, width=75)
        self.plot2PathText.place(x=1230, y=670)

        self.lb = Listbox(self, height=15, width=100)
        self.lb.place(x=620, y=740)

        self.numberOfPlotsText = Text(self, height=1, width=5)
        self.numberOfPlotsText.place(x=790, y=10)

        self.currentPlotsText = Text(self, height=1, width=5)
        self.currentPlotsText.place(x=930, y=10)

        numberOfPlotsLabel = Label(self, text="Nuber of plots:")
        numberOfPlotsLabel.place(x=700, y=10)

        currentPlotsLabel = Label(self, text="Current plot:")
        currentPlotsLabel.place(x=850, y=10)

        # Defining buttons
        previousButton = Button(self, text="Previous", command=
                                self.previousButtonFunction)
        previousButton.place(x=10, y=670)

        nextButton = Button(self, text="Next", command=self.nextButtonFunction)
        nextButton.place(x=100, y=670)

        differentButton = Button(self, text="Different", command=
                                 self.differentButtonFunction)
        differentButton.place(x=300, y=670)

        deleteButton = Button(self, text="Delete", command=
                                         self.deleteButtonFunction)
        deleteButton.place(x=380, y=670)

        getPathButton = Button(self, text="Get Path", command=
                               self.get_filepaths)
        getPathButton.place(x=350, y=8)

        startFromButton = Button(self, text="Start From", command=
                                 self.startFromButtonFunction)
        startFromButton.place(x=600, y=8)

    #Defining messageboxes
    def onNoPlot(self):
        string = self.listOfPaths[self.i]
        string = string.replace(self.directory1, self.directory2)
        mbox.showerror("Error", "There is no plot {}".format(string))

    def onEqualPath(self):
        mbox.showerror("Error", "The same paths")

    def onLastPicture(self):
        mbox.showinfo("Last plot", "That is the last plot.")

    def onFirstPicture(self):
        mbox.showinfo("First plot", "That is the first plot.")

    # Defining buttons function
    def deleteButtonFunction(self):
        """
        deleteButton functionality, deleting item from listbox.
        """
        result = mbox.askquestion("Delete",
                                  "Delete highlighted item?",
                                  icon='warning')
        if result == 'yes':
            self.lb.delete(ANCHOR) #self.lb is listbox
        else:
            return None

    def startFromButtonFunction(self):
        """
        startFromButton functionality, from which chart program is starting.
        """
        # Get value from entry
        a = int(self.startFromEntry.get()) - 1
        # Check if value is proper
        if a < 0 or a >= self.lenght:
            print("Wrong number")
        else:
            self.i = a
            self.picture(self.i)

    def nextButtonFunction(self):
        """
        nextButton functionality, next picture is choosen.
        """
        if self.i == self.lenght - 1:
            self.onLastPicture()
        else:
            self.i += 1
            self.picture(self.i)

    def previousButtonFunction(self):
        """
        previousButton functionality, previousPicture picture is choosen.
        """
        if self.i == 0:
            self.onFirstPicture()
        else:
            self.i -= 1
            self.picture(self.i)

    def differentButtonFunction(self):
        """
        differentButton functionality.
        """
        adr = self.listOfPaths[self.i]
        self.addToListbox(adr)

    def addToListbox(self, adr):
        """
        This function add path to listbox when charts are differentButton.

        Parameters:
        ----------
        adr: str
            Path to chart.
        """
        try:
            if adr in self.lb.get(0, END):
                return None
            else:
                self.lb.insert(0, adr)
        except TypeError:
            self.lb.insert(0, adr)

    def picture(self, adr):
        """
        This function creates three lables with pictures, first label show
        differences between pictures in next two labels.

        Parameters:
        ----------
        adr: str
            Path to chart.
        """
        adress_1 = self.listOfPaths[adr]
        adress_2 = adress_1.replace(self.directory1, self.directory2)

        file_img1 = Image.open(adress_1)
        try:
            file_img2 = Image.open(adress_2)
        except FileNotFoundError:
            adr = self.listOfPaths[self.i]
            self.addToListbox(adr)
            self.onNoPlot()
            return None

        self.fill_text_fields(adress_1, adress_2)
        diff = ImageChops.difference(file_img1, file_img2)
        diff = diff.resize((600, 600))
        diffjov = ImageTk.PhotoImage(diff)
        label1 = Label(self, image=diffjov)
        label1.image = diffjov
        label1.place(x=10, y=60)

        file_img1 = file_img1.resize((600, 600))
        image_2 = ImageTk.PhotoImage(file_img1)
        label2 = Label(self, image=image_2)
        label2.image = image_2
        label2.place(x=620, y=60)

        file_img2 = file_img2.resize((600, 600))
        image_3 = ImageTk.PhotoImage(file_img2)
        label3 = Label(self, image=image_3)
        label3.image = image_3
        label3.place(x=1230, y=60)

    def fill_text_fields(self, adr_1, adr_2):
        """
        This function is added plots pathes to labels and added curent plot
        number to label

        Parameters:
        ----------
        adr_1: str
            Path to chart.
        adr_2: str
             Path to chart.
        """
        self.plot1PathText.config(state="normal")
        self.plot1PathText.delete("1.0", END)
        self.plot1PathText.insert(INSERT, adr_1)
        self.plot1PathText.config(state="disabled")

        self.plot2PathText.config(state="normal")
        self.plot2PathText.delete("1.0", END)
        self.plot2PathText.insert(INSERT, adr_2)
        self.plot1PathText.config(state="disabled")

        self.currentPlotsText.config(state="normal")
        self.currentPlotsText.delete("1.0", END)
        self.currentPlotsText.insert(INSERT, self.i + 1)
        self.currentPlotsText.config(state="disabled")


    def get_filepaths(self):
        """
        This function will generate the file names in a directory
        tree by walking the tree either top-down or bottom-up. For each
        directory in the tree rooted at directory top (including top itself),
        it yields a 3-tuple (dirpath, dirnames, filenames).
        """
        self.directory1 = self.path1.get()
        self.directory2 = self.path2.get()
        if self.directory1 == self.directory2:
            self.onEqualPath()
            return None

        file_paths = [] # List which will store all of the full filepaths.
        self.i = 0

        # Walk the tree.
        for root, directories, files in os.walk(self.directory1):
            for filename in files:
                # Join the two strings in order to form the full filepath.
                filepath = os.path.join(root, filename)
                file_paths.append(filepath) # Add it to the list.

        self.listOfPaths = file_paths
        self.lenght = len(file_paths)
        self.picture(self.i)
        self.numberOfPlotsText.insert(INSERT, self.lenght)
        self.numberOfPlotsText.config(state="disabled")

    def saveToFile(self):
        """
        This function write to file all elemens from listbox to file.
        """
        pathList = self.lb.get(0, END)
        currentPath = os.path.abspath(__file__)
        pathToSave = currentPath.split("\\")
        pathToSave[-1] = "path.txt"
        pathToSave.pop(-2)
        path = "\\".join(pathToSave)
        with open(path, "w") as fp:
            for item in pathList:
                fp.write(item + "\n")

def main():

    root = Tk()
    root.geometry("1920x1080+0+0")
    app = Window()

    def onExit():
        if mbox.askyesno("Exit", "Do you want to quit the application?"):
            app.saveToFile()
            root.destroy()

    root.protocol("WM_DELETE_WINDOW", onExit)
    root.mainloop()



if __name__ == '__main__':
    main()
